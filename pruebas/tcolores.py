exec(open('/home/claude/test/tform2.py').read().split("# foto de prueba")[0])
cols=['Blanco','Amarillo Fosforito','Amarillo-Naranja','Azul','Azul-Blanco','Negro','Rojo','Rosa','Rosa-Blanco','Blanco','Morado']
ARTS[:]=[art('t%d'%i,'CORDAJE TOPO PA2055 (0,68mm) · '+c.upper(),'S1%02d'%i,10+i) for i,c in enumerate(cols)]+[art('hp','Cordaje HPYJ HP-80 Power (0,68mm) Verde','S153',5)]
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,seed())
    pg.goto('https://test.local/app.html?raqueta=1'); pg.wait_for_timeout(2500)
    pg.locator('.tpf-opc', has_text='TOPO').click(); pg.wait_for_timeout(300)
    r=pg.evaluate("[...document.querySelectorAll('.tpf-color')].map(e=>[e.dataset.color,getComputedStyle(e.querySelector('i')).backgroundImage,getComputedStyle(e.querySelector('i')).backgroundColor])")
    d={x[0]:x for x in r}
    ok(len(r)==10 and [x[0] for x in r].count('Blanco')==1, f'{dev}: «Blanco» sale una sola vez (10 colores)')
    ok('230, 255, 0' in d['Amarillo Fosforito'][2], f'{dev}: amarillo fosforito en flúor {d["Amarillo Fosforito"][2]}')
    ok('gradient' in d['Azul-Blanco'][1] and '31, 95, 209' in d['Azul-Blanco'][1] and '245, 245, 245' in d['Azul-Blanco'][1], f'{dev}: Azul-Blanco mitad y mitad')
    ok('gradient' in d['Amarillo-Naranja'][1] and 'gradient' in d['Rosa-Blanco'][1], f'{dev}: Amarillo-Naranja y Rosa-Blanco a dos colores')
    ok('rgb(17, 17, 17)' in d['Negro'][2] and '214, 44, 44' in d['Rojo'][2], f'{dev}: colores lisos bien')
    blanco_id=pg.evaluate("document.querySelector('.tpf-color[data-color=\"Blanco\"]').getAttribute('data-color')")
    pg.locator('.tpf-color[data-color="Blanco"]').click(); pg.wait_for_timeout(200)
    pg.locator('.tpf-colores').screenshot(path=SP+f'col_{dev}.png')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
