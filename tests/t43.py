import asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1690,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':REPORT}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.skin='ultraviolet';applyTheme();S.plans[0].acts.push({name:'Design page X',status:'todo',due:dash(Date.now()-DAY)},{name:'Fetch assignment',status:'blocked',due:dash(Date.now()+7*DAY)});S.brief={day:dash(Date.now()),at:Date.now(),summary:'Today is a light day. Design page X is overdue.',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:Array.from({length:10},(_,i)=>({name:'Idea '+i,what:'What',why:'Why',funds:'$0-100',earn:'$3,000'}))};save();render()")
        await pg.wait_for_timeout(300)
        print('tabs',[x.replace('\n',' ') for x in await pg.locator('.hhead .htabs button').all_inner_texts()],'| default',await pg.locator('.hhead .htabs [aria-pressed=true]').inner_text())
        r=await pg.evaluate("[document.querySelector('.myday').getBoundingClientRect().left<document.querySelector('.hside').getBoundingClientRect().left, !!document.querySelector('#ask')]"); print('My Day on left, no research box on this tab:',r[0],not r[1]); await pg.screenshot(path='h-day.png')
        await pg.click('.hhead [data-v=research]'); await pg.wait_for_timeout(300); print('RESEARCH: ask',await pg.locator('#ask').count(),'carousel',await pg.locator('.scar').count(),'weekly cards',await pg.locator('.wk, .wcard, [data-act=wk-scroll]').count()>0,'| my day here',await pg.locator('.myday').count()); await pg.screenshot(path='h-research.png')
        await pg.click('.hhead [data-v=tasks]'); await pg.wait_for_timeout(300); print('TASKS: lanes',await pg.locator('.lane').count(),'cards',await pg.locator('.kcard').count(),'| home tab still current',await pg.locator('nav [data-v=home][aria-current=page]').count()); await pg.screenshot(path='h-tasks.png')
        await pg.click('.toolbar [data-act=task-new]'); await pg.fill('#tname','From home'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200); print('add task stays on Home tasks tab:',await pg.evaluate("[V.view,V.hview]"),await pg.locator('.kcard').count())
        await pg.click('[data-act=tmode][data-v=cal]'); print('calendar inside Home',await pg.locator('.cal').count()); await pg.click('[data-act=tmode][data-v=board]')
        await pg.click('.hhead [data-v=folders]'); await pg.wait_for_timeout(300); print('FOLDERS: list rows',await pg.locator('.wsside .it').count(),'| right has ask',await pg.locator('.wscol #ask').count()); await pg.screenshot(path='h-folders.png')
        await pg.fill('#ask','Cost of a borehole'); await pg.click('.wscol [data-act=research]'); await pg.wait_for_timeout(2500); print('research from Home folders ->',await pg.evaluate("V.view"),'topics',await pg.evaluate("S.topics.length"))
        await pg.click('nav [data-v=home]'); print('back to Home keeps tab:',await pg.evaluate("V.hview")); await pg.click('.hhead [data-v=day]'); await pg.click('.hside [data-v=updates]'); print('latest updates rows',await pg.locator('.hside .item').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("render()"); await pg.wait_for_timeout(200); o=[]
        for k in ['day','research','tasks','folders']:
            await pg.click(f'.hhead [data-v={k}]'); await pg.wait_for_timeout(200); o.append(await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
        print('phone overflow-x per tab',o,'| errors',errs); await pg.click('.hhead [data-v=day]'); await pg.screenshot(path='h-phone.png')
        await b.close()
asyncio.run(main())
