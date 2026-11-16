_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import time, datetime
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    sd=seed(); T=sd['club/datos']['taller']; base=dict(T['pedidos'][0])
    t1=int(datetime.datetime(2026,11,12,18,40).timestamp()*1000); t2=int(datetime.datetime(2026,11,13,10,5).timestamp()*1000)
    a=dict(base,id='pX',estado='terminado',pagado=False,horaLlegada=t1,horaFin=t2+3600000,marcaModelo='Victor Thruster F')
    c=dict(base,id='pY',estado='terminado',pagado=False,horaLlegada=t2,horaFin=t2+7200000,marcaModelo='Victor Thruster F')
    T['pedidos']=[a,c]
    pg,errs=pagina(b,vw,vh,mov,sd,admin=True)
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(500)
    pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(800)
    tx=pg.locator('.im-recibida').all_inner_texts(); print(dev,tx)
    ok(len(tx)==2 and '12/11/2026 a las 18:40' in tx[0] and '13/11/2026 a las 10:05' in tx[1], f'{dev}: cada raqueta lista dice cuándo la dejaron')
    pg.locator('.im-recibida').first.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'recib_{dev}.png')
    sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: sin descuadre ({sw})')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
