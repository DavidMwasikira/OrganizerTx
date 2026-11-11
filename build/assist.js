/* ================= Assistant (v0.31): ask your own data, meeting minutes, one-click reports, file analysis =================
   Everything the AI is shown here comes from this device (tasks, documents, field log, brain) or from a file the user picks.
   Facts and tables in reports are built locally; the AI words the narrative. Saved results are "papers" in S.papers. */
const ATABS=[['ask','Ask my data'],['meet','Meeting minutes'],['report','Reports'],['files','Analyse files']];
const PKIND={minutes:'Minutes',weekly:'Weekly status report',site:'Daily site report',analysis:'File analysis'};
const plainMd=m=>String(m||'').replace(/```[\s\S]*?```/g,' ').replace(/\[\[IMAGE:[^\]]*\]\]/g,' ').replace(/[#*_>|]/g,' ').replace(/\s+/g,' ').trim();
const isoOk=d=>/^\d{4}-\d\d-\d\d$/.test(String(d||''))?d:'';
const cellMd=x=>String(x==null?'':x).replace(/\|/g,'/').replace(/\n+/g,' ').trim()||'-';
function savePaper(kind,title,mdText,pid,extra){const p={id:'r'+Date.now().toString(36),kind,title:clip(title,90),date:Date.now(),md:mdText,pid:pid||'',...(extra||{})};S.papers.unshift(p);save();return p}
async function paperDoc(p){
  const body=await richHtml(p.md,hosted());
  const ph=(p.photos||[]).length?`<h2>Photos</h2>${p.photos.map(x=>`<p><img src="${x.src}" width="320"><br>${esc(x.cap||'')}</p>`).join('')}`:'';
  return `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><title>${esc(p.title)}</title><style>body{font-family:Calibri,Arial,sans-serif;font-size:11pt;line-height:1.45;max-width:17cm;margin:2cm auto}h1{font-size:20pt}h2{font-size:14pt;margin-top:18pt}table{border-collapse:collapse}td,th{border:1px solid #777;padding:4pt 7pt;text-align:left;vertical-align:top}th{background:#eee}</style></head><body>${body}${ph}<p style="color:#666;font-size:9pt">Prepared with OrganizerTX on ${fmtDate(p.date)}. AI-assisted: check figures and names before sending.</p></body></html>`;
}
/* ---------- 1. Ask my data ---------- */
function dataContext(q){
  const words=new Set(String(q).toLowerCase().match(/[a-z0-9]{3,}/g)||[]),score=t=>{let n=0;new Set(String(t).toLowerCase().match(/[a-z0-9]{3,}/g)||[]).forEach(w=>{if(words.has(w))n++});return n};
  const docs=S.topics.flatMap(t=>t.docs.map(d=>({t,d,s:score(d.title+' '+t.title+' '+String(d.md).slice(0,6000))}))).sort((a,b)=>b.s-a.s||b.d.date-a.d.date);
  return {today:dash(Date.now()),weekday:new Date().toLocaleDateString('en-GB',{weekday:'long'}),
    projects:S.plans.filter(onBoard).map(p=>({id:p.id,name:p.name,progress:pct(p)+'%',tasks:p.acts.length})),
    tasks:allTasks().slice(0,160).map(t=>({id:t.id,task:t.a.name,project:t.p.name,status:stLabel(t.a.status),due:t.due||'',owner:t.a.owner||'',notes:clip(t.a.detail||'',120)})),
    documents:docs.slice(0,24).map(({t,d,s},i)=>({ref:d.ref,folder:t.title,title:d.title,date:dash(d.date),text:plainMd(d.md).slice(0,i<3&&s?2600:240)})),
    fieldLog:S.plans.flatMap(p=>(p.log||[]).map(e=>({project:p.name,date:dash(e.date),kind:LOGK[e.kind][0],text:clip(e.text||e.title||e.url||'',240)}))).sort((a,b)=>a.date<b.date?1:-1).slice(0,40),
    minutesAndReports:S.papers.map(p=>({p,s:score(p.title+' '+p.md)})).sort((a,b)=>b.s-a.s||b.p.date-a.p.date).slice(0,8).map(({p,s},i)=>({kind:PKIND[p.kind],title:p.title,date:dash(p.date),text:plainMd(p.md).slice(0,i<2&&s?2000:260)})),
    brainNotes:String(S.brain.organized||'').slice(0,5000)};
}
const UNDO={};
function applyActions(list){
  const out=[],proj=v=>S.plans.filter(onBoard).find(p=>p.id===v||p.name.toLowerCase()===String(v||'').toLowerCase())||S.plans.find(p=>p.id==='my');
  (Array.isArray(list)?list:[]).slice(0,8).forEach(x=>{
    if(!x||typeof x!=='object')return;const key='u'+Math.random().toString(36).slice(2,9),say=(text,undo)=>{UNDO[key]=undo;out.push({text,key})};
    if(x.type==='add_task'&&String(x.name||'').trim()){const p=proj(x.project),a={name:clip(String(x.name).trim(),120),detail:String(x.notes||'').trim(),status:'todo',due:isoOk(x.due),owner:clip(String(x.owner||'').trim(),40)};p.acts.push(a);
      say(`Added "${a.name}" to ${p.name}${a.due?', due '+fmtShort(a.due):''}${a.owner?', owner '+a.owner:''}`,()=>{const i=p.acts.indexOf(a);if(i>=0)p.acts.splice(i,1)});return}
    const t=findTask(x.id);if(!t)return;const a=t.a;
    if(x.type==='complete_task'||(x.type==='set_status'&&x.status==='done')){const was=a.status,wc=a.closed;a.status='done';a.closed=Date.now();say(`Marked "${a.name}" complete`,()=>{a.status=was;a.closed=wc})}
    else if(x.type==='set_status'&&STATUS.some(s=>s[0]===x.status)){const was=a.status;a.status=x.status;say(`"${a.name}" is now ${stLabel(x.status)}`,()=>{a.status=was})}
    else if(x.type==='set_due'&&(isoOk(x.due)||x.due==='')){const was=a.due;a.due=isoOk(x.due);say(a.due?`"${a.name}" is now due ${fmtShort(a.due)}`:`Removed the due date from "${a.name}"`,()=>{a.due=was})}
    else if(x.type==='set_owner'){const was=a.owner;a.owner=clip(String(x.owner||'').trim(),40);say(`"${a.name}" is now owned by ${a.owner||'nobody'}`,()=>{a.owner=was})}
  });
  return out;
}
function askData(q){
  q=String(q||'').trim();if(!q)return;if(needKey())return;
  S.asst.push({role:'user',text:q,date:Date.now()});V.as.q='';
  job('assist','Looking through your data',async signal=>{
    const hist=S.asst.slice(-7,-1).map(m=>(m.role==='user'?'User: ':'Assistant: ')+clip(m.text,400)).join('\n');
    const r=await callAI({system:systemPrompt(),depth:'helper',maxTokens:3000,signal,messages:[{role:'user',content:
`You are the assistant inside OrganizerTX for ${S.profile.name||'the user'}. Answer from the user's own data below, and carry out simple task commands.
DATA (JSON): ${JSON.stringify(dataContext(q))}
${hist?'EARLIER IN THIS CHAT:\n'+hist+'\n':''}USER: ${q}

Rules:
- Use only the data above. If the answer is not in it, say so plainly and suggest researching it on Home. Never invent tasks, dates, figures or documents.
- Name the document reference, project or date you took a fact from.
- Be brief: a direct answer first, then short bullets if needed. Plain words.
- Only when the user clearly asks to change something, add actions. Work out dates from today (${dash(Date.now())}, ${new Date().toLocaleDateString('en-GB',{weekday:'long'})}); "Friday" means the next Friday.
Reply with only a JSON object:
{"answer":"markdown text","actions":[{"type":"add_task","name":"...","project":"project id or name, or empty for My tasks","due":"YYYY-MM-DD or empty","owner":"name or empty","notes":""},{"type":"complete_task","id":"task id"},{"type":"set_status","id":"task id","status":"todo|doing|blocked|done"},{"type":"set_due","id":"task id","due":"YYYY-MM-DD"},{"type":"set_owner","id":"task id","owner":"name"}]}
Use an empty actions list when nothing should change.`}]});
    const o=grab(r.text,'{','}'),ans=o&&typeof o.answer==='string'?o.answer.trim():String(r.text||'').trim();
    if(!ans)throw new Error('No answer came back. Try asking again.');
    const acts=o?applyActions(o.actions):[];
    S.asst.push({role:'ai',text:ans,date:Date.now(),acts});if(S.asst.length>40)S.asst=S.asst.slice(-40);
  });
}
/* ---------- 2. Meeting notes -> minutes -> tasks ---------- */
let dictating=null;
function dictate(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR){toast('Dictation is not available in this browser. Type or paste the notes instead.');return}
  if(dictating){try{dictating.stop()}catch(e){}dictating=null;render();return}
  const r=new SR();r.continuous=true;r.interimResults=false;r.lang=navigator.language||'en-GB';
  r.onresult=e=>{let t='';for(let i=e.resultIndex;i<e.results.length;i++)if(e.results[i].isFinal)t+=e.results[i][0].transcript;if(t){V.meet.notes=(V.meet.notes?V.meet.notes.replace(/\s*$/,' '):'')+t.trim();const el=$('#mnotes');if(el)el.value=V.meet.notes}};
  r.onerror=e=>{if(e.error!=='no-speech'){toast('Dictation stopped: '+e.error+'.');dictating=null;render()}};r.onend=()=>{if(dictating===r){dictating=null;render()}};
  try{r.start();dictating=r;render()}catch(e){toast('Could not start dictation.')}
}
function makeMinutes(){
  const m=V.meet,notes=String(m.notes||'').trim();if(notes.length<30){toast('Paste or dictate the meeting notes first.');return}if(needKey())return;
  job('meet','Writing the minutes',async signal=>{
    const r=await callAI({system:systemPrompt(),depth:'brief',search:0,maxTokens:6000,signal,messages:[{role:'user',content:
`Turn these rough meeting notes into formal minutes. Use ONLY what the notes say; do not invent attendees, decisions, figures or dates. Where the notes are unclear, put the point under "open".
Meeting title: ${m.title||'(not given)'}
Date: ${m.date}
Attendees given: ${m.who||'(not given)'}
Today is ${dash(Date.now())}. Turn relative dates such as "next Friday" into YYYY-MM-DD, counted from the meeting date.
NOTES:
${notes.slice(0,24000)}

Reply with only a JSON object:
{"title":"short meeting title","summary":"2 to 4 sentences","attendees":["name"],"discussion":[{"topic":"...","points":["..."]}],"decisions":["..."],"actions":[{"task":"starts with a verb","owner":"name or empty","due":"YYYY-MM-DD or empty"}],"open":["question or unclear point"]}`}]});
    const o=grab(r.text,'{','}');if(!o||!o.summary)throw new Error('The minutes came back in a form that could not be read. Try again.');
    const arr=x=>Array.isArray(x)?x.map(y=>typeof y==='string'?y.trim():y).filter(Boolean):[],title=String(o.title||m.title||'Meeting').trim();
    const actions=arr(o.actions).filter(a=>a&&String(a.task||'').trim()).map(a=>({task:clip(String(a.task).trim(),120),owner:clip(String(a.owner||'').trim(),40),due:isoOk(a.due),on:true}));
    const who=arr(o.attendees).length?arr(o.attendees).join(', '):m.who;
    const mdText=[`# Minutes: ${title}`,'',`**Date:** ${fmtDate(new Date(m.date+'T12:00').getTime())}${who?'  \n**Attendees:** '+who:''}`,'','## Summary','',String(o.summary).trim(),
      ...(arr(o.discussion).length?['','## Discussion',...arr(o.discussion).flatMap(d=>['',`### ${String(d.topic||'Item').trim()}`,'',...arr(d.points).map(p=>'- '+p)])]:[]),
      ...(arr(o.decisions).length?['','## Decisions','',...arr(o.decisions).map(d=>'- '+d)]:[]),
      '','## Action items','',...(actions.length?['| # | Action | Owner | Due |','|---|---|---|---|',...actions.map((a,i)=>`| ${i+1} | ${cellMd(a.task)} | ${cellMd(a.owner)} | ${a.due?fmtShort(a.due):'-'} |`)]:['No action items were recorded.']),
      ...(arr(o.open).length?['','## Open questions','',...arr(o.open).map(d=>'- '+d)]:[])].join('\n');
    m.out={title,md:mdText,actions};
  });
}
function saveMinutes(withTasks){
  const m=V.meet,o=m.out;if(!o)return;const p=S.plans.find(x=>x.id===m.pid)||S.plans.find(x=>x.id==='my'),picked=withTasks?o.actions.filter(a=>a.on):[];
  picked.forEach(a=>p.acts.push({name:a.task,owner:a.owner,due:a.due,status:'todo',detail:'From the minutes: '+o.title}));
  const paper=savePaper('minutes',o.title,o.md,p.id);V.meet={title:'',date:dash(Date.now()),who:'',notes:'',pid:m.pid,out:null};V.paper=paper.id;
  toast(picked.length?`Minutes saved and ${picked.length} action${picked.length===1?'':'s'} added to ${p.name}.`:'Minutes saved.');
}
/* ---------- 3. One-click reports ---------- */
function weeklyFacts(pid){
  const from=Date.now()-7*DAY,today=dash(Date.now()),next=dash(Date.now()+7*DAY),inScope=p=>!pid||p.id===pid,ts=allTasks().filter(t=>inScope(t.p)),row=t=>({task:t.a.name,project:t.p.name,owner:t.a.owner||'',due:t.due||''});
  return {period:fmtShort(from)+' to '+fmtShort(Date.now()),scope:pid?(S.plans.find(p=>p.id===pid)||{}).name:'All projects',
    projects:S.plans.filter(p=>onBoard(p)&&inScope(p)&&p.acts.length).map(p=>({name:p.name,progress:pct(p),closed:p.acts.filter(isDone).length,total:p.acts.length})),
    closed:ts.filter(t=>isDone(t.a)&&t.a.closed>from).map(row),doing:ts.filter(t=>t.a.status==='doing').map(row),blocked:ts.filter(t=>t.a.status==='blocked').map(row),
    overdue:ts.filter(t=>!isDone(t.a)&&t.due&&t.due<today).map(row),next:ts.filter(t=>!isDone(t.a)&&t.due&&t.due>=today&&t.due<=next).map(row),
    documents:pid?[]:S.topics.flatMap(t=>t.docs.filter(d=>d.date>from).map(d=>({ref:d.ref,title:d.title,date:dash(d.date)}))),
    fieldNotes:S.plans.filter(inScope).flatMap(p=>(p.log||[]).filter(e=>e.date>from).map(e=>({project:p.name,date:dash(e.date),kind:LOGK[e.kind][0],text:clip(e.text||e.title||e.url||'',260)}))),
    minutes:S.papers.filter(x=>x.kind==='minutes'&&x.date>from&&(!pid||x.pid===pid)).map(x=>({title:x.title,date:dash(x.date)}))};
}
const tblMd=(rows,none)=>rows.length?['| Task | Project | Owner | Due |','|---|---|---|---|',...rows.map(r=>`| ${cellMd(r.task)} | ${cellMd(r.project)} | ${cellMd(r.owner)} | ${r.due?fmtShort(r.due):'-'} |`)].join('\n'):none;
function weeklyTables(f){
  return ['## Status at a glance','','| Project | Progress | Closed | Total |','|---|---|---|---|',...(f.projects.length?f.projects.map(p=>`| ${cellMd(p.name)} | ${p.progress}% | ${p.closed} | ${p.total} |`):['| - | - | - | - |']),
    '','## Completed this week','',tblMd(f.closed,'Nothing was closed this week.'),'','## In progress','',tblMd(f.doing,'Nothing is in progress.'),'','## Blocked and overdue','',tblMd([...f.blocked,...f.overdue.filter(o=>!f.blocked.some(b=>b.task===o.task&&b.project===o.project))],'Nothing is blocked or overdue.'),
    '','## Due in the next 7 days','',tblMd(f.next,'Nothing is due in the next 7 days.')].join('\n');
}
function makeReport(kind){
  const R=V.rep;
  if(kind==='weekly'){
    const f=weeklyFacts(R.wpid),title=`Weekly status report: ${f.scope}, week ${isoWeek(Date.now())}`,head=`# ${title}\n\n**Period:** ${f.period}  \n**Prepared by:** ${S.profile.name||'-'}\n\n`,tables=weeklyTables(f);
    const local=()=>`## Summary\n\n${f.closed.length} task${f.closed.length===1?'':'s'} closed, ${f.doing.length} in progress, ${f.blocked.length} blocked and ${f.overdue.length} overdue.\n\n`;
    const done=body=>{const p=savePaper('weekly',title,head+body+tables,R.wpid);V.paper=p.id};
    if(hosted()&&!cred()){done(local());toast('Report built from your data. Add your '+credName()+' in Settings for a written summary.');render();return}
    job('report','Writing the weekly report',async signal=>{
      let body=local();
      try{const r=await callAI({system:systemPrompt(),depth:'brief',search:0,maxTokens:6000,signal,messages:[{role:'user',content:
`Write the narrative part of a weekly status report for a manager. Use ONLY the facts below; do not invent progress, figures, names or dates. If a section has nothing, say so in one line.
FACTS (JSON): ${JSON.stringify(f)}
Write in markdown with exactly these sections, each short:
## Summary (3 to 5 sentences: overall position and the one thing that needs attention)
## Progress this week
## Risks and blockers (what is blocked or overdue, and what would clear it)
## Plan for next week
## Decisions or support needed
Do not include tables; the tables are added separately. Do not add a title.`}]});if(String(r.text||'').trim().length>80)body=r.text.trim()+'\n\n'}
      catch(e){if(e.name==='AbortError'||e.code==='aborted')throw e;toast('The written summary did not work, so the report uses your data only.')}
      done(body);
    });
  }else{
    const p=S.plans.find(x=>x.id===R.spid);if(!p){toast('Choose a project first.');return}
    const entries=(p.log||[]).filter(e=>dash(e.date)===R.sdate).sort((a,b)=>a.date-b.date);
    if(!entries.length){toast('Nothing was captured for '+p.name+' on '+fmtShort(R.sdate)+'. Use Data Capture on site first.');return}
    const hm=t=>new Date(t).toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'}),tname=e=>{const t=e.task!==undefined&&e.task!==''&&p.acts[+e.task];return t?t.name:''};
    const facts={project:p.name,date:R.sdate,entries:entries.map(e=>({time:hm(e.date),kind:LOGK[e.kind][0],text:e.text||e.title||e.url||'',task:tname(e)})),openTasks:p.acts.filter(a=>!isDone(a)).map(a=>({task:a.name,status:stLabel(a.status),due:a.due||'',owner:a.owner||''})),progress:pct(p)+'%'};
    const title=`Daily site report: ${p.name}, ${fmtShort(R.sdate)}`,head=`# ${title}\n\n**Date:** ${fmtDate(new Date(R.sdate+'T12:00').getTime())}  \n**Prepared by:** ${S.profile.name||'-'}  \n**Project progress:** ${facts.progress}\n\n`;
    const record=['## Site record','','| Time | Type | Note | Task |','|---|---|---|---|',...facts.entries.map(e=>`| ${e.time} | ${e.kind} | ${cellMd(e.text)} | ${cellMd(e.task)} |`)].join('\n');
    const photos=entries.filter(e=>e.kind==='photo'&&e.thumb).map(e=>({src:e.thumb,cap:hm(e.date)+(e.text?' · '+e.text:'')}));
    const local=()=>`## Summary\n\n${entries.length} item${entries.length===1?'':'s'} recorded on site: ${['photo','voice','web','note'].map(k=>{const n=entries.filter(e=>e.kind===k).length;return n?n+' '+LOGK[k][0].toLowerCase()+(n===1?'':'s'):''}).filter(Boolean).join(', ')}.\n\n`;
    const done=body=>{const paper=savePaper('site',title,head+body+record,p.id,{photos});V.paper=paper.id};
    if(hosted()&&!cred()){done(local());toast('Report built from your site record. Add your '+credName()+' in Settings for a written summary.');render();return}
    job('report','Writing the site report',async signal=>{
      let body=local();
      try{const r=await callAI({system:systemPrompt(),depth:'brief',search:0,maxTokens:5000,signal,messages:[{role:'user',content:
`Write the narrative part of a daily site report from the site record below. Use ONLY what was recorded; do not invent quantities, people, weather or events. Photos are listed by their captions only.
FACTS (JSON): ${JSON.stringify(facts)}
Write in markdown with exactly these sections, each short:
## Summary (2 to 4 sentences)
## Work done today
## Observations and issues
## Next steps
Do not include tables or a title; the site record table is added separately.`}]});if(String(r.text||'').trim().length>60)body=r.text.trim()+'\n\n'}
      catch(e){if(e.name==='AbortError'||e.code==='aborted')throw e;toast('The written summary did not work, so the report uses your site record only.')}
      done(body);
    });
  }
}
/* ---------- 4. Upload and analyse files ---------- */
const FTASK={sum:['Summarise','Summarise this document for a busy manager: what it is, the key points, figures and dates, obligations or actions for the reader, and anything unusual. End with a short list of questions worth asking.'],
  quote:['Check a quotation','Check this quotation. Re-add the arithmetic line by line and state any totals that do not add up. List what is included, what is missing or excluded, the validity, payment and delivery terms, and warranty. Flag unit rates that look unusual for '+'{place}'+' and say clearly that market rates were not verified. End with questions to send to the supplier.'],
  contract:['Review a contract','Review this contract for the reader as a party to it. Give: the parties, scope, price and payment terms, key dates and deadlines, obligations of each side, penalties and liabilities, termination, and dispute resolution. Then list the clauses that carry the most risk and why, and what to clarify or negotiate. Say plainly that this is an AI reading, not legal advice.'],
  compare:['Compare two documents','Compare the two documents. Start with a one-paragraph verdict, then a table of the differences that matter (item, first document, second document, why it matters), then what is the same, then what to check before choosing or signing.'],
  ask:['Ask a question','Answer the user\'s question from the document. Quote the clause, page or line you relied on where you can. If the document does not answer it, say so.']};
const fileKind=f=>{const n=f.name.toLowerCase();return /\.pdf$/.test(n)||f.type==='application/pdf'?'pdf':/^image\//.test(f.type)?'image':/\.docx$/.test(n)?'docx':/\.(xlsx|xls)$/.test(n)?'sheet':/\.(txt|md|csv|json|html?|xml|log|rtf)$/.test(n)||/^text\//.test(f.type)?'text':''};
const libLoad={};
const loadLib=(k,src)=>libLoad[k]||(libLoad[k]=new Promise((ok,no)=>{const sc=document.createElement('script');sc.src=src;sc.onload=ok;sc.onerror=()=>{delete libLoad[k];no(new Error('Could not load the reader for this file type. Check your internet connection.'))};document.head.appendChild(sc)}));
const b64=f=>new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(String(r.result).split(',')[1]);r.onerror=()=>no(new Error('Could not read '+f.name+'.'));r.readAsDataURL(f)});
async function fileBlocks(f,label){
  const k=fileKind(f),cap=t=>String(t).slice(0,120000);
  if(k==='text')return [{type:'text',text:`${label} (${f.name}):\n${cap(await f.text())}`}];
  if(k==='docx'){await loadLib('mammoth','https://cdn.jsdelivr.net/npm/mammoth@1.8.0/mammoth.browser.min.js');const r=await window.mammoth.extractRawText({arrayBuffer:await f.arrayBuffer()});return [{type:'text',text:`${label} (${f.name}):\n${cap(r.value)}`}]}
  if(k==='sheet'){await loadLib('xlsx','https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js');const wb=window.XLSX.read(await f.arrayBuffer(),{type:'array'});return [{type:'text',text:`${label} (${f.name}):\n${cap(wb.SheetNames.map(n=>`Sheet "${n}":\n`+window.XLSX.utils.sheet_to_csv(wb.Sheets[n])).join('\n\n'))}`}]}
  if(k==='pdf'){if(f.size>12e6)throw new Error(f.name+' is larger than 12 MB. Split it or export fewer pages.');return [{type:'text',text:`${label} (${f.name}) follows.`},{type:'document',source:{type:'base64',media_type:'application/pdf',data:await b64(f)}}]}
  if(k==='image'){if(f.size>4.5e6)throw new Error(f.name+' is larger than 4.5 MB. Use a smaller picture.');return [{type:'text',text:`${label} (${f.name}) follows.`},{type:'image',source:{type:'base64',media_type:f.type,data:await b64(f)}}]}
  throw new Error(f.name+' is not a type OrganizerTX can read. Use PDF, Word, Excel, a picture or a text file.');
}
let FA_FILES=[];
function analyseFiles(){
  const A=V.fa,fs=FA_FILES;if(!fs.length){toast('Choose a file first.');return}
  if(A.task==='compare'&&fs.length<2){toast('Choose two files to compare.');return}
  if(A.task==='ask'&&!A.q.trim()){toast('Type your question about the file.');return}
  if(needKey())return;
  if(!hosted()&&fs.some(f=>['pdf','image'].includes(fileKind(f)))){toast('PDFs and pictures can be analysed in the installed version. In this preview, use Word, Excel or text files.');return}
  A.out='';A.names=fs.map(f=>f.name);
  job('files','Reading '+(fs.length>1?'the files':fs[0].name),async(signal,onText,onStatus)=>{
    const blocks=[];for(let i=0;i<fs.length;i++)blocks.push(...await fileBlocks(fs[i],fs.length>1?(i?'SECOND DOCUMENT':'FIRST DOCUMENT'):'DOCUMENT'));
    onStatus('Analysing');
    const ask=`${FTASK[A.task][1].replace('{place}',place())}${A.q.trim()?'\n\nThe user adds: '+A.q.trim():''}\n\nWrite in markdown with clear headings and tables where they help. Start with a heading that names the document. Use only what is in the file${fs.length>1?'s':''}; where something is missing or unreadable, say so. Give amounts as written in the document.`;
    const allText=blocks.every(b=>b.type==='text'),content=allText?blocks.map(b=>b.text).join('\n\n-----\n\n')+'\n\n-----\n\n'+ask:[...blocks,{type:'text',text:ask}];
    const r=await callAI({system:systemPrompt(),depth:'brief',search:0,maxTokens:8000,signal,onText:t=>{A.out=t;onText(t)},messages:[{role:'user',content}]});
    A.out=String(r.text||'').trim();if(!A.out)throw new Error('No analysis came back. Try again.');A.done=true;
  });
}
/* ---------- the Assistant page ---------- */
function paperView(p){
  return `<div class="page wide asst"><div class="sheetbar noprint" style="padding-left:0;padding-right:0"><button class="btn ghost" data-act="paper-close">&larr; Back</button><span class="pill on">${PKIND[p.kind]}</span><span class="small muted">${fmtDT(p.date)}</span><span style="flex:1"></span>
    <button class="btn" data-act="paper-word">${hosted()?'Word':'Download'}</button><button class="btn" data-act="print">Print or PDF</button><button class="btn" data-act="paper-copy">Copy</button><button class="btn danger" data-act="paper-del">Delete</button></div>
    <div class="md paperdoc">${md(p.md)}${(p.photos||[]).length?`<h2>Photos</h2><div class="pphotos">${p.photos.map(x=>`<figure><img src="${x.src}" alt=""><figcaption class="small muted">${esc(x.cap||'')}</figcaption></figure>`).join('')}</div>`:''}</div>
    <p class="small muted noprint">AI-assisted. Check names, figures and dates before you send it.</p></div>`;
}
function viewAssist(){
  const paper=V.paper&&S.papers.find(p=>p.id===V.paper);if(paper)return paperView(paper);
  const tab=ATABS.some(t=>t[0]===V.atab)?V.atab:'ask',projs=S.plans.filter(onBoard),popt=(sel,all)=>`${all?`<option value="">${all}</option>`:''}${projs.map(p=>`<option value="${p.id}" ${p.id===sel?'selected':''}>${esc(p.name)}</option>`).join('')}`;
  const mine=k=>busy&&busy.topicId===k,working=k=>mine(k)?`<div class="working"><span class="spin"></span><span id="joblabel">${esc(busy.label)}...</span><button class="btn ghost small" data-act="stop">Stop</button></div>`:'';
  const body={
    ask:()=>{const ex=['What is overdue or blocked?','Add a task to call the supplier on Friday','What did my latest report conclude?','Summarise this week’s field notes'];
      return `<div class="achat" id="achat">${S.asst.length?S.asst.map(m=>m.role==='user'?`<div class="amsg me">${esc(m.text)}</div>`:`<div class="amsg ai"><div class="md">${md(m.text)}</div>${(m.acts||[]).map(a=>`<div class="aact ${a.undone?'un':''}"><span>${a.undone?'Undone: ':'&#10003; '}${esc(a.text)}</span>${!a.undone&&UNDO[a.key]?`<button class="btn ghost small" data-act="asst-undo" data-v="${a.key}">Undo</button>`:''}</div>`).join('')}</div>`).join('')
        :`<div class="aempty"><h2>Ask about your own work</h2><p class="muted" style="margin:.3em 0 12px">Answers come from your tasks, documents, field log, minutes and brain on this device. You can also give commands.</p><div class="row" style="justify-content:center">${ex.map(x=>`<button class="chip" data-act="asst-ex" data-v="${esc(x)}">${esc(x)}</button>`).join('')}</div></div>`}${working('assist')}</div>
        <div class="composer abar"><textarea id="aq" data-bind="as.q" rows="1" placeholder="Ask a question, or say what to do: add a task, mark one complete, move a date..." aria-label="Ask your data">${esc(V.as.q)}</textarea><button class="btn primary" data-act="asst-send" ${busy?'disabled':''}>Ask</button>${S.asst.length?'<button class="btn ghost small" data-act="asst-clear">Clear</button>':''}</div>`},
    meet:()=>{const m=V.meet,o=m.out;
      return o?`<div class="row" style="justify-content:space-between"><h2 style="font-size:1.15rem">Check the minutes</h2><button class="btn ghost small" data-act="meet-back">&larr; Edit the notes</button></div>
        <div class="agrid"><div class="card md" style="max-height:62vh;overflow:auto">${md(o.md)}</div>
        <div class="card" style="display:flex;flex-direction:column;gap:10px"><span class="lbl">Action items to add to the board</span>
          ${o.actions.length?o.actions.map((a,i)=>`<div class="mact"><button class="box" role="checkbox" aria-checked="${a.on}" aria-label="Add this action" data-act="meet-tick" data-v="${i}">${a.on?'&#10003;':''}</button><div class="grow"><span class="b" style="font-weight:600">${esc(a.task)}</span><span class="row" style="gap:6px;margin-top:4px"><input type="text" data-bind="meet.out.actions.${i}.owner" value="${esc(a.owner)}" placeholder="Owner" aria-label="Owner" style="max-width:150px;min-height:34px"><input type="date" data-bind="meet.out.actions.${i}.due" value="${esc(a.due)}" aria-label="Due date" style="width:auto;min-height:34px"></span></div></div>`).join(''):'<p class="small muted" style="margin:0">No action items were found in the notes.</p>'}
          <div class="field"><label for="mpid">Add them to</label><select id="mpid" data-bind="meet.pid">${popt(m.pid||'my')}</select></div>
          <div class="row"><button class="btn primary" data-act="meet-save" data-v="1">Save minutes${o.actions.some(a=>a.on)?' and add '+o.actions.filter(a=>a.on).length+' to the board':''}</button><button class="btn" data-act="meet-save" data-v="">Save minutes only</button></div></div></div>`
      :`<div class="agrid"><div class="card" style="display:flex;flex-direction:column;gap:12px">
          <div class="row" style="align-items:flex-start"><div class="field" style="flex:2;min-width:180px"><label for="mtitle">Meeting</label><input type="text" id="mtitle" data-bind="meet.title" value="${esc(m.title)}" placeholder="Site progress meeting"></div><div class="field" style="flex:1;min-width:140px"><label for="mdate">Date</label><input type="date" id="mdate" data-bind="meet.date" value="${esc(m.date)}"></div></div>
          <div class="field"><label for="mwho">Attendees (optional)</label><input type="text" id="mwho" data-bind="meet.who" value="${esc(m.who)}" placeholder="Names, separated by commas"></div>
          <div class="field"><label for="mnotes">Notes</label><textarea id="mnotes" data-bind="meet.notes" rows="9" placeholder="Paste rough notes, a WhatsApp thread or a transcript here, or press Dictate and talk.">${esc(m.notes)}</textarea></div>
          ${working('meet')}
          <div class="row"><button class="btn primary" data-act="meet-go" ${busy?'disabled':''}>Write the minutes</button><button class="btn" data-act="meet-dictate" aria-pressed="${!!dictating}">${ICON.mic.replace('<svg','<svg style="width:18px;height:18px"')}${dictating?'Stop dictating':'Dictate'}</button></div></div>
        <div class="ahint"><span class="lbl">What you get</span><ol><li>Formal minutes: summary, discussion, decisions and open questions.</li><li>Action items with owner and due date, which you can correct.</li><li>Ticked actions go straight onto your task board.</li><li>The minutes are saved and export to Word or PDF.</li></ol></div></div>`},
    report:()=>{const R=V.rep;
      return `${working('report')}<div class="agrid two"><div class="card rcard" style="--pc:var(--s-doing)"><h2>Weekly status report</h2><p class="small muted" style="margin:0">Closed, in progress, blocked, overdue and due next week, with a written summary. Last 7 days.</p>
          <div class="field"><label for="rw">Covers</label><select id="rw" data-bind="rep.wpid">${popt(R.wpid,'All projects')}</select></div><div><button class="btn primary" data-act="rep-go" data-v="weekly" ${busy?'disabled':''}>Write this week’s report</button></div></div>
        <div class="card rcard" style="--pc:var(--s-done)"><h2>Daily site report</h2><p class="small muted" style="margin:0">Built from the photos, voice notes and notes captured for a project on one day.</p>
          <div class="row" style="align-items:flex-start"><div class="field" style="flex:2;min-width:160px"><label for="rs">Project</label><select id="rs" data-bind="rep.spid">${popt(R.spid)}</select></div><div class="field" style="flex:1;min-width:140px"><label for="rd">Day</label><input type="date" id="rd" data-bind="rep.sdate" value="${esc(R.sdate)}"></div></div>
          <div><button class="btn primary" data-act="rep-go" data-v="site" ${busy?'disabled':''}>Write the site report</button></div></div></div>`},
    files:()=>{const A=V.fa;
      return A.out||mine('files')?`<div class="row" style="justify-content:space-between"><h2 style="font-size:1.15rem">${esc(FTASK[A.task][0])}: ${esc((A.names||[]).join(' and '))}</h2>${mine('files')?'':`<span class="row"><button class="btn primary" data-act="fa-save">Save to my reports</button><button class="btn" data-act="fa-copy">Copy</button><button class="btn ghost" data-act="fa-reset">Analyse another</button></span>`}</div>${working('files')}<div class="card md" id="faout">${md(A.out||'',mine('files'))}</div>`
      :`<div class="agrid"><div class="card" style="display:flex;flex-direction:column;gap:14px">
          <label class="capdrop" for="fafile" style="cursor:pointer;text-align:center;padding:22px 14px;border-radius:14px;display:block"><strong>${FA_FILES.length?FA_FILES.map(f=>esc(f.name)+' <span class="small muted">('+fmtSize(f.size)+')</span>').join('<br>'):'Choose a file'}</strong><br><span class="small muted">${FA_FILES.length?'Click to choose different files':'PDF, Word, Excel, picture or text. Choose two to compare.'}</span></label><input type="file" id="fafile" multiple hidden accept=".pdf,.docx,.xlsx,.xls,.txt,.md,.csv,.json,.html,.xml,image/*">
          <div class="field"><span class="lbl">What should I do with it?</span><div class="chips">${Object.entries(FTASK).map(([k,v])=>`<button class="chip" data-act="fa-task" data-v="${k}" aria-pressed="${A.task===k}">${v[0]}</button>`).join('')}</div></div>
          <div class="field"><label for="faq">${A.task==='ask'?'Your question':'Anything to focus on? (optional)'}</label><input type="text" id="faq" data-bind="fa.q" value="${esc(A.q)}" placeholder="${A.task==='ask'?'What is the defects liability period?':'For example: payment terms and penalties'}"></div>
          <div><button class="btn primary" data-act="fa-go" ${busy?'disabled':''}>Analyse</button></div></div>
        <div class="ahint"><span class="lbl">Good to know</span><ul><li>The file is read on this device and sent only to the AI service for this one answer. It is not stored in OrganizerTX.</li><li>Scanned PDFs and photos of documents work, but check the figures it reads.</li><li>A contract review is a reading aid, not legal advice.</li><li>Large files cost more to analyse than a normal question.</li></ul></div></div>`}
  }[tab]();
  const saved=S.papers.slice(0,30);
  return `<div class="page wide asst" style="gap:12px"><div><h1 style="font-size:1.7rem">Assistant</h1><p class="muted small" style="margin:.2em 0 0">Ask your own data, turn meetings into minutes and tasks, write reports, and read files.</p></div>
    <div class="htabs" role="group" aria-label="Assistant tools">${ATABS.map(([k,l])=>`<button data-act="atab" data-v="${k}" aria-pressed="${tab===k}">${l}</button>`).join('')}</div>
    <div class="alay"><div class="amain">${body}</div>
      <aside class="aside2"><span class="lbl">Saved minutes and reports</span>${saved.length?saved.map(p=>`<button class="dchg" data-act="paper-open" data-v="${p.id}"><span class="grow"><span class="b" style="font-weight:600;overflow-wrap:anywhere">${esc(p.title)}</span><span class="b small muted">${PKIND[p.kind]} · ${fmtShort(p.date)}</span></span></button>`).join(''):'<p class="small muted" style="margin:6px 0 0">Minutes, reports and file analyses you save appear here, ready to open, print or send.</p>'}</aside></div></div>`;
}
