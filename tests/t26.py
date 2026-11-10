import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1440,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]};S.plans.push({id:'a1',guide:null,custom:true,name:'Borehole for the farm',what:'',active:true,started:Date.now(),created:Date.now(),weeks:2,summary:'',acts:[{name:'Drilling',status:'doing',start:1,weeks:2}]});save();render()")
        for name,w,h in [('desktop',1440,900),('tablet',820,1180),('phone',390,800)]:
            await pg.set_viewport_size({'width':w,'height':h}); await pg.click('nav [data-v=home]'); await pg.wait_for_timeout(250)
            hb=await pg.locator('main .capbtn.cam').first.bounding_box(); hv=await pg.locator('main .capbtn').count()
            await pg.screenshot(path=f'h-{name}.png')
            await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(250)
            db=await pg.locator('.desk [data-act=cap][data-v=photo]').bounding_box(); link=await pg.locator('.desk .dhead [data-v=field]').is_visible(); tile=await pg.locator('.fold2.big:has-text("Field capture")').is_visible()
            print(f'{name:8s} Home: {hv} capture buttons, camera at y={round(hb["y"])} (screen {h}) | Desktop: camera at y={round(db["y"])}, header link {link}, folder tile {tile} | overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
            if name=='phone': await pg.screenshot(path='d-phone.png')
        await pg.click('nav [data-v=home]'); await pg.click('main .capbtn:has-text("Text note")'); await pg.fill('#captext','Water struck at 85 m.'); await pg.select_option('#capproj',label='Borehole for the farm'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(400)
        print('saved from Home; strip now says:',await pg.locator('main [data-v=field]').first.inner_text())
        await pg.click('main [data-v=field] >> nth=0'); await pg.wait_for_timeout(250); print('field screen:',await pg.locator('main h1').inner_text(),'| projects listed',await pg.locator('main h2').all_inner_texts(),'| rows',await pg.locator('.logrow').count(),'| Back button',await pg.locator('[data-act=back]').count(),'| errors',errs)
        await b.close()
asyncio.run(main())
