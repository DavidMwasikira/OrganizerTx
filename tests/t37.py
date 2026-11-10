import asyncio, json, datetime
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
calls=[]; pgref=[None]; fail={'on':False}
def nxt_friday():
    d=datetime.date.today(); d+=datetime.timedelta(days=((4-d.weekday())%7) or 7); return d.isoformat()
async def handle(r):
    b=r.request.post_data_json; calls.append(b); c=b['messages'][0]['content']; text=c if isinstance(c,str) else ' '.join(x.get('text','') for x in c)
    pg=pgref[0]
    if fail['on']: await r.fulfill(status=500,content_type='application/json',body='{"error":{"message":"boom"}}'); return
    if 'assistant inside OrganizerTX' in text:
        q=text.split('USER: ')[-1].split('\n')[0]
        if 'Add a task' in q: out={'answer':'Done. I added the task for Friday.','actions':[{'type':'add_task','name':'Call the supplier','project':'','due':nxt_friday(),'owner':'David'},{'type':'complete_task','id':'nope:9'}]}
        elif 'complete' in q:
            tid=await pg.evaluate("allTasks().find(t=>t.a.name==='Design page X').id"); out={'answer':'Marked it complete.','actions':[{'type':'complete_task','id':tid}]}
        else: out={'answer':'**1 task is overdue**: Call pump supplier (My tasks), due 2 days ago.','actions':[]}
        body=json.dumps(out)
    elif 'formal minutes' in text:
        body=json.dumps({'title':'Site progress meeting','summary':'The team reviewed drilling progress. Casing is delayed.','attendees':['David','Wanjiru'],'discussion':[{'topic':'Drilling','points':['Reached 60 m','Casing delivery late']}],'decisions':['Order casing from second supplier'],'actions':[{'task':'Order casing from Maji Pumps','owner':'Wanjiru','due':nxt_friday()},{'task':'Send revised programme','owner':'David','due':''}],'open':['Who pays for standby time?']})
    elif 'weekly status report' in text: body='## Summary\n\nOne task closed and one overdue. The supplier call needs attention.\n\n## Progress this week\n\n- Survey closed.\n\n## Risks and blockers\n\n- Fetch assignment is blocked.\n\n## Plan for next week\n\n- Permit.\n\n## Decisions or support needed\n\nNone.'
    elif 'daily site report' in text: body='## Summary\n\nDrilling reached 60 m as recorded.\n\n## Work done today\n\n- Drilling.\n\n## Observations and issues\n\n- None recorded.\n\n## Next steps\n\n- Continue.'
    elif 'quotation' in text.lower() or 'DOCUMENT' in text: body='# Quotation Q-118, Maji Pumps Ltd\n\n## Arithmetic\n\n| Line | Amount |\n|---|---|\n| Pump | Kshs 185,000 |\n| Installation | Kshs 40,000 |\n\nThe stated total of Kshs 235,000 does **not** match the lines, which add to Kshs 225,000.'
    else: body='[]'
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':body}]))
SEED="""()=>{const d=n=>dash(Date.now()+n*DAY);
 S.plans[0].acts.push({name:'Design page X',status:'todo',due:d(0)},{name:'Fetch assignment',status:'blocked',due:d(8)},{name:'Call pump supplier',status:'doing',due:d(-2)});
 S.plans.push({id:'pb',name:'Borehole for the farm',what:'x',custom:true,started:Date.now()-5*DAY,acts:[{name:'Survey',status:'done',closed:Date.now()-DAY},{name:'Permit',status:'doing'}],
   log:[{id:'l1',kind:'note',text:'Drilling reached 60 m by noon',date:Date.now()-3600e3,task:''},{id:'l2',kind:'voice',text:'Casing delivery is late, supplier promises Thursday',date:Date.now()-1800e3,task:''}]});
 S.brief={day:dash(Date.now()),at:Date.now(),summary:'x',pri:[],ai:false};S.weekly={kind:'ai',date:Date.now(),items:[{name:'a',what:'b',why:'c'}]};save();render()}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1670,'height':900},accept_downloads=True); pg=await ctx.new_page(); pgref[0]=pg; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400); await pg.evaluate(SEED); await pg.wait_for_timeout(200)
        await pg.click('nav [data-v=assist]'); await pg.wait_for_timeout(200); print('tabs',await pg.locator('.asst .htabs button').all_inner_texts())
        # 1 ask
        await pg.fill('#aq','What is overdue or blocked?'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(1200)
        c=calls[-1]; ctxs=c['messages'][0]['content']; print('ASK: model',c['model'],'| context has tasks/fieldLog/brain',all(k in ctxs for k in ['"tasks"','"fieldLog"','"brainNotes"','Drilling reached 60 m']),'| size',len(ctxs),'| answer:',(await pg.locator('.amsg.ai').last.inner_text())[:60])
        n0=await pg.evaluate("allTasks().length"); await pg.fill('#aq','Add a task to call the supplier on Friday'); await pg.click('[data-act=asst-send]'); await pg.wait_for_timeout(1200)
        t=await pg.evaluate("(()=>{const a=S.plans.find(p=>p.id==='my').acts.slice(-1)[0];return [a.name,a.due,a.owner,a.status]})()"); print('command: tasks',n0,'->',await pg.evaluate("allTasks().length"),t,'friday ok',t[1]==nxt_friday(),'| action lines',await pg.locator('.aact').all_inner_texts())
        await pg.screenshot(path='as-ask.png')
        await pg.click('[data-act=asst-undo]'); await pg.wait_for_timeout(200); print('undo -> tasks',await pg.evaluate("allTasks().length"),'|',await pg.locator('.aact.un').count(),'undone')
        await pg.fill('#aq','Mark Design page X complete'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(1200); print('complete cmd ->',await pg.evaluate("allTasks().find(t=>t.a.name==='Design page X').a.status"))
        # 2 minutes
        await pg.click('.asst .htabs [data-v=meet]'); await pg.fill('#mtitle','Site meeting'); await pg.fill('#mnotes','Met on site. Drilling at 60 m. Casing late. Wanjiru to order casing from Maji Pumps by Friday. David to send revised programme. Unsure who pays standby.')
        await pg.click('[data-act=meet-go]'); await pg.wait_for_timeout(1500); print('MINUTES: model',calls[-1]['model'],'| actions',await pg.locator('.mact').count(),'| owners',[await x.input_value() for x in await pg.locator('.mact input[type=text]').all()])
        await pg.screenshot(path='as-meet.png')
        await pg.locator('.mact input[type=text]').nth(1).fill('Otieno'); await pg.click('[data-act=meet-tick][data-v="1"]'); await pg.click('[data-act=meet-tick][data-v="1"]'); await pg.select_option('#mpid','pb'); await pg.click('[data-act=meet-save][data-v="1"]'); await pg.wait_for_timeout(400)
        print('saved -> viewer',await pg.locator('.paperdoc h1').inner_text(),'| project tasks',await pg.evaluate("S.plans.find(p=>p.id==='pb').acts.slice(-2).map(a=>[a.name,a.owner,a.due])"),'| papers',await pg.evaluate("S.papers.length"))
        async with pg.expect_download() as dl: await pg.click('[data-act=paper-word]')
        d=await dl.value; path=await d.path(); txt=open(path,encoding='utf-8').read(); print('Word file',d.suggested_filename,len(txt),'has table',('<table' in txt),'has action','Order casing' in txt)
        await pg.screenshot(path='as-paper.png'); await pg.click('[data-act=paper-close]')
        # 3 reports
        await pg.click('.asst .htabs [data-v=report]'); await pg.click('[data-act=rep-go][data-v=weekly]'); await pg.wait_for_timeout(1500)
        tx=await pg.locator('.paperdoc').inner_text(); print('WEEKLY: title',tx.split('\n')[0],'| AI section','needs attention' in tx,'| local tables',all(k in tx for k in ['Status at a glance','Completed this week','Survey','Blocked and overdue','Call pump supplier']))
        await pg.screenshot(path='as-weekly.png'); await pg.click('[data-act=paper-close]')
        await pg.select_option('#rs','pb'); await pg.click('[data-act=rep-go][data-v=site]'); await pg.wait_for_timeout(1500); tx=await pg.locator('.paperdoc').inner_text(); print('SITE:',tx.split('\n')[0],'| record rows','Casing delivery is late' in tx and 'Site record' in tx)
        await pg.click('[data-act=paper-close]'); fail['on']=True; await pg.click('[data-act=rep-go][data-v=weekly]'); await pg.wait_for_timeout(1500); tx=await pg.locator('.paperdoc').inner_text(); print('weekly with AI down still builds:', 'Status at a glance' in tx and '1 overdue' in tx); fail['on']=False; await pg.click('[data-act=paper-close]')
        # 4 files
        await pg.click('.asst .htabs [data-v=files]'); await pg.set_input_files('#fafile','quote.txt'); await pg.click('[data-act=fa-task][data-v=quote]'); await pg.click('[data-act=fa-go]'); await pg.wait_for_timeout(1500)
        c=calls[-1]['messages'][0]['content']; print('FILES: sent as',type(c).__name__,'| file text included','Maji Pumps' in (c if isinstance(c,str) else ''),'| result:',(await pg.locator('#faout').inner_text())[:50].replace('\n',' '))
        await pg.screenshot(path='as-files.png'); await pg.click('[data-act=fa-save]'); await pg.wait_for_timeout(300); print('saved analysis, papers',await pg.evaluate("S.papers.map(p=>p.kind)")); await pg.click('[data-act=paper-close]')
        import base64; open('tiny.pdf','wb').write(b'%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF')
        await pg.set_input_files('#fafile',['tiny.pdf','quote.txt']); await pg.wait_for_timeout(200); print('two files -> task',await pg.evaluate("V.fa.task")); await pg.click('[data-act=fa-go]'); await pg.wait_for_timeout(1500)
        c=calls[-1]['messages'][0]['content']; print('pdf+text sent as blocks:',[x['type'] for x in c]); await pg.click('[data-act=fa-reset]')
        # elsewhere
        await pg.click('nav [data-v=desk]'); await pg.select_option('#dtype','paper'); await pg.wait_for_timeout(200); print('Desktop lists papers',await pg.locator('#deskbody .dfile').count())
        await pg.click('nav [data-v=tasks]'); print('owner on card',await pg.locator('.kcard:has-text("Owner: Wanjiru")').count())
        await pg.reload(); await pg.wait_for_timeout(1500); print('after reload: papers',await pg.evaluate("S.papers.length"),'chat msgs',await pg.evaluate("S.asst.length"))
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('.topstrip [data-v=assist]'); await pg.wait_for_timeout(300); print('phone: assistant opens',await pg.evaluate("V.view"),'overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs); await pg.screenshot(path='as-phone.png')
        await b.close()
asyncio.run(main())
