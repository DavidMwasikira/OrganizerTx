import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def handle(r): await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        cx=await b.new_context(viewport={'width':1300,'height':800},permissions=['clipboard-read','clipboard-write']); pg=await cx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("""const st=['done','done','doing','blocked','todo','todo','todo','todo'];const acts=[['Verify land and survey plot',1,2],['Commission architectural and structural drawings',2,4],['Prepare BQ and select builder',6,3],['Submit county building plan',6,6],['NEMA approval',8,4],['Foundation',12,4],['Walling and roof',16,6],['Finishes and handover',22,5]].map(([n,s,w],i)=>({id:uid(),name:n,start:s,weeks:w,status:st[i],phase:i<3?'Preparation':i<5?'Approvals':'Construction',deps:[]}));acts.forEach((a,i)=>{if(i)a.deps=[acts[i-1].id]});acts[4].deps=[acts[2].id];
          S.plans.push({id:'pb',name:'Three bedroom house',what:'Construction of a three bedroom house in Eldoret with a kitchen, bathroom, study room, store, car park, back yard garden',custom:true,active:true,started:Date.now()-20*DAY,weeks:26,summary:'s',log:[],phases:['Preparation','Approvals','Construction'],miles:[{id:'m1',name:'Permit',date:dash(Date.now()+50*DAY),done:false}],acts});
          S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};S.wsHidden=true;V.view='plan';V.plan='pb';V.ptab='gadv';save();render()""")
        await pg.wait_for_timeout(400)
        import base64
        async def grab(name):
            d=await pg.evaluate("(async()=>{const it=await navigator.clipboard.read();const t=it[0].types;const b=await it[0].getType('image/png');const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i+=8192)s+=String.fromCharCode(...a.subarray(i,i+8192));const im=await createImageBitmap(b);return {types:t,w:im.width,h:im.height,b64:btoa(s)}})()")
            open(name,'wb').write(base64.b64decode(d['b64'])); return d['types'],d['w'],d['h']
        for tab,name in [('gsimple','c-simple.png'),('gadv','c-adv.png'),('wbs','c-wbs.png')]:
            await pg.click(f'.ptabs [data-v={tab}]'); await pg.wait_for_timeout(300)
            await pg.click('[data-act=pv-copy]'); st=[]
            for k in range(12):
                st.append(await pg.evaluate("document.querySelector('[data-act=pv-copy]').className.replace('btn small icon cpy','').trim()||'idle'")); await pg.wait_for_timeout(300)
            print(tab,'button states:',st,'| toast',await pg.locator('.toast').last.inner_text() if await pg.locator('.toast').count() else '-','| clipboard',await grab(name),'| on-screen chart',await pg.evaluate("(r=>[Math.round(r.width),Math.round(r.height)])(document.querySelector('.pviews').getBoundingClientRect())"),'| shot class left',await pg.locator('.shot').count())
        await pg.evaluate("document.documentElement.dataset.theme='dark'"); await pg.click('.ptabs [data-v=gadv]'); await pg.wait_for_timeout(300); await pg.click('[data-act=pv-copy]'); await pg.wait_for_timeout(1500); print('dark',await grab('c-dark.png'),'| errors',errs)
        await b.close()
asyncio.run(main())
