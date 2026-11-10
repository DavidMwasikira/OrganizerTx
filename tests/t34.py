import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.click('nav [data-v=settings]'); await pg.wait_for_timeout(300)
        print('tabs',await pg.locator('.sett .htabs button').all_inner_texts()); await pg.screenshot(path='set-profile.png')
        await pg.fill('#town','Eldoret'); await pg.fill('#country','Uganda'); await pg.click('.sett .htabs [data-v=look]'); await pg.wait_for_timeout(150)
        print('kept after tab switch:',await pg.evaluate("[S.profile.town,S.profile.country]"),'| theme cards',await pg.locator('.skin').count())
        await pg.click('.skin[data-v=ultraviolet]'); await pg.click('[data-act=theme-set][data-v=dark]'); await pg.wait_for_timeout(200); print('skin/theme',await pg.evaluate("[document.documentElement.dataset.skin,document.documentElement.dataset.theme]")); await pg.screenshot(path='set-look.png')
        await pg.click('[data-act=theme-set][data-v=light]'); await pg.click('.skin[data-v=""]')
        await pg.click('.sett .htabs [data-v=research]'); await pg.click('.chip >> nth=0'); await pg.click('[data-act=pdepth][data-v=deep]'); await pg.fill('#dailyat','06:30'); await pg.screenshot(path='set-research.png')
        await pg.click('.sett .htabs [data-v=alerts]'); await pg.fill('#email','a@b.co'); await pg.click('.sett .htabs [data-v=connect]'); print('key field',await pg.input_value('#key'))
        await pg.click('.sett .htabs [data-v=data]'); await pg.wait_for_timeout(150); await pg.screenshot(path='set-data.png'); print('data rows',await pg.locator('.sett .srow strong').all_inner_texts())
        await pg.click('[data-act=save-settings]'); await pg.wait_for_timeout(700); await pg.reload(); await pg.wait_for_timeout(1500)
        print('after reload',await pg.evaluate("[S.profile.town,S.profile.country,S.profile.depth,S.dailyAt,S.email,S.profile.areas.length,S.key]"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("V.view='settings';V.stab='profile';render()"); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs); await pg.screenshot(path='set-phone.png')
        await b.close()
asyncio.run(main())
