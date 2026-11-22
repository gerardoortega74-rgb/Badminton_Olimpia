_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
def ped(i,gar):
  return {'id':i,'clienteId':'c1','marcaModelo':'Raq '+i,'cordajeId':'y1','tensionVertical':11,'tensionHorizontal':11,'precio':0 if gar else 16,'precioSinGarantia':16,'garantia':gar,'estado':'entregado','horaLlegada':AHORA-7200000,'horaInicio':None,'horaFin':AHORA-3600000,'fechaEntrega':AHORA-1800000,'notas':'','pagado':True,'fechaPago':AHORA-1800000,'formaPago':None if gar else 'efectivo','pagoPrevisto':'alRecoger','articulosAdicionales':[]}
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    for ng in (2,0):
      sd=json.loads(json.dumps(seed())); sd['club/datos']['taller']['pedidos']=[ped('A',False),ped('B',False),ped('C',False)]+[ped('G%d'%i,True) for i in range(ng)]
      pg,errs=pagina(b,vw,vh,mov,sd,admin=True)
      pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
      pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(400)
      pg.evaluate("showSection('taller'); TallerApp.irATab('historial')"); pg.wait_for_timeout(800)
      cab=pg.inner_text('.im-hist-resumen'); pg.evaluate("document.querySelector('.im-stats').open=true"); st=pg.inner_text('.im-stats')
      if ng:
        ok('5 raqueta(s) (2 en garantía' in cab and '48,00' in cab, f'{dev}: cabecera del historial: 5 raquetas, 2 en garantía, 48 € ({cab[:70]})')
        ok('🛡️ 2' in st and 'en garantía (sin cobrar)' in st and '5 · 2 🛡️' in st and '2 de las 5 raquetas son de garantía' in st, f'{dev}: estadísticas: dato de garantía y marca en el mes')
        pg.locator('.im-stats').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'garcont_{dev}.png')
      else:
        ok('garantía' not in cab and 'sin cobrar' not in st and '🛡️' not in st.split('Raquetas por mes')[1].split('Ingresos')[0].replace('(🛡️ = de ellas, en garantía)',''), f'{dev}: sin garantías no ensucia nada')
      sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: sin descuadre ({sw})')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
