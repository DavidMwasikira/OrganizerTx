import json, asyncio, sys
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
names=["AI voice agents for clinics","Automated invoice chasing","AI product photo studio","Chatbot set-up for online shops","AI meeting notes service","Niche newsletter with AI research","AI tutoring packs","Document translation desk","AI video shorts editing","Custom GPT-style assistants"]
W=[{"name":n,"what":"Sample entry: what it sells and who buys it.","why":"Sample entry: why now.","funds":"$000 to $000","earn":"$0,000 per month"} for n in names]
SERVER=len(sys.argv)>1
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        prompts=[];mails=[]
        async def api(route):
            body=json.loads(route.request.post_data); prompts.append((body['system'],body['messages'][0]['content'],body['max_tokens']))
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(W)}]))
        async def mail(route):
            mails.append(json.loads(route.request.post_data)); await route.fulfill(status=200,content_type='application/json',body='{"ok":true}')
        await pg.route('https://api.anthropic.com/**',api); await pg.route('https://srv.example/v1/messages',api); await pg.route('https://srv.example/v1/email',mail)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#code' if SERVER else '#key','MU96-7KQ2'); await pg.click('text=Start')
        # pretend an old general list from v0.3 exists, and save an email address
        await pg.evaluate("S.weekly={date:Date.now(),items:[{name:'Old general idea',what:'x',why:'y',funds:'z'}]};S.email='someone@example.com';save()")
        await pg.wait_for_timeout(4500)
        sy,up,mx=prompts[0]
        print('SERVER' if SERVER else 'OWN KEY','| ideas',await pg.locator('.wk li').count(),'| title:',await pg.locator('h2',has_text='Week').inner_text(),'| Kenya rule in system prompt:', 'lives in' in sy,'| old list passed on:', 'Old general idea' in up,'| max',mx)
        r=pg.locator('.wk'); print('row scrolls sideways:',await r.evaluate('e=>e.scrollWidth>e.clientWidth'),end=' | ')
        await pg.click('[data-act=wk-scroll][data-v="1"]'); await pg.wait_for_timeout(700); print('after arrow scrollLeft',await r.evaluate('e=>Math.round(e.scrollLeft)'))
        print('mail note:',await pg.evaluate('S.weeklyMail'),'| server emails',[(m['to'],m['title'],len(m['items'])) for m in mails],'| errors',errs)
        if not SERVER:
            await r.evaluate('e=>e.scrollLeft=0'); await pg.locator('section',has_text='AI business ideas').screenshot(path='weekly2.png')
            await pg.click('nav [data-v=settings]'); print('email field value:',await pg.input_value('#email'))
        await b.close()
asyncio.run(main())
