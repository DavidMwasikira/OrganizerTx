import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
R2=REPORT.replace('## Findings','## How it works\n```mermaid\nflowchart TD\n  A["Borehole"] --> B["Pump"]\n  B --> C["Tank"]\n```\nThe chart shows the flow.\n\n## Findings')
PLAN={"summary":"Start small.","activities":[{"name":f"Step {i}","detail":"Do it.","start":i,"weeks":2,"cost":""} for i in range(1,9)]}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        ctx=await b.new_context(viewport={'width':1360,'height':1000}); pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            u=json.loads(route.request.post_data)['messages'][0]['content']
            t=R2 if 'Research this' in u else UPDATE if 'You are following' in u else json.dumps(PLAN) if 'activity plan' in u else 'A chat answer.' if len(u)<60 else '[]'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,content_type='application/javascript',path='node_modules/mermaid/dist/mermaid.min.js'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        await pg.fill('#ask','How do I size a borehole pump?'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1500)
        await pg.click('[data-act=follow][data-v="168"]'); await pg.click('[data-act=update-now]'); await pg.wait_for_timeout(1200)
        await pg.fill('#chat','And solar?'); await pg.click('[data-act=send]'); await pg.wait_for_timeout(1000)
        await pg.click('nav .create'); await pg.click('[data-x=project]'); await pg.fill('#pname','Borehole for the farm'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(1500)
        await pg.evaluate("""(()=>{const p=S.plans.find(x=>x.name.startsWith('Borehole'));p.acts[0].status='done';p.acts[0].closed=Date.now();p.acts[1].status='done';p.acts[1].closed=Date.now();p.acts[2].status='doing';p.acts[3].status='blocked';
          const my=S.plans.find(x=>x.id==='my');const d=n=>dash(Date.now()+n*864e5);my.acts.push({name:'Call the pump supplier',status:'todo',due:d(-1),detail:''},{name:'Review tender documents',status:'doing',due:d(0),detail:''},{name:'Send quotation',status:'todo',due:d(3),detail:''});
          S.topics[0].docs[0].date-=3*864e5;save()})()""")
        await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(300)
        print('kpis:',[x.replace('\n',' ') for x in await pg.locator('.kpi').all_inner_texts()])
        print('hero',await pg.locator('.hero').inner_text(),'| legend',(await pg.locator('.legend').inner_text()).replace('\n',' '),'| deadlines',await pg.locator('.panel .trow').count(),'| bars',await pg.locator('.cols i').count())
        await pg.screenshot(path='dash1.png',full_page=True)
        await pg.click('nav [data-act=theme]'); await pg.wait_for_timeout(200); await pg.screenshot(path='dash2.png'); await pg.click('nav [data-act=theme]')
        # --- disk saving, using the browser's private file system as a stand-in for the chosen folder ---
        await pg.evaluate("(async()=>{DISK.root=await navigator.storage.getDirectory();DISK.ok=true;await syncDisk(true)})()")
        tree=await pg.evaluate("""(async()=>{const out=[];async function walk(d,pre){for await(const [n,h] of d.entries()){if(h.kind==='directory'){out.push(pre+n+'/');await walk(h,pre+n+'/')}else{const f=await h.getFile();out.push(pre+n+'  ('+f.size+' bytes)')}}}await walk(DISK.root,'');return out.sort()})()""")
        print('disk error:',repr(await pg.evaluate('DISK.err'))); [print('   ',x) for x in tree]
        print('html doc has inline diagram:',await pg.evaluate("""(async()=>{const pr=await DISK.root.getDirectoryHandle('projects');for await(const [n,h] of pr.entries()){if(n.startsWith('P0')){for await(const [fn,fh] of h.entries()){if(fn.endsWith('report_borehole-pump-sizing-basics.html')){const t=await (await fh.getFile()).text();return t.includes('<svg')&&t.includes('Reference')}}}}return 'not found'})()"""))
        n0=len(tree); await pg.click('nav [data-v=tasks]'); await pg.click('[data-act=task-new] >> nth=0'); await pg.fill('#tname','New one'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(3500)
        print('auto-save after a change: last saved set',await pg.evaluate('DISK.last>0'),'| plans file has new task',await pg.evaluate("""(async()=>{const d=await (await DISK.root.getDirectoryHandle('projects')).getDirectoryHandle('_action-plans');return (await (await (await d.getFileHandle('my-tasks.md')).getFile()).text()).includes('New one')})()"""))
        await pg.click('nav [data-v=topics]'); await pg.wait_for_timeout(300); print('folders page line:',await pg.locator('.item .mono').nth(2).inner_text())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('nav [data-v=actions]'); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs); await pg.screenshot(path='dash3.png',full_page=True)
        f=await ctx.new_page(); await f.goto('file:///home/claude/organizertx/index.html'); await f.wait_for_timeout(800)
        print('opened as a file: secure context',await f.evaluate('isSecureContext'),'| folder picker available',await f.evaluate("typeof showDirectoryPicker"))
        await b.close()
asyncio.run(main())
