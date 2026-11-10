import asyncio
from playwright.async_api import async_playwright
SEED="""()=>{const d=n=>{const x=new Date();x.setDate(x.getDate()+n);return x.toISOString().slice(0,10)};
 S.plans[0].acts.push({name:'Design page X',status:'todo',due:d(0)},{name:'Fetch assignment',status:'blocked',due:d(8)},{name:'Call supplier',status:'doing',due:d(-2)},{name:'Pay invoice',status:'done',closed:Date.now()-DAY});
 S.plans.push({id:'pb',name:'Borehole for the farm',what:'x',custom:true,started:Date.now()-5*DAY,acts:[{name:'Survey',status:'done',closed:Date.now()},{name:'Permit',status:'doing'},{name:'Drill',status:'todo'}],log:[]});
 for(let i=0;i<5;i++){const t=JSON.parse(JSON.stringify(S.topics[0]));t.id='x'+i;t.code='P00'+(i+2);t.title=['Borehole for the Farm: Kenya Permits and Costs','AI Video Ads for Kenyan Ecommerce','Practical AI Tools for a Nairobi Engineering Firm','Factory Solar and Batteries in Kenya','Factory Solar Economics'][i];t.created=Date.now()-i*DAY;t.docs.forEach(x=>x.date=Date.now()-i*DAY);t.example=false;S.topics.push(t)} save();render()}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1670,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400); await pg.evaluate(SEED); await pg.wait_for_timeout(200)
        await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(300)
        print('page height',await pg.evaluate("document.querySelector('main').scrollHeight"),'| stats',await pg.locator('.zstat b').all_inner_texts(),'| ring segments',await pg.locator('.zdonut circle').count(),'| legend',[x.replace('\n',' ') for x in await pg.locator('.zdonut .legend span').all_inner_texts()])
        print('attention',[x.replace('\n',' ') for x in await pg.locator('.zbars button').all_inner_texts()],'| tabs',[x.replace('\n',' ') for x in await pg.locator('.dz .htabs button').all_inner_texts()])
        await pg.screenshot(path='dash.png',full_page=False)
        await pg.click('.dz .htabs [data-v=due]'); print('deadline rows',await pg.locator('.dz .trow').count()); await pg.click('.dz .htabs [data-v=data]'); await pg.wait_for_timeout(100); print('data cells',await pg.locator('.zcells>div').count())
        await pg.evaluate("document.querySelector('main').scrollTop=1e6"); await pg.screenshot(path='dash2.png')
        await pg.click('.zstat >> nth=0'); print('stat click ->',await pg.evaluate('V.view')); await pg.click('nav [data-v=actions]'); await pg.click('.mrow >> nth=0'); print('project click ->',await pg.evaluate('V.view'))
        await pg.evaluate("S.theme='dark';applyTheme();V.view='actions';V.dtab2='talk';render()"); await pg.wait_for_timeout(300); await pg.screenshot(path='dash-dark.png'); await pg.evaluate("S.theme='light';applyTheme()")
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("render()"); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs); await pg.screenshot(path='dash-phone.png',full_page=False)
        pg2=await (await b.new_context(viewport={'width':1400,'height':800})).new_page(); e2=[]; pg2.on('pageerror',lambda e:e2.append(str(e)))
        await pg2.goto('http://localhost:8765/index.html'); await pg2.wait_for_timeout(1200); await pg2.fill('#name','N'); await pg2.fill('#country','Kenya'); await pg2.fill('#key','k'); await pg2.click('text=Start'); await pg2.click('nav [data-v=actions]'); await pg2.wait_for_timeout(200); print('empty state ok, errors',e2); await pg2.screenshot(path='dash-empty.png')
        await b.close()
asyncio.run(main())
