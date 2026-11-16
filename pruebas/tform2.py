import json, time, base64, io, sys
from playwright.sync_api import sync_playwright
SP='/tmp/claude-0/-home-claude/3cdf04c3-6017-5b52-901b-0b83f0325f3c/scratchpad/'
HTML=open('/home/claude/Badminton_Olimpia/app.html',encoding='utf-8').read()
MOCK=open('/home/claude/test/mockfb.js').read()
R=[]
def ok(c,m): R.append(bool(c)); print('OK ' if c else 'FALLO', m, flush=True)
AHORA=int(time.time()*1000)
def art(i,n,cod,st,**k): d={'id':i,'nombre':n,'codigo':cod,'tipo':'Cordaje','esCordaje':True,'precio':15,'stock':st,'unidad':'metros','proveedores':[]}; d.update(k); return d
ARTS=[art('s088','CORDAJE TOPO PA2055 (0,68mm) · ROJO','S088',40),art('s126','CORDAJE TOPO PA2055 (0,68mm) · ROSA','S126',30),
 art('s123','CORDAJE TOPO PA2055 (0,68mm) · ROSA-BLANCO','S123',20),art('s151','Cordaje Topo PA2055 (0,68mm) Morado','S151',10),
 art('s999','CORDAJE TOPO PA2055 (0,68mm) · NEGRO','S999',0),
 art('s154','U-Power Z63 (0,63mm) Blanco (Tmax 12.7Kg)','S154',25,precio=18),
 art('y1','Yonex BG65 · Blanco','Y65',30,grupoId='gY',grupoNombre='Yonex BG65',color='Blanco',precio=12),
 art('y2','Yonex BG65 · Negro','Y65',30,grupoId='gY',grupoNombre='Yonex BG65',color='Negro',precio=12)]
def seed(sol=None):
  taller={'clientes':[{'id':'c1','nombre':'Lucía Herrera','telefono':'600111222'}],'articulos':ARTS,'pedidos':[
    {'id':'pA','clienteId':'c1','marcaModelo':'Antigua','cordajeId':'y1','tensionVertical':11,'tensionHorizontal':11,'precio':24,'estado':'pendiente','horaLlegada':AHORA-30*60000,'horaInicio':None,'horaFin':None,'notas':'','pagado':False,'pagoPrevisto':'alRecoger','articulosAdicionales':[],'aplazado':False}],
    'config':{'nombreTaller':'IDERMAY CANTABRIA','precioBaseEncordado':12,'precioSinCordaje':12,'telefonoTienda':'600000000'}}
  s={'club/datos':{'taller':taller},'publico/datos':{'taller':taller}}
  for k,v in (sol or {}).items(): s['solicitudes_raqueta/'+k]=v
  return s
def pagina(b,vw,vh,mov,sd,admin=False):
  pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
  def route(r):
    u=r.request.url
    if 'firebase-app-compat' in u: return r.fulfill(body=MOCK,content_type='text/javascript')
    if u.endswith('.js') or '.mp4' in u or 'gstatic' in u or 'jsdelivr' in u or 'cdnjs' in u: return r.fulfill(status=404,body='')
    if u.startswith('https://test.local/'):
      import os
      pth=u.split('test.local/')[1].split('?')[0]
      if (pth.endswith('.webp') or pth.endswith('.png')) and os.path.exists('/home/claude/Badminton_Olimpia/'+pth): return r.fulfill(body=open('/home/claude/Badminton_Olimpia/'+pth,'rb').read(),content_type='image/webp' if pth.endswith('.webp') else 'image/png')
      return r.fulfill(body=HTML,content_type='text/html')
    return r.abort()
  pg.route('**/*',route)
  pg.add_init_script('window.__SEED='+json.dumps(sd)+';'+('window.__USER={email:"idermaycantabria@gmail.com",uid:"uadm",emailVerified:true};' if admin else '')+'window.open=(u)=>{window.__abierto=u;return null};')
  return pg,errs
# foto de prueba (JPEG generado)
from PIL import Image
import os; im=Image.frombytes('RGB',(3000,2000),os.urandom(3000*2000*3)); buf=io.BytesIO(); im.save(buf,'JPEG',quality=95); JPG=buf.getvalue()
open(SP+'raq.jpg','wb').write(JPG)
CLAVES=['nombre','apellidos','telefono','raqueta','cordajeId','cordajeNombre','color','cordajeIdH','cordajeNombreH','colorH','tension','tensionH','pretensado','foto','comentarios','consentimiento','creadoEn']
def regla_ok(d):
  S=lambda k,mx,mn=0: isinstance(d.get(k),str) and mn<=len(d[k])<=mx
  N=lambda k: isinstance(d.get(k),(int,float)) and not isinstance(d.get(k),bool) and 0<=d[k]<=20
  return (set(d)<=set(CLAVES) and d.get('consentimiento') is True and S('nombre',60,1) and S('apellidos',80) and S('telefono',20,9) and S('raqueta',80)
    and S('cordajeId',60) and S('cordajeNombre',120) and S('color',40) and S('cordajeIdH',60) and S('cordajeNombreH',120) and S('colorH',40)
    and N('tension') and N('tensionH') and isinstance(d.get('pretensado'),bool) and S('comentarios',300) and isinstance(d.get('creadoEn'),(int,float))
    and ('foto' not in d or (isinstance(d['foto'],str) and len(d['foto'])<700000)))
docs=lambda pg: pg.evaluate("Object.entries(window.__STORE).filter(([k])=>k.startsWith('solicitudes_raqueta/')).map(([k,v])=>v)")
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,dev in ((390,844,'mov'),(1366,860,'pc')):
    mov=dev=='mov'
    pg,errs=pagina(b,vw,vh,mov,seed())
    pg.goto('https://test.local/app.html?raqueta=1'); pg.wait_for_timeout(3000)
    ok(pg.locator('#tallerPublicoScreen h1').inner_text()=='Deja tu raqueta', f'{dev}: abre el formulario')
    opc=pg.evaluate("[...document.querySelectorAll('.tpf-opc')].map(b=>[b.querySelector('b').textContent,(b.querySelector('small')||{}).textContent||'',b.dataset.grupo])")
    noms=[o[0] for o in opc]
    topo=[o for o in opc if 'PA2055' in o[0].upper()]
    ok(len(topo)==1 and '4 colores' in topo[0][1], f'{dev}: los TOPO PA2055 sueltos salen como UN cordaje con 4 colores -> {topo}')
    ok(any('U-Power Z63' in n for n in noms) and any(n=='Yonex BG65' for n in noms) and 'Aconséjame tú' in noms, f'{dev}: resto de cordajes bien -> {noms}')
    pg.locator('.tpf-opc', has_text='PA2055').click(); pg.wait_for_timeout(200)
    cols=pg.evaluate("[...document.querySelectorAll('.tpf-color')].map(e=>e.dataset.color)")
    ok(sorted(cols)==['Morado','Rojo','Rosa','Rosa-Blanco'], f'{dev}: colores con stock (sin Negro agotado) -> {cols}')
    # foto: botones
    ok(pg.locator('#frmFotoBtnCamara').is_visible() and pg.locator('#frmFotoBtnGaleria').is_visible(), f'{dev}: botones «Hacer foto» y «Elegir foto» debajo de raqueta')
    y_raq=pg.locator('#frmRaqueta').bounding_box()['y']; y_foto=pg.locator('#frmFotoBtnCamara').bounding_box()['y']
    ok(y_foto>y_raq, f'{dev}: la foto va debajo del campo raqueta')
    ok(pg.get_attribute('#frmFotoCamara','capture')=='environment' and pg.get_attribute('#frmFotoGaleria','capture') is None, f'{dev}: uno abre la cámara y el otro la galería')
    with pg.expect_file_chooser() as fc: pg.click('#frmFotoBtnGaleria')
    fc.value.set_files(SP+'raq.jpg'); pg.wait_for_timeout(1500)
    ok(pg.locator('#frmFotoPrev').is_visible(), f'{dev}: se ve la foto elegida')
    pg.click('#frmFotoQuitar'); pg.wait_for_timeout(200)
    ok(pg.locator('#frmFotoPrev').count()==0, f'{dev}: «Quitar» la quita')
    # pegar foto (Ctrl+V)
    b64=base64.b64encode(JPG).decode()
    pg.evaluate("""(b)=>{const bin=atob(b);const u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
      const f=new File([u],'p.jpg',{type:'image/jpeg'});const dt=new DataTransfer();dt.items.add(f);
      document.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true}));}""", b64); pg.wait_for_timeout(1500)
    ok(pg.locator('#frmFotoPrev').is_visible(), f'{dev}: pegar una foto copiada funciona')
    # datos
    pg.fill('#frmNombre','Héctor'); pg.fill('#frmApellidos','Tovar'); pg.fill('#frmTelefono','612345678'); pg.fill('#frmRaqueta','Yonex Nanoflare 800')
    pg.click('.tpf-color[data-color="Rosa-Blanco"]'); pg.fill('#frmTensionV','11,1'); pg.locator('#frmTensionV').blur(); pg.wait_for_timeout(100)
    ok(pg.input_value('#frmTensionH')=='11,1', f'{dev}: la horizontal se rellena igual')
    ok('24,5 lb' in pg.inner_text('#frmTensionVLb'), f'{dev}: muestra las libras {pg.inner_text("#frmTensionVLb")}')
    pg.fill('#frmTensionH','12.00'); pg.locator('#frmTensionH').blur(); pg.wait_for_timeout(100)
    ok(pg.input_value('#frmTensionH')=='12,00', f'{dev}: acepta punto y deja 12,00 tal cual -> {pg.input_value("#frmTensionH")}')
    ok(pg.locator('#frmPretensado').is_visible(), f'{dev}: casilla de pretensado')
    pg.check('#frmPretensado'); pg.check('#frmConsent')
    ok(pg.locator('#frmFotoPrev').is_visible() and pg.input_value('#frmNombre')=='Héctor', f'{dev}: foto y datos se mantienen al elegir opciones')
    pg.screenshot(path=SP+f'f2_{dev}.png',full_page=True)
    pg.click('#frmEnviar'); pg.wait_for_timeout(900)
    d=(docs(pg) or [{}])[0]
    ok(d.get('cordajeId')=='s123' and d.get('color')=='Rosa-Blanco' and d.get('pretensado') is True and d.get('tension')==11.1 and d.get('tensionH')==12, f'{dev}: guarda cordaje Rosa-Blanco, tensiones y pretensado')
    ok(d.get('foto','').startswith('data:image/jpeg') and len(d.get('foto',''))<600001, f'{dev}: foto comprimida ({len(d.get("foto",""))//1024} KB)')
    ok(regla_ok(d), f'{dev}: cumple la regla de Firebase')
    ok('pretensado' in pg.inner_text('#tallerPublicoScreen').lower(), f'{dev}: el resumen dice pretensado')
    ok(pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1"), f'{dev}: sin desbordar')
    ok(not errs, f'{dev}: sin errores {errs}'); pg.close()
    # ---- taller: aceptar con foto y pretensado ----
    sol={'s1':dict(d, creadoEn=AHORA-10*60000)}
    pg,errs=pagina(b,vw,vh,mov,seed(sol),admin=True)
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(900)
    t=pg.inner_text('#imSolicitudes') if pg.locator('#imSolicitudes').count() else ''
    ok('pretensado' in t and pg.locator('.im-solic-foto').count()==1, f'{dev}: en la Cola se ve pretensado y la foto')
    pg.locator('.im-solic-card').locator('button', has_text='Aceptar').click(); pg.wait_for_timeout(800)
    pp=pg.evaluate("TallerApp.getState().pedidos.find(p=>p.marcaModelo==='Yonex Nanoflare 800')") or {}
    ok(pp.get('pretensado') is True and (pp.get('fotoAntes') or '').startswith('data:image/jpeg') and pp.get('cordajeId')=='s123', f'{dev}: pedido con pretensado, foto y cordaje')
    ok(pg.evaluate("Object.keys(window.__STORE).some(k=>k.startsWith('club/datos/taller_fotos/'))"), f'{dev}: la foto se guarda en las fotos del taller')
    ok(not errs, f'{dev}: taller sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
