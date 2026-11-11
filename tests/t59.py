import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1600,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""const mk=(id,n)=>({id,name:n,what:'x',custom:true,active:true,started:Date.now(),weeks:4,log:[],acts:[{id:uid(),name:'Task A',start:1,weeks:2,status:'todo',deps:[]}]});S.plans.push(mk('p1','Borehole for the farm'),mk('p2','Building new site office'),mk('p3','Three bedroom house'));
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};save();render()""")
        nt=await pg.evaluate("S.topics.length")
        await pg.click('[data-act=hview][data-v=folders]'); await pg.wait_for_timeout(300)
        print('Folders tab ->',await pg.locator('.ptitle h1').inner_text(),'| research start shown',await pg.locator('text=Start a new research').count(),'| list visible',await pg.locator('.wsside').is_visible(),'| tab active',await pg.locator('.hhead [aria-pressed=true]').inner_text())
        print('list:',[x.replace('\n',' | ') for x in await pg.locator('.wsside .itw').all_inner_texts()],'| delete icons',await pg.locator('.wsside .itdel').count())
        await pg.screenshot(path='v53.png')
        await pg.click('.wsside .it >> text=Borehole for the farm'); await pg.wait_for_timeout(200); await pg.click('[data-act=hview][data-v=day]'); await pg.click('[data-act=hview][data-v=folders]'); await pg.wait_for_timeout(200); print('remembers last project:',await pg.locator('.ptitle h1').inner_text())
        await pg.locator('.itw:has-text("Borehole for the farm") .itdel').click(); await pg.wait_for_timeout(200); print('confirm:',(await pg.locator('.modal').inner_text()).replace('\n',' | ')[:170]); await pg.click('.modal [data-x=cancel], .modal .btn:not(.danger):not(.primary)'); await pg.wait_for_timeout(200); print('cancel keeps',await pg.evaluate("S.plans.filter(p=>!p.builtin).length"))
        await pg.locator('.itw:has-text("Borehole for the farm") .itdel').click(); await pg.wait_for_timeout(200); await pg.locator('.modal .btn.danger, .modal .btn.primary').last.click(); await pg.wait_for_timeout(300)
        print('deleted current -> projects',await pg.evaluate("S.plans.filter(p=>!p.builtin).map(p=>p.name)"),'| now showing',await pg.locator('.ptitle h1').inner_text())
        await pg.click('.wstabs button >> text=Research chats'); await pg.wait_for_timeout(200); n=await pg.locator('.wsside .itdel').count(); await pg.locator('.wsside .itdel').first.click(); await pg.wait_for_timeout(200); await pg.locator('.modal .btn.danger, .modal .btn.primary').last.click(); await pg.wait_for_timeout(300); print('folder delete: topics',nt,'->',await pg.evaluate("S.topics.length"),'| still on project',await pg.locator('.ptitle h1').count())
        await pg.click('.wstabs button >> text=Guides'); await pg.wait_for_timeout(200); print('guides have delete icons:',await pg.locator('.wsside .itdel').count())
        for nm in ['Building new site office','Three bedroom house']:
            await pg.click('.wstabs button >> text=Projects'); await pg.locator(f'.itw:has-text("{nm}") .itdel').click(); await pg.wait_for_timeout(200); await pg.locator('.modal .btn.danger, .modal .btn.primary').last.click(); await pg.wait_for_timeout(300)
        print('no projects left -> fallback shows research start',await pg.locator('text=Start a new research').count(),'| view',await pg.evaluate("V.view+'/'+V.hview"))
        await pg.click('[data-act=hview][data-v=research]'); await pg.wait_for_timeout(200); print('Research tab still has the prompt:',await pg.locator('#ask').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("S.plans.push({id:'p9',name:'Phone project',custom:true,active:true,started:Date.now(),weeks:1,log:[],acts:[]});V.view='home';V.hview='folders';render()"); await pg.wait_for_timeout(300)
        print('phone: folder list kept',await pg.locator('.wsside').is_visible(),'| overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"),'| errors',errs); await pg.screenshot(path='v53-phone.png')
        await b.close()
asyncio.run(main())
