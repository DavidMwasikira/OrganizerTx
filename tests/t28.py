import json, asyncio
from playwright.async_api import async_playwright
exec(open('t.py').read().split('calls=[]')[0])
def lum(c):
    import re
    r,g,b=[int(x)/255 for x in re.findall(r'\d+',c)[:3]]
    f=lambda v: v/12.92 if v<=.03928 else ((v+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True);return round((x+.05)/(y+.05),1)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await (await b.new_context(viewport={'width':1400,'height':900})).new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('https://api.anthropic.com/**',lambda r:r.fulfill(status=200,content_type='text/event-stream',body=sse([{'type':'text','text':'[]'}])))
        await pg.goto('http://localhost:8765/index.html'); await pg.wait_for_timeout(1500)
        await pg.fill('#name','David'); await pg.fill('#country','Kenya'); await pg.fill('#key','k'); await pg.click('text=Start'); await pg.evaluate("S.weekly={kind:'ai',date:Date.now(),items:[{name:'x',what:'y',why:'z'}]}")
        await pg.click('nav [data-v=settings]'); print('picker cards:',await pg.locator('.skin').count(),'| selected:',await pg.locator('.skin[aria-pressed=true] .nm').inner_text())
        probe="""()=>{const d=document.createElement('div');document.body.append(d);const g=(bg,fg)=>{d.style.background=`var(${bg})`;d.style.color=`var(${fg})`;const c=getComputedStyle(d);return [c.backgroundColor,c.color]};
          const o={text:g('--bg','--ink'),muted:g('--surface','--muted'),button:g('--accent','--accent-ink'),link:g('--surface','--accent'),chip:g('--accent-soft','--accent'),rail:g('--rail','--rail-ink'),create:g('--create','--create-ink')};d.remove();return o}"""
        for sk in ['ultraviolet','forest','glacier','']:
            await pg.click('nav [data-v=settings]'); await pg.click(f'.skin[data-v="{sk}"]'); await pg.wait_for_timeout(150)
            for mode in ['light','dark']:
                await pg.evaluate(f"S.theme='{mode}';applyTheme()"); await pg.wait_for_timeout(100)
                v=await pg.evaluate(probe); print(f'{sk or "original":12s}{mode:6s}',{k:cr(*x) for k,x in v.items()},'meta',await pg.evaluate("document.querySelector('meta[name=theme-color]').content"))
                if sk:
                    await pg.click('nav [data-v=home]'); await pg.wait_for_timeout(250); await pg.screenshot(path=f'sk-{sk}-{mode}.png'); await pg.click('nav [data-v=settings]')
            await pg.evaluate("S.theme='light';applyTheme()")
        await pg.click('.skin[data-v="glacier"]'); await pg.wait_for_timeout(700); await pg.reload(); await pg.wait_for_timeout(1500)
        print('after reload skin:',await pg.evaluate("document.documentElement.dataset.skin"),'| pressed:',await pg.evaluate("S.skin"))
        await pg.click('nav [data-v=settings]'); await pg.locator('.skins').scroll_into_view_if_needed(); await pg.locator('.skins').screenshot(path='sk-picker.png')
        await pg.click('nav [data-v=desk]'); await pg.wait_for_timeout(300); await pg.screenshot(path='sk-desk.png')
        await pg.set_viewport_size({'width':390,'height':800}); await pg.click('.topstrip [data-v=settings], nav [data-v=settings]'); await pg.wait_for_timeout(200); print('phone overflow-x',await pg.evaluate('document.documentElement.scrollWidth>innerWidth'),'| errors',errs)
        await b.close()
asyncio.run(main())
