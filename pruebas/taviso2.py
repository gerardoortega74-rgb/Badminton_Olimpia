exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
import datetime
F='/tmp/claude-0/-home-claude/3cdf04c3-6017-5b52-901b-0b83f0325f3c/scratchpad/fnt/node_modules/@fontsource/'
def b64(f): return base64.b64encode(open(F+f,'rb').read()).decode()
CSS="@font-face{font-family:'Big Shoulders Display';font-weight:800 900;src:url(data:font/woff2;base64,"+b64('big-shoulders-display/files/big-shoulders-display-latin-900-normal.woff2')+")}@font-face{font-family:'Archivo';src:url(data:font/woff2;base64,"+b64('archivo/files/archivo-latin-400-normal.woff2')+")}"
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,768,False,'pc')):
    web={'eslogan':'El deporte de raqueta más rápido, en Torrelavega','noticias':[{'id':'n1','titulo':'Medalla de bronce Cto.España','texto':'x','fecha':datetime.date.today().isoformat()}]}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,device_scale_factor=1)
    pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':{'web':web}})+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    pg.goto('https://test.local/'); pg.add_style_tag(content=CSS); pg.wait_for_timeout(2500)
    pg.screenshot(path=SP+f'aviso2_{dev}.png'); print(pg.evaluate("document.querySelector('.portada').getBoundingClientRect().height"))
