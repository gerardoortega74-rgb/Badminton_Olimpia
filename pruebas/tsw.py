import subprocess,time,json,sys
from playwright.sync_api import sync_playwright
MOCK=open('/home/claude/test/mockfb.js').read()
srv=subprocess.Popen([sys.executable,'-m','http.server','8765','--bind','127.0.0.1'],cwd='/home/claude/Badminton_Olimpia',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
R=[]
def ok(c,m): R.append(bool(c)); print(('OK  ' if c else 'FALLO ')+m)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844})
    def rt(r):
      u=r.request.url
      if 'firebase-app-compat' in u: return r.fulfill(body=MOCK,content_type='text/javascript')
      if 'localhost:8765' in u: return r.fallback()
      return r.fulfill(status=404,body='')
    ctx.route('**/*',rt)
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    for pag in ('app.html?raqueta=1','index.html','app.html'):
      pg.goto('http://localhost:8765/'+pag); pg.wait_for_timeout(2500)
    ok(pg.evaluate("navigator.serviceWorker.getRegistration().then(r=>!!(r&&r.active))"), 'el service worker se instala')
    ks=pg.evaluate("caches.open('olimpia-v1').then(c=>c.keys()).then(k=>k.map(x=>new URL(x.url).pathname))"); print(ks)
    ok('/app.html' in ks and '/index.html' in ks, 'guarda la app y la web en caché')
    ok(not any('.mp4' in k for k in ks), 'no guarda los vídeos')
    srv.terminate(); srv.wait(); ctx.set_offline(True)
    for pag,sel in (('app.html','meta[name="build-id"]'),('app.html?raqueta=1','#tallerPublicoScreen'),('index.html','.portada')):
      try:
        pg.goto('http://localhost:8765/'+pag,timeout=15000); pg.wait_for_timeout(1500); n=pg.locator(sel).count()
      except Exception as e: n=0; print(str(e)[:120])
      ok(n>=1, f'sin conexión abre {pag}')
    m=json.load(open('/home/claude/Badminton_Olimpia/manifest.webmanifest')); ok(m['start_url']=='app.html' and len(m['icons'])==2, 'manifest correcto')
    print('errores',errs[:3]); b.close()
finally:
  try: srv.terminate()
  except Exception: pass
print('TOTAL',sum(R),'/',len(R))
