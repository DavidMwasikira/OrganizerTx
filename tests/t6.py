import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
W=[{"name":f"Idea {i}","what":"Sells something useful to local firms.","why":"Demand is rising this month.","funds":"Kshs 50,000 (USD 390)"} for i in range(1,11)]
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); calls.append(body['messages'][0]['content'][:40])
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(W)}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','sk-test'); await pg.click('text=Start')
        print('before auto:',await pg.locator('.wk li').count(),'| suggestion cards',await pg.locator('.scard').count())
        await pg.wait_for_timeout(4500)   # first tick at 3s builds it automatically
        print('auto-built:',await pg.locator('.wk li').count(),'| heading:',await pg.locator('h2',has_text='Week').inner_text(),'| calls',calls)
        await pg.click('[data-act=sug-toggle]'); print('collapsed cards',await pg.locator('.scard').count()); await pg.click('[data-act=sug-toggle]')
        ws=await pg.evaluate("[...document.querySelectorAll('.scard')].map(e=>Math.round(e.getBoundingClientRect().width))"); print('card widths',ws)
        print('due now?',await pg.evaluate('weeklyDue()'),'| due if stamped yesterday?',await pg.evaluate('(S.weekly.date-=86400e3*1.5,weeklyDue())'))
        await pg.evaluate('S.weeklyTry=0;tick()'); await pg.wait_for_timeout(1200)
        print('refreshed, calls',len(calls),'| continuity line sent:', await pg.evaluate('S.weekly.date>Date.now()-5000'))
        await pg.click('.wk button >> nth=2'); await pg.wait_for_timeout(200); print('ask box:',await pg.input_value('#ask'))
        await pg.screenshot(path='w1.png',full_page=True)
        await pg.reload(); await pg.wait_for_timeout(1200); print('shown after reload:',await pg.locator('.wk li').count(),'| errors',errs)
        await b.close()
asyncio.run(main())
