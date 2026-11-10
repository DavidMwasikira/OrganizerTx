import re
s=open('../organizertx/index.html').read();js=re.search(r'<script>(.*)</script>',s,re.S).group(1);open('app.js','w').write(js)
i=js.index('/* Read structured answers');j=js.index('function loadGuide');k=js.index('const str=x=>')
open('parse.mjs','w').write(js[k:js.index('\n',k)]+'\n'+js[i:j]+open('cases.js').read())
