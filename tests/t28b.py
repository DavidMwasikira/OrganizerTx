import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':390,'height':800})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("V.view='settings';render()"); await pg.click('.skin[data-v="forest"]'); await pg.wait_for_timeout(200)
        print('phone skin',await pg.evaluate("document.documentElement.dataset.skin"),'overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs)
        await pg.locator('.skins').scroll_into_view_if_needed(); await pg.screenshot(path='sk-phone.png'); await b.close()
asyncio.run(main())
