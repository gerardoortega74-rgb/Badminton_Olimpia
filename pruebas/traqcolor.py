exec(open('/home/claude/test/tcolores.py').read().split("with sync_playwright() as p:")[0])
ARTS.append(art('y1','Yonex BG65 · Rojo','Y65',30,grupoId='gY',grupoNombre='Yonex BG65',color='Rojo',precio=12))
ARTS.append(art('y2','Yonex BG65 · Negro','Y65',30,grupoId='gY',grupoNombre='Yonex BG65',color='Negro',precio=12))
def cuerdas(pg):
  return pg.evaluate("""(()=>{const ls=[...document.querySelectorAll('#frmRaquetaDibujo svg g line[stroke]')];
    const v=ls.filter(l=>l.getAttribute('y1')===l.getAttribute('y2')).map(l=>l.getAttribute('stroke'));
    const h=ls.filter(l=>l.getAttribute('x1')===l.getAttribute('x2')).map(l=>l.getAttribute('stroke'));
    return {v:[...new Set(v)],h:[...new Set(h)],nv:v.length,nh:h.length}})()""")
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,seed())
    pg.goto('https://test.local/app.html?raqueta=1'); pg.wait_for_timeout(2500)
    y_com=pg.locator('#frmComentarios').bounding_box()['y']; y_raq=pg.locator('#frmRaquetaDibujo').bounding_box()['y']
    ok(y_raq>y_com, f'{dev}: la raqueta va debajo de comentarios')
    c=cuerdas(pg); ok(c['nv']==22 and c['nh']==22 and c['v']==['#D9DDE3'], f'{dev}: sin elegir, cuerdas grises')
    pg.locator('.tpf-opc', has_text='TOPO').click(); pg.locator('.tpf-color[data-color="Rojo"]').click(); pg.wait_for_timeout(200)
    c=cuerdas(pg); ok(c['v']==['#D62C2C'] and c['h']==['#D62C2C'], f'{dev}: un color: todas rojas {c}')
    pg.locator('#frmRaquetaDibujo').screenshot(path=SP+f'rqrojo_{dev}.png')
    ok(pg.evaluate("(()=>{const i=document.querySelector('#frmRaquetaDibujo image');return i&&i.getBBox().width>0})()"), f'{dev}: carga la foto de la raqueta')
    pg.locator('.tpf-color[data-color="Azul-Blanco"]').click(); pg.wait_for_timeout(200)
    pg.locator('#frmRaquetaDibujo').screenshot(path=SP+f'rqab_{dev}.png')
    c=cuerdas(pg); ok(c['v']==['#1F5FD1'] and c['h']==['#F5F5F5'], f'{dev}: Azul-Blanco: verticales azules y horizontales blancas {c}')
    ok('Azul-Blanco' in pg.inner_text('#frmRaquetaDibujo'), f'{dev}: pone el nombre del color')
    pg.locator('.tpf-color[data-color="Amarillo Fosforito"]').click(); pg.wait_for_timeout(200)
    c=cuerdas(pg); ok(c['v']==['#E6FF00'], f'{dev}: fosforito en flúor {c}')
    pg.fill('#frmTensionV','11'); pg.locator('#frmTensionV').blur(); pg.fill('#frmTensionH','11,5'); pg.locator('#frmTensionH').blur(); pg.check('#frmPretensado'); pg.wait_for_timeout(200)
    ok('V 11 kg · H 11,5 kg · pretensado' in pg.inner_text('#frmRaquetaDibujo'), f'{dev}: pone tensiones y pretensado')
    # híbrido
    pg.click('.tpf-modo[data-hibrido="1"]'); pg.wait_for_timeout(200)
    pg.locator('.tpf-selector[data-lado="V"] .tpf-opc', has_text='TOPO').click(); pg.locator('.tpf-selector[data-lado="V"] .tpf-color[data-color="Negro"]').click()
    pg.locator('.tpf-selector[data-lado="H"] .tpf-opc', has_text='Yonex BG65').click(); pg.locator('.tpf-selector[data-lado="H"] .tpf-color[data-color="Rojo"]').click(); pg.wait_for_timeout(200)
    c=cuerdas(pg); ok(c['v']==['#111'] and c['h']==['#D62C2C'], f'{dev}: híbrido: verticales negras, horizontales rojas {c}')
    pg.locator('#frmRaquetaDibujo').scroll_into_view_if_needed(); pg.locator('#frmRaquetaDibujo').screenshot(path=SP+f'rq_{dev}.png')
    pg.locator('.tpf-selector[data-lado="H"] .tpf-opc', has_text='TOPO').click(); pg.locator('.tpf-selector[data-lado="H"] .tpf-color[data-color="Rosa-Blanco"]').click(); pg.wait_for_timeout(200)
    c=cuerdas(pg); ok(sorted(c['h'])==sorted(['#F06EA9','#F5F5F5']), f'{dev}: híbrido con horizontal de dos colores: alterna rosa y blanco {c}')
    pg.locator('#frmRaquetaDibujo').screenshot(path=SP+f'rq2_{dev}.png')
    ok(pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1"), f'{dev}: sin desbordar')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
