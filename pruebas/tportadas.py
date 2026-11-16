import json, io, os, time
from playwright.sync_api import sync_playwright
from PIL import Image
SP='/tmp/claude-0/-home-claude/3cdf04c3-6017-5b52-901b-0b83f0325f3c/scratchpad/'
HTML=open('/home/claude/Badminton_Olimpia/app.html',encoding='utf-8').read()
WEB=open('/home/claude/Badminton_Olimpia/index.html',encoding='utf-8').read()
MOCK=open('/home/claude/test/mockfb.js').read()
R=[]
def ok(c,m): R.append(bool(c)); print('OK ' if c else 'FALLO', m, flush=True)
def jpg(col,name):
  im=Image.new('RGB',(1600,900),col); b=io.BytesIO(); im.save(b,'JPEG'); open(SP+name,'wb').write(b.getvalue())
jpg((200,40,40),'p_roja.jpg'); jpg((40,160,60),'p_verde.jpg')
import base64
def durl(col):
  im=Image.new('RGB',(320,180),col); b=io.BytesIO(); im.save(b,'JPEG'); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
STOCK=Image.new('RGB',(64,36),(90,90,200)); bb=io.BytesIO(); STOCK.save(bb,'JPEG'); STOCKJPG=bb.getvalue()
def ruta(html):
  def route(r):
    u=r.request.url
    if 'firebase-app-compat' in u: return r.fulfill(body=MOCK,content_type='text/javascript')
    if 'images.unsplash.com' in u: return r.fulfill(body=STOCKJPG,content_type='image/jpeg')
    if u.endswith('.js') or '.mp4' in u or 'gstatic' in u or 'jsdelivr' in u or 'cdnjs' in u or 'googleapis' in u: return r.fulfill(status=404,body='')
    if u.startswith('https://test.local/'): return r.fulfill(body=html,content_type='text/html')
    return r.abort()
  return route
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    seed={'club/datos':{'club':{'nombre':'Olimpia','web':{'eslogan':'El deporte de raqueta más rápido, en Torrelavega','tienePortada':True}},'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}},
          'club/datos/taller_fotos/web_portada':{'foto':durl((250,200,0))}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('dialog',lambda d: d.accept())
    pg.route('**/*',ruta(HTML))
    pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1200)
    cards=pg.locator('.web-port')
    ok(cards.count()==3, f'{dev}: salen la foto propia antigua y las 2 de ejemplo ({cards.count()})')
    ok(pg.locator('.web-port.oculta').count()==0, f'{dev}: las 3 se ven en la web')
    with pg.expect_file_chooser() as fc: pg.click('.web-port-anadir')
    fc.value.set_files([SP+'p_roja.jpg',SP+'p_verde.jpg']); pg.wait_for_timeout(2500)
    ok(pg.locator('.pw-fondo').is_visible(), f'{dev}: al subir se abre la prueba de cómo queda')
    ok(pg.locator('.pw-marco.pc').is_visible() and pg.locator('.pw-marco.movil').is_visible() and 'RÁPIDO' in pg.inner_text('.pw-marco.pc').upper(), f'{dev}: prueba en ordenador y móvil con la frase')
    pg.screenshot(path=SP+f'port_prev_{dev}.png')
    pg.click('.pw-poner'); pg.wait_for_timeout(500)
    st=pg.evaluate("webCfg().portadas.map(p=>[p.id,p.tipo,p.visible])")
    ok(len(st)==5 and [x[1] for x in st]==['propia','propia','propia','ejemplo','ejemplo'], f'{dev}: 2 nuevas delante de las de ejemplo {st}')
    ok(st[1][2]==False and st[2][2]==True, f'{dev}: la nueva entra «en prueba» y la que pusiste en la web queda visible')
    ok(pg.locator('.web-port.oculta').count()==1, f'{dev}: una sigue en prueba')
    docs=pg.evaluate("Object.keys(window.__STORE).filter(k=>k.startsWith('club/datos/taller_fotos/web_portada_'))")
    ok(len(docs)==2, f'{dev}: fotos guardadas en la nube ({len(docs)})')
    # probar desde la tarjeta
    pg.locator('.web-port').nth(1).locator('button[title="Probar cómo queda"]').click(); pg.wait_for_timeout(300)
    ok(pg.locator('.pw-fondo').is_visible(), f'{dev}: 👁️ abre la prueba'); pg.locator('.pw-cab button').click()
    # ocultar ejemplo 1
    pg.locator('.web-port').nth(3).locator('.web-port-ver').click(); pg.wait_for_timeout(300)
    ok(pg.evaluate("webCfg().portadas[3].visible")==False, f'{dev}: ocultar una de ejemplo')
    ok(pg.locator('.web-port').nth(3).locator('.web-port-quitar').count()==0, f'{dev}: las de ejemplo no se borran, solo se ocultan')
    # mover: la verde (en prueba, pos 2) a la izquierda
    idv=pg.evaluate("webCfg().portadas[1].id"); pg.locator('.web-port').nth(1).locator('button[title="Antes"]').click(); pg.wait_for_timeout(300)
    ok(pg.evaluate("webCfg().portadas[0].id")==idv, f'{dev}: ◀ cambia el orden')
    # quitar la antigua
    pg.locator('.web-port[data-id="antigua"] .web-port-quitar').click(); pg.wait_for_timeout(500)
    ok(pg.locator('.web-port').count()==4 and not pg.evaluate("Object.keys(window.__STORE).includes('club/datos/taller_fotos/web_portada')") and pg.evaluate("webCfg().tienePortada")==False, f'{dev}: 🗑️ quita la foto y la borra de la nube')
    ok(pg.evaluate("datosWebPublicos().portadas.length")==4, f'{dev}: la lista va a la web')
    pg.locator('#webPortadas').screenshot(path=SP+f'port_lista_{dev}.png')
    ok(pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1"), f'{dev}: sin desbordar')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}')
    portadas=pg.evaluate("webCfg().portadas"); fotos={k:v for k,v in pg.evaluate("window.__STORE").items() if 'web_portada_' in k}
    pg.close()
    # ---------- la web ----------
    for caso in ('normal','todas_ocultas','antigua'):
      if caso=='normal': web={'eslogan':'x','portadas':portadas}
      elif caso=='todas_ocultas': web={'eslogan':'x','portadas':[dict(x,visible=False) for x in portadas]}
      else: web={'eslogan':'x','tienePortada':True}
      sd={'publico/datos':{'web':web}}; sd.update(fotos); sd['club/datos/taller_fotos/web_portada']={'foto':durl((250,200,0))}
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
      pg.goto('https://test.local/'); pg.wait_for_timeout(2500)
      src=pg.evaluate("[...document.querySelectorAll('#diapos .diapo')].map(d=>d.style.backgroundImage.slice(5,40))")
      if caso=='normal':
        esperado=[x for x in portadas if x['visible']]
        tipos=['unsplash' if 'unsplash' in s_ else 'data' for s_ in src]
        ok(len(src)==len(esperado) and tipos==['unsplash' if x['tipo']=='ejemplo' else 'data' for x in esperado], f'web {dev}: salen solo las visibles y en su orden {tipos} vs {[x["tipo"] for x in esperado]}')
        ok(pg.locator('#puntos button').count()==(len(esperado) if len(esperado)>1 else 0), f'web {dev}: puntos del pase')
      elif caso=='todas_ocultas':
        ok(len(src)==2 and all('unsplash' in x for x in src), f'web {dev}: si ocultas todas, pone las de ejemplo')
      else:
        ok(len(src)==3 and 'data' in src[0], f'web {dev}: webs antiguas sin lista siguen igual (propia primero) {src}')
      ok(not errs, f'web {dev} {caso}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
