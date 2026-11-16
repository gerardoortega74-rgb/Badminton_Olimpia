exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    seed={'club/datos':{'club':{'nombre':'Olimpia','web':{'eslogan':'x','instagram':'badmintonolimpiatorrelavega'}},'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(HTML)); pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(500)
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1200)
    lab=pg.locator('label',has_text='TikTok'); ok(lab.count()>=1, f'{dev}: campo TikTok en Contacto')
    inp=pg.locator('input[placeholder^="usuario sin @ (o pega"]'); inp.scroll_into_view_if_needed(); inp.fill('https://www.tiktok.com/@clubolimpia.tv?lang=es'); inp.dispatch_event('change'); pg.wait_for_timeout(300)
    v=pg.evaluate("webCfg().tiktok"); ok(v=='clubolimpia.tv', f'{dev}: guarda solo el usuario ({v})')
    pg.screenshot(path=SP+f'tiktok_app_{dev}.png'); ok(not errs, f'{dev}: sin errores app {errs}'); pg.close()
    sd={'publico/datos':{'web':{'eslogan':'x','instagram':'badmintonolimpiatorrelavega','facebook':'https://www.facebook.com/badolimpiatorrelavega/?locale=es_ES','tiktok':'clubolimpia.tv'}}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(WEB)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';try{sessionStorage.setItem("introClubVisto","1")}catch(e){}')
    pg.goto('https://test.local/'); pg.wait_for_timeout(2500)
    t=pg.locator('#vias a',has_text='TikTok'); ok(t.count()==1 and t.get_attribute('href')=='https://www.tiktok.com/@clubolimpia.tv', f'{dev}: TikTok en el contacto de la web')
    fb=pg.locator('#vias a',has_text='Facebook').inner_text(); ok('locale' not in fb, f'{dev}: Facebook sin «?locale…» ({fb!r})')
    pg.locator('#vias').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'tiktok_web_{dev}.png')
    ok(not errs, f'{dev}: sin errores web {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
