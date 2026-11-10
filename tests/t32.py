import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':REPORT}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.plans.push({id:'pb',name:'Borehole for the farm',what:'x',custom:true,acts:[{name:'Survey',status:'todo'}],log:[]});save();render()")
        await pg.click('nav [data-v=topics]'); await pg.wait_for_timeout(300)
        print('tabs',await pg.locator('.wstabs button').all_inner_texts(),'| list rows',await pg.locator('.wsside .it').count(),'| ask box',await pg.locator('.wscol #ask').count(),'| carousel cards',await pg.locator('.wscol .scard').count(),'| continue rows',await pg.locator('.wscol .item').count())
        await pg.screenshot(path='folders-lean.png')
        await pg.click('.wstabs button:has-text("Projects")'); await pg.wait_for_timeout(150); print('projects tab ->',await pg.locator('.wsside .it .n').all_inner_texts())
        await pg.click('.wstabs button:has-text("Guides")'); await pg.wait_for_timeout(150); print('guides tab ->',await pg.locator('.wsside .it .n').all_inner_texts())
        await pg.click('.wscol .scard >> nth=0'); await pg.wait_for_timeout(200); print('suggestion filled ask:',(await pg.input_value('#ask'))[:40])
        await pg.fill('#ask','Cost of drilling a borehole in Kiambu'); await pg.click('.wscol [data-act=research]'); await pg.wait_for_timeout(2500)
        print('after Research: view',await pg.evaluate("V.view"),'| topics',await pg.evaluate("S.topics.length"),'| list tab now',await pg.locator('.wstabs [aria-pressed=true]').inner_text(),'| current',await pg.locator('.wsside .it[aria-current=true] .n').inner_text())
        await pg.click('nav [data-v=actions]'); await pg.evaluate("ACT['open-plan']('pb');render()"); await pg.wait_for_timeout(200); print('open project elsewhere -> tab',await pg.locator('.wstabs [aria-pressed=true]').inner_text())
        await pg.click('nav [data-v=home]'); print('home still has ask + carousel',await pg.locator('#ask').count(),await pg.locator('.scar').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('nav [data-v=topics]'); await pg.wait_for_timeout(200); print('phone: list rows',await pg.locator('.wsside .it').count(),'overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs); await pg.screenshot(path='folders-phone.png')
        await b.close()
asyncio.run(main())
