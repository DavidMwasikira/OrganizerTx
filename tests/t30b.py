import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        for w in [390,820,1670]:
            pg=await (await b.new_context(viewport={'width':w,'height':850})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1200)
            await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(300)
            r=await pg.evaluate("(()=>{const c=document.querySelector('.card.ask').getBoundingClientRect(),b=document.querySelector('[data-act=research]').getBoundingClientRect();return [Math.round(c.right),Math.round(b.right),innerWidth,document.documentElement.scrollWidth>innerWidth]})()")
            print(w,'card right, Research right, viewport, overflow:',r,'errors',errs)
            if w==390:
                await pg.evaluate("document.querySelector('main').scrollTop=430"); await pg.screenshot(path='lean-phone2.png')
            if w==1670:
                await pg.evaluate("S.theme='dark';S.skin='ultraviolet';S.capPin=true;applyTheme();render()"); await pg.wait_for_timeout(400); await pg.screenshot(path='lean-uv.png')
        await b.close()
asyncio.run(main())
