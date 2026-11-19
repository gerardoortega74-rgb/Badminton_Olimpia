_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import urllib.parse
SALTAR="document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"
G=[{'articuloId':'g1','cantidad':1,'precioUnitario':3,'nombre':'Grip Toalla · Azul'}]
def ped(i,est,**k):
  d={'id':i,'clienteId':'c1','marcaModelo':'Raq '+i,'cordajeId':'y1','tensionVertical':11,'tensionHorizontal':12,'precio':19,'estado':est,'horaLlegada':AHORA-3*3600000,'horaInicio':None,'horaFin':None,'notas':'','pagado':False,'pagoPrevisto':'alRecoger','articulosAdicionales':G,'aplazado':False}
  d.update(k); return d
def sem():
  sd=json.loads(json.dumps(seed())); t=sd['club/datos']['taller']
  t['articulos'].append({'id':'g1','nombre':'Grip Toalla · Azul','codigo':'G1','stock':5,'precio':3,'unidad':'unidades','tipo':'articulo'})
  t['pedidos']=[ped('CURSO','en_proceso',horaInicio=AHORA-600000),ped('COLA','pendiente'),ped('LISTA','terminado',horaFin=AHORA-3600000),ped('APLAZ','pendiente',aplazado=True),ped('ENTREG','entregado',horaFin=AHORA-7200000,fechaEntrega=AHORA-3600000),
                ped('SIN','terminado',horaFin=AHORA-3000000,articulosAdicionales=[])]
  sd['publico/datos']['taller']=json.loads(json.dumps(t)); return sd
TX='1 × Grip Toalla · Azul'
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,sem(),admin=True)
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(400)
    pg.evaluate("showSection('taller')"); pg.wait_for_timeout(900)
    def tarjeta(txt): return pg.locator('.im-raqueta',has_text=txt)
    for n,et in (('Raq COLA','en la cola'),('Raq LISTA','en Listas para recoger'),('Raq APLAZ','en Aplazadas')):
      c=tarjeta(n); ok(c.count()>=1 and TX in c.first.inner_text(), f'{dev}: el grip se ve {et}')
    ok(TX not in tarjeta('Raq SIN').first.inner_text() and tarjeta('Raq SIN').first.locator('.im-extras').count()==0, f'{dev}: sin artículos no sale la línea')
    ok(TX in tarjeta('Raq CURSO').first.inner_text(), f'{dev}: y en la que se está encordando')
    for n in ('Raq CURSO','Raq COLA','Raq LISTA','Raq APLAZ'):
      g=tarjeta(n).first.evaluate("c=>{const e=c.querySelector('.im-extras').getBoundingClientRect(),d=c.querySelector('.im-det').getBoundingClientRect();return Math.abs(e.left-d.left)<2&&e.width>150}")
      ok(g, f'{dev}: la línea del grip queda alineada con el resto ({n})')
    tarjeta('Raq CURSO').first.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'extras_curso_{dev}.png')
    tarjeta('Raq LISTA').first.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'extras_{dev}.png')
    tarjeta('Raq LISTA').first.locator('button',has_text='Avisar por WhatsApp').click(); pg.wait_for_timeout(400)
    u=urllib.parse.unquote(pg.locator('#tallerModalRoot a[href*="wa.me"]').get_attribute('href')); print('  ',u[:230].replace('\n',' | '))
    ok('Incluye también: '+TX in u and '19,00' in u, f'{dev}: el WhatsApp de aviso nombra el grip')
    pg.evaluate("document.getElementById('tallerModalRoot').innerHTML=''")
    tarjeta('Raq SIN').first.locator('button',has_text='Avisar por WhatsApp').click(); pg.wait_for_timeout(300)
    u=urllib.parse.unquote(pg.locator('#tallerModalRoot a[href*="wa.me"]').get_attribute('href')); ok('Incluye' not in u, f'{dev}: sin artículos el mensaje queda como antes')
    pg.evaluate("document.getElementById('tallerModalRoot').innerHTML=''")
    ok(pg.evaluate("window.__STORE['publico/datos']") is not None, 'x')
    pg.evaluate("(()=>{TallerApp.getState().clientes[0].nombre='Lucía H';TallerApp.saveLocal();programarSyncNube()})()"); pg.wait_for_timeout(3500)
    pub=pg.evaluate("window.__STORE['publico/datos'].taller.pedidos.find(p=>p.id==='LISTA').articulosAdicionales"); ok(pub==[{'cantidad':1,'nombre':'Grip Toalla · Azul'}], f'{dev}: a la página del cliente va solo nombre y cantidad {pub}')
    pg.evaluate("TallerApp.irATab('historial')"); pg.wait_for_timeout(700)
    h=pg.locator('.im-hist-card',has_text='Raq ENTREG'); ok(h.count()>=1 and TX in h.first.inner_text(), f'{dev}: se ve en el Historial')
    st=pg.evaluate("window.__STORE"); ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
    # página de seguimiento del cliente
    pg2,errs2=pagina(b,vw,vh,mov,st,admin=False)
    pg2.goto('https://test.local/app.html?tallerpublico=1&pedido=LISTA'); pg2.wait_for_timeout(3000)
    d=pg2.locator('.tpb-detalle'); ok(d.count()==1 and 'También lleva' in d.inner_text() and TX in d.inner_text(), f'{dev}: la página de seguimiento del cliente muestra el grip')
    d.scroll_into_view_if_needed(); pg2.screenshot(path=SP+f'extras_pub_{dev}.png')
    pg2.goto('https://test.local/app.html?tallerpublico=1&pedido=SIN'); pg2.wait_for_timeout(2500)
    ok('También lleva' not in pg2.locator('.tpb-detalle').inner_text(), f'{dev}: y sin artículos no sale')
    ok(not [e for e in errs2 if 'hasPending' not in e], f'{dev}: sin errores (público) {errs2}'); pg2.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
