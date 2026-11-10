import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':390,'height':800})).new_page()
        errs=[];seen=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            rq=route.request; seen.append((rq.url,rq.headers.get('x-slot'),'x-api-key' in rq.headers))
            if rq.headers.get('x-slot')!='MU96-7KQ2':
                return await route.fulfill(status=401,content_type='application/json',body=json.dumps({'error':{'message':'That access code is not active. Ask the organiser for a slot.'}}))
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':REPORT}]))
        await pg.route('https://srv.example/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        print('code field',await pg.locator('#code').count(),'key field',await pg.locator('#key').count())
        await pg.fill('#name','Test'); await pg.fill('#country','Kenya'); await pg.fill('#code','BAD'); await pg.click('text=Start')
        await pg.fill('#ask','pumps'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(800)
        print('error shown:',await pg.locator('.msg.err').inner_text())
        await pg.click('[data-act=nav][data-v=settings] >> visible=true'); await pg.fill('#code','MU96-7KQ2'); await pg.click('[data-act=save-settings]')
        await pg.click('nav [data-v=home]'); await pg.fill('#ask','pumps again'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1000)
        print('docs',await pg.evaluate('S.topics[0].docs.length'),'| requests',seen,'| errors',errs)
        await b.close()
asyncio.run(main())
