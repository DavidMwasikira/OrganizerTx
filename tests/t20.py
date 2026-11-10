import json, asyncio, base64
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
it=lambda *a:[{"head":h,"text":t} for h,t in a]
S=[
 {"layout":"title","tone":"dark","title":"SolarCold Market Rooms","text":"Sample deck: cold storage that traders rent by the crate."},
 {"layout":"panel","tone":"dark","title":"Company overview","text":"Sample text. We build and run solar cold rooms at open-air markets, rented to traders by the crate per day.","image":"market traders vegetables"},
 {"layout":"text","tone":"dark","title":"The problem","text":"Sample text. Traders lose a share of fresh produce to heat before it sells.","bullets":["No affordable cold storage at markets","Losses cut income every week"],"image":"vegetable market stall","source":"Sample source"},
 {"layout":"steps","tone":"dark","title":"Our solution","items":it(("Store","Traders leave crates overnight"),("Cool","Solar keeps produce fresh"),("Sell","Produce sells at full price"))},
 {"layout":"steps","tone":"light","title":"How it works","items":it(("Register","Trader signs up"),("Drop","Crates are tagged"),("Pay","Daily fee by mobile money"),("Collect","Crates returned"),("Repeat","Weekly plans"))},
 {"layout":"stats","tone":"dark","title":"Market opportunity","text":"Sample figures only.","items":it(("Kshs 0.0bn","Market size (sample)"),("00%","Yearly growth (sample)"),("0,000","Traders within reach (sample)")),"source":"Sample source"},
 {"layout":"text","tone":"dark","title":"Target customer","text":"Sample text. Fresh produce traders at large municipal markets.","image":"woman selling fruit market"},
 {"layout":"grid","tone":"dark","title":"Business model canvas","items":it(("Key partners","County, solar suppliers"),("Key activities","Run cold rooms"),("Key resources","Units, staff"),("Value proposition","Less waste, more income"),("Customer relationships","Daily contact"),("Channels","Market agents"),("Customer segments","Produce traders"),("Cost structure","Units, staff, rent"),("Revenue streams","Crate fees"))},
 {"layout":"steps","tone":"light","title":"Revenue model","items":it(("Who pays","Traders"),("For what","Crate per day"),("How","Mobile money"),("How often","Daily or weekly"))},
 {"layout":"table","tone":"dark","title":"Pricing","table":{"head":["Plan","Price","Includes"],"rows":[["Daily","Kshs 00 (USD 0.0)","One crate, one night"],["Weekly","Kshs 000 (USD 0.0)","One crate, seven nights"],["Bulk","Kshs 0,000 (USD 00)","Ten crates, monthly"]]}},
 {"layout":"table","tone":"dark","title":"Competitive landscape","table":{"head":["Competitor","Price","Strength","Weakness"],"rows":[["Sample A","Higher","Large units","Far from markets"],["Sample B","Similar","Known brand","Needs grid power"],["Ice sellers","Low","Everywhere","Short-lived"]]}},
 {"layout":"panel","tone":"dark","title":"Our advantage","bullets":["At the market, not across town","Runs without grid power","Pay per crate, no contract"]},
 {"layout":"text","tone":"light","title":"Go-to-market","text":"Sample text. Start with one market and trader groups.","bullets":["Month 1: pilot unit","Month 2: agents recruited","Month 3: second market"]},
 {"layout":"stats","tone":"dark","title":"Traction so far","items":it(("0","Pilot units (sample)"),("00","Traders signed (sample)"),("0","Letters of intent (sample)"))},
 {"layout":"steps","tone":"dark","title":"Roadmap","items":it(("Q1 2027","Pilot"),("Q2 2027","Two markets"),("Q4 2027","Five markets"),("2028","Second county"))},
 {"layout":"grid","tone":"dark","title":"Team","items":it(("Founder","Engineering and operations"),("Operations lead","Market relations"),("Finance","Accounts and reporting"),("Advisers","Cold chain and county affairs"))},
 {"layout":"table","tone":"light","title":"Financial projections","text":"Estimates.","table":{"head":["","Year 1","Year 2","Year 3"],"rows":[["Revenue","0","0","0"],["Costs","0","0","0"],["Profit","0","0","0"]]}},
 {"layout":"table","tone":"dark","title":"Funding and use","table":{"head":["Use","Amount","Share"],"rows":[["Cold room units","0","60%"],["Working capital","0","25%"],["Launch and training","0","15%"]]}},
 {"layout":"grid","tone":"dark","title":"Risks","items":it(("Low uptake","Free trial week"),("Theft","Tagged crates, guard"),("Breakdown","Service contract"),("Permits","Early county agreement"),("Weather","Battery reserve"))},
 {"layout":"close","tone":"dark","title":"Next steps","text":"Sample ask: funding for five units.","bullets":["Decision wanted this quarter","Contact: name, phone, email"]},
]
for i,x in enumerate(S): x.setdefault("notes","Sample speaker note for slide %d."%(i+1))
DECK={"title":"SolarCold Market Rooms","subtitle":"Sample deck: cold storage that traders rent by the crate.","slides":S}
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1420,'height':900},accept_downloads=True); pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        async def api(route):
            body=json.loads(route.request.post_data); u=body['messages'][0]['content']; calls.append(body)
            await route.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'Here is the deck:\n```json\n'+json.dumps(DECK)+'\n```' if 'pitch presentation' in u else '[]'}]))
        await pg.route('https://api.anthropic.com/**',api)
        await pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=200,content_type='application/javascript',path='node_modules/pptxgenjs/dist/pptxgen.bundle.js'))
        await pg.route('https://commons.wikimedia.org/**',lambda r:r.fulfill(status=200,content_type='application/json',headers={'access-control-allow-origin':'*'},body=json.dumps({'query':{'pages':{'2':{'index':1,'title':'File:M.png','imageinfo':[{'thumburl':'https://upload.wikimedia.org/m.png','descriptionurl':'https://commons.wikimedia.org/wiki/File:M.png','extmetadata':{'Artist':{'value':'Jane Doe'},'LicenseShortName':{'value':'CC BY-SA 4.0'}}}]}}}})))
        await pg.route('https://upload.wikimedia.org/**',lambda r:r.fulfill(status=200,content_type='image/png',headers={'access-control-allow-origin':'*'},body=PNG))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        print('skills on Home:',await pg.locator('#skill option').all_inner_texts())
        await pg.select_option('#skill',label='Business idea presentation'); await pg.fill('#ask','Solar cold rooms for market traders'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1800)
        u=calls[0]['messages'][0]['content']; print('prompt has skill slide list',('Business model canvas' in u),'and JSON shape',('"layout"' in u),'| max',calls[0]['max_tokens'])
        print('chat card:',(await pg.locator('.doccard').inner_text()).replace('\n',' | ')[:230])
        await pg.click('[data-act=open-doc]'); await pg.wait_for_timeout(600)
        print('viewer: thumbnails',await pg.locator('.thumbs button').count(),'| stage title:',await pg.locator('.stage .sl h1').inner_text())
        await pg.screenshot(path='p0.png')
        for i,name in [(1,'p1'),(7,'p7'),(10,'p10')]:
            await pg.click(f'.thumbs button >> nth={i}'); await pg.wait_for_timeout(350); await pg.locator('.stage .sl').screenshot(path=name+'.png')
        await pg.keyboard.press('ArrowRight'); print('arrow key ->',await pg.evaluate('V.slide'),'| photo credit on slide 2:',await pg.evaluate("(document.querySelector('.thumbs button:nth-child(2) small')||{}).textContent"))
        async with pg.expect_download() as dl: await pg.click('[data-act=deck-dl]')
        d=await dl.value; await d.save_as('deck.pptx'); print('downloaded',d.suggested_filename)
        print('errors',errs)
        await b.close()
asyncio.run(main())
