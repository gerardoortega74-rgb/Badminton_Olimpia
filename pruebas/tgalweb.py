exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
def foto(c):
  im=Image.new('RGB',(400,300),c); b=io.BytesIO(); im.save(b,'JPEG'); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
F=[foto((i*15,100,200-i*10)) for i in range(14)]
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    for caso,web,docs in (('partes',{'eslogan':'x','nGaleria':14,'galeriaPartes':3},{'web_galeria':F[:6],'web_galeria_1':F[6:12],'web_galeria_2':F[12:]}),('antigua',{'eslogan':'x','nGaleria':8},{'web_galeria':F[:8]})):
      sd={'publico/datos':{'web':web}}
      for k,v in docs.items(): sd['club/datos/taller_fotos/'+k]={'fotos':v}
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
      pg.goto('https://test.local/'); pg.wait_for_timeout(2500)
      n=pg.locator('#fotosGaleria img').count(); esp=14 if caso=='partes' else 8
      ok(n==esp and pg.locator('#galeria').is_visible(), f'web {dev} {caso}: «En la pista» enseña {n}/{esp} fotos')
      if caso=='partes': pg.locator('#galeria').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'pista_{dev}.png')
      ok(not errs, f'web {dev} {caso}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
