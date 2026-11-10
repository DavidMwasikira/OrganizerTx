// OrganizerTX server (Cloudflare Worker).
// It keeps your Anthropic API key secret, lets in only people with a valid access code,
// and caps how many requests each code can make per day.
//
// Settings (Worker > Settings > Variables and Secrets):
//   ANTHROPIC_API_KEY  secret   your key from console.anthropic.com
//   SLOTS              secret   one entry per paying user:  CODE=Name, CODE=Name
//                               e.g.  MU96-7KQ2=David, MU96-X4P9=Wanjiru
//   DAILY_LIMIT        text     requests per code per day (default 40)
//   ALLOWED_ORIGIN     text     optional: your app's web address, so no other site can use the server
//   BREVO_API_KEY      secret   optional, for email: an API key from brevo.com (SMTP & API > API Keys)
//   SENDER_EMAIL       text     optional, for email: an address you verified as a sender in Brevo
//   EMAIL_DAILY_LIMIT  text     emails per code per day (default 3)
// Binding (optional but recommended): a KV namespace bound as USAGE, used for the daily cap.

// The last one is used if the app asks for a model that is not on this list. Remove 'claude-opus-5-5' to keep Deep research on the cheaper model.
const MODELS = ['claude-haiku-5-5', 'claude-opus-5-5', 'claude-sonnet-5-5'];
const MAX_TOKENS = 24000;   // a ceiling: the models think before they write, and thinking counts against it
const MAX_SEARCHES = 12;

function slots(env) {
  const out = {};
  String(env.SLOTS || '').split(/[,\n]/).forEach(pair => {
    const [code, name] = pair.split('=').map(x => (x || '').trim());
    if (code) out[code.toUpperCase()] = name || code;
  });
  return out;
}

// Email through Brevo (brevo.com). The server builds the message itself from plain text fields,
// so an access code cannot be used to send arbitrary content.
const esc = s => String(s == null ? '' : s).slice(0, 300).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
async function sendEmail(req, env, code, cors, fail) {
  if (!env.BREVO_API_KEY || !env.SENDER_EMAIL) return fail(501, 'email is not set up on the server yet');
  let b;
  try { b = await req.json(); } catch (e) { return fail(400, 'the request could not be read'); }
  const to = String(b && b.to || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(to) || to.length > 200) return fail(400, 'the email address is not valid');
  const items = Array.isArray(b.items) ? b.items.slice(0, 10) : [];
  if (!items.length) return fail(400, 'there was nothing to send');
  if (env.USAGE) {
    const key = 'mail:' + code + ':' + new Date().toISOString().slice(0, 10);
    const used = parseInt(await env.USAGE.get(key) || '0', 10);
    if (used >= parseInt(env.EMAIL_DAILY_LIMIT || '3', 10)) return fail(429, 'the daily email limit for this access code was reached');
    await env.USAGE.put(key, String(used + 1), { expirationTtl: 172800 });
  }
  const title = esc(b.title || 'Weekly AI business ideas').slice(0, 120);
  const html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#10212E;max-width:640px">'
    + '<h2 style="color:#0A6B7A">' + title + '</h2><ol>'
    + items.map(x => '<li style="margin-bottom:14px"><strong>' + esc(x && x.name) + '</strong><br>' + esc(x && x.what)
      + '<br><span style="color:#566878">Why now: ' + esc(x && x.why) + '<br>Funds: ' + esc(x && x.funds) + ' &middot; Could earn: ' + esc(x && x.earn) + '</span></li>').join('')
    + '</ol><p style="color:#566878;font-size:13px">AI suggestions, not financial advice. Sent by OrganizerTX because this address is saved in the app\'s Settings. Remove it there to stop these emails.</p></div>';
  const up = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'accept': 'application/json', 'api-key': env.BREVO_API_KEY },
    body: JSON.stringify({ sender: { name: env.SENDER_NAME || 'OrganizerTX', email: env.SENDER_EMAIL }, to: [{ email: to }], subject: 'OrganizerTX: ' + title, htmlContent: html })
  });
  if (!up.ok) { let m = ''; try { m = (await up.json()).message || ''; } catch (e) {} return fail(502, 'the email service refused it' + (m ? ' (' + m + ')' : '')); }
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { ...cors, 'content-type': 'application/json' } });
}

export default {
  async fetch(req, env) {
    const cors = {
      'access-control-allow-origin': env.ALLOWED_ORIGIN || '*',
      'access-control-allow-headers': 'content-type,x-slot',
      'access-control-allow-methods': 'POST,OPTIONS',
      'access-control-max-age': '86400'
    };
    const fail = (status, message) => new Response(JSON.stringify({ error: { message } }), { status, headers: { ...cors, 'content-type': 'application/json' } });

    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    const path = new URL(req.url).pathname;
    if (req.method !== 'POST' || (path !== '/v1/messages' && path !== '/v1/email')) return fail(404, 'Not found.');

    const code = (req.headers.get('x-slot') || '').trim().toUpperCase();
    if (!code || !slots(env)[code]) return fail(401, 'That access code is not active. Ask the organiser for a slot.');

    if (path === '/v1/email') return sendEmail(req, env, code, cors, fail);
    if (!env.ANTHROPIC_API_KEY) return fail(500, 'The server has no API key set yet.');

    let body;
    try { body = await req.json(); } catch (e) { return fail(400, 'The request could not be read.'); }
    if (!body || !Array.isArray(body.messages)) return fail(400, 'The request could not be read.');

    // Only pass on what the app needs, so a code cannot be used to run up costs in other ways.
    const clean = {
      model: MODELS.includes(body.model) ? body.model : MODELS[MODELS.length - 1],
      max_tokens: Math.min(Number(body.max_tokens) || 1000, MAX_TOKENS),
      messages: body.messages,
      stream: body.stream === true
    };
    if (typeof body.system === 'string') clean.system = body.system;
    if (body.thinking && body.thinking.type === 'disabled') clean.thinking = { type: 'disabled' };
    if (body.output_config && ['low', 'medium', 'high'].includes(body.output_config.effort)) clean.output_config = { effort: body.output_config.effort };
    const search = Array.isArray(body.tools) && body.tools.find(t => t && t.name === 'web_search');
    if (search) clean.tools = [{ type: 'web_search_20250305', name: 'web_search', max_uses: Math.min(Number(search.max_uses) || 3, MAX_SEARCHES) }];

    if (env.USAGE) {
      const key = code + ':' + new Date().toISOString().slice(0, 10);
      const used = parseInt(await env.USAGE.get(key) || '0', 10);
      const limit = parseInt(env.DAILY_LIMIT || '40', 10);
      if (used >= limit) return fail(429, 'This access code has reached its limit for today. It resets at midnight UTC.');
      await env.USAGE.put(key, String(used + 1), { expirationTtl: 172800 });
    }

    const up = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify(clean)
    });
    return new Response(up.body, { status: up.status, headers: { ...cors, 'content-type': up.headers.get('content-type') || 'application/json', 'cache-control': 'no-store' } });
  }
};
