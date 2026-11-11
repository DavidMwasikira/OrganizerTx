import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def handle(r): await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        cx=await b.new_context(viewport={'width':1690,'height':950}); pg=await cx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""const st=['done','done','doing','blocked','todo','todo','todo','todo'];const acts=[['Verify land and survey plot',1,2],['Commission architectural and structural drawings',2,4],['Prepare BQ and select builder',6,3],['Submit county building plan',6,6],['NEMA approval',8,4],['Foundation',12,4],['Walling and roof',16,6],['Finishes and handover',22,5]].map(([n,s,w],i)=>({id:uid(),name:n,start:s,weeks:w,status:st[i],phase:i<3?'Preparation':i<5?'Approvals':'Construction',deps:[]}));acts.forEach((a,i)=>{if(i)a.deps=[acts[i-1].id]});acts[4].deps=[acts[2].id];
          S.plans.push({id:'pb',name:'Three bedroom house',what:'Construction of a three bedroom house in Eldoret with a kitchen, bathroom, study room, store, car park, back yard garden',custom:true,active:true,started:Date.now()-20*DAY,weeks:26,summary:'s',log:[],phases:['Preparation','Approvals','Construction'],miles:[{id:'m1',name:'Permit',date:dash(Date.now()+50*DAY),done:false}],acts});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};S.wsHidden=true;V.view='plan';V.plan='pb';V.ptab='gadv';save();render()""")
        await pg.wait_for_timeout(400)
        print('dashboard link:',await pg.locator('main >> text=Dashboard').count(),'| header toggles visible',await pg.locator('.htog button:visible').count(),'| old Folders button',await pg.locator('.wstog.show').count(),'| title toggles',await pg.locator('.ttog button').all_inner_texts(),'| title y',await pg.evaluate("Math.round(document.querySelector('.ptitle h1').getBoundingClientRect().top)"),'| tabs y',await pg.evaluate("Math.round(document.querySelector('.ptabs').getBoundingClientRect().top)"),'| chart y',await pg.evaluate("Math.round(document.querySelector('.ag').getBoundingClientRect().top)"))
        print('slider:',await pg.locator('#gzoom').count(),'| toggle',await pg.locator('.agdates .seg button').all_inner_texts())
        print('bars:',await pg.evaluate("[...document.querySelectorAll('.agline .bar')].map(b=>[b.className.replace('bar ','').trim(),getComputedStyle(b).backgroundColor,getComputedStyle(b).borderRadius])"))
        await pg.screenshot(path='v48-w.png')
        for k in ['m','q','fit','w']:
            await pg.click(f'[data-act=gscale][data-v={k}]'); await pg.wait_for_timeout(400)
            print(k,'| head',(await pg.locator('.aghd').inner_text()).replace('\n',' ')[:120],'| chart w',await pg.evaluate("Math.round(document.querySelector('.agtl').getBoundingClientRect().width)"),'of',await pg.evaluate("document.querySelector('.agr').clientWidth"),'| scrolls',await pg.evaluate("(r=>r.scrollWidth>r.clientWidth+1)(document.querySelector('.agr'))"))
            await pg.screenshot(path=f'v48-{k}.png')
        await pg.click('[data-act=gscale][data-v=fit]'); await pg.wait_for_timeout(300); await pg.click('[data-act=gcols]'); await pg.wait_for_timeout(400); print('fit after hiding columns: scrolls',await pg.evaluate("(r=>r.scrollWidth>r.clientWidth+1)(document.querySelector('.agr'))")); await pg.click('[data-act=gcols]')
        await pg.click('.ttog [data-act=ws-hide]'); await pg.wait_for_timeout(300); print('folders shown',await pg.locator('.wsside').is_visible(),'| fit still no scroll',not await pg.evaluate("(r=>r.scrollWidth>r.clientWidth+1)(document.querySelector('.agr'))")); await pg.screenshot(path='v48-list.png')
        await pg.click('.ttog [data-act=rail-hide]'); await pg.wait_for_timeout(300); print('rail hidden',not await pg.locator('nav').is_visible(),'| restore',await pg.locator('.ttog [data-act=rail-show]').inner_text()); await pg.click('.ttog [data-act=rail-show]')
        await pg.click('.aghelp summary'); await pg.wait_for_timeout(200); print('help:',(await pg.locator('.aghelp p').inner_text())[:80])
        await pg.click('.ptabs [data-v=gsimple]'); await pg.wait_for_timeout(300); print('simple bars:',await pg.evaluate("[...document.querySelectorAll('.gantt .tr i')].map(b=>b.className)"),'| legend',await pg.locator('.gleg').inner_text()); await pg.locator('.pviews').screenshot(path='v48-simple.png')
        await pg.evaluate("document.documentElement.dataset.theme='dark'"); await pg.click('.ptabs [data-v=gadv]'); await pg.wait_for_timeout(400); await pg.screenshot(path='v48-dark.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(300); print('phone overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"),'| errors',errs); await pg.screenshot(path='v48-phone.png')
        await b.close()
asyncio.run(main())
