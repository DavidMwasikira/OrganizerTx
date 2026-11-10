import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        for v in ['settings','tasks']:
            await pg.click(f'nav [data-v={v}]'); await pg.wait_for_timeout(200); print(v,'Back button',await pg.locator('main [data-act=back]').count())
        await pg.click('nav [data-v=settings]'); await pg.click('.sett .htabs [data-v=research]'); await pg.wait_for_timeout(200); await pg.screenshot(path='set-research.png')
        await pg.click('main [data-act=back]'); await pg.wait_for_timeout(200); print('back went to',await pg.evaluate('V.view'),'errors',errs)
        await b.close()
asyncio.run(main())
