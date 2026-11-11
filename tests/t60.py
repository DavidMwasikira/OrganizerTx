import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':1100})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""S.plans.push({id:'p3',name:'Three bedroom house',what:'x',custom:true,active:true,started:Date.now(),weeks:4,log:[],acts:[{id:uid(),name:'Verify land and survey plot',status:'todo',due:dash(Date.now()),time:'13:00',hours:2,subs:[{name:'Land search',done:true},{name:'Book surveyor',done:false}],deps:[]},{id:uid(),name:'Design page X',status:'todo',due:dash(Date.now()-DAY),deps:[]},{id:uid(),name:'Commission drawings',status:'todo',due:dash(Date.now()+DAY),hours:1.5,deps:[]}]});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};save();render()""")
        await pg.wait_for_timeout(300)
        print('columns:',[x.replace('\n',' ') for x in await pg.locator('.dpcol .dph').all_inner_texts()],'| width',await pg.evaluate("(a=>[Math.round(a.width),Math.round(document.querySelector('.hbody').getBoundingClientRect().width)])(document.querySelector('.dp').getBoundingClientRect())"),'| font',await pg.evaluate("getComputedStyle(document.querySelector('.dp')).fontSize"))
        inp=pg.locator('.dpcol.now .dpadd'); await inp.fill('10:00 Site meeting with architect 1h'); await inp.press('Enter'); await pg.wait_for_timeout(300)
        await pg.locator('.dpcol.now .dpadd').fill('Call the surveyor 30m'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        await pg.locator('.dpcol >> nth=2 >> .dpadd').fill('2pm Review BQ'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(300)
        print('my tasks:',await pg.evaluate("S.plans.find(p=>p.id==='my').acts.map(a=>[a.name,a.due===dash(Date.now()),a.time||'',a.hours||0])"),'| focus kept',await pg.evaluate("document.activeElement.className"))
        print('today cards:',[x.replace('\n',' | ') for x in await pg.locator('.dpcol.now .dpc').all_inner_texts()],'| header',(await pg.locator('.dpcol.now .dph').inner_text()).replace('\n',' '))
        print('calendar blocks:',[x.replace('\n',' ') for x in await pg.locator('.dpgrid .blk').all_inner_texts()])
        await pg.locator('.dpcol.now .dpc:has-text("Call the surveyor") input[type=time]').fill('13:30'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(300); print('time set -> blocks',await pg.locator('.dpgrid .blk').count(),'| overlap lanes',await pg.evaluate("[...document.querySelectorAll('.dpgrid .blk')].map(b=>Math.round(b.getBoundingClientRect().left))"))
        await pg.locator('.dpcol.now .dpc:has-text("Site meeting") .ck').click(); await pg.wait_for_timeout(200); print('ticked:',await pg.evaluate("S.plans.find(p=>p.id==='my').acts[0].status"))
        await pg.locator('.dps button >> text=Book surveyor').click(); await pg.wait_for_timeout(200); print('subtask:',await pg.evaluate("S.plans.find(p=>p.id==='p3').acts[0].subs.map(x=>x.done)"))
        # drag overdue card to day 3
        a=await pg.locator('.dpc:has-text("Design page X")').bounding_box(); c=await pg.locator('.dpcol >> nth=3').bounding_box()
        await pg.evaluate("""()=>{const src=[...document.querySelectorAll('.dpc')].find(x=>x.textContent.includes('Design page X')),dst=document.querySelectorAll('.dpcol')[3],dt=new DataTransfer();src.dispatchEvent(new DragEvent('dragstart',{bubbles:true,dataTransfer:dt}));dst.dispatchEvent(new DragEvent('dragover',{bubbles:true,cancelable:true,dataTransfer:dt}));dst.dispatchEvent(new DragEvent('drop',{bubbles:true,cancelable:true,dataTransfer:dt}))}"""); await pg.wait_for_timeout(300)
        print('dragged -> due in days:',await pg.evaluate("(new Date(S.plans.find(p=>p.id==='p3').acts[1].due)-new Date(dash(Date.now())))/864e5"))
        await pg.screenshot(path='v55.png',full_page=True)
        await pg.click('[data-act=dp-go][data-v="5"]'); await pg.wait_for_timeout(200); print('next:',(await pg.locator('.dpcol .dph >> nth=0').inner_text()).replace('\n',' ')); await pg.click('[data-act=dp-go][data-v="0"]')
        await pg.locator('.dpc .nm').first.click(); await pg.wait_for_timeout(200); print('opens task dialog:',await pg.locator('.modal').count()); await pg.keyboard.press('Escape')
        await pg.reload(); await pg.wait_for_timeout(1500); print('after reload my tasks',await pg.evaluate("S.plans.find(p=>p.id==='my').acts.length"))
        await pg.evaluate("document.documentElement.dataset.theme='dark'"); await pg.wait_for_timeout(200); await pg.locator('.dp').screenshot(path='v55-dark.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(300); print('phone overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"),'| errors',errs); await pg.locator('.dp').screenshot(path='v55-phone.png')
        await b.close()
asyncio.run(main())
