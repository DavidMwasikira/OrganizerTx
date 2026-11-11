/* ================= v0.45: project views (brief, simple timeline, advanced Gantt, WBS) =================
   One schedule and one phase list feed every view, so an edit in any of them shows everywhere at once. */
const PHC=['var(--k1)','var(--k2)','var(--k3)','var(--k4)','var(--k5)','var(--k6)'];
/* phases in order; tasks with no (or an unknown) phase fall into a last, unnamed group */
function phasesOf(p){
  const names=(p.phases||[]).filter(Boolean),out=names.map((n,i)=>({name:n,idx:i,acts:[]})),loose={name:'',idx:-1,acts:[]};
  p.acts.forEach((a,i)=>{const g=out.find(x=>x.name===a.phase)||loose;g.acts.push({a,i})});
  if(loose.acts.length||!out.length)out.push(loose);return out;
}
/* keep the task list in WBS order (phase by phase), which is also the numbering order */
function orderActs(p){const names=(p.phases||[]);const rank=a=>{const k=names.indexOf(a.phase);return k<0?names.length:k};p.acts=p.acts.map((a,i)=>({a,i})).sort((x,y)=>rank(x.a)-rank(y.a)||x.i-y.i).map(x=>x.a)}
const wbsCode=(p,g,k)=>(p.phases||[]).filter(Boolean).length?(g.idx<0?(p.phases.length+1):g.idx+1)+'.'+(k+1):String(k+1);
/* start week and length of every task: what was typed wins; otherwise a task starts when the tasks it depends on end */
function schedOf(p){
  const m=taskIndex(),memo=new Map(),wk=a=>Math.max(1,Math.round(num(a.weeks)||Math.ceil(num(a.days)/7)||1));
  const st=(a,depth)=>{if(memo.has(a.id))return memo.get(a.id);let v=num(a.start)>0?Math.round(num(a.start)):1;
    if(!(num(a.start)>0)&&depth<60)predsOf(a,m).filter(x=>x.p===p).forEach(x=>{v=Math.max(v,st(x.a,depth+1)+wk(x.a))});memo.set(a.id,v);return v};
  const rows=p.acts.map(a=>({a,start:st(a,0),weeks:wk(a)})),W=Math.max(1,p.weeks||1,...rows.map(r=>r.start+r.weeks-1));
  return {rows,W,by:new Map(rows.map(r=>[r.a.id,r])),t0:p.started||Date.now()};
}
const weekDate=(S0,w)=>S0.t0+(w-1)*7*DAY;
function suggestPhases(p){
  if(needKey())return;
  job('phases','Grouping the tasks into phases',async signal=>{
    const r=await callAI({system:systemPrompt(),depth:'helper',maxTokens:3000,signal,messages:[{role:'user',content:
`Group the tasks of the project "${p.name}" into 3 to 6 phases for a work breakdown structure. Phase names are 1 to 3 words (for example Preparation, Approvals, Procurement, Construction, Handover). Every task goes in exactly one phase; keep the phases in working order.
TASKS:
${p.acts.map((a,i)=>(i+1)+'. '+a.name).join('\n')}
Reply with only a JSON object: {"phases":["name", "..."],"tasks":[{"n":1,"phase":"name"}]}`}]});
    const o=grab(r.text,'{','}');if(!o||!Array.isArray(o.phases)||!Array.isArray(o.tasks))throw new Error('The phases came back in a form that could not be read. Try again.');
    const names=[...new Set(o.phases.map(x=>clip(String(x||'').trim(),40)).filter(Boolean))].slice(0,8);if(!names.length)throw new Error('No phases were suggested. Add them by hand.');
    const acts=p.acts.slice();o.tasks.forEach(t=>{const a=acts[(+t.n)-1],ph=clip(String(t.phase||'').trim(),40);if(a&&names.includes(ph))a.phase=ph});
    p.phases=names;orderActs(p);
  });
}
function simpleGantt(p,S0){
  const W=S0.W,step=W<=8?1:W<=16?2:4,ticks=[];for(let w=1;w<=W;w+=step)ticks.push(`<span style="left:${100*(w-1)/W}%">W${w}</span>`);
  const now=p.active||p.custom?(Date.now()-S0.t0)/(7*DAY)/W*100:-1,mark=now>=0&&now<=100?`<u style="left:${now}%" title="Today"></u>`:'';
  return `<div class="gantt" style="--wk:${100/W}%" role="img" aria-label="Timeline of ${W} weeks"><span></span><div class="sc">${ticks.join('')}</div>${S0.rows.map((r,i)=>`<span class="gn">${i+1}. ${esc(r.a.name)}</span><div class="tr"><i class="${isDone(r.a)?'done':''}" style="left:${100*(r.start-1)/W}%;width:${100*r.weeks/W}%" title="${esc(r.a.name)}: week ${r.start}${r.weeks>1?' to '+(r.start+r.weeks-1):''}"></i>${mark}</div>`).join('')}</div>
  <p class="small muted" style="margin:10px 0 0">W1 is the first week. Filled bars are finished tasks; the orange line is today.</p>`;
}
function advGantt(p,S0){
  const RH=34,WK=30,W=S0.W,groups=phasesOf(p),named=(p.phases||[]).filter(Boolean).length>0,cols=V.gcols!==false,m=taskIndex(),crit=(criticalPaths(m).get(p.id)||{ids:new Set()}).ids;
  const left=[],right=[],pos=new Map();let r=0;
  const miles=(p.miles||[]).filter(x=>isoOk(x.date));
  if(miles.length){left.push(`<div class="agrow ms"><span></span><span class="nm"><b>Milestones</b></span><span class="x"></span><span class="x"></span><span class="x"></span><span class="x"></span><span class="x"></span></div>`);
    right.push(`<div class="agline">${miles.map(x=>{const w=(new Date(x.date+'T12:00').getTime()-S0.t0)/(7*DAY);return w>=-0.5&&w<=W+0.5?`<i class="dia ${x.done?'done':''}" style="left:${Math.max(0,w*WK)}px" title="Milestone: ${esc(x.name)}, ${fmtShort(x.date)}"></i>`:''}).join('')}</div>`);r++}
  groups.forEach(g=>{const c=PHC[(g.idx<0?groups.length-1:g.idx)%PHC.length],rows=g.acts.map(({a})=>S0.by.get(a.id));
    if(named){const s=rows.length?Math.min(...rows.map(x=>x.start)):1,e=rows.length?Math.max(...rows.map(x=>x.start+x.weeks)):2,dn=g.acts.filter(({a})=>isDone(a)).length,hrs=g.acts.reduce((t,{a})=>t+num(a.hours),0);
      left.push(`<div class="agrow ph" style="--c:${c}"><span class="no">${r+1}</span><span class="nm">${g.idx<0?'<b>Not in a phase</b>':`<input type="text" data-gp="${g.idx}" value="${esc(g.name)}" aria-label="Phase name">`}</span><span class="x">${g.idx<0?p.phases.length+1:g.idx+1}</span><span class="x">${rows.length?fmtShort(weekDate(S0,s)):'-'}</span><span class="x">${rows.length?e-s:'-'}</span><span class="x small">${g.acts.length} task${g.acts.length===1?'':'s'}</span><span class="x">${hrs?hrs+' h':'-'}</span></div>`);
      right.push(`<div class="agline">${rows.length?`<i class="sum" style="--c:${c};left:${(s-1)*WK}px;width:${(e-s)*WK}px" title="${esc(g.name||'Not in a phase')}: ${dn} of ${g.acts.length} done"><b style="width:${g.acts.length?100*dn/g.acts.length:0}%"></b></i>`:''}</div>`);r++}
    g.acts.forEach(({a,i},k)=>{const x=S0.by.get(a.id);pos.set(a.id,{r,x1:(x.start-1)*WK,x2:(x.start-1+x.weeks)*WK});
      left.push(`<div class="agrow ${isDone(a)?'done':''}" style="--c:${c}"><span class="no">${r+1}</span><span class="nm ${named?'in':''}"><input type="text" data-g="${i}|name" value="${esc(a.name)}" aria-label="Task name"></span><span class="x">${wbsCode(p,g,k)}</span><span class="x"><input type="date" data-g="${i}|start" value="${dash(weekDate(S0,x.start))}" aria-label="Planned start"></span><span class="x"><input type="text" inputmode="numeric" data-g="${i}|weeks" value="${x.weeks}" aria-label="Weeks"></span><span class="x"><input type="text" data-g="${i}|cost" value="${esc(a.cost||(a.budget?a.budget.cur+' '+num(a.budget.amt).toLocaleString('en-GB'):''))}" placeholder="-" aria-label="Planned cost"></span><span class="x"><input type="text" inputmode="decimal" data-g="${i}|hours" value="${num(a.hours)||''}" placeholder="-" aria-label="Work hours"></span></div>`);
      right.push(`<div class="agline"><button class="bar ${isDone(a)?'done':a.status==='doing'?'doing':''} ${crit.has(a.id)&&!isDone(a)?'crit':''}" style="--c:${c};left:${(x.start-1)*WK}px;width:${x.weeks*WK}px" data-act="task-open" data-v="${p.id}:${i}" title="${i+1}. ${esc(a.name)}: ${fmtShort(weekDate(S0,x.start))}, ${x.weeks} week${x.weeks===1?'':'s'}${crit.has(a.id)?' · on the critical path':''}" aria-label="${esc(a.name)}"></button></div>`);r++})});
  const links=[];p.acts.forEach(a=>predsOf(a,m).filter(x=>x.p===p).forEach(pr=>{const A=pos.get(pr.a.id),B=pos.get(a.id);if(!A||!B)return;const y1=A.r*RH+RH/2,y2=B.r*RH+RH/2,x1=A.x2,x2=B.x1,cl=crit.has(a.id)&&crit.has(pr.a.id)?'c':'';
    const d=x2>=x1+12?`M${x1} ${y1}h6V${y2}H${x2-1}`:`M${x1} ${y1}h6V${y2-(y2>y1?RH/2:-RH/2)+0.5}H${x2-8}V${y2}H${x2-1}`;links.push(`<path d="${d}" class="${cl}" marker-end="url(#ah${cl})"/>`)}));
  const step=W<=12?1:W<=26?2:4,head=[];for(let w=1;w<=W;w++)head.push(`<span style="left:${(w-1)*WK}px;width:${WK}px" class="${(w-1)%step?'':'t'}">${(w-1)%step?'':`<b>W${w}</b><small>${fmtShort(weekDate(S0,w))}</small>`}</span>`);
  const now=(Date.now()-S0.t0)/(7*DAY)*WK;
  return `<div class="row" style="justify-content:space-between"><span class="small muted">Type in any cell to change it. Click a bar to open the task. Arrows show what must finish first; red marks the critical path.</span><span class="row">${named?'':`<button class="btn small" data-act="ph-ai" ${busy?'disabled':''}>Group into phases with AI</button>`}<button class="btn small" data-act="gcols" aria-pressed="${!cols}">${cols?'Hide the detail columns':'Show the detail columns'}</button></span></div>
  <div class="ag ${cols?'':'nocols'}"><div class="agl"><div class="agrow hd"><span>#</span><span>Task name</span><span class="x">WBS</span><span class="x">Planned start</span><span class="x">Weeks</span><span class="x">Planned cost</span><span class="x">Work hours</span></div>${left.join('')}</div>
    <div class="agr" tabindex="0" aria-label="Gantt chart, scroll sideways"><div class="agtl" style="width:${W*WK}px"><div class="aghd">${head.join('')}</div><div class="agbody" style="background-size:${WK}px 100%">${right.join('')}<svg class="aglinks" width="${W*WK}" height="${r*RH}" aria-hidden="true"><defs><marker id="ah" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z"/></marker><marker id="ahc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8z" class="c"/></marker></defs>${links.join('')}</svg>${now>=0&&now<=W*WK?`<u class="agnow" style="left:${now}px" title="Today"></u>`:''}</div></div></div></div>`;
}
function wbsHtml(p){
  const groups=phasesOf(p),named=(p.phases||[]).filter(Boolean).length>0,s=budSum(p),hrs=p.acts.reduce((t,a)=>t+num(a.hours),0);
  return `<div class="row" style="justify-content:space-between"><span class="small muted">Type in a box to rename it. Drag a task onto another task or phase to move it. Changes show at once on the board and both timelines.</span><span class="row">${named?'':`<button class="btn small" data-act="ph-ai" ${busy?'disabled':''}>Group into phases with AI</button>`}<button class="btn small primary" data-act="ph-add">+ Add phase</button></span></div>
  <div class="wbswrap" tabindex="0" aria-label="Work breakdown structure, scroll sideways"><div class="wbs">
    <div class="wroot"><b>${esc(p.name)}</b><span class="small">${pct(p)}% done · ${p.acts.length} task${p.acts.length===1?'':'s'}${hrs?' · '+hrs+' h':''}${s.n?' · '+money(s.planned):''}</span></div>
    <div class="wcols ${groups.length===1?'one':''}">${groups.map((g,gi)=>{const c=PHC[(g.idx<0?groups.length-1:g.idx)%PHC.length],dn=g.acts.filter(({a})=>isDone(a)).length;
      return `<div class="wcol" data-ph="${g.idx}" style="--c:${c}"><div class="wph">${g.idx<0?`<b>${named?(p.phases.length+1)+'. Not in a phase':'Tasks'}</b>`:`<span class="code">${g.idx+1}.</span><input type="text" data-gp="${g.idx}" value="${esc(g.name)}" aria-label="Phase name"><button class="x" data-act="ph-del" data-v="${g.idx}" aria-label="Remove this phase" title="Remove this phase (its tasks are kept)">&times;</button>`}<span class="small">${g.acts.length?Math.round(100*dn/g.acts.length):0}% · ${g.acts.length} task${g.acts.length===1?'':'s'}</span></div>
        <div class="wts">${g.acts.map(({a,i},k)=>`<div class="wt ${isDone(a)?'done':''}" draggable="true" data-wi="${i}" title="Drag to move"><span class="code">${wbsCode(p,g,k)}</span><input type="text" data-g="${i}|name" value="${esc(a.name)}" aria-label="Task name"><button class="o" data-act="task-open" data-v="${p.id}:${i}" aria-label="Open this task" title="Open this task">&rsaquo;</button></div>`).join('')}<button class="wadd" data-act="ph-task" data-v="${g.idx}">+ Add task</button></div></div>`}).join('')}</div></div></div>`;
}
function planViews(p){
  if(!p.acts.length)return p.summary?`<p style="margin:0">${esc(p.summary)}</p>`:'';
  const tab=['brief','adv','wbs'].includes(V.gtab)?V.gtab:'simple',S0=schedOf(p),mine=busy&&busy.topicId==='phases';
  return `<section class="card pviews"><div class="htabs" role="group" aria-label="Project views">${[['brief','Project Brief'],['simple','Simple'],['adv','Advanced'],['wbs','WBS']].map(([k,l])=>`<button data-act="gtab" data-v="${k}" aria-pressed="${tab===k}">${l}</button>`).join('')}</div>
    ${mine?`<div class="working"><span class="spin"></span><span id="joblabel">${esc(busy.label)}...</span><button class="btn ghost small" data-act="stop">Stop</button></div>`:''}
    ${tab==='brief'?`<div><button class="fold" data-act="brief-fold" aria-expanded="${V.briefShut!==true}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg><span class="lbl">Project brief</span></button>${V.briefShut===true?'':`<p style="margin:8px 0 0">${p.summary?esc(p.summary):'<span class="muted">No brief yet. Draft the plan with AI, or describe the project when you create it.</span>'}</p><div class="facts" style="margin-top:10px"><span><b>Timeline</b>${S0.W} week${S0.W===1?'':'s'}</span><span><b>Starts</b>${fmtShort(S0.t0)}</span><span><b>Ends about</b>${fmtShort(weekDate(S0,S0.W+1))}</span><span><b>Tasks</b>${p.acts.length}</span></div>`}</div>`
      :tab==='simple'?simpleGantt(p,S0):tab==='adv'?advGantt(p,S0):wbsHtml(p)}</section>`;
}
