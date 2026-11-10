import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
LIST=[{"name":f"Business {i}","what":"Sells AI help to small firms.","why":"Strong local demand.","a":"Kshs 150,000 to 400,000 (USD 1,150 to 3,100)","b":"Kshs 80,000 to 200,000 (USD 620 to 1,550)","payback":"8 to 14 months","risk":"Medium"} for i in range(1,11)]
PLAN={"summary":"Start small. Done means three paying clients.","activities":[{"name":f"Activity {i}","detail":"Do the thing and produce the output.","start":1+2*(i-1),"weeks":3,"cost":"Kshs 5,000 (USD 39)"} for i in range(1,9)]}
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':390,'height':800})).new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); calls.append(body); u=body['messages'][0]['content']
            if 'Rank the 10' in u or 'best AI stack' in u: t='Here you go:\n'+json.dumps(LIST)
            elif 'activity plan' in u: t='```json\n'+json.dumps(PLAN)+'\n```'
            elif 'Research this' in u: t=REPORT
            else: t='## Profile\nx'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','sk-test'); await pg.click('text=Start'); await pg.wait_for_timeout(300)
        await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(200); await pg.screenshot(path='d0.png',full_page=True)
        await pg.click('nav [data-v=topics]'); await pg.click('[data-act=open-guide][data-v=biz]'); await pg.wait_for_timeout(1200)
        print('guide items',await pg.locator('[data-act=open-item]').count(),'| ask mentions Kenya+Kshs:', 'Kenya' in calls[0]['messages'][0]['content'] and 'Kshs' in calls[0]['messages'][0]['content'])
        await pg.screenshot(path='d1.png',full_page=True)
        await pg.click('[data-act=open-item][data-v="2"]'); await pg.wait_for_timeout(1200)
        print('acts',await pg.locator('.act').count(),'| gantt bars',await pg.locator('.gantt .tr i').count(),'| weeks',await pg.evaluate('S.plans[0].weeks'))
        await pg.click('[data-act=plan-add]'); await pg.click('.act .box >> nth=0'); await pg.click('.act .box >> nth=1'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='d2.png',full_page=True)
        print('pct text',await pg.locator('.pct').first.inner_text())
        await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='d3.png',full_page=True)
        print('dashboard:',(await pg.locator('main').inner_text()).replace('\n',' | ')[:420])
        await pg.click('nav [data-v=topics]'); await pg.click('[data-act=open-guide][data-v=stack]'); await pg.wait_for_timeout(1000)
        print('stack items',await pg.locator('[data-act=open-item]').count(),'| reload keeps plans:',end=' ')
        await pg.wait_for_timeout(500); await pg.reload(); await pg.wait_for_timeout(1500)
        print(await pg.evaluate('[S.plans.length,S.plans[0].active,Object.keys(S.guides)]'),'| errors',errs)
        await b.close()
asyncio.run(main())
