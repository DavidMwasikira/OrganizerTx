import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1700,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.skin='ultraviolet';applyTheme();S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:Array.from({length:10},(_,i)=>({name:'AI Cost and Model Routing Consulting '+i,what:'Audit a firm\\'s AI bills and route tasks to cheaper models.',why:'Prices were cut in early Nov.',funds:'$0-100',earn:'$3,000-8,000 (estimate)'}))};V.hview='research';save();render()")
        await pg.wait_for_timeout(300)
        r=await pg.evaluate("(()=>{const a=document.querySelector('.rsug').getBoundingClientRect(),b=document.querySelector('.rgrid>section:nth-child(2)').getBoundingClientRect();return [Math.round(a.left),Math.round(a.width),Math.round(b.left),Math.round(b.width),Math.abs(a.top-b.top)<2]})()")
        print('two columns [left x,w | right x,w | same row]:',r,'| titles',[x.replace('\n',' / ') for x in await pg.locator('.ttl2').all_inner_texts()])
        await pg.screenshot(path='rs-two.png')
        await pg.click('.rsug .scard >> nth=0'); print('suggestion fills box:',len(await pg.input_value('#ask'))>5); await pg.click('[data-act=sug-toggle]'); await pg.wait_for_timeout(150); print('collapse works:',await pg.locator('.scar').count()==0); await pg.click('[data-act=sug-toggle]')
        await pg.click('.hhead [data-v=folders]'); await pg.wait_for_timeout(200); print('Folders pane title:',(await pg.locator('.wscol .ttl2').inner_text()).replace('\n',' / '))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('.hhead [data-v=research]'); await pg.wait_for_timeout(200); print('phone: single column',await pg.evaluate("document.querySelector('.rsug').getBoundingClientRect().width>300"),'overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs)
        await b.close()
asyncio.run(main())
