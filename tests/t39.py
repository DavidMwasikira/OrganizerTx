import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ' '.join(x.get('text','') for x in c)
    if 'Convert this budget' in text: body=json.dumps({'currency':'Kshs','lines':[{'category':'Materials','item':'PVC casing, 60 m','planned':90000,'actual':0},{'category':'Equipment','item':'Solar pump, 2 kW','planned':185000,'actual':0}],'stated_total':275000,'notes':''})
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.route('https://cdn.jsdelivr.net/npm/xlsx@0.18.5/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=open('node_modules/xlsx/dist/xlsx.full.min.js',encoding='utf-8').read()))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};save()")
        # A: total only
        await pg.click('nav [data-v=actions]'); await pg.click('[data-act=proj-new]'); await pg.screenshot(path='np-modal.png'); await pg.fill('#pname','Site office'); await pg.uncheck('#pdraft'); await pg.fill('#pbud','640,000'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(400)
        print('A total only -> tab',await pg.locator('[data-act=ptab][aria-pressed=true]').inner_text(),'| tiles',[x.replace('\n',' ') for x in await pg.locator('.btile').all_inner_texts()][:2])
        await pg.click('[data-act=ptab][data-v=plan]'); await pg.wait_for_timeout(150); print('plan tab strip:',(await pg.locator('.bstrip').inner_text()).replace('\n',' ')); await pg.screenshot(path='np-strip.png')
        await pg.click('.bstrip'); await pg.wait_for_timeout(150); print('strip click ->',(await pg.locator('[data-act=ptab][aria-pressed=true]').inner_text()).split('\n')[0])
        # B: file at creation
        await pg.click('nav [data-v=actions]'); print('dashboard row:',(await pg.locator('.mrow .sub').first.inner_text())[-45:]); await pg.click('[data-act=proj-new]'); await pg.fill('#pname','Borehole'); await pg.uncheck('#pdraft'); await pg.set_input_files('#pbudfile','budget.xlsx'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(2500)
        print('B file at creation -> review shown',await pg.locator('[data-act=bud-accept][data-v=replace]').count(),'| project',await pg.locator('.wscol h1').inner_text()); await pg.click('[data-act=bud-accept][data-v=replace]'); await pg.wait_for_timeout(200); print('lines',await pg.evaluate("budOf(curPlan()).lines.length"))
        # C: no budget
        await pg.click('nav [data-v=actions]'); await pg.click('[data-act=proj-new]'); await pg.fill('#pname','Fence'); await pg.uncheck('#pdraft'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(300); print('C none -> strip:',(await pg.locator('.bstrip').inner_text()).replace('\n',' ')[:70],'| errors',errs)
        await b.close()
asyncio.run(main())
