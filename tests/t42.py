import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.skin='ultraviolet';applyTheme();S.plans.push({id:'pb',name:'Building new site office',what:'x',custom:true,started:Date.now(),acts:[],log:[],budget:{lines:[{cat:'Other',item:'Overall budget',planned:16500000,actual:14950000}]}});S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};V.view='plan';V.plan='pb';V.ptab='budget';save();render()")
        for w in [1700,1100,390]:
            await pg.set_viewport_size({'width':w,'height':900}); await pg.wait_for_timeout(250)
            r=await pg.evaluate("[...document.querySelectorAll('.btile')].map(t=>{const b=t.querySelector('b'),r=t.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height),Math.round(b.getBoundingClientRect().height),b.scrollWidth<=t.clientWidth]})")
            print(w,'tiles [w,h,value height,fits]:',r); await pg.locator('.btiles').screenshot(path=f'tiles-{w}.png')
        print('errors',errs); await b.close()
asyncio.run(main())
