import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
BRAIN = """# David Mwasikira: Knowledge Base

## Profile and interests
**Focus areas:** Engineering, Business, Technology and AI, Energy, Jobs and careers.
**Current focus:** Energy economics for factory-scale solar and battery systems.

## Energy
### Factory solar and battery economics
#### Modelling approach
- Model solar and battery separately, then together.
- Solar usually carries the project economics. The battery's value depends on the tariff.
#### Key value drivers
- Demand charges, time-of-use spreads and export credit rules determine whether a project makes sense.
- Get 12 months of interval data before requesting or accepting any quote.
- Tariff class largely decides whether a battery pays.
#### Pricing benchmarks
- Compare quotes against BNEF for batteries and SEIA/Wood Mackenzie for solar.
- Installed factory-scale prices run well above global turnkey averages.
- No Kenyan factory-scale price benchmark has been found.

## Technology and AI
### AI tools for an engineering firm
- Start with document drafting and tender review before design automation.
- Engineers Board of Kenya guidance on AI sign-off is still unclear.
- Keep client drawings out of public AI tools unless the contract allows it.
### AI video advertising
- A lean launch needs modest capital; human editing protects quality.
- Several Nairobi studios already advertise AI video.

## Business
- Validate demand with a paid pilot before buying equipment.
- VAT registration threshold should be confirmed with KRA before pricing.
"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1420,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.click('text=Engineering'); await pg.click('text=Energy'); await pg.click('text=Business'); await pg.click('text=Technology and AI'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("""(B)=>{const now=Date.now();S.brain.organized=B;S.brain.lastOrg=now;
          const mk=(n,title,docs)=>({id:'t'+n,code:'P00'+n,title,query:title,depth:'moderate',interval:n%2?168:0,nextDue:now+9e8,created:now-n*864e5,asked:true,unread:0,nUser:1,chat:[{role:'user',text:title,date:now}],docs:docs.map((d,i)=>({ref:'P00'+n+'-'+(i?'U0'+i:'R01')+'-20261110',type:i?'U':'R',title:d,date:now-i*36e5,depth:'moderate',sources:[],md:'# '+d+'\\n\\n## Summary\\n- Key point about '+d.toLowerCase()+'.\\n- A second point on costs and tariffs.'}))});
          S.topics=[mk(5,'AI Video Ads for Kenyan Ecommerce: Feasibility',['AI Video Ads for Kenyan Ecommerce: Feasibility']),mk(4,'Practical AI Tools for a Nairobi Engineering Firm',['Practical AI Tools for a Nairobi Engineering Firm','Update: New AI guidance for engineers']),mk(3,'Factory Solar and Batteries in Kenya',['Factory Solar and Batteries in Kenya','Update: Battery prices fall again','Update: New solar tariff rules']),mk(2,'Factory Solar and Battery Economics, November 2026',['Factory Solar and Battery Economics'])];
          S.brain.entries=[{date:now,topic:'x',text:'- [Factory Solar and Batteries in Kenya] Export credit is capped under the net-metering rules.'},{date:now,topic:'x',text:'- [AI Video Ads for Kenyan Ecommerce: Feasibility] Film licence position for AI-only video is unconfirmed.'}];
          S.plans.push({id:'a1',guide:null,custom:true,name:'Borehole for the farm',what:'Water for irrigation',active:true,started:now,created:now,weeks:8,summary:'',acts:['Hydrogeological survey','Drilling permit','Choose solar pump','Drill and case','Install tank','Commission system'].map((x,i)=>({name:x,detail:'',status:i<2?'done':'todo',start:i+1,weeks:2}))});
          S.plans.find(x=>x.id==='my').acts.push({name:'Call the solar pump supplier',status:'todo',detail:''},{name:'Review tender documents',status:'doing',detail:''});
          S.weekly={kind:'ai',date:now,items:['AI voice agents for clinics','Automated invoice chasing','AI product photo studio','Chatbot set-up for online shops','AI meeting notes service','Niche newsletter with AI research','AI tutoring packs','Document translation desk','AI video shorts editing','Custom assistants for firms'].map(n=>({name:n,what:'Sells to small businesses online.',why:'Demand is rising.',funds:'$200',earn:'$1,500'}))};save()}""",BRAIN)
        await pg.click('nav [data-v=brain]'); await pg.wait_for_timeout(1200)
        print('stats:',(await pg.locator('.bstats').inner_text()).replace('\n',' '),'| legend:',(await pg.locator('.blegend').inner_text()).replace('\n',' ')[:170])
        await pg.screenshot(path='m1.png')
        await pg.fill('#bq','tariff'); await pg.wait_for_timeout(300); print('search hits:',await pg.locator('#bhits button').all_inner_texts())
        await pg.click('#bhits button >> nth=0'); await pg.fill('#bq',''); await pg.wait_for_timeout(900)
        print('panel:',(await pg.locator('#bpanel').inner_text()).replace('\n',' | ')[:330])
        await pg.screenshot(path='m2.png')
        await pg.click('[data-bact=focus]'); await pg.wait_for_timeout(300); await pg.click('#bpanel .cn >> nth=0'); await pg.wait_for_timeout(600); print('followed a connection ->',await pg.locator('#bpanel h3').inner_text())
        await pg.click('[data-bact=close]')
        # click a point on the canvas itself
        pt=await pg.evaluate("(()=>{const n=BM.nodes.filter(n=>n.src==='topic').sort((a,b)=>a.sz-b.sz)[0];const b=document.querySelector('#bcanvas').getBoundingClientRect();return [b.left+n.sx,b.top+n.sy,n.title]})()")
        await pg.mouse.click(pt[0],pt[1]); await pg.wait_for_timeout(300); print('canvas click on',repr(pt[2]),'-> panel',repr(await pg.evaluate("BM.sel&&BM.by[BM.sel].title")))
        y0=await pg.evaluate('BM.yaw'); await pg.mouse.move(700,700); await pg.mouse.down(); await pg.mouse.move(900,650,steps=5); await pg.mouse.up(); print('drag turned it:',abs(await pg.evaluate('BM.yaw')-y0)>.5,end=' | ')
        await pg.mouse.wheel(0,-600); await pg.wait_for_timeout(100); print('zoom',round(await pg.evaluate('BM.zoom'),2),end=' | ')
        await pg.click('[data-bact=src][data-v=task]'); print('tasks hidden:',await pg.evaluate("BM.off.task"))
        await pg.click('#bpanel [data-act=open-topic]'); await pg.wait_for_timeout(300); print('Open ->',await pg.evaluate('V.view'))
        await pg.go_back(); await pg.wait_for_timeout(400); await pg.click('[data-act=btab][data-v=notes]'); await pg.wait_for_timeout(200); print('notes tab keeps text + editor:',await pg.locator('#braintext').count(),await pg.locator('.md h2').count())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('[data-act=btab][data-v=map]'); await pg.wait_for_timeout(800)
        print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs); await pg.screenshot(path='m3.png')
        await b.close()
asyncio.run(main())
