_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    sd=seed()
    for a in sd['club/datos']['taller']['articulos']: a['unidad']='metros'
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True)
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("showSection('taller'); TallerApp.irATab('nuevo')"); pg.wait_for_timeout(800)
    sels=lambda: pg.evaluate("[...document.querySelectorAll('#tallerMainArea select')].map((s,i)=>i+':'+[...s.options].slice(0,3).map(o=>o.value).join(','))")
    J="""(([v,h])=>{const ss=[...document.querySelectorAll('#tallerMainArea select')].filter(s=>[...s.options].some(o=>o.value==='y1'));
      if(v!==null){ss[0].value=v;ss[0].dispatchEvent(new Event('change'))} if(h!==null){ss[1].value=h;ss[1].dispatchEvent(new Event('change'))}
      const nums=[...document.querySelectorAll('#tallerMainArea input[type=number][step="0.5"]')].slice(3,5);return nums.map(n=>n.value)})"""
    r=pg.evaluate(J,['y1',None]); ok(r[0]=='9', f'{dev}: un cordaje -> 9 m {r}')
    hib=pg.locator('label', has_text='Híbrido').locator('input'); (hib.tap() if mov else hib.click()); pg.wait_for_timeout(200)
    r=pg.evaluate(J,[None,'s154']); ok(r[0]=='5' and r[1]=='4', f'{dev}: dos cordajes -> 5 m verticales + 4 m horizontales {r}')
    (hib.tap() if mov else hib.click()); pg.wait_for_timeout(200)
    r=pg.evaluate("[...document.querySelectorAll('#tallerMainArea input[type=number][step=\"0.5\"]')].slice(3,5).map(n=>n.value)"); ok(r[0]=='9', f'{dev}: quitar híbrido -> vuelve a 9 m {r}')
    # cantidad cambiada a mano se respeta
    (hib.tap() if mov else hib.click()); pg.wait_for_timeout(200)
    pg.evaluate(J,[None,'s154']); pg.evaluate("(()=>{const n=document.querySelectorAll('#tallerMainArea input[type=number][step=\"0.5\"]')[3];n.value='6';})()")
    r=pg.evaluate(J,[None,'y2']); ok(r[0]=='6' and r[1]=='4', f'{dev}: si lo cambias a mano no lo toca {r}')
    # addPedido (formulario del cliente)
    st=pg.evaluate("""(()=>{const s=TallerApp.getState();const a=id=>s.articulos.find(x=>x.id===id).stock;const b1=a('y1'),b2=a('s154');
      TallerApp.addPedido({clienteId:'c1',cordajeId:'y1',cordajeIdH:'s154',tensionVertical:11,tensionHorizontal:11});const p=s.pedidos[s.pedidos.length-1];
      return [p.cantidadCordaje,p.cantidadCordajeH,b1-a('y1'),b2-a('s154')]})()""")
    ok(st==[5,4,5,4], f'{dev}: pedido híbrido descuenta 5 m del vertical y 4 m del horizontal {st}')
    st=pg.evaluate("""(()=>{const s=TallerApp.getState();TallerApp.addPedido({clienteId:'c1',cordajeId:'y1',tensionVertical:11});return s.pedidos[s.pedidos.length-1].cantidadCordaje})()""")
    ok(st==9, f'{dev}: pedido de un cordaje descuenta 9 m ({st})')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
