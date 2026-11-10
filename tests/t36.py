import asyncio, json
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
SEED="""()=>{const d=n=>dash(Date.now()+n*DAY);
 S.plans[0].acts.push({name:'Design page X',status:'todo',due:d(0)},{name:'Fetch assignment',status:'blocked',due:d(8)},{name:'Call pump supplier',status:'doing',due:d(-2)},{name:'Pay invoice',status:'todo',due:d(2)});
 const t=S.topics[0];t.interval=24;t.nextDue=Date.now()+DAY;t.unread=1;t.docs.push({ref:'P001-U01',type:'U',title:'Update: solar pump prices fell 8%',date:Date.now()-3600e3,md:'# Update\\n\\nPrices for 2 kW solar pumps fell about 8% this month.',sources:[]});S.brief=null;S.briefTry=0;save();render()}"""
mode={'v':'good'};calls=[]
async def handle(r):
    body=r.request.post_data_json; calls.append(body)
    if mode['v']=='bad': await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'sorry, no json'}])); return
    ids=await pgref[0].evaluate("allTasks().map(t=>t.id+'|'+t.a.name)")
    tid=[x.split('|')[0] for x in ids if 'Call pump' in x][0]
    out={'summary':'One task is overdue and one is due today. Start by calling the pump supplier, which is two days late. Solar pump prices fell 8% in your followed topic.','priorities':[{'id':tid,'title':'Call the pump supplier','why':'Two days overdue and already started.'},{'id':'made-up-99','title':'Invented task','why':'Should be dropped.'},{'id':'topic:'+await pgref[0].evaluate("S.topics[0].id"),'title':'Read the solar pump price update','why':'Prices fell 8%, which affects the irrigation budget.'}]}
    await r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':json.dumps(out)}]))
pgref=[None]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1670,'height':900}); await ctx.grant_permissions(['clipboard-read','clipboard-write'])
        pg=await ctx.new_page(); pgref[0]=pg; errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',handle)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.wait_for_timeout(400)
        print('new user, no tasks:',await pg.locator('.daysum').inner_text(),'| AI calls',len(calls))
        await pg.evaluate("tick()"); await pg.wait_for_timeout(300); print('empty-day brief made without AI:',await pg.evaluate("[S.brief&&S.brief.ai,S.brief&&S.brief.day===dash(Date.now())]"),'calls',len(calls))
        await pg.evaluate(SEED); await pg.wait_for_timeout(200)
        print('before AI (own ranking):',await pg.locator('.dpri .t').all_inner_texts(),'| chips',[x.replace('\n',' ') for x in await pg.locator('.dchip').all_inner_texts()])
        await pg.evaluate("tick()"); await pg.wait_for_timeout(1500)
        print([(c['model'],c['messages'][0]['content'][:40] if isinstance(c['messages'][0]['content'],str) else 'blocks') for c in calls]); print('auto brief: ai',await pg.evaluate("S.brief.ai"),'| model',calls[-1]['model'],'| summary:',(await pg.locator('.daysum').inner_text())[:70])
        print('priorities:',await pg.locator('.dpri .t').all_inner_texts(),'| label',await pg.locator('.myday .lbl >> nth=1').inner_text(),'| changes',await pg.locator('.dchg').count())
        n=len(calls); await pg.evaluate("tick()"); await pg.wait_for_timeout(500); print('second tick same day makes no new call:',len(calls)==n)
        await pg.screenshot(path='myday.png')
        await pg.click('.dpri li >> nth=0 >> .box'); await pg.wait_for_timeout(200); print('ticked first priority -> done class',await pg.locator('.dpri li.done').count(),'| overdue chip',(await pg.locator('.dchip >> nth=0').inner_text()).replace('\n',' '))
        await pg.click('[data-act=brief-copy]'); await pg.wait_for_timeout(200); print('copied:',repr((await pg.evaluate("navigator.clipboard.readText()"))[:120]))
        await pg.click('.dpri li >> nth=1 >> .linkish'); await pg.wait_for_timeout(200); print('click priority 2 ->',await pg.evaluate("V.view")); await pg.keyboard.press('Escape'); await pg.evaluate("document.querySelector('.modal')&&document.querySelector('.modal [data-x=cancel]')&&document.querySelector('.modal [data-x=cancel]').click()")
        await pg.evaluate("V.view='home';render()"); mode['v']='bad'; await pg.click('[data-act=brief-now]'); await pg.wait_for_timeout(1500)
        print('AI failure -> fallback: ai',await pg.evaluate("S.brief.ai"),'| err',await pg.evaluate("S.brief.err"),'| priorities',await pg.locator('.dpri .t').all_inner_texts())
        await pg.click('[data-act=day-toggle]'); await pg.wait_for_timeout(150); print('collapsed: priorities shown',await pg.locator('.dpri').count(),'summary shown',await pg.locator('.daysum').count()); await pg.click('[data-act=day-toggle]')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.evaluate("render()"); await pg.wait_for_timeout(200)
        y=await pg.evaluate("[document.querySelector('.myday').getBoundingClientRect().top<document.querySelector('.card.ask').getBoundingClientRect().top,document.documentElement.scrollWidth>innerWidth]"); print('phone: My Day above ask box, overflow-x:',y,'| errors',errs); await pg.screenshot(path='myday-phone.png')
        await b.close()
asyncio.run(main())
