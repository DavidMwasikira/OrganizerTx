import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1690,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.skin='ultraviolet';applyTheme();S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};save();render()")
        print('sidebar:',[x.replace('\n',' ') for x in await pg.locator('nav > button').all_inner_texts()])
        await pg.click('.hhead [data-v=folders]'); await pg.wait_for_timeout(200); print('Folders from Home tab: list rows',await pg.locator('.wsside .it').count(),'| sidebar current',await pg.locator('nav [aria-current=page]').inner_text())
        await pg.click('.wsside .it >> nth=0'); await pg.wait_for_timeout(200); print('open chat: sidebar current',await pg.locator('nav [aria-current=page]').inner_text(),'| header tab',(await pg.locator('.hhead [aria-pressed=true]').inner_text()).split('\n')[0])
        await pg.click('.wscol [data-act=nav][data-v=topics]'); await pg.wait_for_timeout(200); print('"← Folders" link ->',await pg.evaluate("[V.view,V.hview]"))
        await pg.click('nav [data-v=settings]'); await pg.wait_for_timeout(200); print('SETTINGS top tabs',await pg.locator('.settop button').all_inner_texts(),'| active',await pg.locator('.settop [aria-pressed=true]').inner_text(),'| sub-tabs',await pg.locator('.sett .htabs:not(.settop) button').count()); await pg.screenshot(path='st-settings.png')
        await pg.click('.settop [data-v=rules]'); await pg.wait_for_timeout(300); print('RULES tab: active',await pg.locator('.settop [aria-pressed=true]').inner_text(),'| files',await pg.locator('.kbside .it').count(),'| sidebar current',await pg.locator('nav [aria-current=page]').inner_text(),'| back',await pg.locator('main [data-act=back]').count()); await pg.screenshot(path='st-rules.png')
        await pg.click('.kbside .it >> nth=2'); await pg.wait_for_timeout(200); print('pick a rule keeps tab:',await pg.evaluate("V.view"),await pg.locator('.settop').count())
        await pg.click('.settop [data-v=settings]'); await pg.wait_for_timeout(200); print('back to Settings ->',await pg.evaluate("V.view"))
        await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(300); n=await pg.locator('.desk [data-act=nav][data-v=rules], .desk [data-v=rules]').count(); 
        if n: await pg.locator('.desk [data-v=rules]').first.click(); await pg.wait_for_timeout(200); print('Desktop "Rules and skills" folder ->',await pg.evaluate("V.view"),'tabs',await pg.locator('.settop').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("V.view='settings';render()"); await pg.wait_for_timeout(200); print('phone bottom bar:',[x.replace('\n',' ') for x in await pg.locator('nav > button:visible').all_inner_texts()],'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await b.close()
asyncio.run(main())
