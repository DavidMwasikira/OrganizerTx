import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
SETUP=open('t21.py').read().split('await pg.evaluate("""')[1].split('""")')[0]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1690,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'An answer.'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate(SETUP); nav=(await pg.locator('nav').bounding_box()); edge=nav['x']+nav['width']
        for v,sel in [('home','.page'),('tasks','.page'),('actions','.page'),('brain','.page'),('rules','.page'),('settings','.page'),('help','.page')]:
            await pg.click(f'[data-act=nav][data-v={v}] >> visible=true'); await pg.wait_for_timeout(250); bx=await pg.locator(sel).first.bounding_box()
            print(f'{v:9s} starts at the sidebar: {round(bx["x"])==round(edge)} | width {round(bx["width"])} of {round(1690-edge)}')
        await pg.screenshot(path='f0.png')
        await pg.click('nav [data-v=topics]'); await pg.wait_for_timeout(250)
        sb=await pg.locator('.wsside').bounding_box(); cb=await pg.locator('.wscol').bounding_box()
        print('Folders: list at sidebar',round(sb['x'])==round(edge),'| list width',round(sb['width']),'| right pane from',round(cb['x']),'width',round(cb['width']),'| right says:',await pg.locator('.wscol h2').inner_text())
        print('groups:',[x.replace('\n',' ') for x in await pg.locator('.wsside .g').all_inner_texts()])
        await pg.screenshot(path='f1.png')
        await pg.click('.wsside .it:has-text("Factory Solar")'); await pg.wait_for_timeout(250); print('clicked a conversation -> right pane:',await pg.locator('.wscol .thead h1').inner_text(),'| list still shown',await pg.locator('.wsside').is_visible(),'| highlighted',await pg.locator('.wsside .it[aria-current=true] .n').inner_text())
        await pg.screenshot(path='f2.png')
        await pg.fill('#chat','hello'); await pg.click('[data-act=send]'); await pg.wait_for_timeout(900); print('chat works in the pane:',(await pg.locator('.msg.ai').last.inner_text()).split('\n')[0])
        await pg.click('.wsside .it:has-text("Borehole for the farm")'); await pg.wait_for_timeout(250); print('clicked a project -> right pane:',await pg.locator('.wscol .thead h1').inner_text(),'| gantt',await pg.locator('.gantt').count(),'| Folders tab highlighted',await pg.locator('nav [data-v=topics][aria-current=page]').count())
        await pg.click('.wsside .it:has-text("Best AI stack")'); await pg.wait_for_timeout(600); print('guide in pane:',await pg.locator('.wscol .thead h1').inner_text())
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('nav [data-v=topics]'); await pg.wait_for_timeout(250)
        print('phone Folders: list shown',await pg.locator('.wsside').is_visible(),'| right pane hidden',not await pg.locator('.wscol').is_visible(),'| overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
        await pg.click('.wsside .it >> nth=1'); await pg.wait_for_timeout(250); print('phone: tapped -> chat full screen',await pg.locator('.wscol').is_visible(),'list hidden',not await pg.locator('.wsside').is_visible(),'| errors',errs)
        await b.close()
asyncio.run(main())
