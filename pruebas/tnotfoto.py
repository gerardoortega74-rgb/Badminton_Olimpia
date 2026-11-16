exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
from PIL import ImageDraw
def foto(w,h):
  im=Image.new('RGB',(w,h),(40,120,60)); d=ImageDraw.Draw(im); d.rectangle([0,0,w,int(h*0.08)],fill=(220,30,30)); b=io.BytesIO(); im.save(b,'JPEG'); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    web={'eslogan':'x','noticias':[{'id':'n1','titulo':'Medalla de bronce Cto. España','texto':'Texto largo '*60,'fecha':'2026-11-08','tieneFoto':True},
      {'id':'n2','titulo':'Otra','texto':'abc','fecha':'2026-11-01','tieneFoto':True}]}
    sd={'publico/datos':{'web':web},'club/datos/taller_fotos/web_noticia_n1':{'foto':foto(1200,1000)},'club/datos/taller_fotos/web_noticia_n2':{'foto':foto(900,1200)}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    pg.goto('https://test.local/'); pg.wait_for_timeout(3000)
    info=pg.evaluate("[...document.querySelectorAll('.noticia img')].map(i=>{const r=i.getBoundingClientRect();const cs=getComputedStyle(i);return {nw:i.naturalWidth,nh:i.naturalHeight,w:r.width,h:r.height,fit:cs.objectFit}})")
    print(dev,info)
    i0=info[0]; ok(i0['nw'] and abs(i0['w']/i0['h']-i0['nw']/i0['nh'])<0.02, f'{dev}: la foto principal se ve entera, sin recortar')
    ok(all(x['fit']=='contain' for x in info), f'{dev}: ninguna foto se recorta')
    pg.locator('.noticia').first.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
    pg.screenshot(path=SP+f'not_{dev}.png')
    ok(not errs, f'{dev}: sin errores {errs}')
  b.close()
print('TOTAL',sum(R),'/',len(R))
