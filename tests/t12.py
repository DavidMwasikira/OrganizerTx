import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); u=body['messages'][0]['content']; calls.append(body)
            t=REPORT if 'Research this' in u else 'Press **Create**, then Task.' if 'help assistant' in body['system'] else '[]'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        await pg.fill('#ask','borehole pump'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act=open-doc] >> nth=0'); await pg.wait_for_timeout(400)
        print('doc open: sidebar visible',await pg.locator('nav').is_visible(),'| back beside doc',await pg.locator('.docpage [data-act=close-doc]').count())
        await pg.click('[data-act=share-doc]'); await pg.wait_for_timeout(200)
        links=await pg.evaluate("[...document.querySelectorAll('.sharegrid a')].map(a=>[a.textContent,a.href.slice(0,46)])"); [print('   ',l) for l in links]
        print('   whatsapp text:',await pg.evaluate("decodeURIComponent(document.querySelector('.sharegrid a').href.split('text=')[1]).replace(/\\n/g,' / ')"))
        await pg.screenshot(path='v1.png'); await pg.click('[data-x=cancel]')
        await pg.click('nav [data-act=theme]'); await pg.wait_for_timeout(200)
        print('theme now',await pg.evaluate('document.documentElement.dataset.theme'),'| bg',await pg.evaluate("getComputedStyle(document.body).backgroundColor"))
        await pg.screenshot(path='v2.png')
        await pg.click('[data-act=rail-hide]'); await pg.wait_for_timeout(200); print('rail hidden: nav visible',await pg.locator('nav').is_visible(),'| show button',await pg.locator('.railshow').is_visible())
        await pg.click('.railshow'); await pg.wait_for_timeout(200); print('rail shown again',await pg.locator('nav').is_visible())
        await pg.click('[data-act=close-doc]'); print('back -> folder view',await pg.locator('.thread').count())
        await pg.click('nav [data-v=help]'); await pg.wait_for_timeout(200); n0=await pg.locator('.hq').count()
        await pg.fill('#helpq','backup'); await pg.wait_for_timeout(100); print('help guides',n0,'| search "backup" ->',await pg.locator('.hq').count(),await pg.locator('.hq summary').first.inner_text())
        await pg.fill('#helpask','How do I add a task?'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(900)
        print('assistant:',await pg.locator('.msg.ai').last.inner_text(),'| model',calls[-1]['model'],'| guide in system',('Back up or move my data' in calls[-1]['system']))
        await pg.screenshot(path='v3.png')
        await pg.wait_for_timeout(400); await pg.reload(); await pg.wait_for_timeout(1200); print('after reload theme',await pg.evaluate('document.documentElement.dataset.theme'))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(200)
        print('phone: top strip',await pg.locator('.topstrip').is_visible(),'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await pg.screenshot(path='v4.png')
        await b.close()
asyncio.run(main())
