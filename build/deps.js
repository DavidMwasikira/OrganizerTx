/* ================= v0.44: task numbers, dependencies and critical path =================
   A task's number is its position in its project, so it never changes when the card moves between lanes.
   a.deps holds the ids of the tasks that must be done first (they may belong to another project). */
function taskIndex(){const m=new Map();S.plans.forEach(p=>p.acts.forEach((a,i)=>{if(!a.id)a.id=uid();m.set(a.id,{a,p,i,n:i+1})}));return m}
const predsOf=(a,m)=>(a.deps||[]).map(id=>m.get(id)).filter(Boolean);
const waitingOn=(a,m)=>predsOf(a,m).filter(x=>!isDone(x.a));
const succsOf=(a,m)=>[...m.values()].filter(x=>(x.a.deps||[]).includes(a.id));
const depLabel=(x,home)=>x.p===home?String(x.n):x.p.name+' '+x.n;
const durOf=a=>num(a.days)>0?num(a.days):num(a.weeks)>0?num(a.weeks)*7:1;
/* would making `a` depend on `cand` create a loop? true when `cand` already (directly or not) depends on `a` */
function loops(a,cand,m){const seen=new Set(),go=x=>{if(x===a)return true;if(seen.has(x.id))return false;seen.add(x.id);return predsOf(x,m).some(y=>go(y.a))};return go(cand)}
/* earliest finish of each task (days) and, per project, the chain of tasks that sets its finish date */
function criticalPaths(m){
  m=m||taskIndex();const ef=new Map(),busyIds=new Set(),EF=a=>{if(ef.has(a.id))return ef.get(a.id);if(busyIds.has(a.id))return durOf(a);busyIds.add(a.id);const v=durOf(a)+Math.max(0,...predsOf(a,m).map(x=>EF(x.a)));busyIds.delete(a.id);ef.set(a.id,v);return v};
  const out=new Map();
  S.plans.forEach(p=>{const linked=p.acts.some(a=>predsOf(a,m).length||succsOf(a,m).length);if(!linked||!p.acts.length)return;
    let last=p.acts[0];p.acts.forEach(a=>{if(EF(a)>EF(last))last=a});
    const chain=[],seen=new Set();let cur=last;while(cur&&!seen.has(cur.id)){seen.add(cur.id);chain.unshift(m.get(cur.id));const ps=predsOf(cur,m);cur=ps.length?ps.reduce((b,x)=>EF(x.a)>EF(b.a)?x:b).a:null}
    out.set(p.id,{days:EF(last),chain,ids:seen})});
  return out;
}
/* the one rule: a task cannot be completed while something it depends on is not done */
function blockDone(a,quiet){const m=taskIndex(),w=waitingOn(a,m),me=m.get(a.id);if(!w.length)return false;
  if(!quiet)toast(`Task ${me?me.n+' ':''}"${clip(a.name,36)}" cannot be completed until ${w.map(x=>'task '+depLabel(x,me&&me.p)+' "'+clip(x.a.name,30)+'"').join(' and ')} ${w.length===1?'is':'are'} done.`);return true}
function linkInOrder(p){p.acts.forEach((a,i)=>{if(!a.id)a.id=uid();a.deps=i?[p.acts[i-1].id]:[]})}
function aiDeps(p){
  if(needKey())return;const m=taskIndex();
  job('deps','Working out the task sequence',async signal=>{
    const r=await callAI({system:systemPrompt(),depth:'helper',maxTokens:3000,signal,messages:[{role:'user',content:
`These are the tasks of the project "${p.name}"${p.what?' ('+p.what+')':''}, numbered in their current order:
${p.acts.map((a,i)=>(i+1)+'. '+a.name+(a.detail?' - '+clip(a.detail,120):'')).join('\n')}

For each task, say which tasks must be finished before it can be finished (its direct predecessors only, by number). Use real-world logic: for example a permit before construction, design before procurement. Tasks that can run side by side must not depend on each other. A task may have no predecessor.
Reply with only a JSON array, one object per task: [{"n":1,"after":[]},{"n":2,"after":[1]}]`}]});
    const arr=grab(r.text,'[',']');if(!Array.isArray(arr)||!arr.length)throw new Error('The sequence came back in a form that could not be read. Try again.');
    p.acts.forEach(a=>{a.deps=[]});let n=0;
    arr.forEach(o=>{const a=p.acts[(+o.n)-1];if(!a||!Array.isArray(o.after))return;o.after.forEach(k=>{const pre=p.acts[(+k)-1];if(pre&&pre!==a&&!a.deps.includes(pre.id)&&!loops(a,pre,taskIndex())){a.deps.push(pre.id);n++}})});
    if(!n)throw new Error('No dependencies were suggested. Use "Link tasks in order", or set them by hand in each task.');
  });
}
/* markers shown on a board card and in the list */
function depMarks(t,m,crit){
  const a=t.a,ps=predsOf(a,m),w=ps.filter(x=>!isDone(x.a)),ss=succsOf(a,m),c=crit.get(t.p.id);
  if(!ps.length&&!ss.length)return '';
  return `<span class="deps">${ps.length?`<span title="Must be done first: ${esc(ps.map(x=>depLabel(x,t.p)+'. '+x.a.name).join('; '))}">After ${esc(ps.map(x=>depLabel(x,t.p)).join(', '))}</span>`:'<span title="Nothing has to be done before this task">Start here</span>'}${ss.length?`<span title="Waiting for this task: ${esc(ss.map(x=>depLabel(x,t.p)+'. '+x.a.name).join('; '))}">Before ${esc(ss.map(x=>depLabel(x,t.p)).join(', '))}</span>`:''}${w.length&&!isDone(a)?`<span class="wait" title="Cannot be completed until these are done">&#128274; Waiting on ${esc(w.map(x=>depLabel(x,t.p)).join(', '))}</span>`:''}${c&&c.ids.has(a.id)&&!isDone(a)?'<span class="crit" title="On the critical path: a delay here delays the whole project">Critical</span>':''}</span>`;
}
/* the bar above the board when one project is chosen */
function depBar(p,m,crit){
  if(!p||p.acts.length<2)return '';const any=p.acts.some(a=>predsOf(a,m).length),c=crit.get(p.id),mine=busy&&busy.topicId==='deps';
  if(mine)return `<div class="working"><span class="spin"></span><span id="joblabel">${esc(busy.label)}...</span><button class="btn ghost small" data-act="stop">Stop</button></div>`;
  if(!any)return `<div class="depbar"><span class="grow"><strong>No task sequence yet.</strong> <span class="small muted">Set which tasks come first, so a task cannot be completed before the ones it depends on.</span></span><button class="btn" data-act="dep-order" data-v="${p.id}">Link tasks in order</button><button class="btn primary" data-act="dep-ai" data-v="${p.id}" ${busy?'disabled':''}>Let AI work out the sequence</button></div>`;
  const cross=c?c.chain.filter(x=>x.p!==p).length:0;
  return `<div class="depbar"><span class="grow"><span class="lbl">Critical path${c?' · about '+Math.round(c.days)+' day'+(Math.round(c.days)===1?'':'s'):''}</span><span class="cpath">${c?c.chain.map(x=>`<button class="${isDone(x.a)?'done':''}" data-act="task-open" data-v="${x.p.id}:${x.i}" title="${esc(x.a.name)}">${esc(depLabel(x,p))}</button>`).join('<i>&rarr;</i>'):''}</span>${cross?`<span class="small muted">Includes ${cross} task${cross===1?'':'s'} from another project.</span>`:''}</span><button class="btn ghost small" data-act="dep-ai" data-v="${p.id}" ${busy?'disabled':''}>Rework with AI</button><button class="btn ghost small" data-act="dep-clear" data-v="${p.id}">Clear sequence</button></div>`;
}
/* which projects wait on which */
function projectLinks(m){
  m=m||taskIndex();const out=[];m.forEach(x=>predsOf(x.a,m).forEach(pr=>{if(pr.p!==x.p)out.push({from:pr,to:x})}));return out;
}
