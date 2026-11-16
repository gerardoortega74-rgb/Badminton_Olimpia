_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import time
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    sd=seed(); t=sd['club/datos']['taller']
    t['pedidos'].append({'id':'pL','clienteId':'c1','marcaModelo':'Babolat satelite','cordajeId':'y1','tensionVertical':11,'tensionHorizontal':11,'precio':12.89,'estado':'terminado','horaLlegada':AHORA-90*60000,'horaInicio':AHORA-60*60000,'horaFin':AHORA-20*60000,'notas':'','pagado':False,'pagoPrevisto':'alRecoger','articulosAdicionales':[],'aplazado':False})
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True); pg.on('dialog',lambda d: d.accept())
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(800)
    btn=pg.locator('.im-editar-lista'); ok(btn.count()==1 and btn.is_visible(), f'{dev}: botón «Editar precio» en Listas para recoger')
    btn.click(); pg.wait_for_timeout(300)
    pg.fill('#imEdPrecio','16'); pg.locator('#tallerModalRoot button', has_text='Guardar').first.click(); pg.wait_for_timeout(500)
    pr=pg.evaluate("TallerApp.getState().pedidos.find(p=>p.id==='pL').precio")
    ok(pr==16, f'{dev}: precio cambiado a 16 € ({pr})')
    ok('16,00' in pg.inner_text('#tallerMainArea'), f'{dev}: se ve el precio nuevo en la tarjeta')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
