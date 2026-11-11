import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        out=[{'title':'Net-metering rules','text':'Kenya gazetted net-metering and export credit rules for factory solar.'},{'title':'KPLC tariff history','text':'Current KPLC large-customer tariff schedule with fuel and forex adjustments.'},'A plain string idea about borehole permits for farms']
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(out)}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""S.skin='ultraviolet';applyTheme();S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};
          S.ideas=["Engineers Board of Kenya guidance on the use of AI tools in engineering design and sign-off","Status of Kenya's proposed AI Bill and ODPC guidance on AI processing of personal data for engineering firms","Factory energy audit and 12-month interval-data collection methods for Kenyan manufacturers before solar or battery procurement","Current KPLC large-customer tariff schedule (post-July 2025) with fuel and forex adjustment history, to model CI1 and CI3 battery value","Kenyan reseller and local pricing for factory-scale solar and battery systems, to test vendor quotes against BNEF and SEIA/Wood Mackenzie floors","Kenya's gazetted net-metering and export credit rules for factory solar (confirm the 50% export credit and retail-rate position)"];V.hview='research';save();render()""")
        await pg.wait_for_timeout(300)
        print('legacy strings -> headings:',await pg.locator('.svert .st').all_inner_texts())
        r=await pg.evaluate("(()=>{const e=document.querySelector('.svert'),s=getComputedStyle(e);return [s.flexDirection,s.overflowY,e.scrollHeight>e.clientHeight,e.scrollWidth<=e.clientWidth+1]})()"); print('vertical, scrolls down, taller than box, no sideways scroll:',r)
        await pg.screenshot(path='sv.png')
        await pg.click('.svert .scard >> nth=1'); print('click fills box:',(await pg.input_value('#ask'))[:40])
        await pg.click('[data-act=fresh-ideas]'); await pg.wait_for_timeout(1200); print('fresh ideas ->',await pg.locator('.svert .st').all_inner_texts())
        await pg.evaluate("S.ideas=[];render()"); await pg.wait_for_timeout(150); print('starter suggestions headings:',await pg.locator('.svert .st').all_inner_texts())
        await pg.click('.hhead [data-v=folders]'); await pg.wait_for_timeout(200); print('Folders pane uses the list too:',await pg.locator('.wscol .svert .scard').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('.hhead [data-v=research]'); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs)
        await b.close()
asyncio.run(main())
