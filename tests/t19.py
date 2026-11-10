import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
REV=REPORT.replace('- Point two.','- Point two.\n- Solar pumps suit this yield.').replace('===TAKEAWAYS===','## What changed in this revision\n- Added solar pump finding.\n- Removed diesel option.\n\n===TAKEAWAYS===')
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1420,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); u=body['messages'][0]['content']; calls.append(body)
            t=REV if 'Rewrite the document so that it reflects' in u else REPORT if 'Research this' in u else 'Yes, a solar pump suits it.' if 'reading this document' in body['system'] else '[]'
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':t}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        # --- rules and skills ---
        await pg.click('nav [data-v=rules]'); await pg.wait_for_timeout(200)
        print('files:',[x.strip() for x in await pg.locator('.kbside .it').all_inner_texts()])
        await pg.screenshot(path='r1.png')
        await pg.fill('#libtext',(await pg.input_value('#libtext'))+'\n- Always include a section called Engineering notes.\n'); print('live preview shows edit:', 'Engineering notes' in await pg.locator('#libprev').inner_text())
        await pg.click('[data-act=lib-save]'); await pg.click('.kbside .it >> nth=3'); await pg.uncheck('#libon'); await pg.wait_for_timeout(100)
        await pg.click('[data-act=lib-new][data-v=r]'); await pg.fill('#libtext','# My house rule\n\n## Do\n- Mention the county.\n'); await pg.click('[data-act=lib-save]')
        await pg.click('.kbside .it:has-text("Feasibility")'); await pg.wait_for_timeout(150); print('skill view:',await pg.locator('.kbhead .crumb').inner_text(),'|',(await pg.locator('.kbhead p').first.inner_text())[:60])
        await pg.screenshot(path='r2.png')
        await pg.click('nav [data-v=home]'); print('skill menu:',await pg.locator('#skill option').all_inner_texts())
        await pg.select_option('#skill',label='Feasibility study'); await pg.fill('#ask','borehole pump'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1500)
        u=[c for c in calls if 'Research this' in c['messages'][0]['content']][0]['messages'][0]['content']
        print('research prompt: edited rule',('Engineering notes' in u),'| new rule',('Mention the county' in u),'| switched-off rule left out',('Draw a flow chart whenever' not in u),'| skill',('Build a simple break-even' in u),'| front matter stripped',('description: Tests whether' not in u))
        # --- document follow-ups and Save ---
        await pg.click('[data-act=open-doc] >> nth=0'); await pg.wait_for_timeout(300)
        print('doc bottom: ask box',await pg.locator('#docask').count(),'| save button:',await pg.locator('[data-act=doc-save]').inner_text())
        await pg.click('[data-act=doc-save]'); await pg.wait_for_timeout(200); print('save with nothing new:',await pg.locator('.toast').inner_text())
        await pg.fill('#docask','Would a solar pump work?'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(1000)
        print('answer:',await pg.locator('.doctalk .msg.ai').last.inner_text(),'| button now:',await pg.locator('[data-act=doc-save]').inner_text())
        await pg.screenshot(path='r3.png',full_page=False)
        await pg.click('[data-act=doc-save]'); await pg.wait_for_timeout(1300)
        ip=[c for c in calls if 'Rewrite the document so that it reflects' in c['messages'][0]['content']][0]['messages'][0]['content']
        print('integration prompt has discussion',('QUESTION: Would a solar pump work?' in ip),'+ rules',('<rules>' in ip),'| doc now rev',await pg.evaluate("topic().docs[0].rev"),'| new text in doc',('Solar pumps suit this yield' in await pg.locator('.sheet').inner_text()),'| title block:',(await pg.locator('.titleblock').inner_text()).replace('\n',' ')[-40:])
        print('after save:',(await pg.locator('.doctalk').inner_text()).replace('\n',' | ')[150:330])
        await pg.click('[data-act=doc-restore]'); await pg.click('.modal [data-x="1"]'); await pg.wait_for_timeout(200); print('restored rev',await pg.evaluate("topic().docs[0].rev"),'| pending again',await pg.evaluate("docPending(topic().docs[0])"))
        # --- files on disk, both directions ---
        await pg.evaluate("(async()=>{DISK.root=await navigator.storage.getDirectory();DISK.ok=true;await syncDisk(true)})()")
        ls=await pg.evaluate("""(async()=>{const out=[];async function walk(d,pre){for await(const [n,h] of d.entries()){if(n==='projects')continue;if(h.kind==='directory')await walk(h,pre+n+'/');else out.push(pre+n)}}await walk(DISK.root,'');return out.sort()})()""")
        print('disk error',repr(await pg.evaluate('DISK.err'))); [print('   ',x) for x in ls]
        await pg.wait_for_timeout(1700)
        await pg.evaluate("""(async()=>{const r=await DISK.root.getDirectoryHandle('rules');await writeFile(r,'02-formatting-and-style.md','# Formatting and style\\n\\n## Do\\n- Edited in Notepad.\\n');await writeFile(r,'09-added-by-hand.md','# Added by hand\\n\\n## Do\\n- Works.\\n');await syncDisk()})()""")
        print('edited on disk -> app:',await pg.evaluate("S.rules.find(r=>r.file==='02-formatting-and-style.md').text.includes('Edited in Notepad')"),'| file added by hand -> app:',await pg.evaluate("S.rules.some(r=>r.file==='09-added-by-hand.md')"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('nav [data-v=rules]'); await pg.wait_for_timeout(200)
        print('phone: 6 tabs fit, overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs); await pg.screenshot(path='r4.png')
        await b.close()
asyncio.run(main())
