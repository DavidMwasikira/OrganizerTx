import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1420,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'An answer.'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("""()=>{const now=Date.now();S.weekly={kind:'ai',date:now,items:[{name:'x',what:'y',why:'z'}]};
          const mk=(n,title,iv)=>({id:'t'+n,code:'P00'+n,title,query:'Research brief: '+title,depth:'moderate',interval:iv,nextDue:now+9e8,created:now,asked:true,unread:n===3?1:0,nUser:1,chat:[{role:'user',text:'Research brief for '+title+' with several objectives listed here to make it long.',date:now},{role:'doc',ref:'P00'+n+'-R01-20261110',date:now}],docs:[{ref:'P00'+n+'-R01-20261110',type:'R',title,date:now,depth:'moderate',sources:[],md:'# '+title+'\\n\\n## Summary\\n- Point one.\\n- Point two.'}]});
          S.topics=[mk(5,'AI Video Ads for Kenyan Ecommerce: Feasibility',0),mk(4,'Practical AI Tools for a Nairobi Engineering Firm',0),mk(3,'Factory Solar and Batteries in Kenya',168),mk(2,'Factory Solar and Battery Economics, November 2026',0)];
          S.plans.push({id:'a1',guide:null,custom:true,name:'Borehole for the farm',what:'',active:true,started:now,created:now,weeks:4,summary:'',acts:[{name:'Survey',status:'done',start:1,weeks:1},{name:'Drill',status:'todo',start:2,weeks:2}]});save()}""")
        await pg.click('nav [data-v=topics]'); await pg.click('[data-act=open-topic] >> nth=0'); await pg.wait_for_timeout(300)
        print('groups:',[x.replace('\n',' ') for x in await pg.locator('.wsside .g').all_inner_texts()],'| current:',await pg.locator('.wsside .it[aria-current=true] .n').inner_text())
        cb=await pg.locator('.composer').bounding_box(); print('composer at bottom of screen:',cb['y']+cb['height']>850,'| page beside list:',(await pg.locator('.wscol .page').bounding_box())['x']>(await pg.locator('.wsside').bounding_box())['x']+270)
        await pg.screenshot(path='ws1.png')
        await pg.click('.wsside .it:has-text("Factory Solar and Batteries in Kenya")'); await pg.wait_for_timeout(200); print('switched chat ->',await pg.locator('.thead h1').inner_text())
        await pg.click('[data-act=tab][data-v=folder]'); print('folder tab keeps list:',await pg.locator('.wsside').count())
        await pg.click('.wsside .it:has-text("Borehole")'); await pg.wait_for_timeout(200); print('switched to project ->',await pg.locator('.thead h1').inner_text(),'| list shown',await pg.locator('.wsside').count()); await pg.screenshot(path='ws2.png')
        await pg.click('.wsside .it:has-text("Best AI stack")'); await pg.wait_for_timeout(600); print('guide ->',await pg.locator('.thead h1').inner_text())
        await pg.click('.wsside .it:has-text("AI Video Ads")'); await pg.click('[data-act=open-doc] >> nth=0'); await pg.wait_for_timeout(200); print('document view: list hidden',await pg.locator('.wsside').count()==0)
        await pg.click('[data-act=close-doc]'); await pg.fill('#chat','hello'); await pg.click('[data-act=send]'); await pg.wait_for_timeout(900); print('chat still works:',await pg.locator('.msg.ai').last.inner_text())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(200); print('phone: drop-down',await pg.locator('#wspick').is_visible(),'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await pg.select_option('#wspick',label='Borehole for the farm'); await pg.wait_for_timeout(200); print('phone switch ->',await pg.evaluate('V.view'),'| errors',errs)
        await b.close()
asyncio.run(main())
