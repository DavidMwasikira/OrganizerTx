import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page()
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.click('nav [data-v=desk]'); await pg.click('#dq'); await pg.keyboard.type('sol',delay=60); await pg.wait_for_timeout(200)
        print('typed:',await pg.input_value('#dq'),'| focus on',await pg.evaluate("document.activeElement.id"),'| tabs',await pg.locator('.desk .htabs button').all_inner_texts())
        await b.close()
asyncio.run(main())
