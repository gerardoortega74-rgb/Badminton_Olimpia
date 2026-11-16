exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    web={'eslogan':'x','redes':{'paginaId':'P1','paginaNombre':'Club','instagramId':'IG1'},'noticias':[
      {'id':'n1','titulo':'Medalla de bronce','texto':'Texto viejo','fecha':'2026-11-08','tieneFoto':False,'redes':{'fb':{'fecha':1,'postId':'P1_99','imagenUrl':'https://x/y.jpg'},'ig':{'fecha':1,'mediaId':'M77'}}},
      {'id':'n2','titulo':'Sin publicar','texto':'a','fecha':'2026-11-01','tieneFoto':False}]}
    seed={'club/datos':{'club':{'nombre':'Olimpia','web':web},'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('dialog',lambda d: (None if d.type=='confirm' else errs.append('ALERT '+d.message), d.accept()))
    pg.route('**/*',ruta(HTML))
    pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};localStorage.setItem("badmintonTokenMeta","TK");')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(1200)
    pg.evaluate("""window.__log=[];const of=window.fetch;window.fetch=(u,o)=>{if(String(u).includes('graph.facebook.com')){const m={};if(o&&o.body&&o.body.forEach)o.body.forEach((v,k)=>m[k]=v);window.__log.push({u:String(u),met:o&&o.method,m});return Promise.resolve(new Response('{"success":true}'));}return of(u,o);}""")
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1200)
    pg.locator('.web-redes-act').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'botones_{dev}.png')
    ok(pg.locator('.web-redes-act').count()==1, f'{dev}: botón «Actualizar en Facebook» solo en la noticia publicada ({pg.locator(".web-redes-act").count()})')
    ta=pg.locator('textarea').filter(has_text='Texto viejo').first
    ta.fill('Texto NUEVO corregido')
    btn=pg.locator('.web-redes-act'); btn.scroll_into_view_if_needed()
    (btn.tap() if mov else btn.click()); pg.wait_for_timeout(800)
    lg=pg.evaluate("window.__log"); print(lg)
    ok(len(lg)==1 and lg[0]['u'].endswith('/P1_99') and lg[0]['met']=='POST' and 'Texto NUEVO corregido' in lg[0]['m'].get('message',''), f'{dev}: manda el texto nuevo a la publicación de Facebook')
    ok('actualizado' in pg.locator('.web-redes-act').inner_text(), f'{dev}: confirma «Facebook actualizado»')
    ok(pg.evaluate("webCfg().noticias[0].texto")=='Texto NUEVO corregido', f'{dev}: la noticia guarda el texto nuevo')
    pg.evaluate("window.__log=[]")
    rb=pg.locator('.web-redes-reig'); ok(rb.count()==1, f'{dev}: botón «Volver a publicar en Instagram»')
    rb.scroll_into_view_if_needed(); (rb.tap() if mov else rb.click()); pg.wait_for_timeout(1500)
    lg=pg.evaluate("window.__log"); print(lg)
    ok(any(l['u'].startswith('https://graph.facebook.com/M77') and l['met']=='DELETE' for l in lg), f'{dev}: borra la publicación de Instagram')
    ok(pg.evaluate("!webCfg().noticias[0].redes.ig"), f'{dev}: queda marcada como no publicada en Instagram')
    ok(pg.locator('.rd-modal').count()==1, f'{dev}: se abre «Publicar en redes» para volver a publicar')
    chk=pg.evaluate("[...document.querySelectorAll('.rd-modal input[type=checkbox]')].slice(0,2).map(c=>c.checked)")
    ok(chk==[False,True], f'{dev}: viene marcado solo Instagram (Facebook ya está) {chk}')
    pg.screenshot(path=SP+f'actfb_{dev}.png')
    ok(not errs, f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
