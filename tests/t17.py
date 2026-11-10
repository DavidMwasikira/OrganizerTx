import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
BRAIN=open('t16.py').read().split('BRAIN = """')[1].split('"""')[0].replace("## Business\n- Validate demand with a paid pilot before buying equipment.\n- VAT registration threshold should be confirmed with KRA before pricing.\n","## Open follow-ups\n- Confirm the gazetted export credit rate and the retail-rate position.\n- Obtain a current KPLC tariff schedule, as the file on record is from July 2025.\n- Confirm whether AI-generated ads need a KFCB licence.\n- Find a reliable supplier of industrial sewing machines in Mombasa.\n")
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1420,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); u=body['messages'][-1]['content']; calls.append(u if isinstance(u,str) else 'blocks')
            t=REPORT if 'Research this' in str(u) else 'The export credit is **50%** per the gazetted rules.' if 'Follow-up from' in str(u) else '[]'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("""(B)=>{const now=Date.now();S.brain.organized=B;S.brain.lastOrg=now;S.weekly={kind:'ai',date:now,items:[{name:'x',what:'y',why:'z'}]};
          const mk=(n,title,body)=>({id:'t'+n,code:'P00'+n,title,query:title,depth:'moderate',interval:0,nextDue:0,created:now,asked:true,unread:0,nUser:1,chat:[{role:'user',text:title,date:now},{role:'doc',ref:'P00'+n+'-R01-20261110',date:now}],docs:[{ref:'P00'+n+'-R01-20261110',type:'R',title,date:now,depth:'moderate',sources:[],md:'# '+title+'\\n\\n## Summary\\n- '+body}]});
          S.topics=[mk(5,'AI Video Ads for Kenyan Ecommerce: Feasibility','KFCB licence for filming and AI-generated ads is unconfirmed.'),mk(3,'Factory Solar and Batteries in Kenya','Net-metering export credit and KPLC tariff schedule decide the economics.')];save()}""",BRAIN)
        await pg.click('nav [data-v=brain]'); await pg.click('[data-act=btab][data-v=notes]'); await pg.wait_for_timeout(300)
        print('sidebar:',[x.replace('\n',' ') for x in await pg.locator('.kbside .g, .kbside .it').all_inner_texts()])
        print('overview tiles:',[x.replace('\n',' ') for x in await pg.locator('.kpi').all_inner_texts()],'| section cards',await pg.locator('.kbcards > *').count(),'| editor hidden in a fold',await pg.locator('details.hq #braintext').count())
        await pg.screenshot(path='n1.png')
        await pg.click('.kbside .it:has-text("Factory solar")'); await pg.wait_for_timeout(200)
        print('selected:',await pg.locator('.kbhead h2').inner_text(),'| cards',await pg.locator('.kbcards .panel h2').all_inner_texts(),'| editor on this screen',await pg.locator('#braintext').count())
        await pg.screenshot(path='n2.png')
        await pg.click('[data-act=share-kb]'); await pg.wait_for_timeout(200)
        txt=await pg.evaluate("decodeURIComponent(document.querySelector('.sharegrid a').href.split('text=')[1])")
        print('share text starts:',repr(txt[:120]),'| mentions other sections or editor:', 'AI video advertising' in txt or 'Profile and interests' in txt); await pg.click('[data-x=cancel]')
        await pg.click('.kbside .it:has-text("Open follow-ups")'); await pg.wait_for_timeout(200)
        print('follow-ups:'); [print('   ',x.replace('\n',' | ')) for x in await pg.locator('.fu').all_inner_texts()]
        await pg.screenshot(path='n3.png')
        await pg.click('.fu >> nth=0 >> [data-act=fu-go]'); await pg.wait_for_timeout(1200)
        print('after Research this: view',await pg.evaluate('V.view+" "+topic().code'),'| chat now',await pg.evaluate("topic().chat.map(m=>m.role)"),'| answer:',await pg.locator('.msg.ai').last.inner_text())
        await pg.click('[data-act=share-msg]'); await pg.wait_for_timeout(200); print('share one answer:',repr((await pg.evaluate("decodeURIComponent(document.querySelector('.sharegrid a').href.split('text=')[1])")).replace('\n',' / ')[:230])); await pg.click('[data-x=cancel]')
        await pg.click('[data-act=share-chat]'); await pg.wait_for_timeout(200); print('share chat:',repr((await pg.evaluate("decodeURIComponent(document.querySelector('.sharegrid a').href.split('text=')[1])")).replace('\n',' / ')[:200])); await pg.click('[data-x=cancel]')
        await pg.go_back(); await pg.wait_for_timeout(400); print('back on notes, first follow-up now reads:',(await pg.locator('.fu').first.inner_text()).replace('\n',' | '))
        await pg.click('.fu >> nth=3 >> [data-act=fu-go]'); await pg.wait_for_timeout(1300); print('unmatched follow-up -> new folder:',await pg.evaluate('S.topics[0].title'))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('nav [data-v=brain]'); await pg.wait_for_timeout(300)
        print('phone: picker shown',await pg.locator('#kbpick').is_visible(),'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await b.close()
asyncio.run(main())
