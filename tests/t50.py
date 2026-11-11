import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
mode={'v':'deps'}
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ''
    if 'direct predecessors' in text: body=json.dumps([{'n':1,'after':[]},{'n':2,'after':[1]},{'n':3,'after':[1]},{'n':4,'after':[2,3]},{'n':5,'after':[4,1]},{'n':2,'after':[5]}])
    elif 'activity plan' in text: body=json.dumps({'summary':'Plan.','activities':[{'name':'Survey site','detail':'d','start':1,'weeks':1,'cost':'','after':[]},{'name':'Get permit','detail':'d','start':2,'weeks':3,'cost':'','after':[1]},{'name':'Buy materials','detail':'d','start':2,'weeks':1,'cost':'','after':[1]},{'name':'Build','detail':'d','start':5,'weeks':4,'cost':'','after':[2,3]}]})
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':1500})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""S.skin='ultraviolet';applyTheme();S.plans.push({id:'pb',name:'Building new site office',what:'x',custom:true,started:Date.now(),log:[],acts:['Define needs, size and budget','Register business and tax IDs','Secure land and do due diligence','Appoint architect and engineers','NEMA environmental approval'].map(n=>({name:n,status:'todo'}))},
          {id:'pc',name:'Borehole for the farm',what:'y',custom:true,started:Date.now(),log:[],acts:[{name:'Hydrogeological survey',status:'todo'},{name:'Drill',status:'todo'}]});S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};V.view='tasks';V.tfilter='pb';save();render()""")
        await pg.wait_for_timeout(300)
        print('numbered cards:',await pg.locator('.kcard .t').all_inner_texts()); print('bar:',(await pg.locator('.depbar').inner_text()).replace('\n',' ')[:70])
        await pg.click('[data-act=dep-ai]'); await pg.wait_for_timeout(1500)
        print('AI sequence (loop 2<-5 rejected):',await pg.evaluate("(()=>{const m=taskIndex();return S.plans.find(p=>p.id==='pb').acts.map(a=>predsOf(a,m).map(x=>x.n))})()"))
        print('critical path:',(await pg.locator('.cpath').inner_text()).replace('\n',' '),'|',await pg.locator('.depbar .lbl').inner_text())
        print('card markers:',[ (await x.inner_text()).replace('\n',' · ') for x in await pg.locator('.kcard .deps').all()])
        await pg.screenshot(path='dp-board.png')
        # rule: cannot complete 2 before 1 (drag)
        await pg.drag_and_drop('.kcard:has-text("Register business")','.lane[data-lane=done]'); await pg.wait_for_timeout(300); print('drag task 2 to Complete while 1 open -> status',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts[1].status"),'| toast:',(await pg.locator('.toast').last.inner_text())[:90] if await pg.locator('.toast').count() else '-')
        await pg.drag_and_drop('.kcard:has-text("Register business")','.lane[data-lane=doing]'); await pg.wait_for_timeout(300); print('drag task 2 to In progress allowed ->',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts[1].status"),'| number kept:',await pg.locator('.lane[data-lane=doing] .kcard .t').inner_text())
        await pg.drag_and_drop('.kcard:has-text("Define needs")','.lane[data-lane=done]'); await pg.wait_for_timeout(300); await pg.drag_and_drop('.kcard:has-text("Register business")','.lane[data-lane=done]'); await pg.wait_for_timeout(300)
        print('after 1 done, 2 can complete ->',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts.slice(0,2).map(a=>a.status)"),'| order in Complete lane:',await pg.locator('.lane[data-lane=done] .kcard .t').all_inner_texts())
        # dialog: status done blocked, deps editor, cross-project
        await pg.click('.kcard:has-text("NEMA")'); await pg.wait_for_timeout(200); print('dialog deps chips:',[x.replace('\n',' ') for x in await pg.locator('#tdeps .pill').all_inner_texts()])
        await pg.select_option('#tstat','done'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200); print('dialog save as done blocked (dialog still open):',await pg.locator('.modal').count()==1)
        await pg.select_option('#tstat','todo'); opts=await pg.locator('#tdepadd optgroup').evaluate_all("els=>els.map(e=>e.label)"); print('picker groups:',opts)
        val=await pg.evaluate("S.plans.find(p=>p.id==='pc').acts[1].id"); await pg.select_option('#tdepadd',val); await pg.fill('#tdays','10'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(300)
        print('cross-project marker:',(await pg.locator('.kcard:has-text("NEMA") .deps').inner_text()).replace('\n',' · '))
        # loop prevention in picker: task 1 must not offer tasks that depend on it
        await pg.click('.kcard:has-text("Define needs")'); await pg.wait_for_timeout(200); n=await pg.locator('#tdepadd optgroup >> nth=0 >> option').count(); print('task 1 picker groups (own project must be absent):',await pg.locator('#tdepadd optgroup').evaluate_all('els=>els.map(e=>e.label)')); await pg.click('[data-x=cancel]')
        # new task defaults to follow the last one
        await pg.click('.toolbar [data-act=task-new]'); await pg.wait_for_timeout(200); print('new task default dependency:',[x.replace('\n',' ') for x in await pg.locator('#tdeps .pill').all_inner_texts()]); await pg.fill('#tname','Hand over'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200)
        print('critical path now:',(await pg.locator('.cpath').inner_text()).replace('\n',' '),'|',await pg.locator('.depbar .lbl').inner_text(),'|',(await pg.locator('.depbar').inner_text()).replace('\n',' ')[-90:])
        await pg.click('[data-act=tmode][data-v=list]'); await pg.wait_for_timeout(200); print('list rows:',[x.split('\n')[0] for x in await pg.locator('table.tl tbody tr td:nth-child(2)').all_inner_texts()][:3]); await pg.click('[data-act=tmode][data-v=board]')
        await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(300); print('DASHBOARD links:',(await pg.locator('.plink').inner_text()).replace('\n',' '))
        await pg.screenshot(path='dp-dash.png')
        # link in order + AI-drafted plan
        await pg.evaluate("V.view='tasks';V.tfilter='pc';render()"); await pg.click('[data-act=dep-order]'); await pg.wait_for_timeout(200); print('link in order ->',(await pg.locator('.cpath').inner_text()).replace('\n',' '))
        await pg.click('.toolbar [data-act=proj-new]'); await pg.fill('#pname','Fence the plot'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(2500)
        print('AI plan sequence:',await pg.evaluate("(()=>{const m=taskIndex(),p=S.plans[S.plans.length-1];return [p.name,p.acts.map(a=>predsOf(a,m).map(x=>x.n))]})()"))
        await pg.reload(); await pg.wait_for_timeout(1500); print('after reload deps kept:',await pg.evaluate("(()=>{const m=taskIndex();return S.plans.find(p=>p.id==='pb').acts.map(a=>predsOf(a,m).map(x=>depLabel(x,S.plans.find(p=>p.id==='pb'))))})()"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("V.view='tasks';V.tfilter='pb';render()"); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs)
        await b.close()
asyncio.run(main())
