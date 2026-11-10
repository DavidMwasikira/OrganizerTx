import json, asyncio
from playwright.async_api import async_playwright
def sse(blocks, stop='end_turn'):
    out=[]
    ev=lambda d: out.append('event: x\ndata: '+json.dumps(d)+'\n\n')
    ev({'type':'message_start','message':{}})
    for i,b in enumerate(blocks):
        if b['type']=='text':
            ev({'type':'content_block_start','index':i,'content_block':{'type':'text','text':''}})
            t=b['text']
            for k in range(0,len(t),40): ev({'type':'content_block_delta','index':i,'delta':{'type':'text_delta','text':t[k:k+40]}})
            for c in b.get('citations',[]): ev({'type':'content_block_delta','index':i,'delta':{'type':'citations_delta','citation':c}})
        elif b['type']=='server_tool_use':
            ev({'type':'content_block_start','index':i,'content_block':{'type':'server_tool_use','id':'s1','name':'web_search','input':{}}})
            ev({'type':'content_block_delta','index':i,'delta':{'type':'input_json_delta','partial_json':json.dumps(b['input'])}})
        else:
            ev({'type':'content_block_start','index':i,'content_block':b})
        ev({'type':'content_block_stop','index':i})
    ev({'type':'message_delta','delta':{'stop_reason':stop}})
    return ''.join(out)
cit={'type':'web_search_result_location','url':'https://example.org/a','title':'Example source','cited_text':'x'}
REPORT="# Borehole pump sizing basics\n\n## Summary\n- Point one about **head**.\n- Point two.\n\n## Findings\n| Item | Value |\n|---|---|\n| Head | 60 m |\n\nText para.\n\n## Recommended next steps\n1. Measure yield.\n2. Get quotes.\n\n===TAKEAWAYS===\n- Size on total dynamic head.\n- Check yield first.\n"
UPDATE="# Update: New pump tariffs announced\n\n## What is new\nSomething changed.\n\n## What it means for you\nCosts.\n\n## Suggested next step\nCall supplier.\n\n===TAKEAWAYS===\nNONE\n"
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':390,'height':800})
        pg=await ctx.new_page()
        errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' and 'fonts' not in m.text and 'ERR_' not in m.text else None)
        async def api(route):
            body=json.loads(route.request.post_data); calls.append(body)
            u=body['messages'][0]['content']
            if len(calls)==1:  # pause_turn path first
                r=sse([{'type':'text','text':'Let me search.'},{'type':'server_tool_use','input':{'query':'pump sizing'}},{'type':'web_search_tool_result','tool_use_id':'s1','content':[{'type':'web_search_result','url':'https://example.org/a','title':'Example source','encrypted_content':'zz'}]}],'pause_turn')
            elif 'Research this' in u: r=sse([{'type':'text','text':REPORT[:200]},{'type':'text','text':REPORT[200:],'citations':[cit]}])
            elif 'You are following' in u: r=sse([{'type':'text','text':UPDATE}])
            elif 'knowledge base, followed' in u: r=sse([{'type':'text','text':'## Profile and interests\nEngineer.\n\n## Water\n- Size on head.'}])
            else: r=sse([{'type':'text','text':'A **chat** answer.'}])
            await route.fulfill(status=200,content_type='text/event-stream',body=r)
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='1-setup.png',full_page=True)
        await pg.fill('#name','David Mwasikira'); await pg.fill('#country','Kenya'); await pg.click('text=Engineering'); await pg.click('text=Energy')
        await pg.fill('#key','sk-test'); await pg.click('text=Start'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='2-home.png',full_page=True)
        await pg.fill('#ask','How do I size a borehole pump?'); await pg.click('[data-act=research]'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='3-topic.png',full_page=True)
        await pg.click('[data-act=follow][data-v="168"]'); await pg.wait_for_timeout(200)
        await pg.click('[data-act=update-now]'); await pg.wait_for_timeout(1200)
        await pg.fill('#chat','What about solar pumps?'); await pg.click('[data-act=send]'); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='4-thread.png',full_page=True)
        await pg.click('[data-act=open-doc] >> nth=0'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='5-doc.png',full_page=True)
        await pg.click('[data-act=close-doc]'); await pg.click('[data-act=tab][data-v=folder]'); await pg.wait_for_timeout(200)
        await pg.screenshot(path='6-folder.png',full_page=True)
        await pg.click('[data-act=nav][data-v=brain]'); await pg.click('[data-act=tidy]'); await pg.wait_for_timeout(1000)
        await pg.screenshot(path='7-brain.png',full_page=True)
        st=await pg.evaluate('JSON.stringify({t:S.topics[0],b:S.brain})')
        d=json.loads(st); t=d['t']
        print('title',t['title'],'| docs',[(x['ref'],x['sources']) for x in t['docs']],'| interval',t['interval'],'| chat roles',[m['role'] for m in t['chat']])
        print('doc md starts',repr(t['docs'][0]['md'][:60])); print('brain',d['b'])
        print('calls',len(calls),'| 2nd call last msg role',calls[1]['messages'][-1]['role'],[x['type'] for x in calls[1]['messages'][-1]['content']])
        # reload persistence + due update catch-up
        await pg.evaluate('S.topics[0].nextDue=Date.now()-1000;store.set(JSON.parse(JSON.stringify(S)))'); await pg.wait_for_timeout(400)
        await pg.reload(); await pg.wait_for_timeout(5000)
        print('after reload docs',await pg.evaluate('S.topics[0].docs.length'),'unread',await pg.evaluate('S.topics[0].unread'))
        await pg.set_viewport_size({'width':1200,'height':800}); await pg.wait_for_timeout(200)
        await pg.screenshot(path='8-desktop.png')
        print('errors',errs)
        await b.close()
asyncio.run(main())
