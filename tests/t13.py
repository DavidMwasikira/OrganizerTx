import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
async def run(b,url,label):
    pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
    await pg.goto(url); await pg.wait_for_timeout(1500)
    await pg.fill('#name','D'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
    await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
    v=lambda: pg.evaluate("V.view+(V.doc?'+doc':'')+(V.view==='topic'?':'+V.tab:'')")
    print(label,'| home has Back:',await pg.locator('[data-act=back]').count(),end=' | ')
    await pg.click('nav [data-v=tasks]'); await pg.click('nav [data-v=topics]'); print('on',await v(),'Back shown',await pg.locator('[data-act=back]').count(),end=' | ')
    await pg.click('[data-act=back]'); await pg.wait_for_timeout(200); a=await v(); await pg.click('[data-act=back]'); await pg.wait_for_timeout(200); print('Back ->',a,'-> Back ->',await v())
    await pg.click('nav [data-v=topics]'); await pg.click('[data-act=open-topic] >> nth=0'); await pg.click('[data-act=open-doc] >> nth=0'); await pg.wait_for_timeout(200); seq=[await v()]
    await pg.click('[data-act=close-doc]'); await pg.wait_for_timeout(200); seq.append(await v())
    await pg.go_back(); await pg.wait_for_timeout(300); seq.append(await v()); await pg.go_back(); await pg.wait_for_timeout(300); seq.append(await v())
    print('   doc Back, then browser Back twice:',' -> '.join(seq),'| errors',errs)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        await run(b,'http://localhost:8765/index.html','WEB ')
        await run(b,'file:///home/claude/organizertx/index.html','FILE')
        await b.close()
asyncio.run(main())
