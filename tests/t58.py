import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
asked=[]
async def handle(r):
    b=r.request.post_data_json; c=b['messages'][0]['content']; text=c if isinstance(c,str) else ' '.join(x.get('text','') for x in c); asked.append(text)
    if 'Suggest cleaning fixes' in text: body=json.dumps([{'type':'rename','col':'Inv No','to':'Invoice number','why':'Abbreviated header'},{'type':'map','col':'Supplier','map':{'D&S':'Davis & Shirtliff Ltd','Bamburi Cement':'Bamburi Cement Ltd'},'why':'Same supplier written two ways'},{'type':'note','text':'INV-003 is far larger than the others: check the decimal point.'},{'type':'rename','col':'Nope','to':'x','why':'bad'}])
    elif 'Do NOT answer with figures' in text: body=json.dumps({'title':'Spend by supplier in October','filters':[{'col':'date','op':'contains','value':'2026-10'}],'group':['supplier'],'bucket':'','measures':[{'col':'amount','agg':'sum'}],'sort':'value-desc','limit':0,'chart':'bar','assumptions':['Took Amount as invoiced cost'],'cannot':''})
    elif 'These figures were calculated' in text: body='Davis & Shirtliff Ltd is the largest at 470,000. The cause is not in the data.'
    elif 'Extract every table' in text: body=json.dumps({'tables':[{'name':'Quote lines','page':'1','columns':['Item','Qty','Amount'],'rows':[['Pump',1,85000],['Cable',40,12000],['Total','',97000]],'uncertain':[{'row':2,'column':'Amount','why':'second digit unclear'}]}],'notes':''})
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        cx=await b.new_context(viewport={'width':1500,'height':950},permissions=['clipboard-read','clipboard-write'],accept_downloads=True); pg=await cx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.route('https://cdn.jsdelivr.net/npm/xlsx@0.18.5/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=open('node_modules/xlsx/dist/xlsx.full.min.js',encoding='utf-8').read()))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        await pg.evaluate("S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};save();render()")
        await pg.click('[data-act=hview][data-v=analytics]'); await pg.wait_for_timeout(300)
        print('steps:',[x.replace('\n',' ') for x in await pg.locator('.ansteps button').all_inner_texts()])
        await pg.set_input_files('input[data-change=an-files]',['invoices.xlsx','tiny.pdf','bad.zzz']); await pg.wait_for_timeout(3500)
        print('tiles:',[x.replace('\n',' | ') for x in await pg.locator('.anstats > *').all_inner_texts()])
        print('files:',[x.replace('\n',' ').replace('\t',' | ') for x in await pg.locator('.antl tbody tr').all_inner_texts()])
        await pg.screenshot(path='an1.png')
        await pg.click('.ansteps [data-v="2"]'); await pg.wait_for_timeout(300)
        print('tables:',[x.replace('\n',' ')[:230] for x in await pg.locator('.antb label').all_inner_texts()])
        print('review:',(await pg.locator('.anflag').first.inner_text()).replace('\n',' | '))
        await pg.fill('.anflag input','12500'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(300); print('corrected ->',await pg.evaluate("S.an.tables.find(t=>t.name==='Quote lines').rows[1]"),'| flags left',await pg.locator('.anflag').count())
        await pg.screenshot(path='an2.png',full_page=True)
        # clean
        await pg.click('.ansteps [data-v="3"]'); await pg.wait_for_timeout(300)
        print('suggestions:');[print('  ',x.replace('\n',' | ')[:330]) for x in await pg.locator('.ansug').all_inner_texts()]
        await pg.screenshot(path='an3.png',full_page=True)
        for k in range(8):
            if not await pg.locator('.ansug [data-act=an-accept]:not([disabled])').count(): break
            await pg.locator('.ansug [data-act=an-accept]:not([disabled])').last.click(); await pg.wait_for_timeout(200)
        print('after local accepts: steps',await pg.evaluate("S.an.tables[0].steps.map(s=>AN_STEP[s.type](s))"),'| rows',await pg.evaluate("anApply(S.an.tables[0]).rows.length"),'| total',await pg.evaluate("(d=>anSum(d,anMeasure(d)))(anApply(S.an.tables[0]))"),'| types',await pg.evaluate("anApply(S.an.tables[0]).types"))
        await pg.click('[data-act=an-ai-clean]'); await pg.wait_for_timeout(1500)
        print('AI suggestions:');[print('  ',x.replace('\n',' | ')[:300]) for x in await pg.locator('.ansug').all_inner_texts()]
        for k in range(4):
            if not await pg.locator('.ansug [data-act=an-accept]:not([disabled])').count(): break
            await pg.locator('.ansug [data-act=an-accept]:not([disabled])').first.click(); await pg.wait_for_timeout(200)
        print('cols now',await pg.evaluate("anApply(S.an.tables[0]).cols"),'| suppliers',await pg.evaluate("[...new Set(anApply(S.an.tables[0]).rows.map(r=>r[1]))]"))
        await pg.locator('[data-change=an-step-on]').first.uncheck(); await pg.wait_for_timeout(200); print('undo first step -> rows',await pg.evaluate("anApply(S.an.tables[0]).rows.length")); await pg.locator('[data-change=an-step-on]').first.check(); await pg.wait_for_timeout(200)
        # combine
        await pg.select_option('#anb',label='Projects'); await pg.wait_for_timeout(200); print('join keys preselected:',await pg.input_value('#anka'),await pg.input_value('#ankb')); await pg.click('[data-act=an-combine]'); await pg.wait_for_timeout(300)
        print('combined:',await pg.evaluate("(t=>{const d=anApply(t);return [t.name,d.cols,d.rows.length,d.info]})(anT())"))
        await pg.screenshot(path='an3b.png',full_page=True)
        # analyse
        await pg.click('.ansteps [data-v="4"]'); await pg.wait_for_timeout(300)
        print('default:',await pg.evaluate("JSON.stringify(V.an.spec)"),'| rows',[x.replace('\t',' | ') for x in await pg.locator('.anres .antl tbody tr').all_inner_texts()][:5])
        await pg.fill('#anq','Which suppliers were paid the most in October?'); await pg.click('[data-act=an-ask]'); await pg.wait_for_timeout(1500)
        print('asked spec:',await pg.evaluate("JSON.stringify(V.an.spec)")); print('result:',[x.replace('\t',' | ') for x in await pg.locator('.anres .antl tbody tr').all_inner_texts()]); print('calc:',(await pg.locator('.ancalc').inner_text()).replace('\n',' / ')[:700])
        await pg.click('[data-act=an-explain]'); await pg.wait_for_timeout(1200); print('narrative:',await pg.locator('.annar p').inner_text()); await pg.screenshot(path='an4.png',full_page=True)
        # visualise
        await pg.click('.ansteps [data-v="5"]'); await pg.wait_for_timeout(300); await pg.screenshot(path='an5.png',full_page=True)
        await pg.locator('.ansvg g.mk').first.click(); await pg.wait_for_timeout(300); print('drill:',(await pg.locator('.andrill').inner_text()).replace('\n',' | ').replace('\t',' ')[:330])
        await pg.click('[data-act=an-pin]'); await pg.wait_for_timeout(200)
        for k in ['line','grouped','pie','scatter','table']:
            await pg.click(f'[data-act=an-chart][data-v={k}]'); await pg.wait_for_timeout(200); await pg.locator('.anres').screenshot(path=f'an5-{k}.png'); print(k,'marks',await pg.locator('.anres .ansvg .mk').count())
        await pg.click('[data-act=an-tpl]') if await pg.locator('[data-act=an-tpl]').count() else None
        await pg.click('.ansteps [data-v="4"]'); await pg.click('[data-act=an-tpl][data-v=trend]'); await pg.click('.ansteps [data-v="5"]'); await pg.wait_for_timeout(300); await pg.click('[data-act=an-pin]'); await pg.locator('.anres').screenshot(path='an5-trend.png'); print('trend rows',await pg.evaluate("anRun(anT(),V.an.spec).rows.map(r=>[r.key[0],r.vals[0]])"))
        await pg.click('.ansteps [data-v="4"]'); await pg.click('[data-act=an-tpl][data-v=fix]'); await pg.wait_for_timeout(200); print('fix:',(await pg.locator('.anres').inner_text()).replace('\n',' | ').replace('\t',' ')[:300])
        await pg.click('[data-act=an-tpl][data-v=share]'); await pg.click('.ansteps [data-v="5"]'); await pg.wait_for_timeout(300); await pg.locator('.anres').screenshot(path='an5-share.png')
        await pg.click('[data-act=an-copy]'); await pg.wait_for_timeout(1500); print('copy:',await pg.evaluate("(async()=>{const it=await navigator.clipboard.read();const b=await it[0].getType('image/png');const im=await createImageBitmap(b);return [im.width,im.height]})()"))
        async with pg.expect_download() as d: await pg.click('[data-act=an-csv]')
        print('csv:',(await d.value).suggested_filename, open(await (await d.value).path()).read()[:120].replace('\r\n',' / '))
        # refresh
        await pg.click('.ansteps [data-v="6"]'); await pg.wait_for_timeout(300)
        await pg.locator('.anstep input[type=file]').first.set_input_files('invoices-nov.xlsx'); await pg.wait_for_timeout(2000)
        print('refresh:',(await pg.locator('.anstep .annote').first.inner_text()),'| rows after steps',await pg.evaluate("anApply(S.an.tables[0]).rows.length"),'| steps kept',await pg.evaluate("S.an.tables[0].steps.length"),'| ver',await pg.evaluate("S.an.tables[0].ver"))
        print('log:',await pg.evaluate("S.an.log.slice(0,4).map(l=>l.text.slice(0,90))")); await pg.screenshot(path='an6.png',full_page=True)
        async with pg.expect_download() as d: await pg.click('[data-act=an-clean-xlsx]')
        print('xlsx:',(await d.value).suggested_filename)
        await pg.reload(); await pg.wait_for_timeout(1500); print('after reload: tables',await pg.evaluate("S.an.tables.length"),'views',await pg.evaluate("S.an.views.length"))
        await pg.click('[data-act=hview][data-v=analytics]'); await pg.click('.ansteps [data-v="5"]'); await pg.wait_for_timeout(300); print('dashboard pins',await pg.locator('.anpin').count())
        await pg.click('.ansteps [data-v="1"]'); await pg.click('[data-act=an-retry]'); await pg.wait_for_timeout(300); print('retry after reload ->',await pg.locator('.toast').inner_text())
        await pg.evaluate("document.documentElement.dataset.theme='dark'"); await pg.click('.ansteps [data-v="5"]'); await pg.wait_for_timeout(300); await pg.screenshot(path='an-dark.png')
        await pg.set_viewport_size({'width':390,'height':800})
        for st in range(1,7):
            await pg.click(f'.ansteps [data-v="{st}"]'); await pg.wait_for_timeout(250); print('phone step',st,'overflow',await pg.evaluate("document.documentElement.scrollWidth>innerWidth"))
        await pg.screenshot(path='an-phone.png'); print('errors',errs)
        await b.close()
asyncio.run(main())
