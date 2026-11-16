exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
POD=[{'categoria':'IM A','primero':'Ana','segundo':'Bea','terceros':['C','D']}]
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    for caso,enweb in (('interno',False),('público',True)):
      hist=[{'id':'t1','nombre':'Torneo Navidad','estado':'finalizado','fechaInicio':'2026-10-01','podios':POD,'enWeb':enweb}]
      st={'meta':{'title':'Liga interna','date':'2026-11-10'},'categories':[]}
      sd={'publico/datos':{'web':{'eslogan':'x'},'torneosHistorial':hist,'torneo':st,'torneoActivoId':'t2','torneoEnDirecto':True,'torneoActivoEnWeb':enweb}}
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
      pg.goto('https://test.local/'); pg.wait_for_timeout(2500)
      pod=pg.locator('.podio').count(); dire=pg.locator('#enDirecto').inner_text().strip()
      if enweb: ok(pod==1 and dire!='', f'{dev} {caso}: con «Mostrar en la web» salen podios y directo')
      else: ok(pod==0 and dire=='' and 'torneo organizado' not in pg.inner_text('body'), f'{dev} {caso}: torneo interno no sale en la web (podios={pod}, directo={dire!r})')
      ok(not errs, f'{dev} {caso}: sin errores {errs}'); pg.close()
    # app: casilla en Configuración del torneo
    seed={'club/datos':{'club':{'nombre':'Olimpia'},'torneosHistorial':[{'id':'t2','nombre':'Liga','estado':'en_curso','snapshot':None}],'torneoActivoId':'t2','torneo':{'meta':{'title':'Liga','date':''},'categories':[]},'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(HTML)); pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})")
    pg.evaluate("showSection('torneo')"); pg.wait_for_timeout(500); pg.evaluate("TorneoApp.irATab('config')"); pg.wait_for_timeout(500)
    ok(pg.evaluate("estadoPublicoParaNube().torneoActivoEnWeb")==False, f'{dev}: torneo nuevo NO sale en la web por defecto')
    c=pg.locator('.torneo-enweb input'); ok(c.count()==1, f'{dev}: casilla «Mostrar este torneo en la web»'); c.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'enweb_{dev}.png')
    c.check(); pg.wait_for_timeout(400)
    ok(pg.evaluate("estadoPublicoParaNube().torneoActivoEnWeb")==True, f'{dev}: al marcarla sí se publica')
    ok(not errs, f'{dev}: sin errores app {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
