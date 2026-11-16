_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import datetime
def ts(dias=0,h=11,m=0):
  d=datetime.datetime.now().replace(hour=h,minute=m,second=0,microsecond=0)-datetime.timedelta(days=dias); return int(d.timestamp()*1000)
def iso(dias=0): return (datetime.date.today()-datetime.timedelta(days=dias)).isoformat()
def seedC():
  sd=seed(); t=sd['club/datos']['taller']
  P=lambda i,pr,forma,dias,h: {'id':i,'clienteId':'c1','marcaModelo':'R'+i,'cordajeId':'y1','tensionVertical':11,'tensionHorizontal':11,'precio':pr,'estado':'entregado','horaLlegada':ts(dias,9),'horaInicio':ts(dias,9,30),'horaFin':ts(dias,10),'fechaEntrega':ts(dias,h),'fechaPago':ts(dias,h),'formaPago':forma,'notas':'','pagado':True,'pagoPrevisto':'alRecoger','articulosAdicionales':[],'aplazado':False}
  t['pedidos']=[P('e1',16,'efectivo',0,10),P('e2',28,'bizum',0,12),P('e3',16,'tarjeta',0,17),P('ayer',20,'efectivo',1,12)]
  t['contabilidad']={'movimientos':[
    {'id':'m1','fecha':iso(0),'tipo':'ingreso','categoria':'Venta en tienda','concepto':'Ticket T-0041','importe':9},
    {'id':'m2','fecha':iso(0),'tipo':'ingreso','categoria':'Venta en tienda','concepto':'Ticket T-0042','importe':12},
    {'id':'m3','fecha':iso(0),'tipo':'gasto','categoria':'Material','concepto':'Cinta','importe':5},
    {'id':'m4','fecha':iso(1),'tipo':'ingreso','categoria':'Venta en tienda','concepto':'Ticket T-0040','importe':2.75}]}
  t['ventasTienda']=[
    {'id':'v1','numero':41,'fecha':ts(0,11),'pago':'efectivo','lineas':[{'nombre':'Llavero volante','cantidad':2,'precio':4.5}],'total':9,'anulada':False,'movimientoId':'m1'},
    {'id':'v2','numero':42,'fecha':ts(0,13),'pago':'bizum','lineas':[{'nombre':'Llavero 3D','cantidad':2,'precio':6}],'total':12,'anulada':False,'movimientoId':'m2'},
    {'id':'v0','numero':40,'fecha':ts(1,13),'pago':'efectivo','lineas':[{'nombre':'Grip toalla','cantidad':1,'precio':2.75}],'total':2.75,'anulada':False,'movimientoId':'m4'}]
  return sd
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,seedC(),admin=True)
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("showSection('taller'); TallerApp.irATab('contabilidad')"); pg.wait_for_timeout(500)
    pg.click('#imTabCaja'); pg.wait_for_timeout(500)
    cards=pg.evaluate("[...document.querySelectorAll('#imCajaDia .stat-card')].map(c=>c.innerText.replace(/\\s+/g,' '))")
    ok(cards[:4]==['81,00 € Cobrado','25,00 € 💶 Efectivo','16,00 € 💳 Tarjeta','40,00 € 📱 Bizum'], f'{dev}: hoy: 81 € (efectivo 25, tarjeta 16, bizum 40) {cards}')
    t=pg.inner_text('#imCajaDia')
    ok('3 · 60,00' in t and '2 tickets · 21,00' in t and 'Gastos' in t and pg.inner_text('#imCajaNeto')=='76,00 €', f'{dev}: encordados 3·60, tienda 2·21, neto 76')
    ok('Llavero volante' in t and 'Llavero 3D' in t and 'Grip toalla' not in t, f'{dev}: artículos vendidos solo de hoy')
    ok('3 recibidas · 3 encordadas · 3 entregadas' in t, f'{dev}: actividad de raquetas')
    pg.fill('#imCajaFondo','50'); pg.fill('#imCajaContado','70'); pg.locator('#imCajaContado').blur(); pg.wait_for_timeout(200)
    r=pg.inner_text('#imCajaRes'); ok('75,00' in r and 'Faltan 5,00' in r, f'{dev}: arqueo: esperado 75, faltan 5 ({r})')
    pg.fill('#imCajaContado','75'); pg.locator('#imCajaContado').blur(); pg.wait_for_timeout(200)
    ok('cuadra' in pg.inner_text('#imCajaRes'), f'{dev}: con 75 la caja cuadra')
    pg.screenshot(path=SP+f'caja_{dev}.png', full_page=True)
    pg.click('#imCajaWa'); u=pg.evaluate("window.__abierto||''"); import urllib.parse as up; tx=up.unquote(u)
    ok(u.startswith('https://wa.me/?text=') and 'TOTAL COBRADO: 81,00' in tx and 'Bizum: 40,00' in tx and 'diferencia +0,00' in tx, f'{dev}: resumen por WhatsApp')
    pg.click('#imCajaAnt'); pg.wait_for_timeout(400)
    cards=pg.evaluate("[...document.querySelectorAll('#imCajaDia .stat-card')].map(c=>c.innerText.replace(/\\s+/g,' '))")
    ok(cards[0]=='22,75 € Cobrado', f'{dev}: ayer: 22,75 € {cards[0]}')
    ok(pg.input_value('#imCajaContado')=='', f'{dev}: el arqueo es de cada día')
    pg.evaluate("document.getElementById('imCajaFecha').value=''"); 
    pg.locator('#imCajaDia button', has_text='Hoy').click(); pg.wait_for_timeout(300)
    ok(pg.input_value('#imCajaContado')=='75' and pg.input_value('#imCajaFondo')=='50', f'{dev}: guarda el arqueo de hoy')
    ok(pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1"), f'{dev}: sin desbordar')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
