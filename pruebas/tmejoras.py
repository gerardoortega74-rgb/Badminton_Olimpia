_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import time
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    sd=json.loads(json.dumps(seed())); T=sd['club/datos']['taller']; now=int(time.time()*1000); D=86400000; base=dict(T['pedidos'][0])
    T['articulos'].append({'id':'grip','nombre':'Grip Toalla','tipo':'Grip','esCordaje':False,'precio':3,'stock':1,'unidad':'unidades'})
    T['articulos'].append({'id':'cero','nombre':'Llavero nunca vendido','tipo':'Otro','esCordaje':False,'precio':0,'stock':0,'unidad':'unidades'})
    for a in T['articulos']:
      if a['id']=='s151': a['stock']=10
    mk=lambda i,**k: dict(base,id=i,**k)
    T['pedidos']=[mk('v1',estado='terminado',pagado=False,precio=14,marcaModelo='Yonex Arc 11',cordajeId='y1',tensionVertical=11,tensionHorizontal=12,horaLlegada=now-12*D,horaFin=now-10*D),
      mk('v2',estado='entregado',pagado=False,precio=16,marcaModelo='Victor Thruster',cordajeId='s088',tensionVertical=10.5,tensionHorizontal=11.5,pretensado=True,horaLlegada=now-40*D,horaFin=now-39*D,fechaEntrega=now-30*D),
      mk('v3',estado='entregado',pagado=True,precio=14,marcaModelo='Yonex Arc 11',cordajeId='y1',tensionVertical=11,horaLlegada=now-70*D,horaFin=now-69*D,fechaEntrega=now-69*D),
      mk('v4',estado='terminado',pagado=False,precio=14,marcaModelo='Reciente',cordajeId='y1',tensionVertical=12,horaLlegada=now-2*D,horaFin=now-1*D)]
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True); pg.on('dialog',lambda d:d.accept())
    pg.add_init_script("localStorage.setItem('badmintonTokenMeta','TK');localStorage.setItem('badmintonTokenMetaFecha',String(Date.now()-56*86400000));")
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(500)
    pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(800)
    av=pg.locator('.im-avisos'); ok(av.count()==1, f'{dev}: panel de avisos en la cola')
    res=av.locator('summary').inner_text(); print(dev,res)
    ok('1 sin recoger' in res and '1 sin pagar' in res and '2 con poco stock' in res, f'{dev}: cuenta bien (sin recoger >7 días, sin pagar, stock bajo; ignora lo reciente y lo nunca vendido)')
    av.locator('summary').click(); pg.wait_for_timeout(200); av.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'avisos_{dev}.png')
    sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: avisos sin descuadre ({sw})')
    av.locator('.im-aviso-recordar').click(); pg.wait_for_timeout(400)
    ok('lista%20para%20recoger' in pg.locator('#tallerModalRoot a').get_attribute('href'), f'{dev}: «Recordar» abre el WhatsApp con el mensaje')
    pg.evaluate("document.getElementById('tallerModalRoot').innerHTML=''")
    # estadísticas
    pg.evaluate("TallerApp.irATab('historial')"); pg.wait_for_timeout(600)
    e=pg.evaluate("(()=>{document.querySelector('.im-stats').open=true;return null})()")
    tx=pg.inner_text('.im-stats'); ok('4' in tx and 'Yonex BG65' in tx and 'raquetas encordadas' in tx, f'{dev}: estadísticas con totales y cordaje más usado')
    pg.locator('.im-stats').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'stats_{dev}.png')
    sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: estadísticas sin descuadre ({sw})')
    # repetir
    pg.evaluate("TallerApp.irATab('nuevo')"); pg.wait_for_timeout(600)
    pg.locator('input[placeholder="Nombre o teléfono del cliente"]').fill('Luc'); pg.wait_for_timeout(300)
    pg.locator('.im-resultados .chip').first.click(); pg.wait_for_timeout(300)
    rb=pg.locator('.im-repetir-btn'); print(dev,rb.all_inner_texts())
    ok(rb.count()==3, f'{dev}: «Como la última vez» con sus últimas raquetas distintas ({rb.count()})')
    rb.filter(has_text='Victor Thruster').click(); pg.wait_for_timeout(400)
    v=pg.evaluate("""(()=>{const A=document.getElementById('tallerMainArea');const ss=[...A.querySelectorAll('select')].filter(s=>[...s.options].some(o=>o.value==='s088'));const n=[A.querySelector('input[placeholder="Ej: 10.5"]').value,A.querySelector('input[placeholder="Ej: 10"]').value];return [ss[0].value,n,[...A.querySelectorAll('input[type=text]')].some(i=>i.value==='Victor Thruster')]})()""")
    print(dev,v); ok(v[0]=='s088' and v[1]==['10.5','11.5'] and v[2], f'{dev}: rellena raqueta, cordaje y tensiones de la última vez')
    # config avisos y token meta
    pg.evaluate("TallerApp.irATab('config')"); pg.wait_for_timeout(500)
    i=pg.locator('.im-cfg-dias'); ok(i.count()==1, f'{dev}: ajustes de avisos en Configuración'); i.fill('20'); i.dispatch_event('change'); pg.wait_for_timeout(200)
    ok(pg.evaluate("avisosTallerPrueba=TallerApp.getState().config.diasRecordatorio")==20, f'{dev}: guarda los días')
    pg.evaluate("goToClubGestion('web')"); pg.wait_for_timeout(1000)
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
