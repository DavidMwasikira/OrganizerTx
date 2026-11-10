import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.plans[0].acts.push({name:'Design page X',status:'todo',due:new Date().toISOString().slice(0,10)},{name:'Fetch assignment',status:'blocked',due:'2026-11-18'},{name:'Call supplier',status:'doing'});save()")
        await pg.click('nav [data-v=tasks]'); await pg.wait_for_timeout(300)
        bg=lambda k: pg.evaluate(f"getComputedStyle(document.querySelector('.lane[data-lane={k}]')).backgroundColor")
        print('before hover',await bg('doing'),'| lane height',await pg.evaluate("Math.round(document.querySelector('.lane').getBoundingClientRect().height)"))
        await pg.hover('.lane[data-lane=doing] header'); await pg.wait_for_timeout(300)
        print('hover In progress ->',await bg('doing'),'| others',await bg('todo'),'| tip',repr(await pg.evaluate("getComputedStyle(document.querySelector('.lane[data-lane=doing] header'),'::after').content")))
        await pg.screenshot(path='board.png')
        await pg.evaluate("S.theme='dark';applyTheme()"); await pg.wait_for_timeout(300); print('dark hover',await bg('doing')); await pg.screenshot(path='board-dark.png'); await pg.evaluate("S.theme='light';applyTheme()")
        await pg.mouse.move(900,860); await pg.click('.lane[data-lane=done] .laneadd'); await pg.wait_for_timeout(200); print('add dialog open',await pg.locator('.modal').count(),'| status preset',await pg.input_value('#tstat'))
        await pg.fill('#tname','Pay invoice'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200); print('done lane cards',await pg.locator('.lane[data-lane=done] .kcard').count())
        await pg.drag_and_drop('.lane[data-lane=todo] .kcard','.lane[data-lane=doing]'); await pg.wait_for_timeout(300); print('after drag: doing cards',await pg.locator('.lane[data-lane=doing] .kcard').count())
        await pg.click('[data-act=tmode][data-v=list]'); print('list rows',await pg.locator('table.tl tbody tr').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('[data-act=tmode][data-v=board]'); await pg.wait_for_timeout(200); print('phone overflow-x page',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs); await pg.screenshot(path='board-phone.png')
        await b.close()
asyncio.run(main())
