_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import io, random
from PIL import Image, ImageDraw, ImageFilter
random.seed(3)
def foto(fondo, ruido=10, objeto=(215,40,50), hueco=False):
  im=Image.new('RGB',(500,640),fondo); px=im.load()
  for y in range(640):
    for x in range(500):
      d=random.randint(-ruido,ruido); px[x,y]=tuple(max(0,min(255,c+d+ (y//80 if fondo[0]<100 else 0))) for c in fondo)
  dr=ImageDraw.Draw(im); dr.ellipse((140,90,360,400),fill=objeto); dr.rectangle((235,400,265,580),fill=(240,240,235) if fondo[0]<100 else (30,30,30))
  if hueco: dr.ellipse((200,170,300,300),fill=fondo)
  im=im.filter(ImageFilter.GaussianBlur(0.6)); bf=io.BytesIO(); im.save(bf,'JPEG',quality=85); return 'data:image/jpeg;base64,'+base64.b64encode(bf.getvalue()).decode()
CASOS={'oscuro':(foto((22,22,26)),'oscuro',True),'negro puro':(foto((0,0,0),0),'oscuro',True),'oscuro azulado':(foto((14,20,38),8),'oscuro',True),'claro':(foto((244,244,242),6),'claro',True),'gris medio':(foto((128,128,128),6),'claro',False),
       'oscuro con objeto negro':(foto((235,235,235),5,objeto=(15,15,15)),'claro',True)}
JS="""async([src])=>{let tipo='';const r=await tdoRecortarFondo(src,'t'+Math.random(),{max:700,calidad:.82,oscuro:'auto',alDetectar:t=>tipo=t});
 const im=new Image();await new Promise(o=>{im.onload=o;im.src=r});const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);
 const a=(x,y)=>g.getImageData(x,y,1,1).data[3];return {tipo,igual:r===src,esq:[a(3,3),a(im.width-4,3),a(3,im.height-4),a(im.width-4,im.height-4)],centro:a(250,250),mango:a(250,500),png:r}}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  pg,errs=pagina(b,1366,700,False,json.loads(json.dumps(seed())),admin=True)
  pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
  hoja=Image.new('RGB',(len(CASOS)*260,2*340),'#888')
  for n,(nom,(src,tipo,quita)) in enumerate(CASOS.items()):
    r=pg.evaluate(JS,[src])
    if quita: ok(r['tipo']==tipo and not r['igual'] and max(r['esq'])<=10 and r['centro']>=250 and r['mango']>=250, f'{nom}: detecta fondo {tipo}, lo quita y deja el artículo entero {r["tipo"]} esq={r["esq"]} centro={r["centro"]} mango={r["mango"]}')
    else: ok(r['igual'], f'{nom}: no toca la foto')
    o=Image.open(io.BytesIO(base64.b64decode(src.split(',')[1]))).resize((250,320)); hoja.paste(o,(n*260,0))
    if not r['igual']:
      q=Image.open(io.BytesIO(base64.b64decode(r['png'].split(',')[1]))).convert('RGBA').resize((250,320)); fd=Image.new('RGBA',(250,320),(60,160,90,255)); fd.alpha_composite(q); hoja.paste(fd.convert('RGB'),(n*260,340))
  hoja.save(SP+'fondo_casos.png')
  # sin 'auto' (lo que usa la tienda al pintar): todo como antes
  r=pg.evaluate("async([src])=>{const r=await tdoRecortarFondo(src,'z'+Math.random(),{max:420});return r===src}",[CASOS['oscuro'][0]]); ok(r, 'en la tienda (sin auto) una foto de fondo oscuro no se toca')
  ok(not [e for e in errs if 'hasPending' not in e], f'sin errores {errs}'); pg.close(); b.close()
print('TOTAL',sum(R),'/',len(R))
# ---- en la app: botón «✂️ Quitar fondo» de un artículo con foto de fondo oscuro ----
R2=[]
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    sd=json.loads(json.dumps(seed())); sd['club/datos']['taller']['articulos'].append({'id':'mo1','nombre':'Mochila Prueba','codigo':'M1','stock':3,'precio':30,'unidad':'unidades','tipo':'articulo','foto':CASOS['oscuro'][0]})
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True); pg.on('dialog',lambda d:d.accept())
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(400)
    pg.evaluate("showSection('taller'); TallerApp.irAAlmacen('articulos')"); pg.wait_for_timeout(900)
    bt=pg.locator('button',has_text='Quitar fondo')
    if bt.count()==0: pg.locator('tr',has_text='Mochila Prueba').locator('td.c-ed button').first.click(); pg.wait_for_timeout(700); bt=pg.locator('button',has_text='Quitar fondo')
    ok(bt.count()>=1, f'{dev}: botón «Quitar fondo» en la ficha del artículo ({bt.count()})')
    if bt.count():
      bt.first.scroll_into_view_if_needed(); bt.first.click(); pg.wait_for_timeout(1500)
      t=pg.inner_text('#tallerModalRoot'); ok('He quitado el fondo oscuro' in t, f'{dev}: avisa de que ha quitado el fondo oscuro')
      pg.screenshot(path=SP+f'fondo_modal_{dev}.png')
      pg.locator('#tallerModalRoot button',has_text='Usar sin fondo').click(); pg.wait_for_timeout(800)
      f=pg.evaluate("TallerApp.getState().articulos.find(a=>a.id==='mo1').foto.slice(0,16)"); ok(f.startswith('data:image/webp') or f.startswith('data:image/png'), f'{dev}: la foto queda guardada transparente ({f})')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
