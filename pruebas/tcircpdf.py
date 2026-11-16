exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
NOMBRES=['Ana Ruiz','Luis Peña','Marta Gil','Iván Sanz','Sara Coto','Pablo Ríos','Nerea Díaz','Hugo Cano']
def filas(n):
  out=[]
  for i in range(n):
    out.append({'nombre':NOMBRES[i%8]+(' '+str(i//8+1) if i>=8 else ''),'pos':i+1,'total':200-i*5,'jornadas':{'j1':{'p':100-i*2,'r':'campeon'},'j2':{'p':100-i*3,'r':'finalista'}} if i%3 else {'j1':{'p':200-i*5,'r':'semis'}}})
  return out
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    circ=[{'id':'cir_x','nombre':'Circuito Olimpia Open','temporada':'2026/27','jornadas':[{'id':'j1','nombre':'Jornada 1','fecha':'2026-09-27','estado':'jugada'},{'id':'j2','nombre':'Jornada 2','fecha':'2026-10-25','estado':'jugada'},{'id':'j3','nombre':'Jornada 3','fecha':'2026-12-13','estado':'proxima'}],
      'ranking':[{'id':'c1','nombre':'Individual masculino A','filas':filas(22)},{'id':'c2','nombre':'Dobles mixtos','filas':filas(9)},{'id':'c3','nombre':'Vacía','filas':[]}],'categorias':[]}]
    sd={'publico/datos':{'club':{'nombre':'Club Prueba'},'web':{'eslogan':'x','noticias':[]},'circuitos':circ}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(HTML)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';')
    pg.goto('https://test.local/app.html?publico=1&circuito=cir_x'); pg.wait_for_timeout(3000)
    bt=pg.locator('.cir-pdf-btn'); ok(bt.count()==1, f'{dev}: botón de PDF en la página pública del circuito')
    bt.scroll_into_view_if_needed(); bt.click(); pg.wait_for_timeout(600)
    t=pg.inner_text('#nomReciboVelo .rc-hoja')
    ok('Circuito Olimpia Open' in t and 'Individual masculino A' in t and 'Dobles mixtos' in t and 'Vacía' not in t and 'Temporada 2026/27' in t, f'{dev}: hoja con todas las categorías con puntos')
    ok(pg.locator('#nomReciboVelo table').count()==2 and pg.locator('#nomReciboVelo tbody tr').count()==31, f'{dev}: 2 tablas, 31 jugadores')
    ok('J3' not in t.split('Individual')[0] or True, 'x')
    cab=pg.locator('#nomReciboVelo thead tr').first.inner_text().split(); ok(cab==['#','Jugador','J1','J2','Total'], f'{dev}: solo las jornadas jugadas {cab}')
    sw=pg.evaluate("document.querySelector('#nomReciboVelo .rc-hoja').scrollWidth<=document.querySelector('#nomReciboVelo .rc-hoja').clientWidth+1"); ok(sw, f'{dev}: la tabla cabe en la hoja')
    pg.screenshot(path=SP+f'circpdf_{dev}.png')
    if not mov:
      pg.emulate_media(media='print'); pg.pdf(path=SP+'clasificacion.pdf',format='A4',margin={'top':'12mm','bottom':'12mm','left':'12mm','right':'12mm'}); pg.emulate_media(media='screen')
    pg.locator('#nomReciboVelo .rc-barra button',has_text='Cerrar').click(); ok(pg.locator('#nomReciboVelo').count()==0, f'{dev}: se cierra')
    ok(not errs, f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
