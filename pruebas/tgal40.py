exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
import random
def foto(i):
  random.seed(i); im=Image.frombytes('RGB',(500,375),bytes(random.getrandbits(8) for _ in range(500*375*3))); b=io.BytesIO(); im.save(b,'JPEG',quality=70); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
F=[foto(i) for i in range(14)]
print('tam foto', len(F[0]))
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    # galería antigua de 8 en un solo documento
    web={'eslogan':'x','nGaleria':8,'noticias':[]}
    seed={'club/datos':{'club':{'nombre':'Olimpia','web':web},'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}},'club/datos/taller_fotos/web_galeria':{'fotos':F[:8]}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('dialog',lambda d: (errs.append('ALERT '+d.message), d.accept()))
    pg.route('**/*',ruta(HTML))
    pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(800)
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1500)
    ok(pg.locator('.web-subir-galeria').count()==1, f'{dev}: con 8 fotos aún deja añadir más')
    for i in range(8,14):
      with pg.expect_file_chooser() as fc: pg.locator('.web-subir-galeria').click()
      open(SP+'g.jpg','wb').write(base64.b64decode(F[i].split(',')[1])); fc.value.set_files(SP+'g.jpg'); pg.wait_for_timeout(900)
    st=pg.evaluate("Object.fromEntries(Object.entries(window.__STORE).filter(([k])=>k.includes('web_galeria')).map(([k,v])=>[k,(v.fotos||[]).length]))")
    n=pg.evaluate("webCfg().nGaleria"); partes=pg.evaluate("webCfg().galeriaPartes")
    ok(n==14 and sum(st.values())==14, f'{dev}: 14 fotos guardadas {st} n={n} partes={partes}')
    tams=pg.evaluate("Object.entries(window.__STORE).filter(([k])=>k.includes('web_galeria')).map(([k,v])=>JSON.stringify(v).length)")
    ok(all(t<900000 for t in tams), f'{dev}: ningún documento pasa del límite {tams}')
    pub=pg.evaluate("JSON.parse(JSON.stringify(estadoPublicoParaNube())).web")
    pg.close()
    # web pública
    sd={'publico/datos':{'web':{'eslogan':'x','nGaleria':n,'galeriaPartes':partes}}}
    for k,v in st.items(): pass
    store=None
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov)
    errs2=[]; pg.on('pageerror',lambda e: errs2.append(str(e)))
    pg.route('**/*',ruta(WEB))
    # reconstruir fotos por partes en el orden de la app
    pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    ok(pub.get('galeriaPartes')==partes, f'{dev}: la web pública recibe el número de partes')
    ok(not errs, f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
