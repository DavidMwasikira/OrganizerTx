import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
        ctx=await b.new_context(viewport={'width':390,'height':800},permissions=['microphone']); pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("""()=>{const now=Date.now();S.weekly={kind:'ai',date:now,items:[{name:'x',what:'y',why:'z'}]};S.plans.push({id:'a1',guide:null,custom:true,name:'Borehole for the farm',what:'Water for irrigation',active:true,started:now,created:now,weeks:4,summary:'',acts:[{name:'Hydrogeological survey',status:'done',start:1,weeks:1},{name:'Drilling',status:'doing',start:2,weeks:2}]});save();V.view='plan';V.plan='a1';render()}""")
        await pg.wait_for_timeout(300)
        print('capture buttons:',[x.strip() for x in await pg.locator('.capbar .capbtn').all_inner_texts()])
        # photo
        await pg.click('.capbtn.cam'); await pg.wait_for_timeout(200)
        print('camera input: accept',await pg.get_attribute('#capcam','accept'),'capture',await pg.get_attribute('#capcam','capture'))
        await pg.screenshot(path='c1.png')
        await pg.set_input_files('#capcam','site1.jpg'); await pg.wait_for_timeout(700); await pg.set_input_files('#capgal',['site2.jpg']); await pg.wait_for_timeout(700)
        print('previews',await pg.locator('#capprev img').count()); await pg.select_option('#captask',label='Drilling'); await pg.fill('#captext','Rig on site, casing delivered'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(900)
        info=await pg.evaluate("(async()=>{const l=S.plans.find(p=>p.id==='a1').log;const b=await blobGet(l[0].id);return [l.length,l[0].w,l[0].h,l[0].size,b&&b.type,l[0].thumb.length,l[0].task]})()")
        print('photos saved: count,w,h,bytes,type,thumb chars,task =',info)
        # voice
        await pg.click('.capbar .capbtn:has-text("Voice note")'); await pg.wait_for_timeout(200); await pg.click('#recbtn'); await pg.wait_for_timeout(1800)
        print('recording state:',(await pg.locator('#recstate').inner_text())[:40]); await pg.click('#recbtn'); await pg.wait_for_timeout(500)
        print('after stop:',(await pg.locator('#recstate').inner_text())[:34],'| player shown',await pg.locator('#recplay').is_visible())
        await pg.fill('#captext','Order two more lengths of casing. Call the supplier before Friday.'); await pg.check('#capmk'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(700)
        print('voice saved:',await pg.evaluate("(async()=>{const p=S.plans.find(p=>p.id==='a1'),e=p.log.find(x=>x.kind==='voice');const b=await blobGet(e.id);return [e.dur,e.size>0,b&&b.type,p.acts[p.acts.length-1].name]})()"))
        # web note
        await pg.click('.capbar .capbtn:has-text("Web page note")'); await pg.fill('#capurl','wra.go.ke/permits'); await pg.fill('#captitle','WRA permit fees'); await pg.fill('#capquote','Category B permits apply to irrigation.'); await pg.fill('#captext','Check which category our abstraction falls in.'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(400)
        await pg.click('.capbar .capbtn:has-text("Text note")'); await pg.fill('#captext','Water struck at 85 m.'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(400)
        print('log rows:',[x.replace('\n',' | ')[:110] for x in await pg.locator('.logrow').all_inner_texts()])
        await pg.locator('.card:has(.capbar)').scroll_into_view_if_needed(); await pg.screenshot(path='c2.png')
        await pg.click('.logph button >> nth=0'); await pg.wait_for_timeout(500); print('photo opens full size:',await pg.evaluate("document.querySelector('.modal img').naturalWidth"),'px wide'); await pg.fill('.modal #captext','Edited comment'); await pg.click('.modal [data-x=save]'); await pg.wait_for_timeout(200)
        await pg.click('.logrow:has-text("WRA permit fees")'); await pg.wait_for_timeout(200); print('web note edit keeps url:',await pg.input_value('#capurl')); await pg.click('.modal [data-x=cancel]')
        # disk + memory + desktop
        await pg.evaluate("(async()=>{DISK.root=await navigator.storage.getDirectory();DISK.ok=true;await syncDisk(true)})()")
        ls=await pg.evaluate("""(async()=>{const out=[];async function walk(d,pre){for await(const [n,h] of d.entries()){if(h.kind==='directory')await walk(h,pre+n+'/');else if(pre.includes('field-log'))out.push(pre+n+' ('+(await h.getFile()).size+' B)')}}await walk(DISK.root,'');return out.sort()})()""")
        print('disk error',repr(await pg.evaluate('DISK.err'))); [print('   ',x) for x in ls]
        print('memory row:',await pg.evaluate("memoryUse().rows.filter(r=>r[0].startsWith('Photos')).map(r=>[r[0],fmtSize(r[2]),r[3]])"),'| desktop field captures',await pg.evaluate("deskFiles().filter(f=>f.kind==='field').length"))
        await pg.click('.logph button >> nth=1'); await pg.wait_for_timeout(300); await pg.click('.modal [data-x=del]'); await pg.wait_for_timeout(300); print('after delete: photos',await pg.locator('.logph button').count(),'| blob removed',await pg.evaluate("(async()=>{const keys=await new Promise(ok=>{const r=store.db.transaction('kv').objectStore('kv').getAllKeys();r.onsuccess=()=>ok(r.result)});return keys.filter(k=>String(k).startsWith('blob:')).length})()"),'left')
        await pg.wait_for_timeout(400); await pg.reload(); await pg.wait_for_timeout(1500); print('after reload: entries',await pg.evaluate("S.plans.find(p=>p.id==='a1').log.length"),'| photo still loads',await pg.evaluate("(async()=>{const e=S.plans.find(p=>p.id==='a1').log.find(x=>x.kind==='photo');const b=await blobGet(e.id);return !!b&&b.size>1000})()"),'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await b.close()
asyncio.run(main())
