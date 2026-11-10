import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
names=["Solar cold rooms for market traders","Poultry feed mixing","Motorbike spares delivery","Bookkeeping service for small shops","Borehole maintenance contracts","School uniform tailoring","Drip irrigation kits installation","Phone repair and accessories","Avocado aggregation for export","Short-course tutoring online"]
W=[{"name":n,"what":"Sample entry: what it sells and who buys.","why":"Sample entry: why this week.","funds":"Kshs 000,000 (USD 0,000)"} for n in names]
MESSY="I searched for current conditions [see sources]. Here is the list:\n```json\n"+json.dumps(W)[:-1]+",\n]\n```\nNote: figures are estimates."
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':MESSY}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(4500)
        print('messy answer read:',await pg.locator('.wk li').count(),'ideas | error banner',await pg.locator('section .banner').count(),'| errors',errs)
        await pg.locator('section',has_text='best business ideas').screenshot(path='weekly.png')
        await b.close()
asyncio.run(main())
