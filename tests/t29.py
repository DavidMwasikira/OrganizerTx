import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1400,'height':800})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("""()=>{const big=Array.from({length:14},(_,i)=>({name:'Idea '+i,what:'What it is '.repeat(20),why:'Why '.repeat(30),funds:'Kshs 1',profit:'Kshs 2',payback:'3 months',risk:'Low'}));
          S.guides.biz={date:Date.now(),items:big};for(let i=0;i<14;i++)S.plans.push({id:'p'+i,name:'Project '+i,what:'x',custom:true,acts:Array.from({length:25},(_,j)=>({name:'Task '+j,detail:'',status:'todo'})),log:[]});save()}""")
        probe="""()=>{const m=document.querySelector('main');m.scrollTop=1e6;const o={scrolled:Math.round(m.scrollTop)};for(const c of ['.wsside','.kbside','.libgrid>*:first-child','.dsplit>*:first-child']){const e=document.querySelector(c);if(e){const r=e.getBoundingClientRect();o[c]=[Math.round(r.top),Math.round(r.bottom)]}}return o}"""
        for name,js in [('guide',"V.view='guide';V.guide='biz'"),('project',"V.view='plan';V.plan='p3'"),('folders',"V.view='topics'"),('tasks',"V.view='tasks'"),('dashboard',"V.view='actions'"),('brain notes',"V.view='brain';V.btab='notes'"),('rules',"V.view='rules'"),('home',"V.view='home'"),('topic chat',"V.view='topic';V.topic=S.topics[0].id;V.tab='chat'")]:
            await pg.evaluate(js+";V.doc=null;render()"); await pg.wait_for_timeout(300); print(f'{name:12s}',await pg.evaluate(probe))
            if name=='guide': await pg.screenshot(path='stick.png')
        print('errors',errs); await b.close()
asyncio.run(main())
