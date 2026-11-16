_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    for caso,val,esp in (('sin poner',None,'Bizum al 647 67 57 10'),('otro','600111222','Bizum al 600111222'),('vacío a propósito','','Bizum')):
      sd=json.loads(json.dumps(seed())); cfg=sd['club/datos']['taller'].setdefault('config',{}); cfg.pop('bizumTaller',None)
      if val is not None: cfg['bizumTaller']=val
      pg,errs=pagina(b,vw,vh,mov,sd,admin=True)
      pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
      pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(400)
      pg.evaluate("showSection('taller')"); pg.wait_for_timeout(500); pg.evaluate("TallerApp.irATab('config')"); pg.wait_for_timeout(700)
      v=pg.locator('.im-cfg-bizum').input_value() if pg.locator('.im-cfg-bizum').count() else '??'
      ok(v==(val if val is not None else '647 67 57 10'), f'{dev} {caso}: Configuración muestra «{v}»')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev} {caso}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
