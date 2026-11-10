import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.plans.push({id:'pb',name:'Site office',what:'x',custom:true,started:Date.now(),acts:[],log:[],budget:{lines:[{cat:'Other',item:'Overall budget',planned:16500000,actual:0},{cat:'Materials',item:'Cement',planned:500000,actual:0}]}});V.view='plan';V.plan='pb';V.ptab='budget';save();render()")
        await pg.click('[data-bud="0|actual"]'); await pg.keyboard.type('14950000'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        print('after Enter: spent tile',(await pg.locator('.btile >> nth=1').inner_text()).replace('\n',' '),'| focus kept',await pg.evaluate("document.activeElement.dataset.bud"))
        await pg.keyboard.press('Shift+Tab'); await pg.keyboard.type('17000000'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(200)
        print('after Tab: budget tile',(await pg.locator('.btile >> nth=0').inner_text()).replace('\n',' '),'| focus moved to',await pg.evaluate("document.activeElement.dataset.bud"),'| errors',errs)
        await b.close()
asyncio.run(main())
