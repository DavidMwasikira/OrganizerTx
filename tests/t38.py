import asyncio, json, datetime
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
calls=[]; bad={'on':False}
async def handle(r):
    b=r.request.post_data_json; calls.append(b); c=b['messages'][0]['content']; text=c if isinstance(c,str) else ' '.join(x.get('text','') for x in c)
    if 'Convert this budget' in text:
        lines=[{'category':'Professional services','item':'Drilling, 60 m','planned':300000,'actual':0},{'category':'Materials','item':'PVC casing, 60 m','planned':90000,'actual':0},{'category':'Equipment','item':'Solar pump, 2 kW','planned':185000,'actual':0},{'category':'Permits and fees','item':'County permit','planned':25000,'actual':0},{'category':'Nonsense','item':'Hydrogeologist survey','planned':'40,000','actual':0}]
        if bad['on']: lines=lines[:4]
        body=json.dumps({'currency':'Kshs','lines':lines,'stated_total':640000,'notes':''})
    elif 'weekly status report' in text: body='## Summary\n\nBudget is 14% used and one high risk is open.\n\n## Progress this week\n\n- x\n\n## Risks and blockers\n\n- x\n\n## Plan for next week\n\n- x\n\n## Decisions or support needed\n\nNone.'
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
SEED="""()=>{S.plans.push({id:'pb',name:'Borehole for the farm',what:'x',custom:true,started:Date.now()-5*DAY,acts:[{name:'Survey',status:'todo',owner:'Wanjiru',due:dash(Date.now()+2*DAY)}],log:[]});
 S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};save();render()}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1670,'height':900}); pg=await ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.route('https://cdn.jsdelivr.net/npm/xlsx@0.18.5/**',lambda r:r.fulfill(status=200,content_type='application/javascript',body=open('node_modules/xlsx/dist/xlsx.full.min.js',encoding='utf-8').read()))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400); await pg.evaluate(SEED); await pg.wait_for_timeout(200)
        # --- task with owner, repeat, reminder
        await pg.click('nav [data-v=tasks]'); await pg.click('.toolbar [data-act=task-new]'); await pg.fill('#tname','Weekly site inspection'); today=datetime.date.today().isoformat()
        await pg.fill('#tdued',today); await pg.fill('#towner','Otieno'); await pg.select_option('#trep','weekly'); past=(datetime.datetime.now()-datetime.timedelta(minutes=2)).strftime('%Y-%m-%dT%H:%M'); await pg.fill('#trem',past); await pg.click('[data-x=save]'); await pg.wait_for_timeout(300)
        print('card meta:',(await pg.locator('.kcard:has-text("Weekly site inspection")').inner_text()).replace('\n',' | '),'| owner filter options',await pg.locator('#towner2 option').all_inner_texts())
        await pg.evaluate("checkReminders()"); await pg.wait_for_timeout(300); print('REMINDER bar:',(await pg.locator('.rembar').inner_text()).replace('\n',' ')[:80],'| fires once:',await pg.evaluate("(checkReminders(),S.rems.length)"))
        await pg.screenshot(path='tp-board.png'); await pg.click('[data-act=rem-x]'); print('dismissed',await pg.locator('.rembar').count()==0)
        tid=await pg.evaluate("allTasks().find(t=>t.a.name==='Weekly site inspection').id"); await pg.evaluate(f"ACT['task-done']('{tid}');render()"); await pg.wait_for_timeout(300)
        nx=(datetime.date.today()+datetime.timedelta(days=7)).isoformat(); r=await pg.evaluate("allTasks().filter(t=>t.a.name==='Weekly site inspection').map(t=>[t.a.status,t.due,t.a.owner,t.a.repeat,!!t.a.remind])"); print('RECURRING after completing:',r,'| next due right',r[-1][1]==nx)
        await pg.evaluate("render();render()"); print('no duplicate spawn:',await pg.evaluate("allTasks().filter(t=>t.a.name==='Weekly site inspection').length")==2)
        await pg.select_option('#towner2','Wanjiru'); await pg.wait_for_timeout(150); print('owner filter Wanjiru -> cards',await pg.locator('.kcard').count()); await pg.select_option('#towner2','all')
        # --- calendar
        await pg.click('[data-act=tmode][data-v=cal]'); await pg.wait_for_timeout(200); print('CALENDAR:',await pg.locator('.calbar h2').inner_text(),'| cells',await pg.locator('.cal .cc').count(),'| events',await pg.locator('.cal .ce').count(),'| today marked',await pg.locator('.cal .cc.now').count())
        await pg.locator(f'.cal [data-act=task-new-day][data-v="{nx}"]').click(); print('click date -> due preset',await pg.input_value('#tdued')==nx); await pg.fill('#tname','Pay driller'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200)
        await pg.click('[data-act=cal-nav][data-v="1"]'); m2=await pg.locator('.calbar h2').inner_text(); await pg.click('[data-act=cal-nav][data-v="0"]'); print('next month ->',m2,'| back to',await pg.locator('.calbar h2').inner_text())
        # --- project controls
        await pg.evaluate("ACT['open-plan']('pb');render()"); await pg.wait_for_timeout(200); print('PROJECT tabs',[x.replace('\n',' ') for x in await pg.locator('.htabs button').all_inner_texts()])
        await pg.click('.htabs [data-v=budget]'); await pg.set_input_files('#budfile','budget.xlsx'); await pg.wait_for_timeout(2500)
        sent=calls[-1]['messages'][0]['content']; print('BUDGET import: excel text sent',isinstance(sent,str) and 'pvc casing' in sent and '640000' in sent,'| model',calls[-1]['model'])
        print('review:',(await pg.locator('section.card >> nth=0 >> p').first.inner_text())[:110],'| rows',await pg.locator('section.card >> nth=0 >> tbody tr').count(),'| bad category fixed ->',await pg.locator('section.card >> nth=0 >> tbody tr >> nth=4 >> td >> nth=0').inner_text())
        await pg.screenshot(path='tp-import.png'); await pg.click('[data-act=bud-accept][data-v=replace]'); await pg.wait_for_timeout(200)
        print('tiles',[x.replace('\n',' ') for x in await pg.locator('.btile').all_inner_texts()],'| lines',await pg.evaluate("budOf(curPlan()).lines.length"))
        a=pg.locator('[data-bud="0|actual"]'); await a.fill('90,000'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(100); print('focus stays in table after Tab:',await pg.evaluate("!!(document.activeElement.dataset&&document.activeElement.dataset.bud)")); await pg.click('h1'); await pg.wait_for_timeout(200)
        print('after spend: tiles',[x.replace('\n',' ') for x in await pg.locator('.btile').all_inner_texts()]); await pg.click('[data-act=bud-add]'); await pg.wait_for_timeout(100); print('add line ->',await pg.evaluate("budOf(curPlan()).lines.length")); await pg.click('[data-act=bud-del][data-v="5"]')
        await pg.screenshot(path='tp-budget.png')
        bad['on']=True; await pg.set_input_files('#budfile','budget.xlsx'); await pg.wait_for_timeout(2500); print('mismatch warning:',await pg.locator('section.card >> nth=0 >> p.banner').count()==1); await pg.click('[data-act=bud-accept][data-v=""]'); bad['on']=False
        await pg.click('.htabs [data-v=risks]'); await pg.click('[data-act=risk-new]'); await pg.fill('#rtitle','Casing delivery may slip a week'); await pg.select_option('#rlevel','high'); await pg.fill('#rowner','Wanjiru'); await pg.fill('#raction','Order from second supplier'); await pg.click('[data-x=save]'); await pg.wait_for_timeout(200)
        print('RISKS:',(await pg.locator('.rrow').inner_text()).replace('\n',' | ')[:90],'| pills',await pg.locator('.page .pill').all_inner_texts()[:3] if False else [x for x in (await pg.locator('.page > .row .pill').all_inner_texts())])
        await pg.click('.htabs [data-v=miles]'); await pg.fill('#mname','Drilling complete'); await pg.fill('#mdate2',nx); await pg.click('[data-act=mile-add]'); await pg.wait_for_timeout(150); await pg.fill('#mname','Permit issued'); await pg.fill('#mdate2',(datetime.date.today()-datetime.timedelta(days=3)).isoformat()); await pg.click('[data-act=mile-add]'); await pg.wait_for_timeout(150)
        print('MILESTONES states',await pg.locator('.mact .pill').all_inner_texts()); await pg.click('[data-act=mile-tick] >> nth=0'); await pg.wait_for_timeout(150); print('after tick',await pg.locator('.mact .pill').all_inner_texts(),'| tab badge',(await pg.locator('.htabs [data-v=miles]').inner_text()).replace('\n',' ')); await pg.screenshot(path='tp-miles.png')
        await pg.click('nav [data-v=tasks]'); print('milestone on calendar',await pg.locator('.cal .ce.ms').count()); await pg.screenshot(path='tp-cal.png')
        await pg.click('nav [data-v=assist]'); await pg.click('.asst .htabs [data-v=report]'); await pg.click('[data-act=rep-go][data-v=weekly]'); await pg.wait_for_timeout(1500); tx=await pg.locator('.paperdoc').inner_text(); print('weekly report has controls:',all(k in tx for k in ['Budget','Kshs 640,000','Open risks and issues','Casing delivery may slip','Milestones','Drilling complete']))
        await pg.reload(); await pg.wait_for_timeout(1500); print('after reload: lines',await pg.evaluate("budOf(S.plans.find(p=>p.id==='pb')).lines.length"),'risks',await pg.evaluate("S.plans.find(p=>p.id==='pb').risks.length"),'miles',await pg.evaluate("S.plans.find(p=>p.id==='pb').miles.length"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("V.view='tasks';V.tmode='cal';render()"); await pg.wait_for_timeout(200); o1=await pg.evaluate('document.documentElement.scrollWidth>innerWidth'); await pg.screenshot(path='tp-cal-phone.png')
        await pg.evaluate("V.view='plan';V.plan='pb';V.ptab='budget';render()"); await pg.wait_for_timeout(200); print('phone overflow-x: calendar',o1,'budget',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| photo button visible',await pg.locator('label[for=budcam]').is_visible(),'| errors',errs); await pg.screenshot(path='tp-budget-phone.png')
        await b.close()
asyncio.run(main())
