_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    sd=seed(); sd['club/datos']['taller']['pedidos'][0]['aplazado']=True
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True); pg.on('dialog',lambda d:d.accept())
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(500)
    pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(800)
    bt=pg.locator('.im-aplazada-editar'); ok(bt.count()==1, f'{dev}: botón Editar en aplazadas')
    bt.scroll_into_view_if_needed(); (bt.tap() if mov else bt.click()); pg.wait_for_timeout(600)
    ok(pg.locator('#imEdPrecio').is_visible(), f'{dev}: se abre la edición')
    pg.fill('#imEdPrecio','30'); pg.screenshot(path=SP+f'aplaz_{dev}.png')
    g=pg.locator('#tallerModalRoot button', has_text='Guardar').first; (g.tap() if mov else g.click()); pg.wait_for_timeout(600)
    for _ in range(2):
      c=pg.locator('#tallerModalRoot button', has_text='Sí').or_(pg.locator('#tallerModalRoot button', has_text='Confirmar')).or_(pg.locator('#tallerModalRoot button', has_text='Guardar'))
      if c.count(): (c.first.tap() if mov else c.first.click()); pg.wait_for_timeout(500)
    st=pg.evaluate("(()=>{const p=TallerApp.getState().pedidos.find(x=>x.id==='pA');return [p.precio,p.aplazado]})()")
    ok(st==[30,True], f'{dev}: guarda el cambio y sigue aplazada {st}')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
