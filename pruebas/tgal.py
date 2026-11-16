exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
def foto(c):
  im=Image.new('RGB',(1600,1200),c); b=io.BytesIO(); im.save(b,'JPEG',quality=90); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    web={'eslogan':'x','noticias':[{'id':'n1','titulo':'Medalla','texto':'t','fecha':'2026-11-08','tieneFoto':True,'extras':['fa']}]}
    seed={'club/datos':{'club':{'nombre':'Olimpia','web':web},'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}},
      'club/datos/taller_fotos/web_noticia_n1':{'foto':foto((200,50,50))},'club/datos/taller_fotos/web_noticia_n1_fa':{'foto':foto((50,50,200))}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('dialog',lambda d: (errs.append('ALERT '+d.message), d.accept()))
    pg.route('**/*',ruta(HTML))
    pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(1000)
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1500)
    bs=pg.locator('.web-a-galeria'); ok(bs.count()==2, f'{dev}: botón «Galería» en las 2 fotos de la noticia ({bs.count()})')
    bs.nth(1).scroll_into_view_if_needed(); (bs.nth(1).tap() if mov else bs.nth(1).click()); pg.wait_for_timeout(2000)
    gal=pg.evaluate("(window.__STORE['club/datos/taller_fotos/web_galeria']||{}).fotos||[]")
    ok(len(gal)==1, f'{dev}: la foto se guarda en la galería de la web ({len(gal)})')
    ok(pg.evaluate("webCfg().nGaleria")==1, f'{dev}: la web sabe que hay 1 foto en la galería')
    pg.wait_for_timeout(800)
    txt=pg.locator('.web-a-galeria').all_inner_texts(); ok(txt.count('🖼 ✓')==1, f'{dev}: esa foto sale marcada ✓ {txt}')
    pg.locator('.web-a-galeria').nth(1).scroll_into_view_if_needed(); pg.screenshot(path=SP+f'gal_{dev}.png')
    bb=pg.locator('.web-a-galeria', has_text='🖼 ✓'); (bb.tap() if mov else bb.click()); pg.wait_for_timeout(1500)
    gal=pg.evaluate("(window.__STORE['club/datos/taller_fotos/web_galeria']||{}).fotos||[]")
    ok(len(gal)==0, f'{dev}: pulsar otra vez la quita de la galería')
    ok(not errs, f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
