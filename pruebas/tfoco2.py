import sys; sys.argv=['x']
exec(open('tform2.py').read().split('with sync_playwright() as p:')[0])
SP2=SP
from playwright.sync_api import sync_playwright
# foto de prueba: mitad izquierda roja, derecha azul (3000x2000)
from PIL import Image
im=Image.new('RGB',(3000,2000),(220,30,30)); im.paste((30,30,220),(1500,0,3000,2000)); b=io.BytesIO(); im.save(b,'JPEG',quality=90)
DU='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  br=p.chromium.launch()
  pg,errs=pagina(br,1366,860,False,seed(),admin=True)
  def r2(r):
    if r.request.url.split('?')[0].endswith('/mp4-muxer.js'): return r.fulfill(body=open('/home/claude/Badminton_Olimpia/mp4-muxer.js','rb').read(),content_type='text/javascript')
    return r.fallback()
  pg.route('**/mp4-muxer.js*',r2)
  pg.add_init_script("window.__reelCodecsPrueba={video:['vp09.00.10.08'],audio:'opus'}")
  pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500)
  res=pg.evaluate("(du)=>crearReel({id:'n1',titulo:'Prueba'},[du,du],{id:'ninguna'},()=>{},[{x:0.9,y:0.5},{x:0.1,y:0.5}]).then(r=>({t:r.blob.size,d:r.duracion})).catch(e=>'ERR '+e.message)", DU)
  ok(isinstance(res,dict) and res['t']>10000, f'reel completo con focos se crea {res}')
  ok(not errs, f'sin errores {errs[:2]}')
print('TOTAL', sum(R), '/', len(R))
