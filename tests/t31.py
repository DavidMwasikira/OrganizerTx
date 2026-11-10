import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(400)
        print('height',await pg.evaluate("document.querySelector('main').scrollHeight"),'| capture card visible',await pg.locator('.desk .caphome').is_visible(),'| By type list gone',await pg.locator('.desk h2:has-text("By type")').count()==0)
        print('tabs',await pg.locator('.desk .htabs button').all_inner_texts(),'| folder tiles',await pg.locator('#deskbody .fold2').count())
        await pg.screenshot(path='desk-lean.png',full_page=False)
        await pg.click('.desk .htabs [data-v=files]'); await pg.wait_for_timeout(150); print('files tab rows',await pg.locator('#deskbody .dfile').count())
        await pg.click('.desk .htabs [data-v=folders]'); await pg.select_option('#dtype','lib'); await pg.wait_for_timeout(200)
        print('after choosing type:',await pg.locator('.desk .htabs [aria-pressed=true]').inner_text(),'| rows',await pg.locator('#deskbody .dfile').count(),'| options',await pg.locator('#dtype option').all_inner_texts())
        await pg.select_option('#dtype','all'); await pg.fill('#dq','solar'); await pg.wait_for_timeout(400); print('search:',await pg.locator('.desk .htabs button').all_inner_texts(),'| focus kept',await pg.evaluate("document.activeElement.id"))
        await pg.fill('#dq',''); await pg.hover('.capnav'); await pg.wait_for_timeout(200); print('flyout on desktop page',await pg.locator('.capfly').is_visible())
        await pg.mouse.move(900,400); await pg.evaluate("document.querySelector('main').scrollTop=1e6"); await pg.wait_for_timeout(200); await pg.screenshot(path='desk-lean2.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("render()"); await pg.wait_for_timeout(200)
        print('phone: capture card',await pg.locator('.desk .caphome').is_visible(),'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await pg.locator('#deskbody').scroll_into_view_if_needed(); await pg.screenshot(path='desk-phone.png'); await b.close()
asyncio.run(main())
