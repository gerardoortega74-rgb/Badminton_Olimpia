_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import base64, io, random
from PIL import Image, ImageDraw
def foto(col):
  im=Image.new('RGB',(300,300),(255,255,255)); d=ImageDraw.Draw(im); d.ellipse((60,40,240,260),fill=col); b=io.BytesIO(); im.save(b,'JPEG'); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
random.seed(3)
def seedT(n):
  sd=seed(); arts=sd['club/datos']['taller']['articulos']
  for i in range(n): arts.append({'id':'o%d'%i,'nombre':'Artículo %d'%i,'tipo':['Grip','Mochila','Volantes'][i%3],'precio':10+i,'stock':5,'ventaOnline':True,'foto':foto((random.randint(0,255),random.randint(0,255),random.randint(0,255))),'proveedores':[]})
  sd['publico/datos']={'taller':sd['club/datos']['taller']}
  return sd
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1440,900,False,'pc')):
    for n in (4,25):
      pg,errs=pagina(b,vw,vh,mov,seedT(n))
      pg.goto('https://test.local/app.html?tiendaonline=1'); pg.wait_for_timeout(9000)
      r=pg.evaluate("""(()=>{const cs=[...document.querySelectorAll('.th-card')].filter(c=>c.offsetParent&&getComputedStyle(c).display!=='none'&&parseFloat(getComputedStyle(c).opacity)>0.7);
        const bx=cs.map(c=>c.getBoundingClientRect()); let peor=0;
        for(let i=0;i<bx.length;i++)for(let j=i+1;j<bx.length;j++){const a=bx[i],b=bx[j];const ix=Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left)),iy=Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));const f=ix*iy/Math.min(a.width*a.height,b.width*b.height);peor=Math.max(peor,f);}
        const imgs=[...document.querySelectorAll('.th-card .th-objeto img')];
        return {vis:cs.length, peor:Math.round(peor*100), capas:Math.max(...[...document.querySelectorAll('.th-card .th-objeto')].map(o=>o.querySelectorAll('img').length),0), gira:imgs.some(i=>/rotateY\\((?!0)/.test(i.style.transform)||/rotateY\\((?!0)/.test(i.parentElement.style.transform)), tilt:[...document.querySelectorAll('.th-card')].some(c=>/rotateY\\(-?[1-9]/.test(c.style.transform))};})()""")
      ok(r['capas']<=1, f'{dev} {n} artículos: sin extrusión (capas por artículo {r["capas"]})')
      ok(not r['gira'] and not r['tilt'], f'{dev} {n}: los artículos no giran')
      ok(r['peor']<=35, f'{dev} {n}: los de delante no se amontonan (solape máximo {r["peor"]}%, visibles {r["vis"]})')
      pg.screenshot(path=SP+f'carrt_{dev}_{n}.png')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev} {n}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
