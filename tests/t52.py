import asyncio, json, datetime
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ''
    if 'direct predecessors' in text: body=json.dumps([{'n':1,'after':[]},{'n':2,'after':[1]},{'n':3,'after':[1]},{'n':4,'after':[2,3]},{'n':5,'after':[]},{'n':6,'after':[4]}])
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':1000})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""S.skin='ultraviolet';applyTheme();const acts=[['Define needs',1,2],['Register business',1,2],['Secure land',2,3],['Appoint architect',4,5],['NEMA approval',8,4],['Build',12,6]].map(([n,s,w])=>({id:uid(),name:n,start:s,weeks:w,status:'todo',deps:[],due:dash(Date.now()+30*DAY)}));
          S.plans.push({id:'pb',name:'Building new site office',what:'x',custom:true,active:true,started:Date.now()-10*DAY,weeks:17,summary:'s',log:[],miles:[{name:'Permit',date:dash(Date.now()+50*DAY),done:false}],acts});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};V.view='plan';V.plan='pb';V.ptab='gadv';save();render()""")
        await pg.wait_for_timeout(300)
        # 1 hide list
        w0=await pg.evaluate("Math.round(document.querySelector('.wscol').getBoundingClientRect().width)"); await pg.click('.ttog [data-act=ws-hide]'); await pg.wait_for_timeout(200)
        print('hide list: project width',w0,'->',await pg.evaluate("Math.round(document.querySelector('.wscol').getBoundingClientRect().width)"),'| list visible',await pg.locator('.wsside').is_visible(),'| show button',await pg.locator('.ttog [data-act=ws-hide]').count())
        await pg.screenshot(path='lk-wide.png'); await pg.reload(); await pg.wait_for_timeout(1500); await pg.evaluate("V.view='plan';V.plan='pb';V.ptab='gadv';render()"); await pg.wait_for_timeout(200); print('stays hidden after reload:',await pg.locator('.wsside').is_visible()==False)
        # 2 today line
        print('today label:',await pg.locator('.agnow b').inner_text(),'| x px',await pg.evaluate("Math.round(parseFloat(document.querySelector('.agnow').style.left))"),'(10 days = 43 px expected)')
        # 3 project dates
        st=await pg.input_value('#pstart'); en=await pg.input_value('#pend'); due0=await pg.evaluate("S.plans.find(p=>p.id==='pb').acts[0].due"); ms0=await pg.evaluate("S.plans.find(p=>p.id==='pb').miles[0].date"); bar0=await pg.input_value('[data-g="2|start"]')
        new=(datetime.date.fromisoformat(st)+datetime.timedelta(days=14)).isoformat(); await pg.fill('#pstart',new); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(300)
        print('start',st,'->',await pg.input_value('#pstart'),'| end',en,'->',await pg.input_value('#pend'),'| task due',due0,'->',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts[0].due"),'| milestone',ms0,'->',await pg.evaluate("S.plans.find(p=>p.id==='pb').miles[0].date"),'| task 3 start',bar0,'->',await pg.input_value('[data-g="2|start"]'))
        print('today now before start:',await pg.locator('.agout').inner_text() if await pg.locator('.agout').count() else await pg.locator('.agnow b').inner_text())
        en2=await pg.input_value('#pend'); back=(datetime.date.fromisoformat(en2)-datetime.timedelta(days=14)).isoformat(); await pg.fill('#pend',back); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(300); print('set end back 14 days -> start',await pg.input_value('#pstart'),'(=',st,')')
        # 4 link by drag
        await pg.evaluate("document.querySelector('.ag').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
        a=await pg.locator('.agline .lk >> nth=0').bounding_box(); bb=await pg.locator('.agline .bar >> nth=2').bounding_box()
        await pg.hover('.agline >> nth=1'); await pg.mouse.move(a['x']+5,a['y']+5); await pg.mouse.down(); await pg.mouse.move(bb['x']+20,bb['y']+8,steps=8); await pg.mouse.up(); await pg.wait_for_timeout(300)
        print('drag link 1->3: deps of task 3',await pg.evaluate("(()=>{const m=taskIndex();return predsOf(S.plans.find(p=>p.id==='pb').acts[2],m).map(x=>x.n)})()"),'| lines',await pg.locator('.aglinks path[marker-end]').count())
        # click-click link 3 -> 4
        await pg.evaluate("document.querySelector('.ag').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
        h=await pg.locator('.agline .lk >> nth=2').bounding_box(); await pg.mouse.move(h['x']+5,h['y']+5); await pg.mouse.down(); await pg.mouse.up(); await pg.wait_for_timeout(250); print('click dot -> banner:',(await pg.locator('.banner.linking').inner_text())[:60])
        await pg.locator('.agline .bar >> nth=3').click(); await pg.wait_for_timeout(300); print('then click bar 4: deps of 4',await pg.evaluate("(()=>{const m=taskIndex();return predsOf(S.plans.find(p=>p.id==='pb').acts[3],m).map(x=>x.n)})()"),'| dialog opened',await pg.locator('.modal').count())
        # loop refused: 4 -> 1
        await pg.evaluate("document.querySelector('.ag').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(200)
        h=await pg.locator('.agline .lk >> nth=3').bounding_box(); b1=await pg.locator('.agline .bar >> nth=0').bounding_box(); await pg.mouse.move(h['x']+5,h['y']+5); await pg.mouse.down(); await pg.mouse.move(b1['x']+10,b1['y']+8,steps=8); await pg.mouse.up(); await pg.wait_for_timeout(300); print('loop 4->1 refused: deps of 1',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts[0].deps.length"))
        cols=await pg.evaluate("[...document.querySelectorAll('.aglinks path[marker-end]')].map(p=>[p.getAttribute('class')||'normal',getComputedStyle(p).stroke,getComputedStyle(p).strokeWidth])"); print('line styles:',cols)
        await pg.locator('.pviews').screenshot(path='lk-adv.png')
        # remove link by clicking line
        await pg.evaluate("document.querySelector('[data-unlink]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); await pg.wait_for_timeout(200); await pg.click('.modal .btn.primary, .modal [data-x=ok], .modal [data-x=yes]'); await pg.wait_for_timeout(300); print('after removing one link: lines',await pg.locator('.aglinks path[marker-end]').count())
        # 5 AI optimise
        await pg.click('[data-act=dep-opt]'); await pg.wait_for_timeout(200)
        if await pg.locator('.modal').count(): await pg.click('.modal .btn.primary')
        await pg.wait_for_timeout(1500)
        print('AI: deps',await pg.evaluate("(()=>{const m=taskIndex();return S.plans.find(p=>p.id==='pb').acts.map(a=>predsOf(a,m).map(x=>x.n))})()"),'| every task connected',await pg.evaluate("(()=>{const m=taskIndex();return S.plans.find(p=>p.id==='pb').acts.every(a=>predsOf(a,m).length||succsOf(a,m).length)})()"),'| starts',await pg.evaluate("schedOf(S.plans.find(p=>p.id==='pb')).rows.map(r=>r.start)"),'| lines',await pg.locator('.aglinks path[marker-end]').count())
        await pg.locator('.pviews').screenshot(path='lk-ai.png')
        await pg.click('.ttog [data-act=ws-hide]'); await pg.wait_for_timeout(200); print('show list again:',await pg.locator('.wsside').is_visible(),'| errors',errs)
        await b.close()
asyncio.run(main())
