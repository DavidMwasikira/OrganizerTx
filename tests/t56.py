import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
asked=[]
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ''; asked.append(text)
    n=text.count('\n',text.find('open risks and issues:'),text.find('For each one')) -1 if 'open risks and issues:' in text else 0
    out=[{'n':k+1,'proposal':'Build 85 m² at about Kshs 3,400,000 in two phases','figures':[{'label':'Floor area','value':'85 m²'},{'label':'Build cost','value':'Kshs 3,400,000'}],'newBudgetTotal':3400000 if k==0 else 0,'assumptions':'Basic finishes at Kshs 40,000 per m²','resolution':f'Do the land search at Eldoret registry this week and confirm zoning ({k+1}).','owner':'Site engineer','reviewInWeeks':2,'tasks':['Official land search'] if k==0 else [],'levelAfter':'low','settled':k==1,'needs':'Your title deed number' if k==0 else ''} for k in range(n)]
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(out)}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        cx=await b.new_context(viewport={'width':1690,'height':950}); pg=await cx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""const st=['done','done','doing','blocked','todo','todo','todo','todo','todo'];const acts=[['Verify land and survey plot',1,2],['Commission architectural and structural drawings',2,4],['Prepare BQ and select builder',6,3],['Submit county building plan approval',6,6],['NEMA screening and permits',6,4],['Mobilise site and materials',12,2],['Build foundation and floor slab',14,3],['Raise walls and roof',17,6],['Final inspection',25,1]].map(([n,s,w],i)=>({id:uid(),name:n,start:s,weeks:w,status:st[i],phase:i<3?'Preparation':i<5?'Approvals':i<8?'Construction':'Handover',deps:[]}));
          S.plans.push({id:'pb',name:'Three bedroom house',what:'Construction of a three bedroom house in Eldoret',custom:true,active:true,started:Date.now()-45*DAY,weeks:26,summary:'s',log:[],phases:['Preparation','Approvals','Construction','Handover'],miles:[],risks:[{type:'risk',level:'high',title:'Plot title or zoning problems could stop approval.',action:'Do the search',status:'open'},{type:'issue',level:'med',title:'Architect has not delivered drawings.',action:'',status:'open'},{type:'risk',level:'low',title:'Prices may rise.',action:'',status:'open'},{type:'risk',level:'low',title:'Old one',action:'',status:'closed'}],acts});
          S.plans.push({id:'pf',name:'Flat project',what:'x',custom:true,active:true,started:Date.now(),weeks:6,log:[],acts:[{id:uid(),name:'One short task',start:1,weeks:1,status:'todo',deps:[]},{id:uid(),name:'Second',start:2,weeks:5,status:'todo',deps:[]}]});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};S.wsHidden=true;V.view='plan';V.plan='pb';V.ptab='risks';save();render()""")
        await pg.wait_for_timeout(400)
        print('buttons:',await pg.locator('[data-act=risk-fix]').all_inner_texts())
        await pg.evaluate("S.plans.find(p=>p.id==='pb').budget={lines:[{id:'l1',cat:'Other',item:'Build',planned:2450000}]};render()")
        await pg.click('[data-act=risk-fix][data-v=all]'); await pg.wait_for_timeout(1500)
        print('prompt asks for figures:','"figures"' in asked[-1],'| proposals',await pg.locator('.fix').count(),'| headline',await pg.locator('.fix .prop >> nth=0').inner_text(),'| fields',await pg.locator('.fix >> nth=0 >> .fxs label').all_inner_texts(),'| budget box',await pg.locator('.fix >> nth=0 >> label.row').inner_text())
        await pg.screenshot(path='v50-risks.png')
        await pg.fill('[data-fx="0|0"]','90 m²'); await pg.click('.fix >> nth=0 >> [data-act=fix-ok]'); await pg.wait_for_timeout(300)
        print('accepted:',await pg.evaluate("(()=>{const p=S.plans.find(p=>p.id==='pb');return JSON.stringify({r:p.risks[0],lines:p.budget.lines.map(l=>[l.cat,l.item,l.planned]),total:budSum(p).planned})})()"))
        print('row:',(await pg.locator('.rrow >> nth=0').inner_text()).replace('\n',' | ')[:300])
        await pg.uncheck('#fixb1') if await pg.locator('#fixb1').count() else None
        await pg.click('[data-act=fix-all]'); await pg.wait_for_timeout(300); print('accept all: total still',await pg.evaluate("budSum(S.plans.find(p=>p.id==='pb')).planned"),'| pending',await pg.locator('.fix').count())
        await pg.screenshot(path='v50-saved.png')
        # simple gantt
        await pg.click('.ptabs [data-v=gsimple]'); await pg.wait_for_timeout(300)
        print('gantt:',await pg.evaluate("""(()=>{const bars=[...document.querySelectorAll('.sg .sb')],R=bars.map(b=>b.getBoundingClientRect());let ov=0;const labs=[...document.querySelectorAll('.sg .sb em,.sg .sbo')].map(e=>e.getBoundingClientRect());for(let i=0;i<labs.length;i++)for(let j=i+1;j<labs.length;j++){const a=labs[i],b=labs[j];if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)ov++}
          return {bars:bars.map(b=>b.className.replace('sb ','')+':'+(b.querySelector('em')?b.querySelector('em').textContent:'out')),phases:[...document.querySelectorAll('.sgp b')].map(x=>x.textContent),dates:[...document.querySelectorAll('.sgd span')].map(x=>x.textContent+(x.className?'*':'')),labelOverlaps:ov,clipped:[...document.querySelectorAll('.sg .sb em')].filter(e=>e.getBoundingClientRect().right>e.parentElement.getBoundingClientRect().right-12).length}})()"""))
        await pg.screenshot(path='v49-gantt.png')
        await pg.evaluate("V.plan='pf';render()"); await pg.wait_for_timeout(300); await pg.locator('.pviews').screenshot(path='v49-flat.png')
        await pg.evaluate("V.plan='pb';document.documentElement.dataset.theme='dark';render()"); await pg.wait_for_timeout(300); await pg.locator('.pviews').screenshot(path='v49-dark.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(300); print('phone overflow gantt',await pg.evaluate("document.documentElement.scrollWidth>innerWidth")); await pg.screenshot(path='v49-phone.png')
        await pg.evaluate("V.ptab='risks';render()"); await pg.wait_for_timeout(300); print('phone overflow risks',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"),'| errors',errs); await pg.screenshot(path='v49-phone-r.png')
        await b.close()
asyncio.run(main())
