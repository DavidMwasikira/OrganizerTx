import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
OBJ=["Estimate startup costs and monthly running costs","Identify the best AI tools to teach","Outline a four-week launch plan","Assess demand among small businesses in Kenya","Compare pricing of similar workshops","List the main risks and how to reduce them","Find channels to reach paying customers","Project income for the first six months"]
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); u=body['messages'][0]['content']; calls.append((body['model'],'tools' in body,u[:28]))
            if 'Suggest 8 specific' in u: t='Here are some:\n'+json.dumps(OBJ)
            elif 'Rewrite the research request' in u: t='Research how to run paid online AI workshops for small teams in Kenya.\n- Estimate startup costs\n- Outline a launch plan'
            elif 'Research this' in u: t=REPORT
            else: t='[]'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")   # keep the daily list out of this test
        await pg.fill('#ask','AI workshops for small teams'); await pg.click('[data-act=obj-suggest]'); await pg.wait_for_timeout(1000)
        print('objectives offered',await pg.locator('.objbox label').count())
        await pg.check('#obj0'); await pg.check('#obj2'); await pg.check('#obj5'); await pg.uncheck('#obj2'); await pg.wait_for_timeout(100)
        print('prompt now:',repr(await pg.input_value('#ask')))
        await pg.screenshot(path='o1.png')
        await pg.click('[data-act=refine]'); await pg.wait_for_timeout(1000)
        print('refined:',repr((await pg.input_value('#ask'))[:70]),'| undo offered',await pg.locator('[data-act=refine-undo]').count())
        await pg.click('[data-act=refine-undo]'); print('after undo ends with objectives:',(await pg.input_value('#ask')).endswith('reduce them'))
        await pg.click('[data-v=deep]'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1500)
        print('calls (model, web search, start):'); [print('  ',c) for c in calls]
        print('research prompt carries objectives:', await pg.evaluate("S.topics[0].query.includes('Objectives:')"),'| temp title one line:',await pg.evaluate("!S.topics[0].title.includes('\\n')"),'| errors',errs)
        await b.close()
asyncio.run(main())
