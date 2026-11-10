import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
W=[{"name":f"Idea {i}","what":"x","why":"y","funds":"z"} for i in range(1,11)]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        # A: hosted, service fails first, then works
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); n=[0]
        async def api(route):
            n[0]+=1
            if n[0]==1: return await route.fulfill(status=400,content_type='application/json',body=json.dumps({'error':{'message':'Web search is not enabled for this organization.'}}))
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(W)}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','D'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(4500)
        print('A after failed auto-load:',await pg.locator('.wk li').count(),'|',await pg.locator('section .banner').inner_text())
        await pg.click('text=Load this week'); await pg.wait_for_timeout(1200)
        print('A after pressing button:',await pg.locator('.wk li').count(),'| error banner left',await pg.locator('section .banner').count())
        # B: preview inside Claude (simulated bridge), nothing clicked
        pg2=await (await b.new_context(viewport={'width':1280,'height':900})).new_page()
        await pg2.add_init_script("window.claude={use:async n=>n==='sample'?(async()=>({text:%s})):null}" % json.dumps(json.dumps(W)))
        await pg2.goto('http://localhost:8765/index.html'); await pg2.wait_for_timeout(1500)
        await pg2.fill('#name','D'); await pg2.fill('#country','Kenya'); await pg2.click('text=Start'); await pg2.wait_for_timeout(4500)
        print('B preview, no clicks:',await pg2.locator('.wk li').count())
        await b.close()
asyncio.run(main())
