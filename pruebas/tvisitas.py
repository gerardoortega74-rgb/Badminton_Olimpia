exec(open('/home/claude/test/tportadas.py').read().split("with sync_playwright() as p:")[0])
import datetime
WEB=open('/home/claude/Badminton_Olimpia/index.html',encoding='utf-8').read()
CLAVES={'pagina','dia','hora','disp','origen','interno','secciones','clics','segundos','creado'}
def visitas(pg): return pg.evaluate("Object.entries(window.__STORE).filter(([k])=>k.startsWith('visitas/')).map(([k,v])=>v)")
def regla(d): return set(d)==CLAVES and isinstance(d['secciones'],list) and len(d['secciones'])<=15 and isinstance(d['clics'],list) and len(d['clics'])<=25 and all(isinstance(x,str) and len(x)<=30 for x in d['clics']) and isinstance(d['segundos'],int) and 0<=d['segundos']<=7200 and len(d['origen'])<=40 and d['disp'] in ('movil','pc','tablet')
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    # 1. web: visita normal
    pub={'web':{'eslogan':'x'}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,user_agent=('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148' if mov else None)); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':pub})+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    pg.goto('https://test.local/?x'.replace('?x','')); pg.wait_for_timeout(2000)
    v=visitas(pg); ok(len(v)==1 and v[0]['pagina']=='web' and v[0]['interno']==False and v[0]['disp']==('movil' if mov else 'pc'), f'{dev}: cuenta la visita a la web {v and {k:v[0][k] for k in ("pagina","disp","interno","origen")}}')
    pg.evaluate("document.getElementById('horarios').scrollIntoView()"); pg.wait_for_timeout(500)
    pg.evaluate("document.getElementById('contacto').scrollIntoView()"); pg.wait_for_timeout(500)
    if mov: pg.evaluate("document.querySelector('#contacto a, #contacto button') && 0")
    pg.locator('#zona a').first.evaluate("a=>{a.addEventListener('click',e=>e.preventDefault(),{once:true});a.click()}"); pg.wait_for_timeout(4800)
    d=visitas(pg)[0]
    ok('inicio' in d['secciones'] and 'horarios' in d['secciones'] and 'contacto' in d['secciones'], f'{dev}: apunta las partes vistas {d["secciones"]}')
    ok(len(d['clics'])>=1, f'{dev}: apunta lo que pulsa {d["clics"]}')
    ok(regla(d), f'{dev}: cumple la regla de Firebase {sorted(d)}')
    ok(pg.locator('#avisoCookies').count()==0, f'{dev}: sin Google Analytics configurado no hay aviso de cookies')
    ok(not errs, f'{dev}: sin errores {errs}'); pg.close()
    # 2. dispositivo del club
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov)
    pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':pub})+';localStorage.setItem("badmintonClubGlobal","{}");try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    pg.goto('https://test.local/'); pg.wait_for_timeout(1500)
    ok(visitas(pg)[0]['interno']==True, f'{dev}: las visitas desde un aparato del club se marcan como propias'); pg.close()
    # 3. Google Analytics con permiso
    for elec in ('Rechazar','Aceptar'):
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':{'web':{'gaId':'G-ABC123XYZ'}}})+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
      pg.goto('https://test.local/'); pg.wait_for_timeout(1500)
      ok(pg.locator('#avisoCookies').is_visible(), f'{dev}: con Google Analytics sale el aviso de cookies')
      ok(pg.evaluate("!document.querySelector('script[src*=googletagmanager]')"), f'{dev}: no carga Google antes de aceptar')
      pg.click(f'#avisoCookies button:has-text("{elec}")'); pg.wait_for_timeout(400)
      carg=pg.evaluate("!!document.querySelector('script[src*=\"googletagmanager.com/gtag/js?id=G-ABC123XYZ\"]')")
      ok(carg==(elec=='Aceptar') and pg.locator('#avisoCookies').count()==0, f'{dev}: {elec}: Google {"cargado" if carg else "no cargado"}')
      pg.reload(); pg.wait_for_timeout(1500)
      ok(pg.locator('#avisoCookies').count()==0, f'{dev}: {elec}: no vuelve a preguntar')
      ok(pg.locator('#linkCookies').is_visible(), f'{dev}: enlace «Preferencias de cookies» en el pie')
      ok(not errs, f'{dev} GA {elec}: sin errores {errs}'); pg.close()
    # 4. páginas de la app para clientes
    for q,pag in (('tiendaonline=1','tienda'),('raqueta=1','raqueta'),('tallerpublico=1&pedido=x','seguimiento')):
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(HTML)); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':{'web':{}},'club/datos':{'club':{'nombre':'Olimpia'}}})+';')
      pg.goto('https://test.local/app.html?'+q); pg.wait_for_timeout(2500)
      v=visitas(pg); ok(len(v)==1 and v[0]['pagina']==pag and regla(v[0]), f'{dev}: cuenta la visita a {pag}')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev} {pag}: sin errores {errs}'); pg.close()
    # 5. panel de visitas en la app
    hoy=datetime.date.today(); dd=lambda n:(hoy-datetime.timedelta(n)).isoformat()
    sd={'club/datos':{'club':{'nombre':'Olimpia','web':{}}}}
    vs=[('web',0,'movil','google',['inicio','horarios'],['Inscripción'],False),('web',0,'pc','directo',['inicio'],[],False),('tienda',1,'movil','instagram',[],['Pedir por WhatsApp'],False),
        ('raqueta',3,'movil','whatsapp',[],['Enviar','Formulario enviado'],False),('web',10,'pc','directo',['inicio','contacto'],[],False),('web',0,'pc','directo',['inicio'],[],True),('web',45,'pc','directo',['inicio'],[],False)]
    for i,(pg_,n,dsp,ori,sec,cl,inter) in enumerate(vs): sd['visitas/v%d'%i]={'pagina':pg_,'dia':dd(n),'hora':18,'disp':dsp,'origen':ori,'interno':inter,'secciones':sec,'clics':cl,'segundos':90,'creado':0}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(HTML)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"u",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1500)
    t=pg.inner_text('#webVisitas')
    tarj=pg.evaluate("[...document.querySelectorAll('.vis-tarj b')].map(b=>b.textContent)")
    ok(tarj[:3]==['5','2','1'], f'{dev}: 30 días: 5 visitas, 2 hoy, 1 ayer (sin las del club ni las de hace 45 días) {tarj}')
    ok('Google' in t and 'Instagram' in t and 'Horarios' in t and 'Tienda online' in t and 'Inscripción' in t, f'{dev}: páginas, partes vistas, clics y origen')
    pg.check('#visInternas'); pg.wait_for_timeout(800)
    ok(pg.evaluate("document.querySelector('.vis-tarj b').textContent")=='6', f'{dev}: contando las del club: 6')
    pg.select_option('#visDias','90'); pg.wait_for_timeout(800)
    ok(pg.evaluate("document.querySelector('.vis-tarj b').textContent")=='7', f'{dev}: 90 días: 7')
    pg.locator('.vis-panel').screenshot(path=SP+f'visitas_{dev}.png')
    pg.fill('#webGaId','g-abc123xyz'); pg.click('#webGaGuardar'); pg.wait_for_timeout(300)
    ok(pg.evaluate("webCfg().gaId")=='G-ABC123XYZ' and pg.evaluate("datosWebPublicos().gaId")=='G-ABC123XYZ', f'{dev}: guarda el código de Google Analytics')
    pg.fill('#webGaId','hola'); pg.click('#webGaGuardar'); ok('tiene que ser' in pg.inner_text('#webGaMsg'), f'{dev}: avisa si el código está mal')
    ok(pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1"), f'{dev}: sin desbordar')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: panel sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
