exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
import datetime
hoy=datetime.date.today().isoformat(); vieja=(datetime.date.today()-datetime.timedelta(days=40)).isoformat()
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    for caso,f in (('reciente',hoy),('vieja',vieja)):
      web={'eslogan':'El deporte de raqueta más rápido, en Torrelavega','noticias':[{'id':'n1','titulo':'Medalla de bronce Cto.España','texto':'x','fecha':f}]}
      sd={'publico/datos':{'web':web}}
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
      pg.goto('https://test.local/'); pg.wait_for_timeout(2500); pg.evaluate('scrollTo(0,0)')
      vis=pg.locator('#avisoNoticia').is_visible()
      if caso=='reciente':
        ok(vis and 'Medalla de bronce' in pg.inner_text('#avisoNoticia'), f'{dev}: sale el aviso de noticia nueva en la portada')
        bb=pg.locator('#avisoNoticia').bounding_box(); ok(bb['x']>=0 and bb['x']+bb['width']<=vw, f'{dev}: cabe en pantalla {bb}')
        pg.screenshot(path=SP+f'aviso_{dev}.png')
        (pg.tap('#avisoNoticia') if mov else pg.click('#avisoNoticia')); pg.wait_for_timeout(1200)
        y=pg.evaluate("document.getElementById('noticias').getBoundingClientRect().top")
        ok(abs(y)<150, f'{dev}: al pulsarlo baja a las noticias ({y})')
      else: ok(not vis, f'{dev}: noticia de hace 40 días -> sin aviso')
      ok(not errs, f'{dev} {caso}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
