import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1420,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("""()=>{const now=Date.now();S.weekly={kind:'ai',date:now,items:[{name:'x',what:'y',why:'z'}]};
          const mk=(n,title,iv,types)=>({id:'t'+n,code:'P00'+n,title,query:title,depth:'moderate',interval:iv,nextDue:now+9e8,created:now-n*864e5,asked:true,unread:0,nUser:1,chat:[{role:'user',text:title,date:now},{role:'ai',text:'Answer',date:now-n*36e5}],docs:types.map((ty,i)=>({ref:'P00'+n+'-'+ty+'0'+(i+1)+'-20261110',type:ty,title:(ty==='U'?'Update: ':'')+title,date:now-(n*5+i)*36e5,depth:'moderate',sources:[],md:'# '+title+'\\n\\n## Summary\\n- Point.',deck:ty==='P'?{title,subtitle:'s',slides:[{layout:'title',tone:'dark',title,text:'',bullets:[],items:[],table:null,image:'',source:'',notes:''}]}:undefined}))});
          S.topics=[mk(6,'Borehole for the Farm: Kenya Permits and Costs',0,['R']),mk(5,'AI Video Ads for Kenyan Ecommerce: Feasibility',0,['R','P']),mk(4,'Practical AI Tools for a Nairobi Engineering Firm',0,['R']),mk(3,'Factory Solar and Batteries in Kenya',168,['R','U','U'])];
          S.plans.push({id:'a1',guide:null,custom:true,name:'Borehole for the farm',what:'',active:true,started:now,created:now,weeks:4,summary:'',acts:[{name:'Survey',status:'done',start:1,weeks:1},{name:'Permit',status:'done',start:1,weeks:1},{name:'Drill',status:'todo',start:2,weeks:2}]});
          S.plans.find(x=>x.id==='my').acts.push({name:'Call supplier',status:'todo',detail:''});save()}""")
        await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(500)
        print('main folders:',[x.replace('\n',' / ') for x in await pg.locator('.fold2.big').all_inner_texts()])
        print('by type:',[x.replace('\n',' ').replace('···','').strip() for x in await pg.locator('.dsplit .drow').all_inner_texts()])
        print('all folders',await pg.locator('#deskbody .fold2').count(),'| recent files',await pg.locator('.dfile').count(),'| glance:',(await pg.locator('.dring').inner_text()).replace('\n',' ')[:120])
        await pg.screenshot(path='dk1.png',full_page=True)
        await pg.fill('#dq','solar'); await pg.wait_for_timeout(150); print('search "solar": folders',await pg.locator('#deskbody .fold2').count(),'files',await pg.locator('.dfile').count(),'| box still focused',await pg.evaluate("document.activeElement.id"))
        await pg.fill('#dq',''); await pg.click('.dsplit .drow:has-text("Presentations")'); await pg.wait_for_timeout(150); print('Presentations filter:',await pg.locator('.dfile').all_inner_texts())
        await pg.click('.dfile >> nth=0'); await pg.wait_for_timeout(300); print('opened file ->',await pg.evaluate("V.view+' doc='+V.doc"),'deck viewer',await pg.locator('.deck').count())
        await pg.go_back(); await pg.wait_for_timeout(300); await pg.click('[data-act=dmode][data-v=list]'); print('list mode rows',await pg.locator('#deskbody .drow').count())
        await pg.click('.fold2.big:has-text("Rules and skills")'); print('main folder ->',await pg.evaluate('V.view'))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(300)
        print('phone: 7 tabs, overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| tab widths',await pg.evaluate("[...document.querySelectorAll('nav button[data-v]')].filter(b=>b.offsetWidth).map(b=>b.offsetWidth)"),'| errors',errs)
        await pg.screenshot(path='dk2.png')
        await b.close()
asyncio.run(main())
