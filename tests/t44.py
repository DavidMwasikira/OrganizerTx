import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1690,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.skin='ultraviolet';applyTheme();S.plans.push({id:'pb',name:'Borehole',what:'x',custom:true,started:Date.now(),acts:[{name:'Survey',status:'todo'}],log:[]});S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};save();render()")
        async def chk(name):
            await pg.wait_for_timeout(200); n=await pg.locator('.hhead').count(); vis=await pg.locator('.hhead h1').is_visible() if n else False
            act=(await pg.locator('.hhead .htabs [aria-pressed=true]').inner_text()).split('\n')[0] if await pg.locator('.hhead .htabs [aria-pressed=true]').count() else '-'
            print(f'{name:16s} heading shown {n==1 and vis} | active tab: {act} | back button {await pg.locator("main [data-act=back]").count()}')
        for v in ['home','assist','desk','tasks','actions','topics','brain','rules','help','settings']:
            await pg.click(f'nav [data-v={v}]'); await chk(v)
        await pg.click('nav [data-v=topics]'); await pg.click('.wsside .it >> nth=0'); await chk('open chat'); await pg.screenshot(path='hh-chat.png')
        await pg.evaluate("ACT['open-doc']&&0"); 
        d=await pg.locator('[data-act=open-doc]').count()
        if d: await pg.locator('[data-act=open-doc]').first.click(); await chk('open document')
        await pg.evaluate("V.doc=null;ACT['open-plan']('pb');render()"); await chk('open project'); await pg.evaluate("V.view='guide';V.guide='biz';render()"); await chk('guide'); await pg.evaluate("V.view='field';render()"); await chk('field log')
        await pg.click('.hhead [data-v=research]'); await chk('tab from elsewhere'); print('-> view',await pg.evaluate("[V.view,V.hview]"),'ask box',await pg.locator('#ask').count())
        await pg.evaluate("V.view='topic';V.topic=S.topics[0].id;render()"); await pg.wait_for_timeout(200)
        r=await pg.evaluate("(()=>{const m=document.querySelector('main');m.scrollTop=400;const s=document.querySelector('.wsside').getBoundingClientRect();return [Math.round(s.top),Math.round(s.height)]})()"); print('scrolled chat: side list still pinned at top',r)
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("render()"); await chk('phone chat'); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'errors',errs); await pg.screenshot(path='hh-phone.png')
        await b.close()
asyncio.run(main())
