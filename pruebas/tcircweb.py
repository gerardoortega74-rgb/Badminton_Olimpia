exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    circ=[{'id':'cir_x','nombre':'Circuito Olimpia Open','jornadas':[{'id':'j1','nombre':'Jornada 1','fecha':'2026-09-27','estado':'jugada'},{'id':'j2','nombre':'Jornada 3','fecha':'2026-12-13','estado':'proxima'}],'ranking':[],'categorias':[]}]
    sd={'publico/datos':{'web':{'eslogan':'x','noticias':[]},'circuitos':circ}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    pg.goto('https://test.local/'); pg.wait_for_timeout(2500)
    c=pg.locator('.circuito-web'); ok(c.count()==1 and c.is_visible() and 'Jornada 3' in c.inner_text(), f'web {dev}: aviso del circuito en Noticias y torneos')
    ok(pg.locator('.circuito-web a').get_attribute('href')=='app.html?publico=1&circuito=cir_x', f'web {dev}: enlace a la página del circuito')
    c.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'circweb_{dev}.png')
    ok(not errs, f'web {dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
