exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    for q,app in (('?fbclid=PAZXh0bgNhZW0CMTEAAabc&utm_source=ig&utm_medium=social&utm_content=link_in_bio',False),('?_t=ZN-8abc&_r=1&is_from_webapp=1&sender_device=pc',False),('?ttclid=E.C.P.abc',False),('?igsh=MXcyZ2tqZ3Rz',False),('',False),('?tiendaonline=1&fbclid=abc',True),('?publico=1',True)):
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.route('**/app.html*', lambda r: r.fulfill(body='<html>app</html>', content_type='text/html')); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':{'web':{'eslogan':'x'}}})+';')
      pg.goto('https://test.local/'+q); pg.wait_for_timeout(1500)
      url=pg.url; intro=1 if pg.evaluate("(()=>{try{return sessionStorage.getItem('introClubVisto')}catch(e){return null}})()")=='1' else 0
      if app: ok('app.html' in url, f'{dev} {q[:20]}: va a la app ({url[-40:]})')
      else: ok('app.html' not in url and intro==1, f'{dev} {q[:25] or "(sin nada)"}: abre la web con el vídeo (intro={intro})')
      pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
