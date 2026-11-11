import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ''
    if 'work breakdown structure' in text: body=json.dumps({'phases':['Preparation','Approvals','Construction','Handover'],'tasks':[{'n':1,'phase':'Preparation'},{'n':2,'phase':'Preparation'},{'n':3,'phase':'Preparation'},{'n':4,'phase':'Preparation'},{'n':5,'phase':'Approvals'},{'n':6,'phase':'Approvals'},{'n':7,'phase':'Construction'},{'n':8,'phase':'Approvals'},{'n':9,'phase':'Construction'},{'n':10,'phase':'Construction'},{'n':11,'phase':'Handover'},{'n':12,'phase':'Handover'}]})
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
ACTS=[('Define needs, size and budget',1,2),('Register business and tax IDs',1,2),('Secure land and do due diligence',2,3),('Appoint architect and engineers',4,5),('NEMA environmental approval',8,8),('County plan approval and permit',9,8),('Tender and appoint contractor',12,5),('NCA project registration and levy',17,1),('Construction and site supervision',18,6),('Power, water and internet connections',19,5),('Fire check and occupation certificate',24,2),('Business permit, insurance, fit-out',24,3)]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':1000})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""(A)=>{S.skin='ultraviolet';applyTheme();const acts=A.map(([n,s,w])=>({id:uid(),name:n,start:s,weeks:w,status:'todo',cost:'Kshs 50,000'}));acts.forEach((a,i)=>{a.deps=i?[acts[i-1].id]:[]});acts[5].deps=[acts[3].id];acts[9].deps=[acts[7].id];acts[0].status='done';acts[1].status='doing';
          S.plans.push({id:'pb',name:'Building new site office',what:'Setting up a new business premise',custom:true,active:true,started:Date.now()-14*DAY,weeks:26,summary:'Register the business, secure the land, get the drawings, then clear the approvals.',log:[],miles:[{name:'Permit issued',date:dash(Date.now()+100*DAY),done:false}],acts});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};V.view='plan';V.plan='pb';save();render()}""",ACTS)
        await pg.wait_for_timeout(300); print('tabs:',await pg.locator('.ptabs button').all_inner_texts(),'| default',await pg.locator('.ptabs [aria-pressed=true]').inner_text(),'| simple rows',await pg.locator('.sg .sgn').count())
        await pg.click('.ptabs [data-v=brief]'); await pg.wait_for_timeout(150); print('brief shown:',(await pg.locator('.pviews p').first.inner_text())[:40]); await pg.click('[data-act=brief-fold]'); await pg.wait_for_timeout(100); print('folded:',await pg.locator('.pviews p').count()==0); await pg.click('[data-act=brief-fold]')
        await pg.click('.ptabs [data-v=gadv]'); await pg.wait_for_timeout(300)
        r=await pg.evaluate("""(()=>{const L=[...document.querySelectorAll('.agl .agrow')].map(e=>Math.round(e.getBoundingClientRect().top)),R=[Math.round(document.querySelector('.aghd').getBoundingClientRect().top),...[...document.querySelectorAll('.agline')].map(e=>Math.round(e.getBoundingClientRect().top))];
          const bars=[...document.querySelectorAll('.agline .bar')].map(e=>e.getBoundingClientRect());let ov=0;for(let i=0;i<bars.length;i++)for(let j=i+1;j<bars.length;j++){const a=bars[i],b=bars[j];if(a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom)ov++}
          return {rows:L.length,aligned:JSON.stringify(L)===JSON.stringify(R),bars:bars.length,barOverlaps:ov,links:document.querySelectorAll('.aglinks path:not(marker path)').length-2,crit:document.querySelectorAll('.agline .bar.crit').length,dia:document.querySelectorAll('.agline .dia').length}})()"""); print('ADVANCED:',r)
        await pg.locator('.pviews').screenshot(path='pv-adv.png')
        await pg.click('[data-act=gcols]'); await pg.wait_for_timeout(200); print('hide columns: WBS col visible',await pg.locator('.agl .agrow.hd .x').first.is_visible(),'| chart width',await pg.evaluate("Math.round(document.querySelector('.agr').getBoundingClientRect().width)")); await pg.locator('.pviews').screenshot(path='pv-adv2.png'); await pg.click('[data-act=gcols]')
        # edit in table: name, weeks, start, hours
        await pg.fill('[data-g="2|name"]','Secure the land'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(200); await pg.fill('[data-g="2|weeks"]','6'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200); await pg.fill('[data-g="2|hours"]','40'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        print('edited ->',await pg.evaluate("(()=>{const a=S.plans.find(p=>p.id==='pb').acts[2];return [a.name,a.weeks,a.hours]})()"),'| bar width',await pg.evaluate("Math.round(document.querySelectorAll('.agline .bar')[2].getBoundingClientRect().width)"))
        await pg.click('.ptabs [data-v=gsimple]'); await pg.wait_for_timeout(150); print('simple shows new name:',await pg.locator('.sg .sgn >> nth=2').inner_text())
        await pg.click('.ptabs [data-v=wbs]'); await pg.wait_for_timeout(200); print('WBS before phases: columns',await pg.locator('.wcol').count(),'tasks',await pg.locator('.wt').count())
        await pg.click('[data-act=ph-ai]'); await pg.wait_for_timeout(1500); print('AI phases:',await pg.evaluate("S.plans.find(p=>p.id==='pb').phases"),'| codes',await pg.locator('.wt .code').all_inner_texts())
        r=await pg.evaluate("""(()=>{const bx=[...document.querySelectorAll('.wroot,.wph,.wt')].map(e=>e.getBoundingClientRect());let ov=0;for(let i=0;i<bx.length;i++)for(let j=i+1;j<bx.length;j++){const a=bx[i],b=bx[j];if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)ov++}return {boxes:bx.length,overlaps:ov,clipped:[...document.querySelectorAll('.wt .ed,.wph .ed')].filter(e=>e.scrollWidth>e.clientWidth+1).length}})()"""); print('WBS boxes:',r); await pg.locator('.pviews').screenshot(path='pv-wbs.png')
        await pg.click('.wph .ed >> nth=1'); await pg.keyboard.press('Control+A'); await pg.keyboard.type('Permits'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300); print('rename phase ->',await pg.evaluate("[S.plans.find(p=>p.id==='pb').phases[1],S.plans.find(p=>p.id==='pb').acts.filter(a=>a.phase==='Permits').length]"))
        await pg.click('.wt .ed >> nth=0'); await pg.keyboard.press('Control+A'); await pg.keyboard.type('Define the needs'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        # drag task 4.1 into phase 3 (Construction)
        src=await pg.locator('.wcol[data-ph="3"] .wt >> nth=0').bounding_box(); tgt=await pg.locator('.wcol[data-ph="2"] .wt >> nth=0').bounding_box(); nm=await pg.locator('.wcol[data-ph="3"] .wt .ed >> nth=0').inner_text()
        await pg.mouse.move(src['x']+12,src['y']+15); await pg.mouse.down(); await pg.mouse.move(tgt['x']+60,tgt['y']+12,steps=10); await pg.mouse.up(); await pg.wait_for_timeout(400)
        print('dragged "'+nm+'" ->',await pg.evaluate("(()=>{const P=S.plans.find(p=>p.id==='pb'),a=P.acts.find(x=>x.name==='"+nm+"');return [a.phase,P.acts.indexOf(a)+1]})()"),'| first in Construction now:',await pg.locator('.wcol[data-ph="2"] .wt .ed >> nth=0').inner_text())
        await pg.click('[data-act=ph-add]'); await pg.wait_for_timeout(200); await pg.click('.wcol >> nth=-1 >> [data-act=ph-task]'); await pg.wait_for_timeout(200); print('add phase + task: phases',await pg.evaluate("S.plans.find(p=>p.id==='pb').phases.length"),'tasks',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts.length"))
        await pg.click('.ptabs [data-v=gadv]'); await pg.wait_for_timeout(300); print('advanced now has phase rows:',await pg.locator('.agrow.ph').count(),'| first task name:',await pg.input_value('[data-g="0|name"]')); await pg.locator('.pviews').screenshot(path='pv-adv3.png')
        await pg.evaluate("V.view='tasks';V.tfilter='pb';render()"); await pg.wait_for_timeout(200); print('board shows renamed task:',(await pg.locator('.kcard .t').first.inner_text()))
        await pg.reload(); await pg.wait_for_timeout(1500); print('after reload phases',await pg.evaluate("S.plans.find(p=>p.id==='pb').phases"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("V.view='plan';V.plan='pb';V.ptab='gadv';render()"); await pg.wait_for_timeout(200); o1=await pg.evaluate('document.documentElement.scrollWidth>innerWidth'); await pg.evaluate("V.ptab='wbs';render()"); await pg.wait_for_timeout(200); print('phone overflow-x adv,wbs:',o1,await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await b.close()
asyncio.run(main())
