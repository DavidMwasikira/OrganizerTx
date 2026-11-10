import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        for name,w in [('desktop',1670),('tablet',820),('phone',390)]:
            await pg.set_viewport_size({'width':w,'height':900}); await pg.click('nav [data-v=home]'); await pg.wait_for_timeout(200)
            sec=await pg.locator('section[aria-label="Field capture"]').bounding_box(); btn=await pg.locator('main .capbtn.cam').bounding_box()
            dirn=await pg.evaluate("getComputedStyle(document.querySelector('main .capbtn')).flexDirection")
            await pg.locator('section[aria-label="Field capture"]').screenshot(path=f'fc-{name}.png')
            await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(200); dsec=await pg.locator('.desk .dcard >> nth=0').bounding_box(); ddir=await pg.evaluate("getComputedStyle(document.querySelector('.desk .dcap')).flexDirection")
            print(f'{name:8s} Home: {dirn:6s} panel {round(sec["height"])} px, button {round(btn["height"])} px | Desktop: {ddir:6s} panel {round(dsec["height"])} px | overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await pg.click('.desk [data-act=cap][data-v=note]'); await pg.fill('#captext','ok'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(300); print('buttons still work:',await pg.evaluate('logCount()'),'| errors',errs)
        await b.close()
asyncio.run(main())
