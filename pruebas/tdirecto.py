exec(open('/home/claude/test/tportadas.py').read().split("with sync_playwright() as p:")[0])
WEB=open('/home/claude/Badminton_Olimpia/index.html',encoding='utf-8').read()
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    for caso,flag in (('sin torneo en juego',False),('torneo en juego',True),('datos antiguos',None)):
      pub={'web':{'eslogan':'x'},'torneo':{'meta':{'title':'Bádminton Olimpia Torrelavega'},'categories':[]},'torneoActivoId':'t1'}
      if flag is not None: pub['torneoEnDirecto']=flag
      pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps({'publico/datos':pub})+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
      pg.goto('https://test.local/'); pg.wait_for_timeout(2000)
      hay=pg.locator('.en-directo').count()>0; area=pg.locator('#areaTorneo').is_visible()
      ok(hay==(flag is True) and area==(flag is True), f'{dev} {caso}: aviso en directo {"sí" if hay else "no"}, acceso torneo {"sí" if area else "no"}')
      ok(not errs, f'{dev} {caso}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
