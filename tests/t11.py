import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
def sse2(blocks,stop='end_turn'):
    out=[];ev=lambda d: out.append('data: '+json.dumps(d)+'\n\n')
    for i,b in enumerate(blocks):
        if b['type']=='thinking':
            ev({'type':'content_block_start','index':i,'content_block':{'type':'thinking','thinking':'','signature':''}})
            ev({'type':'content_block_delta','index':i,'delta':{'type':'signature_delta','signature':'SIG123'}})
        elif b['type']=='text':
            ev({'type':'content_block_start','index':i,'content_block':{'type':'text','text':''}}); ev({'type':'content_block_delta','index':i,'delta':{'type':'text_delta','text':b['text']}})
        elif b['type']=='server_tool_use':
            ev({'type':'content_block_start','index':i,'content_block':{'type':'server_tool_use','id':'s1','name':'web_search','input':{}}}); ev({'type':'content_block_delta','index':i,'delta':{'type':'input_json_delta','partial_json':'{"query":"q"}'}})
        else: ev({'type':'content_block_start','index':i,'content_block':b})
        ev({'type':'content_block_stop','index':i})
    ev({'type':'message_delta','delta':{'stop_reason':stop}}); return ''.join(out)
OBJ=json.dumps(["Estimate the startup costs involved","Identify the tools needed first","Outline a launch plan by week"])
calls=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1280,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        mode={'v':'real'}
        async def api(route):
            body=json.loads(route.request.post_data); u=body['messages'][0]['content']; calls.append(body)
            helper='thinking' in body
            if mode['v']=='starved' and not helper:   # what the real service did to v0.5: thinking ate the allowance
                return await route.fulfill(status=200,content_type='text/event-stream',body=sse2([{'type':'thinking'}],'max_tokens'))
            if mode['v']=='reject' and helper:
                return await route.fulfill(status=400,content_type='application/json',body=json.dumps({'error':{'message':'thinking cannot be disabled'}}))
            if 'Research this' in u:
                if len(body['messages'])==1: r=sse2([{'type':'thinking'},{'type':'server_tool_use'},{'type':'web_search_tool_result','tool_use_id':'s1','content':[]}],'pause_turn')
                else: r=sse2([{'type':'thinking'},{'type':'text','text':REPORT}])
            elif 'Suggest 8' in u: r=sse2([{'type':'text','text':OBJ}])
            elif 'Rewrite' in u: r=sse2([{'type':'text','text':'A refined brief.'}])
            else: r=sse2([{'type':'thinking'},{'type':'text','text':'[]'}])
            await route.fulfill(status=200,content_type='text/event-stream',body=r)
        await pg.route('https://api.anthropic.com/**',api)
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start')
        await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        await pg.fill('#ask','AI workshops'); await pg.click('[data-act=obj-suggest]'); await pg.wait_for_timeout(900)
        h=calls[-1]; print('1 helper request: model',h['model'],'| thinking',h.get('thinking'),'| effort',h.get('output_config'),'| max',h['max_tokens'],'| objectives shown',await pg.locator('.objbox label').count())
        await pg.click('[data-act=refine]'); await pg.wait_for_timeout(900); print('2 refine:',repr(await pg.input_value('#ask')))
        mode['v']='reject'; n=len(calls); await pg.fill('#ask','Another topic'); await pg.click('[data-act=obj-suggest]'); await pg.wait_for_timeout(900)
        print('3 if the service rejects thinking-off: retried without it ->',len(calls)-n,'requests, objectives',await pg.locator('.objbox label').count())
        mode['v']='real'; await pg.click('[data-act=research]'); await pg.wait_for_timeout(1800)
        cont=[c for c in calls if len(c['messages'])==2][0]['messages'][1]['content']
        print('4 research with thinking + resumed search: doc filed',await pg.evaluate('S.topics[0].docs.length'),'| thinking block returned intact',cont[0],'| max',[c for c in calls if 'Research this' in c['messages'][0]['content']][0]['max_tokens'])
        mode['v']='starved'; await pg.click('nav [data-v=home]'); await pg.click('[data-act=weekly-now]'); await pg.wait_for_timeout(900)
        print('5 starved answer now says:',await pg.locator('section .banner').inner_text(),'| errors',errs)
        await b.close()
asyncio.run(main())
