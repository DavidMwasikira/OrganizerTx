/* ================= v0.32: time and people (owners, reminders, repeating tasks, calendar) and project controls ================= */
const REPEAT={'':'Does not repeat',daily:'Every day',weekdays:'Every weekday',weekly:'Every week',monthly:'Every month'};
const localISO=t=>{const d=new Date(t),z=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate())+'T'+z(d.getHours())+':'+z(d.getMinutes())};
function nextDate(d,rep){const x=new Date((isoOk(d)||dash(Date.now()))+'T12:00');if(rep==='daily')x.setDate(x.getDate()+1);else if(rep==='weekdays'){do{x.setDate(x.getDate()+1)}while([0,6].includes(x.getDay()))}else if(rep==='monthly')x.setMonth(x.getMonth()+1);else x.setDate(x.getDate()+7);return dash(x.getTime())}
/* when a repeating task is completed (by any route), the next one is created once */
function sweepRecurring(){
  let made=null;const today=dash(Date.now());
  S.plans.forEach(p=>p.acts.slice().forEach(a=>{if(!a.repeat||!REPEAT[a.repeat]||!isDone(a)||a.spawned)return;a.spawned=true;
    let due=nextDate(a.due,a.repeat),guard=0;while(due<=today&&guard++<400)due=nextDate(due,a.repeat);
    const shift=a.remind&&a.due?new Date(a.remind).getTime()-new Date(a.due+'T00:00').getTime():null;
    made={name:a.name,detail:a.detail||'',owner:a.owner||'',status:'todo',due,repeat:a.repeat,remind:shift!==null&&isFinite(shift)?localISO(new Date(due+'T00:00').getTime()+shift):''};p.acts.push(made)}));
  if(made){save();setTimeout(()=>toast('Repeating task: the next "'+clip(made.name,40)+'" is set for '+fmtShort(made.due)+'.'),50)}
}
async function notifyNow(title,body,tag){if(!('Notification' in window)||Notification.permission!=='granted')return;try{const reg=navigator.serviceWorker&&await navigator.serviceWorker.getRegistration();if(reg)reg.showNotification(title,{body,icon:'icon-192.png',tag});else new Notification(title,{body})}catch(e){}}
function checkReminders(){
  if(!S.profile||!S.profile.setup)return;let hit=false;const now=Date.now();
  allTasks().forEach(t=>{const a=t.a;if(!a.remind||a.reminded||isDone(a))return;const at=new Date(a.remind).getTime();if(!isFinite(at)||at>now)return;
    a.reminded=true;hit=true;(S.rems=S.rems||[]).unshift({name:a.name,proj:t.p.name,due:t.due||'',at:now});S.rems=S.rems.slice(0,6);
    notifyNow('Reminder: '+a.name,t.p.name+(t.due?' · due '+fmtShort(t.due):''),'rem'+now)});
  if(hit){save();render()}
}
const remBar=()=>(S.rems||[]).length?`<div class="rembar" role="status">${S.rems.map((r,i)=>`<div><span class="ic">${ICON.bell}</span><span class="grow"><strong>Reminder:</strong> ${esc(r.name)} <span class="small muted">${esc(r.proj)}${r.due?' · due '+fmtShort(r.due):''}</span></span><button class="btn ghost small" data-act="nav" data-v="tasks">Open board</button><button class="btn ghost small" data-act="rem-x" data-v="${i}" aria-label="Dismiss reminder">Dismiss</button></div>`).join('')}</div>`:'';
const owners=()=>[...new Set(S.plans.flatMap(p=>p.acts.map(a=>(a.owner||'').trim())).concat(S.plans.flatMap(p=>(p.risks||[]).map(r=>(r.owner||'').trim()))).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
const initials=n=>String(n||'').split(/\s+/).filter(Boolean).slice(0,2).map(w=>w[0].toUpperCase()).join('');
function calendarHtml(tasks){
  const ym=/^\d{4}-\d\d$/.test(V.calM||'')?V.calM:dash(Date.now()).slice(0,7),[Y,M]=ym.split('-').map(Number),first=new Date(Y,M-1,1),start=new Date(Y,M-1,1-((first.getDay()+6)%7)),today=dash(Date.now());
  const miles=S.plans.filter(p=>onBoard(p)&&(V.tfilter==='all'||p.id===V.tfilter)).flatMap(p=>(p.miles||[]).filter(m=>isoOk(m.date)).map(m=>({m,p})));
  const cells=[];for(let i=0;i<42;i++){const d=new Date(start);d.setDate(start.getDate()+i);const k=dash(d.getTime());if(i>=35&&d.getMonth()!==M-1&&cells.length%7===0)break;cells.push({k,d,inM:d.getMonth()===M-1})}
  return `<div class="calbar"><div class="row" style="gap:6px"><button class="btn wknav" data-act="cal-nav" data-v="-1" aria-label="Previous month">&lsaquo;</button><button class="btn wknav" data-act="cal-nav" data-v="1" aria-label="Next month">&rsaquo;</button><button class="btn ghost small" data-act="cal-nav" data-v="0">Today</button></div><h2 style="font-size:1.2rem">${first.toLocaleDateString('en-GB',{month:'long',year:'numeric'})}</h2><span class="small muted">${tasks.filter(t=>t.due&&t.due.slice(0,7)===ym).length} due this month</span></div>
    <div class="cal" role="grid" aria-label="Calendar">${['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map(d=>`<div class="ch">${d}</div>`).join('')}${cells.map(c=>{const ts=tasks.filter(t=>t.due===c.k),ms=miles.filter(x=>x.m.date===c.k),all=ts.length+ms.length;
      return `<div class="cc ${c.inM?'':'out'} ${c.k===today?'now':''}" role="gridcell"><button class="cd" data-act="task-new-day" data-v="${c.k}" aria-label="Add a task on ${fmtShort(c.k)}" title="Add a task on ${fmtShort(c.k)}">${c.d.getDate()}</button>${ms.slice(0,1).map(x=>`<button class="ce ms" data-act="open-plan" data-v="${x.p.id}" title="Milestone: ${esc(x.m.name)} (${esc(x.p.name)})">&#9670; ${esc(x.m.name)}</button>`).join('')}${ts.slice(0,3-Math.min(1,ms.length)).map(t=>`<button class="ce" data-s="${t.a.status}" data-act="task-open" data-v="${esc(t.id)}" title="${esc(t.a.name)} · ${esc(t.p.name)}${t.a.owner?' · '+esc(t.a.owner):''}">${t.a.repeat?'&#8635; ':''}${esc(t.a.name)}</button>`).join('')}${all>3?`<span class="small muted cm">+${all-3} more</span>`:''}</div>`}).join('')}</div>
    <p class="small muted" style="margin:0">Click a date to add a task on that day. &#8635; marks a repeating task and &#9670; a project milestone. Tasks without a due date are on the Board and List.</p>`;
}
/* ---------- project controls: budget, risks and issues, milestones ---------- */
const BCATS=['Labour','Materials','Equipment','Transport','Permits and fees','Professional services','Contingency','Other'];
const curSym=()=>((CURRENCY[S.profile.country]||'').match(/\(([^)]+)\)/)||[])[1]||'';
const money=n=>(curSym()?curSym()+' ':'')+Math.round(+n||0).toLocaleString('en-GB');
const num=v=>{const n=parseFloat(String(v==null?'':v).replace(/[^0-9.\-]/g,''));return isFinite(n)?n:0};
const budOf=p=>(p.budget=p.budget&&Array.isArray(p.budget.lines)?p.budget:{lines:[]});
const budSum=p=>{const L=budOf(p).lines,planned=L.reduce((a,l)=>a+num(l.planned),0),actual=L.reduce((a,l)=>a+num(l.actual),0);return {planned,actual,left:planned-actual,used:planned?Math.round(100*actual/planned):0,n:L.length}};
const LEVELS3={high:['High','var(--bad)'],med:['Medium','var(--signal)'],low:['Low','var(--s-done)']};
const mileState=m=>m.done?['Done','on']:!isoOk(m.date)?['No date','']:m.date<dash(Date.now())?['Late','due']:[(d=>d===0?'Today':'In '+d+' day'+(d===1?'':'s'))(Math.round((new Date(m.date+'T12:00')-new Date(dash(Date.now())+'T12:00'))/DAY)),''];
function importBudget(file){
  const p=curPlan();if(!p||!file)return;if(needKey())return;
  if(!hosted()&&['pdf','image'].includes(fileKind(file))){toast('Photos and PDFs can be read in the installed version. In this preview, use an Excel or CSV file.');return}
  job('budget','Reading '+file.name,async(signal,onText,onStatus)=>{
    const blocks=await fileBlocks(file,'BUDGET DOCUMENT');onStatus('Converting to budget lines');
    const ask=`Convert this budget, bill of quantities or cost estimate into budget lines for the project "${p.name}".
Rules:
- One line per cost item. Leave out subtotal, total, VAT-summary and header rows.
- "item": a clear, properly capitalised title (fix abbreviations and typing errors; keep quantities and units if shown, e.g. "PVC casing, 60 m").
- "category": exactly one of ${JSON.stringify(BCATS)}.
- "planned": the budgeted or quoted amount for the line as a plain number (quantity x rate if only those are given). "actual": amount spent so far if the document shows it, otherwise 0.
- Copy numbers exactly as written; do not round, convert currency or invent lines. If a figure is unreadable, use 0 and mention it in "notes".
Reply with only a JSON object: {"currency":"as written in the document or empty","lines":[{"category":"...","item":"...","planned":0,"actual":0}],"stated_total":0,"notes":"anything missing, unreadable or unusual, or empty"}
"stated_total" is the grand total printed in the document (planned side), or 0 if none is shown.`;
    const allText=blocks.every(b=>b.type==='text'),content=allText?blocks.map(b=>b.text).join('\n\n')+'\n\n-----\n\n'+ask:[...blocks,{type:'text',text:ask}];
    const r=await callAI({system:systemPrompt(),depth:'brief',search:0,maxTokens:8000,signal,messages:[{role:'user',content}]});
    const o=grab(r.text,'{','}'),lines=(o&&Array.isArray(o.lines)?o.lines:[]).filter(l=>l&&String(l.item||'').trim()).slice(0,200).map(l=>({cat:BCATS.includes(l.category)?l.category:'Other',item:clip(String(l.item).trim(),120),planned:num(l.planned),actual:num(l.actual)}));
    if(!lines.length)throw new Error('No budget lines could be read from '+file.name+'. Try a clearer photo or an Excel file.');
    V.budImp={pid:p.id,name:file.name,lines,stated:num(o.stated_total),cur:String(o.currency||'').trim(),notes:String(o.notes||'').trim()};V.ptab='budget';
  });
}
function riskModal(i){
  const p=curPlan(),ex=i!==undefined&&i!==''?(p.risks||[])[+i]:null,r=ex||{type:'risk',title:'',level:'med',owner:'',due:'',action:'',status:'open'};
  modal(`<form class="card wide"><h2 style="font-size:1.2rem">${ex?'Edit':'New'} risk or issue</h2>
    <div class="row" style="align-items:flex-start"><div class="field" style="flex:1;min-width:140px"><label for="rtype">Type</label><select id="rtype"><option value="risk" ${r.type==='risk'?'selected':''}>Risk (might happen)</option><option value="issue" ${r.type==='issue'?'selected':''}>Issue (has happened)</option></select></div>
    <div class="field" style="flex:1;min-width:120px"><label for="rlevel">Level</label><select id="rlevel">${Object.entries(LEVELS3).map(([k,v])=>`<option value="${k}" ${r.level===k?'selected':''}>${v[0]}</option>`).join('')}</select></div>
    <div class="field" style="flex:1;min-width:120px"><label for="rstat">Status</label><select id="rstat"><option value="open" ${r.status!=='closed'?'selected':''}>Open</option><option value="closed" ${r.status==='closed'?'selected':''}>Closed</option></select></div></div>
    <div class="field"><label for="rtitle">What is it?</label><input type="text" id="rtitle" value="${esc(r.title)}" placeholder="For example: casing delivery may slip a week"></div>
    <div class="field"><label for="raction">Response or next action</label><textarea id="raction" rows="2" placeholder="What will be done about it">${esc(r.action||'')}</textarea></div>
    <div class="row" style="align-items:flex-start"><div class="field" style="flex:1;min-width:140px"><label for="rowner">Owner</label><input type="text" id="rowner" list="ownerlist" value="${esc(r.owner||'')}" placeholder="Who is handling it?"><datalist id="ownerlist">${owners().map(o=>`<option value="${esc(o)}">`).join('')}</datalist></div>
    <div class="field" style="flex:1;min-width:140px"><label for="rdue">Review or due date</label><input type="date" id="rdue" value="${esc(r.due||'')}"></div></div>
    <div class="row" style="justify-content:space-between">${ex?'<button type="button" class="btn danger" data-x="del">Delete</button>':'<span></span>'}<span class="row"><button type="button" class="btn" data-x="cancel">Cancel</button><button type="submit" class="btn primary" data-x="save">Save</button></span></div></form>`,{
    cancel(){},
    save(el){const title=el.querySelector('#rtitle').value.trim();if(!title){toast('Say what the risk or issue is.');return false}
      const q=id=>el.querySelector(id).value;Object.assign(r,{type:q('#rtype'),level:q('#rlevel'),status:q('#rstat'),title,action:q('#raction').trim(),owner:q('#rowner').trim(),due:q('#rdue')||''});
      if(!ex)(p.risks=p.risks||[]).push(r);save();render()},
    del(){p.risks.splice(+i,1);save();render()}
  });
}
function controlsHtml(p,tab){
  if(tab==='budget'){
    const B=budOf(p),s=budSum(p),imp=V.budImp&&V.budImp.pid===p.id?V.budImp:null,mine=busy&&busy.topicId==='budget';
    const cats=BCATS.map(c=>({c,pl:B.lines.filter(l=>l.cat===c).reduce((a,l)=>a+num(l.planned),0),ac:B.lines.filter(l=>l.cat===c).reduce((a,l)=>a+num(l.actual),0)})).filter(x=>x.pl||x.ac),mx=Math.max(1,...cats.map(x=>Math.max(x.pl,x.ac)));
    const tile=(l,v,c)=>`<div class="btile"><span class="lbl">${l}</span><b style="${c?'color:'+c:''}">${v}</b></div>`;
    const impSum=imp?imp.lines.reduce((a,l)=>a+l.planned,0):0;
    return `${mine?`<div class="working"><span class="spin"></span><span id="joblabel">${esc(busy.label)}...</span><button class="btn ghost small" data-act="stop">Stop</button></div>`:''}
    ${imp?`<section class="card" style="border-color:var(--accent);display:flex;flex-direction:column;gap:10px"><div class="row" style="justify-content:space-between"><h2 style="font-size:1.1rem">Check what was read from ${esc(imp.name)}</h2><span class="small muted">${imp.lines.length} lines${imp.cur?' · currency as written: '+esc(imp.cur):''}</span></div>
      <p class="${imp.stated&&Math.abs(imp.stated-impSum)>1?'banner':'small'}" style="margin:0">${imp.stated?(Math.abs(imp.stated-impSum)>1?`The lines add up to ${money(impSum)}, but the document states a total of ${money(imp.stated)}. Check for a missed or misread line before accepting.`:`&#10003; The lines add up to ${money(impSum)}, which matches the total stated in the document.`):`The lines add up to ${money(impSum)}. The document shows no grand total to check against.`}</p>
      ${imp.notes?`<p class="small muted" style="margin:0">Note from the reading: ${esc(imp.notes)}</p>`:''}
      <div class="tw" style="max-height:300px;overflow:auto"><table class="dt"><thead><tr><th>Category</th><th>Item</th><th style="text-align:right">Planned</th><th style="text-align:right">Actual</th></tr></thead><tbody>${imp.lines.map(l=>`<tr><td>${esc(l.cat)}</td><td>${esc(l.item)}</td><td style="text-align:right">${money(l.planned)}</td><td style="text-align:right">${l.actual?money(l.actual):'-'}</td></tr>`).join('')}</tbody></table></div>
      <div class="row"><button class="btn primary" data-act="bud-accept" data-v="replace">Replace the budget</button>${B.lines.length?'<button class="btn" data-act="bud-accept" data-v="add">Add to the budget</button>':''}<button class="btn ghost" data-act="bud-accept" data-v="">Discard</button></div></section>`:''}
    <div class="btiles">${tile('Budget',money(s.planned))}${tile('Spent',money(s.actual))}${tile(s.left<0?'Over budget':'Remaining',money(Math.abs(s.left)),s.left<0?'var(--bad)':'')}${tile('Used',s.used+'%',s.used>100?'var(--bad)':'')}</div>
    ${cats.length?`<section class="card"><span class="lbl">Spent against budget, by category</span><div class="bcat">${cats.map(x=>`<div title="${x.c}: spent ${money(x.ac)} of ${money(x.pl)}"><span>${x.c}</span><span class="tr"><i class="pl" style="width:${100*x.pl/mx}%"></i><i class="ac ${x.ac>x.pl?'over':''}" style="width:${100*x.ac/mx}%"></i></span><b>${money(x.ac)} <span class="small muted">of ${money(x.pl)}</span></b></div>`).join('')}</div><p class="small muted" style="margin:8px 0 0">Pale bar: budget. Solid bar: spent; it turns red when a category is over budget.</p></section>`:''}
    <section class="card"><div class="row" style="justify-content:space-between"><span class="lbl">Budget lines</span><span class="row"><label class="btn" for="budfile">Import from Excel, PDF or photo</label><input type="file" id="budfile" hidden accept=".xlsx,.xls,.csv,.pdf,image/*"><label class="btn only-narrow" for="budcam">${ICON.camera.replace('<svg','<svg style="width:18px;height:18px"')}Take a photo</label><input type="file" id="budcam" hidden accept="image/*" capture="environment"><button class="btn primary" data-act="bud-add">+ Add line</button></span></div>
      ${B.lines.length?`<div class="tw"><table class="dt bt"><thead><tr><th style="width:190px">Category</th><th>Item</th><th style="width:150px;text-align:right">Planned</th><th style="width:150px;text-align:right">Actual</th><th style="width:44px"></th></tr></thead><tbody>${B.lines.map((l,i)=>`<tr><td><select data-bud="${i}|cat" aria-label="Category">${BCATS.map(c=>`<option ${c===l.cat?'selected':''}>${c}</option>`).join('')}</select></td><td><input type="text" data-bud="${i}|item" value="${esc(l.item)}" aria-label="Item" placeholder="What is it for?"></td><td><input type="text" inputmode="decimal" data-bud="${i}|planned" value="${num(l.planned)||''}" aria-label="Planned amount" placeholder="0" style="text-align:right"></td><td><input type="text" inputmode="decimal" data-bud="${i}|actual" value="${num(l.actual)||''}" aria-label="Actual amount" placeholder="0" style="text-align:right"></td><td><button class="btn ghost small" data-act="bud-del" data-v="${i}" aria-label="Delete line" title="Delete line">&times;</button></td></tr>`).join('')}</tbody><tfoot><tr><td colspan="2" style="font-weight:600">Total</td><td style="text-align:right;font-weight:600">${money(s.planned)}</td><td style="text-align:right;font-weight:600">${money(s.actual)}</td><td></td></tr></tfoot></table></div>`
      :'<p class="small muted" style="margin:10px 0 0">No budget yet. Add lines by hand, or import an Excel sheet, a PDF or a photo of a budget or bill of quantities: the lines are given clear titles and sorted into categories for you to check.</p>'}</section>`;
  }
  if(tab==='risks'){
    const R=(p.risks||[]).map((r,i)=>({r,i})).sort((a,b)=>(a.r.status==='closed')-(b.r.status==='closed')||['high','med','low'].indexOf(a.r.level)-['high','med','low'].indexOf(b.r.level)),open=R.filter(x=>x.r.status!=='closed');
    return `<div class="row" style="justify-content:space-between"><span class="row" style="gap:6px"><span class="pill ${open.filter(x=>x.r.level==='high').length?'due':''}">${open.filter(x=>x.r.level==='high').length} high</span><span class="pill">${open.filter(x=>x.r.type==='risk').length} open risks</span><span class="pill">${open.filter(x=>x.r.type==='issue').length} open issues</span></span><button class="btn primary" data-act="risk-new">+ Add risk or issue</button></div>
      <section class="card">${R.length?R.map(({r,i})=>`<button class="rrow ${r.status==='closed'?'closed':''}" data-act="risk-open" data-v="${i}"><span class="lv" style="--c:${LEVELS3[r.level]?LEVELS3[r.level][1]:'var(--line)'}">${(LEVELS3[r.level]||LEVELS3.med)[0]}</span><span class="grow"><span class="b" style="font-weight:600">${esc(r.title)}</span><span class="b small muted">${r.type==='issue'?'Issue':'Risk'}${r.owner?' · '+esc(r.owner):''}${r.due?' · review '+fmtShort(r.due):''}${r.action?' · '+esc(clip(r.action,90)):''}</span></span><span class="pill ${r.status==='closed'?'on':''}">${r.status==='closed'?'Closed':'Open'}</span></button>`).join(''):'<p class="small muted" style="margin:0">Nothing logged. A risk is something that might go wrong; an issue is something that already has. Log each with an owner and a response so nothing is forgotten.</p>'}</section>`;
  }
  const M=(p.miles||[]).map((m,i)=>({m,i})).sort((a,b)=>(a.m.date||'9')<(b.m.date||'9')?-1:1);
  return `${M.length?`<section class="card"><div class="mstrip">${M.map(({m})=>`<div class="${m.done?'done':isoOk(m.date)&&m.date<dash(Date.now())?'late':''}"><i></i><span class="b" style="font-weight:600">${esc(m.name)}</span><span class="b small muted">${m.date?fmtShort(m.date):'No date'}</span></div>`).join('')}</div></section>`:''}
    <section class="card"><span class="lbl">Milestones</span>
      ${M.map(({m,i})=>`<div class="mact" style="align-items:center"><button class="box" role="checkbox" aria-checked="${!!m.done}" aria-label="Mark reached" data-act="mile-tick" data-v="${i}">${m.done?'&#10003;':''}</button><input type="text" data-mile="${i}|name" value="${esc(m.name)}" aria-label="Milestone" style="flex:1;min-width:120px"><input type="date" data-mile="${i}|date" value="${esc(m.date||'')}" aria-label="Date" style="width:auto"><span class="pill ${mileState(m)[1]}" style="min-width:86px;text-align:center">${mileState(m)[0]}</span><button class="btn ghost small" data-act="mile-del" data-v="${i}" aria-label="Delete milestone" title="Delete">&times;</button></div>`).join('')}
      <div class="row" style="margin-top:12px;align-items:flex-end"><div class="field" style="flex:1;min-width:160px"><label for="mname">New milestone</label><input type="text" id="mname" placeholder="For example: drilling complete"></div><div class="field"><label for="mdate2">Date</label><input type="date" id="mdate2"></div><button class="btn primary" data-act="mile-add">Add</button></div>
      <p class="small muted" style="margin:10px 0 0">Milestones also show on the Tasks calendar.</p></section>`;
}
