_t=open('/home/claude/test/tcarrtienda.py').read(); exec(_t[:_t.index("with sync_playwright() as p:\n  b=")])
def seedA():
  sd=seed(); arts=sd['club/datos']['taller']['articulos']
  arts+= [{'id':'g1','nombre':'Grip Bueno','tipo':'Grip','precio':5,'stock':4,'ventaOnline':True,'foto':foto((200,0,0)),'proveedores':[]},
          {'id':'g2','nombre':'Grip Agotado','tipo':'Grip','precio':5,'stock':0,'ventaOnline':True,'foto':foto((0,200,0)),'proveedores':[]},
          {'id':'m1','nombre':'Mochila · Roja','grupoId':'gm','grupoNombre':'Mochila','color':'Roja','tipo':'Mochila','precio':30,'stock':2,'ventaOnline':True,'foto':foto((200,0,0)),'proveedores':[]},
          {'id':'m2','nombre':'Mochila · Azul','grupoId':'gm','grupoNombre':'Mochila','color':'Azul','tipo':'Mochila','precio':30,'stock':0,'ventaOnline':True,'foto':foto((0,0,200)),'proveedores':[]},
          {'id':'v1','nombre':'Volantes Todo Agotado · Blanco','grupoId':'gv','grupoNombre':'Volantes Todo Agotado','color':'Blanco','tipo':'Volantes','precio':20,'stock':0,'ventaOnline':True,'foto':foto((240,240,240)),'proveedores':[]}]
  sd['publico/datos']={'taller':sd['club/datos']['taller']}
  return sd
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,seedA())
    pg.goto('https://test.local/app.html?tiendaonline=1'); pg.wait_for_timeout(5000)
    t=pg.inner_text('#tiendaOnlineScreen')
    ok('Grip Bueno' in t and 'Grip Agotado' not in t and 'Volantes Todo Agotado' not in t, f'{dev}: los agotados no salen en la tienda')
    ok('Agotado' not in t.replace('Grip Agotado','').replace('Todo Agotado',''), f'{dev}: no aparece ninguna etiqueta «Agotado»')
    ok('Mochila' in t, f'{dev}: la mochila sale (le queda un color)')
    pg.evaluate("(()=>{const c=[...document.querySelectorAll('#tiendaOnlineScreen *')].filter(e=>e.children.length<6&&/Mochila/.test(e.textContent)&&e.closest('#tdoCatalogo, .tdo-cat, .tdo-grid, main'));const b=(c.find(e=>e.matches('button,[role=button],.tdo-card,article'))||c[c.length-1]);(b.closest('button,.tdo-card,article,[data-id]')||b).click()})()"); pg.wait_for_timeout(600)
    cols=pg.evaluate("document.body.innerText.slice(-1500)")
    ok('Azul' not in cols, f'{dev}: en los colores no sale el agotado ({cols[:80]})')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
