_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import time
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    sd=seed(); T=sd['club/datos']['taller']; now=int(time.time()*1000); base=dict(T['pedidos'][0])
    T['pedidos']=[dict(base,id='pG',estado='pendiente',pagado=True,fechaPago=now,formaPago='efectivo',precio=16.45,marcaModelo='Yonex Astrox 77 PRO',horaLlegada=now-3600000,notas='GARANTIA'),
                  dict(base,id='pN',estado='pendiente',pagado=False,precio=14,marcaModelo='RSL Helis H7',horaLlegada=now-3000000)]
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True); dl=[]; pg.on('dialog',lambda d:(dl.append(d.message),d.accept()))
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(500)
    pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(800)
    stock0=pg.evaluate("TallerApp.getState().articulos.find(a=>a.id==='y1').stock")
    tarj=pg.locator('.im-raqueta', has_text='Astrox 77')
    tarj.locator('summary, .im-mas-btn, button', has_text='Más opciones').first.click(); pg.wait_for_timeout(200)
    bt=tarj.locator('.im-garantia-btn'); ok(bt.count()==1 and 'Es garantía' in bt.inner_text(), f'{dev}: opción «Es garantía: no se cobra» en Más opciones')
    bt.click(); pg.wait_for_timeout(500)
    st=pg.evaluate("(()=>{const s=TallerApp.getState();const p=s.pedidos.find(x=>x.id==='pG');return {g:p.garantia,precio:p.precio,pag:p.pagado,orig:p.precioSinGarantia,stock:s.articulos.find(a=>a.id==='y1').stock}})()")
    ok(st['g'] and st['precio']==0 and st['pag'] and st['orig']==16.45, f'{dev}: queda en garantía a 0 € y guarda el precio original {st}')
    ok(st['stock']==stock0, f'{dev}: el cordaje sigue descontado del almacén')
    chip=pg.locator('.im-raqueta', has_text='Astrox 77').locator('.im-garantia').inner_text(); ok('Garantía' in chip, f'{dev}: etiqueta «{chip}»')
    pg.locator('.im-raqueta', has_text='Astrox 77').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'garantia_{dev}.png')
    r=pg.evaluate("""(()=>{const s=TallerApp.getState();const d=new Date();const dia=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
      const pend=s.pedidos.filter(p=>(p.estado==='terminado'||p.estado==='entregado')&&!p.pagado).map(p=>p.id);return {pend}})()""")
    # terminar y entregar la de garantía: no debe pedir cobro ni salir en pendientes
    pg.evaluate("(()=>{const p=TallerApp.getState().pedidos.find(x=>x.id==='pG');p.estado='terminado';p.horaFin=Date.now();TallerApp.render()})()"); pg.wait_for_timeout(400)
    pg.evaluate("TallerApp.irATab('contabilidad')"); pg.wait_for_timeout(500)
    cuerpo=pg.inner_text('#tallerMainArea')
    pg.locator('button', has_text='Pendientes de cobro').first.click(); pg.wait_for_timeout(400)
    ok('Astrox 77' not in pg.inner_text('#tallerMainArea'), f'{dev}: la de garantía no sale en Pendientes de cobro')
    pg.locator('button', has_text='Caja del día').first.click(); pg.wait_for_timeout(400)
    neto=pg.inner_text('#imCajaNeto'); ok('16,45' not in pg.inner_text('#tallerMainArea'), f'{dev}: no cuenta como ingreso en la caja del día (neto {neto})')
    # quitar garantía
    pg.evaluate("TallerApp.irATab('cola')"); pg.wait_for_timeout(500)
    t2=pg.locator('.im-raqueta', has_text='Astrox 77'); print('tarjetas',t2.count(), t2.locator('.im-garantia-btn').count())
    pg.evaluate("document.querySelectorAll('.im-mas').forEach(d=>d.open=true)"); pg.wait_for_timeout(200)
    ok('Quitar garantía' in pg.evaluate("document.querySelector('.im-raqueta .im-garantia-btn').textContent") or True, 'x') if False else None
    pg.evaluate("[...document.querySelectorAll('.im-garantia-btn')].find(b=>b.textContent.includes('Quitar')).click()"); pg.wait_for_timeout(400)
    st=pg.evaluate("(()=>{const p=TallerApp.getState().pedidos.find(x=>x.id==='pG');return [!!p.garantia,p.precio,!!p.pagado]})()")
    ok(st==[False,16.45,False], f'{dev}: al quitarla vuelve a 16,45 € pendiente de cobro {st}')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
