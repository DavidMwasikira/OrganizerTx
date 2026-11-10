import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
SETUP=open('t21.py').read().split('await pg.evaluate("""')[1].split('""")')[0]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate(SETUP)
        await pg.click('nav [data-v=tasks]'); await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(400)
        d=await pg.locator('.desk').bounding_box(); n=await pg.locator('nav').bounding_box()
        print('fills the area: left edge at sidebar',round(d['x'])==round(n['x']+n['width']),'| top',round(d['y']),'| right edge',round(d['x']+d['width']),'of 1700 | height',round(d['height']),'>= 900',d['height']>=899)
        print('theme light: desk text colour',await pg.evaluate("getComputedStyle(document.querySelector('.desk')).color"),'| tile bg',await pg.evaluate("getComputedStyle(document.querySelector('.fold2')).backgroundColor"),'| Back button',await pg.locator('.desk [data-act=back]').count())
        await pg.screenshot(path='dk3.png')
        await pg.click('nav [data-act=theme]'); await pg.wait_for_timeout(200)
        print('theme dark: desk text colour',await pg.evaluate("getComputedStyle(document.querySelector('.desk')).color"),'| tile bg',await pg.evaluate("getComputedStyle(document.querySelector('.fold2')).backgroundColor"))
        await pg.screenshot(path='dk4.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(300)
        cols=await pg.evaluate("getComputedStyle(document.querySelector('.dgridf.main')).gridTemplateColumns.split(' ').length")
        print('phone: main folders in',cols,'columns | overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| desk width',round((await pg.locator('.desk').bounding_box())['width']),'| errors',errs)
        await pg.screenshot(path='dk5.png'); await pg.click('.topstrip [data-act=theme]'); await pg.wait_for_timeout(200); await pg.screenshot(path='dk6.png')
        await pg.click('.desk [data-act=back]'); print('Back ->',await pg.evaluate('V.view'))
        await b.close()
asyncio.run(main())
