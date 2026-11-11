import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://cdn.jsdelivr.net/npm/xlsx@0.18.5/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=open('node_modules/xlsx/dist/xlsx.full.min.js',encoding='utf-8').read()))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.skin='ultraviolet';applyTheme();S.plans[0].acts.push({name:'Define needs, size and budget',status:'todo',due:'2026-11-23',detail:'Write a one-page brief.'});S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};V.hview='tasks';save();render()")
        await pg.click('.kcard'); await pg.wait_for_timeout(200); print('fields: budget',await pg.locator('#tbud').count(),'currency options',await pg.locator('#tcur option').all_inner_texts(),'| panel hidden at first',await pg.locator('#tsub').is_hidden())
        await pg.fill('#tbud','50,000'); await pg.click('#tsubbtn'); await pg.wait_for_timeout(150)
        r=await pg.evaluate("(()=>{const f=document.querySelector('.tduo form').getBoundingClientRect(),s=document.querySelector('#tsub').getBoundingClientRect();return [Math.round(f.right),Math.round(s.left),s.left>f.right]})()"); print('panel opens on the right of the dialog:',r)
        await pg.fill('#tsubnew','Count staff'); await pg.keyboard.press('Enter'); await pg.fill('#tsubnew','Estimate floor area'); await pg.click('#tsubadd'); await pg.click('[data-st="0"]')
        await pg.set_input_files('#tsubfile','tasklist.txt'); await pg.wait_for_timeout(500); print('after attaching txt:',[await x.input_value() for x in await pg.locator('#tsublist input').all()],'|',await pg.locator('#tsubmsg').inner_text())
        await pg.set_input_files('#tsubfile','budget.xlsx'); await pg.wait_for_timeout(1200); print('after attaching xlsx: count',await pg.locator('#tsublist input').count(),'| last three',[await x.input_value() for x in (await pg.locator('#tsublist input').all())[-3:]])
        await pg.click('[data-sd] >> nth=-1'); print('counter',await pg.locator('#tsubn').inner_text()); await pg.screenshot(path='td.png')
        await pg.click('[data-x=save]'); await pg.wait_for_timeout(300)
        print('saved:',await pg.evaluate("(()=>{const a=S.plans[0].acts.slice(-1)[0];return [a.budget,a.subs.length,a.subs.filter(x=>x.done).length]})()"),'| card:',(await pg.locator('.kcard').inner_text()).replace('\n',' | '))
        await pg.click('.kcard'); await pg.wait_for_timeout(200); print('reopen: budget',await pg.input_value('#tbud'),await pg.input_value('#tcur'),'| panel opens with list',await pg.locator('#tsub').is_visible(),await pg.locator('#tsublist input').count()); await pg.select_option('#tcur','USD'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200); print('currency change ->',await pg.evaluate("S.plans[0].acts.slice(-1)[0].budget"))
        await pg.click('.toolbar [data-act=task-new]'); await pg.fill('#tname','Plain task'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200); print('plain task has no budget/subs:',await pg.evaluate("(()=>{const a=S.plans[0].acts.slice(-1)[0];return [a.budget,a.subs.length]})()"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('.kcard >> nth=0'); await pg.wait_for_timeout(200); 
        if await pg.locator('#tsub').is_hidden(): await pg.click('#tsubbtn')
        r=await pg.evaluate("(()=>{const f=document.querySelector('.tduo form').getBoundingClientRect(),s=document.querySelector('#tsub').getBoundingClientRect();return [s.top>=f.bottom-1,document.documentElement.scrollWidth>innerWidth,document.querySelector('.modal').scrollHeight>innerHeight]})()"); print('phone: panel below dialog, overflow-x, dialog scrolls:',r,'| errors',errs)
        await b.close()
asyncio.run(main())
