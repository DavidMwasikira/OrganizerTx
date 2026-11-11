import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
asked=[]
PLAN={'summary':'Build a borehole for the school.','activities':[{'name':'Survey site','detail':'d','start':1,'weeks':2,'cost':'','after':[],'phase':'Prepare'},{'name':'Get permit','detail':'d','start':2,'weeks':3,'cost':'','after':[1],'phase':'Prepare'},{'name':'Drill','detail':'d','start':5,'weeks':4,'cost':'','after':[2],'phase':'Build'},{'name':'Install pump','detail':'d','start':9,'weeks':2,'cost':'','after':[3],'phase':'Build'}],
 'budget':[{'category':'Labour','item':'Drilling crew','planned':400000},{'category':'Equipment','item':'Pump and solar','planned':350000},{'category':'Nonsense','item':'Permit fees','planned':'50000'}],
 'milestones':[{'name':'Permit issued','week':4},{'name':'Water struck','week':8},{'name':'Handover','week':10}],
 'risks':[{'type':'risk','level':'high','title':'Dry hole','response':'Do a hydro survey first'},{'type':'issue','level':'low','title':'Access road is poor','response':'Grade it'}]}
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ''; asked.append(text)
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(PLAN) if 'activity plan' in text else '[]'}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        cx=await b.new_context(viewport={'width':1600,'height':1000},permissions=['clipboard-read','clipboard-write']); pg=await cx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""const acts=[['Define needs',1,2],['Register business',1,2],['Secure land',2,3],['Appoint architect',4,5],['NEMA approval',8,4],['Build',12,30]].map(([n,s,w],i)=>({id:uid(),name:n,start:s,weeks:w,status:i<2?'done':'todo',phase:i<3?'Prepare':'Deliver',deps:[]}));acts.forEach((a,i)=>{if(i)a.deps=[acts[i-1].id]});
          S.plans.push({id:'pb',name:'Building new site office',what:'x',custom:true,active:true,started:Date.now()-10*DAY,weeks:41,summary:'A new site office for the team.',log:[],phases:['Prepare','Deliver'],miles:[{id:'m1',name:'Permit',date:dash(Date.now()+50*DAY),done:false}],risks:[{type:'risk',level:'high',title:'Rain delays',action:'x',status:'open'}],budget:{lines:[{id:'l1',cat:'Labour',item:'Crew',planned:1000000},{id:'l2',cat:'Materials',item:'Cement',planned:500000}]},spend:[{id:'s1',date:dash(Date.now()),desc:'Deposit',lineId:'l1',net:1365000,vat:0}],acts});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};V.view='plan';V.plan='pb';save();render()""")
        await pg.wait_for_timeout(300)
        print('tabs:',await pg.locator('.ptabs button').all_inner_texts(),'| tab rows',await pg.locator('.ptabs').count(),'| old inner tabs',await pg.locator('[data-act=gtab]').count())
        print('strip: ring',await pg.locator('.bstrip .ring text').text_content(),'| bar inside strip',await pg.locator('.bstrip .bar').count(),'| strip text',(await pg.locator('.bstrip').inner_text()).replace('\n',' | '))
        print('buttons now in activity card:',await pg.locator('section.card:has(.act) [data-act=task-new]').count(),await pg.locator('section.card:has(.act) [data-act=plan-board]').count(),await pg.locator('section.card:has(.act) [data-act=plan-research]').count())
        await pg.screenshot(path='v47-plan.png')
        for k in ['brief','budget','risks','wbs','gsimple','gadv']:
            await pg.click(f'.ptabs [data-v={k}]'); await pg.wait_for_timeout(250)
            print(k,'->',(await pg.locator('main').inner_text())[260:420].replace('\n',' | '),'| copy buttons',await pg.locator('[data-act=pv-copy]').count(),'| overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
            await pg.screenshot(path=f'v47-{k}.png')
        # zoom
        for z in [40,30,12,4]:
            await pg.evaluate(f"(()=>{{const e=document.querySelector('#gzoom');e.value={z};e.dispatchEvent(new Event('change',{{bubbles:true}}))}})()"); await pg.wait_for_timeout(250)
            print('zoom',z,'->',await pg.locator('.agzoom .pill').inner_text(),'| head',(await pg.locator('.agtl').first.inner_text()).replace('\n',' ')[-110:],'| body width',await pg.evaluate("Math.round(document.querySelector('.agbody').getBoundingClientRect().width)"),'| today x',await pg.evaluate("document.querySelector('.agnow')?Math.round(parseFloat(document.querySelector('.agnow').style.left)):null"))
            await pg.locator('.pviews').screenshot(path=f'v47-zoom{z}.png')
        await pg.click('[data-act=pv-copy]'); await pg.wait_for_timeout(300); t=await pg.evaluate("navigator.clipboard.readText()"); print('gantt copy:',t.split('\n')[:3],'| toast',await pg.locator('.toast').inner_text())
        await pg.click('.ptabs [data-v=wbs]'); await pg.click('[data-act=pv-copy]'); await pg.wait_for_timeout(300); print('wbs copy:',(await pg.evaluate("navigator.clipboard.readText()")).split('\n')[:5])
        # toggles
        print('toggles:',await pg.locator('.htog button').all_inner_texts())
        await pg.click('.htog [data-act=rail-hide]'); await pg.wait_for_timeout(200); print('sidebar hidden: nav visible',await pg.locator('nav').is_visible(),'| button says',await pg.locator('.htog [data-act=rail-show]').inner_text())
        await pg.click('.htog [data-act=ws-hide]'); await pg.wait_for_timeout(200); print('list hidden:',not await pg.locator('.wsside').is_visible(),'| says',await pg.locator('.htog [data-act=ws-hide]').inner_text()); await pg.screenshot(path='v47-hidden.png')
        await pg.click('.htog [data-act=rail-show]'); await pg.click('.htog [data-act=ws-hide]'); await pg.wait_for_timeout(200); print('restored: nav',await pg.locator('nav').is_visible(),'| list',await pg.locator('.wsside').is_visible())
        # new project
        await pg.evaluate("projectModal()"); await pg.wait_for_timeout(200); print('boxes:',await pg.locator('.modal label.row').all_inner_texts()); await pg.locator('.modal').screenshot(path='v47-new.png')
        await pg.fill('#pname','School borehole'); await pg.fill('#pwhat','Drill a borehole for the school'); await pg.click('.modal .btn.primary'); await pg.wait_for_timeout(2500)
        print('created:',await pg.evaluate("(()=>{const p=S.plans.find(p=>p.name==='School borehole');return JSON.stringify({acts:p.acts.length,phases:p.phases,lines:p.budget&&p.budget.lines.map(l=>[l.cat,l.item,l.planned]),miles:(p.miles||[]).map(m=>[m.name,m.date]),risks:(p.risks||[]).map(r=>[r.type,r.level,r.title]),gen:p.gen,started:dash(p.started)})})()"))
        print('prompt asked for budget/milestones/risks:',[k in asked[-1] for k in ['"budget"','"milestones"','"risks"']])
        # unticked
        await pg.evaluate("projectModal()"); await pg.fill('#pname','Plain one'); await pg.uncheck('#pgenb'); await pg.uncheck('#pgenx'); await pg.click('.modal .btn.primary'); await pg.wait_for_timeout(2000)
        print('unticked: prompt has extras',[k in asked[-1] for k in ['"budget"','"risks"']],'| saved',await pg.evaluate("(()=>{const p=S.plans.find(p=>p.name==='Plain one');return [p.acts.length,!!p.budget,(p.miles||[]).length,(p.risks||[]).length]})()"))
        # phone
        pg2=await (await b.new_context(viewport={'width':390,'height':800},storage_state=await cx.storage_state())).new_page(); pg2.on('pageerror',lambda e:errs.append(str(e)))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("V.view='plan';V.plan='pb';V.ptab='plan';render()"); await pg.wait_for_timeout(300)
        print('phone: overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"),'| toggles shown',await pg.locator('.htog button:visible').count()); await pg.screenshot(path='v47-phone.png')
        await pg.evaluate("V.ptab='gadv';render()"); await pg.wait_for_timeout(300); print('phone gantt overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth")); await pg.screenshot(path='v47-phone-g.png')
        print('errors',errs); await b.close()
asyncio.run(main())
