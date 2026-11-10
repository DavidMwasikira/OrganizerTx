import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1360,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            u=json.loads(route.request.post_data)['messages'][0]['content']
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':REPORT if 'Research this' in u else UPDATE if 'You are following' in u else '[]'}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        await pg.fill('#ask','How do I size a borehole pump?'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act=follow][data-v="168"]'); await pg.click('[data-act=update-now]'); await pg.wait_for_timeout(1200)
        await pg.evaluate("S.plans.find(x=>x.id==='my').acts.push({name:'Call supplier',status:'todo',due:'',detail:''});S.plans.push({id:'a1',guide:null,custom:true,name:'Borehole for the farm',what:'',active:true,started:Date.now(),created:Date.now(),weeks:0,summary:'',acts:[{name:'Survey',status:'todo'}]})")
        # leave behind what v0.8 would have written: long folder and file names
        await pg.evaluate("""(async()=>{DISK.root=await navigator.storage.getDirectory();DISK.ok=true;const pr=await DISK.root.getDirectoryHandle('projects',{create:true});
          for(const t of S.topics){t.dir=t.code+'_'+fsName(t.title);const d=await pr.getDirectoryHandle(t.dir,{create:true});await writeFile(d,'old-long-name-report_'+fsName(t.title)+'.html','old')}
          const ap=await pr.getDirectoryHandle('_action-plans',{create:true});await writeFile(ap,'borehole-for-the-farm.md','old')})()""")
        walk="""(async()=>{const out=[];async function walk(d,pre){for await(const [n,h] of d.entries()){if(h.kind==='directory'){out.push(pre+n+'/');await walk(h,pre+n+'/')}else out.push(pre+n)}}await walk(DISK.root,'');return out.sort()})()"""
        print('BEFORE (v0.8 names):'); [print('   ',x) for x in await pg.evaluate(walk)]
        await pg.evaluate("syncDisk()"); await pg.wait_for_timeout(500)
        print('AFTER (v0.9):  error',repr(await pg.evaluate('DISK.err'))); [print('   ',x) for x in await pg.evaluate(walk)]
        print('errors',errs)
        await b.close()
asyncio.run(main())
