import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
SETUP=open('t21.py').read().split('await pg.evaluate("""')[1].split('""")')[0]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1690,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate(SETUP); await pg.evaluate("S.topics[0].docs[0].md+='x'.repeat(400000);S.brain.organized='## A\\n- note one here\\n'.repeat(300);save()")
        await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(700)
        m=await pg.evaluate("(()=>{const m=memoryUse();return {total:m.total,sum:m.rows.reduce((a,r)=>a+r[2],0),rows:m.rows.map(r=>[r[0],fmtSize(r[2])])}})()")
        print('parts add up to the total:',m['sum']==m['total'],'| total',m['total'],'bytes'); [print('   ',r) for r in m['rows']]
        print('device line:',await pg.locator('#deskstore').inner_text())
        await pg.screenshot(path='mem.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await b.close()
asyncio.run(main())
