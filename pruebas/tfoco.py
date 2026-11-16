import sys; sys.argv=['x']
exec(open('tform2.py').read().split('with sync_playwright() as p:')[0])
SP2=SP
from playwright.sync_api import sync_playwright
# foto de prueba: mitad izquierda roja, derecha azul (3000x2000)
from PIL import Image
im=Image.new('RGB',(3000,2000),(220,30,30)); im.paste((30,30,220),(1500,0,3000,2000)); b=io.BytesIO(); im.save(b,'JPEG',quality=90)
DU='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
with sync_playwright() as p:
  br=p.chromium.launch()
  for vw,vh,dev in ((390,844,'mov'),(1366,860,'pc')):
    mov=dev=='mov'
    pg,errs=pagina(br,vw,vh,mov,seed(),admin=True)
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(1500)
    pg.evaluate("(du)=>{window.fotosDeNoticia=()=>Promise.resolve([du,du,du]); abrirPublicarRedes({id:'n1',titulo:'Prueba foco',texto:'x'},()=>{});}", DU); pg.wait_for_timeout(1500)
    n=pg.locator('.rd-foco').count(); ok(n==3, f'{dev}: salen las 3 fotos para elegir foco ({n})')
    caj=pg.locator('.rd-foco').nth(0); caj.scroll_into_view_if_needed(); bb=caj.bounding_box()
    m0=pg.evaluate("document.querySelector('.rd-foco .rd-foco-marco').style.left")
    if mov: pg.touchscreen.tap(bb['x']+bb['width']*0.92, bb['y']+bb['height']*0.5)
    else: pg.mouse.click(bb['x']+bb['width']*0.92, bb['y']+bb['height']*0.5)
    pg.wait_for_timeout(300)
    f=pg.evaluate("FOCOS_REEL['n1'][0]"); m1=pg.evaluate("document.querySelector('.rd-foco .rd-foco-marco').style.left")
    ok(f and f['x']>0.85, f'{dev}: tocar guarda el foco a la derecha {f}')
    ok(m0!=m1 and float(m1.rstrip('%'))>50, f'{dev}: el recuadro se mueve ({m0} -> {m1})')
    pg.screenshot(path=SP2+f'foco_{dev}.png', full_page=False)
    # dibujo real: centro del fotograma
    col=pg.evaluate("""(du)=>new Promise(res=>{const im=new Image();im.onload=()=>{const c=document.createElement('canvas');c.width=REEL.ancho;c.height=REEL.alto;const x=c.getContext('2d');
      const out=[];for(const fx of [0.1,0.5,0.9]){im.focoReel={x:fx,y:0.5};dibujarFotoReel(x,im,1,3,0);out.push([...x.getImageData(540,960,1,1).data].slice(0,3));
      // bordes sin negro
      out.push([...x.getImageData(0,0,1,1).data][3],[...x.getImageData(1079,1919,1,1).data][3]);}res(out);};im.src=du;})""", DU)
    ok(col[0][0]>150 and col[0][2]<100, f'{dev}: foco izquierda -> centro rojo {col[0]}')
    ok(col[6][2]>150 and col[6][0]<100, f'{dev}: foco derecha -> centro azul {col[6]}')
    ok(all(a==255 for a in (col[1],col[2],col[4],col[5],col[7],col[8])), f'{dev}: sin bordes vacíos')
    ok(not errs, f'{dev}: sin errores JS {errs[:2]}')
    pg.close()
  br.close()
print('TOTAL', sum(R), '/', len(R))
