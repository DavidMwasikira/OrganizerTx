import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
PLAN={"summary":"Start small.","activities":[{"name":f"Step {i}","detail":"Do it.","start":i,"weeks":2,"cost":""} for i in range(1,7)]}
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':850})).new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); calls.append(body); u=body['messages'][0]['content']
            t=json.dumps(PLAN) if 'activity plan' in u else '## Profile\nx'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','sk-test'); await pg.click('text=Start'); await pg.wait_for_timeout(300)
        # create task via Create menu
        await pg.click('nav .create'); await pg.click('[data-x=task]'); await pg.wait_for_timeout(100)
        await pg.fill('#tname','Call the pump supplier'); await pg.fill('#tdued','2026-11-09'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200)
        await pg.click('nav [data-v=tasks]'); await pg.click('.lane[data-lane=doing] [data-act=task-new]'); await pg.fill('#tname','Review tender documents'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        # project with AI draft
        await pg.click('[data-act=proj-new]'); await pg.fill('#pname','Borehole for the farm'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(1500)
        print('project acts',await pg.locator('.act').count(),'gantt bars',await pg.locator('.gantt .tr i').count(),'| prompt ok:', 'project of the user' in calls[0]['messages'][0]['content'])
        await pg.click('[data-act=plan-board]'); await pg.wait_for_timeout(200)
        print('board filtered cards',await pg.locator('.kcard').count())
        await pg.select_option('#tfilter','all'); await pg.wait_for_timeout(200)
        counts=lambda: pg.evaluate("[...document.querySelectorAll('.lane')].map(l=>l.querySelectorAll('.kcard').length)")
        print('lanes before drag',await counts())
        await pg.locator('.kcard',has_text='Call the pump supplier').drag_to(pg.locator('.lane[data-lane=blocked]')); await pg.wait_for_timeout(300)
        print('lanes after drag',await counts(),'| status',await pg.evaluate("S.plans.find(p=>p.id==='my').acts[0].status"))
        await pg.screenshot(path='b1.png')
        # edit through modal
        await pg.locator('.kcard',has_text='Step 1').click(); await pg.select_option('#tstat','done'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200)
        await pg.click('[data-act=tmode][data-v=list]'); await pg.wait_for_timeout(200)
        print('list rows',await pg.locator('table.tl tbody tr').count())
        await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(200)
        print('dashboard:',(await pg.locator('main .item >> nth=0').inner_text()).replace('\n',' | '))
        await pg.click('nav [data-v=home]'); await pg.wait_for_timeout(200)
        print('today rows',await pg.locator('.hside .trow').count(),'| quick links',await pg.locator('.qcard').count())
        await pg.click('[data-act=pin]'); await pg.check('.modal input >> nth=3'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200)
        print('pins',await pg.evaluate('S.pins'),'| first link:',await pg.locator('.qcard >> nth=0').inner_text())
        await pg.screenshot(path='b2.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(200); await pg.screenshot(path='b3.png')
        await pg.click('nav [data-v=tasks]'); await pg.click('[data-act=tmode][data-v=board]'); await pg.wait_for_timeout(200); await pg.screenshot(path='b4.png')
        print('body overflow-x on phone:',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await pg.wait_for_timeout(400); await pg.reload(); await pg.wait_for_timeout(1500)
        print('after reload plans',await pg.evaluate('S.plans.map(p=>[p.name,p.acts.length])'),'| errors',errs)
        await b.close()
asyncio.run(main())
