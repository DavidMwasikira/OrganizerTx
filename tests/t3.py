import json, asyncio, base64
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
REPORT='''# Electricity tariffs for a small workshop

## Summary
- Point one, Kshs 20 (USD 0.15) per unit.
- Point two.

## How billing works
```mermaid
flowchart TD
  A["Meter reading"] --> B["Energy charge"]
  B --> C{"Above 100 units?"}
  C -->|Yes| D["Higher band"]
  C -->|No| E["Lifeline band"]
```
The chart shows how a bill is built up.

[[IMAGE: electricity meter Kenya | A prepaid electricity meter]]
The photo shows a typical meter.

| Band | Rate |
|---|---|
| Low | Kshs 12 |

```mermaid
flowchart TD
  A[broken --> 
```

## Recommended next steps
1. Check your band.

===TAKEAWAYS===
- Tariffs are banded.
'''
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
calls=[];commons=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':390,'height':800})).new_page()
        errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); calls.append(body)
            u=body['messages'][0]['content']
            r=sse([{'type':'text','text':REPORT}]) if 'Research this' in u else sse([{'type':'text','text':'## Profile\\nx'}])
            await route.fulfill(status=200,content_type='text/event-stream',body=r)
        async def cm(route):
            commons.append(route.request.url)
            await route.fulfill(status=200,content_type='application/json',headers={'access-control-allow-origin':'*'},body=json.dumps({'query':{'pages':{'1':{'index':2,'title':'File:x.svg'},'2':{'index':1,'title':'File:Meter.jpg','imageinfo':[{'thumburl':'https://upload.wikimedia.org/meter.jpg','descriptionurl':'https://commons.wikimedia.org/wiki/File:Meter.jpg','extmetadata':{'Artist':{'value':'<a href="x">Jane Doe</a>'},'LicenseShortName':{'value':'CC BY-SA 4.0'}}}]}}}}))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.route('https://commons.wikimedia.org/**',cm)
        await pg.route('https://upload.wikimedia.org/**',lambda r:r.fulfill(status=200,content_type='image/png',body=PNG))
        await pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,content_type='application/javascript',path='node_modules/mermaid/dist/mermaid.min.js'))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#key','sk-test'); await pg.click('text=Start'); await pg.wait_for_timeout(200)
        print('blocked without country:',await pg.locator('.toast').inner_text())
        await pg.fill('#country','kenya')
        await pg.fill('#town','Eldoret'); await pg.click('[data-act=plevel][data-v=eli10]')
        await pg.screenshot(path='s1.png',full_page=True)
        await pg.click('text=Start'); await pg.wait_for_timeout(300)
        await pg.fill('#ask','electricity tariffs'); await pg.select_option('#level','expert'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(4000)
        sysp=calls[0]['system']; up=calls[0]['messages'][0]['content']
        print('locale:',[l for l in sysp.split('\n') if 'lives in' in l][0][:330])
        print('level:',[l for l in up.split('\n') if 'Reading level' in l][0][:90]); print('visual rule present:', 'mermaid' in up and '[[IMAGE:' in up)
        print('card svg',await pg.locator('.doccard figure.mm svg').count())
        await pg.click('[data-act=open-doc] >> nth=0'); await pg.wait_for_timeout(1500)
        print('doc: svgs',await pg.locator('.sheet figure.mm svg').count(),'| foreignObject',await pg.locator('.sheet foreignObject').count(),'| broken note',await pg.locator('.sheet figure.mm .mmph').count(),'| photo',await pg.locator('.sheet figure.ph img').count(), '|', await pg.locator('.sheet figure.ph figcaption').inner_text())
        print('commons url',commons[0][:150])
        await pg.screenshot(path='s2.png',full_page=True)
        html=await pg.evaluate('(async()=>{const t=S.topics[0];return await docHtml(t,t.docs[0])})()')
        print('export: png diagrams',html.count('data:image/png'),'| photo',html.count('upload.wikimedia.org'),'| size',len(html))
        open('export.html','w').write(html)
        print('errors',errs)
        await b.close()
asyncio.run(main())
