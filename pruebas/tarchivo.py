_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
SALTAR="document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"
CREAR="""(()=>{const st=JSON.parse(JSON.stringify(TorneoApp.getState()));
 const mk=(id,n,est)=>{const s=JSON.parse(JSON.stringify(st));s.meta.title=n;s.relleno='x'.repeat(20000);return {id,nombre:n,fechaInicio:'2026-01-01',fechaFin:est==='finalizado'?'2026-01-02':'',estado:est,snapshot:s}};
 TorneoApp.setHistorial([mk('T1','Torneo Uno','finalizado'),mk('T2','Torneo Dos','finalizado'),mk('T3','Torneo Vivo','en_curso')]);
 TorneoApp.setTorneoActivoId('T3');TorneoApp.setState(mk('T3','Torneo Vivo','en_curso').snapshot);programarSyncNube();})()"""
HIST="(window.__STORE['club/datos'].torneosHistorial||[]).map(t=>({id:t.id,snap:!!t.snapshot,arch:t.archivado||''}))"
MEM="TorneoApp.getHistorial().map(t=>({id:t.id,snap:!!t.snapshot,arch:t.archivado||'',tit:t.snapshot&&t.snapshot.meta.title}))"
import sys
caso=sys.argv[1]
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,json.loads(json.dumps(seed())),admin=True); dl=[]; pg.on('dialog',lambda d:(dl.append(d.message),d.accept()))
    if caso=='deny': pg.add_init_script("window.__DENY=['/torneos_archivo']")
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(400)
    pg.evaluate(CREAR); pg.wait_for_timeout(4000)
    h=pg.evaluate(HIST); m=pg.evaluate(MEM); tam=pg.evaluate("JSON.stringify(window.__STORE['club/datos']).length")
    if caso=='deny':
      ok(all(x['snap'] and not x['arch'] for x in h), f'{dev}: sin la regla, los torneos siguen enteros en el documento general {h}')
      ok(not pg.evaluate("Object.keys(window.__STORE).some(k=>k.includes('torneos_archivo'))"), f'{dev}: no se archiva nada')
      pg.evaluate("goToClubGestion('datos')"); pg.wait_for_timeout(1000)
      ok(pg.locator('.nube-archivo-falta').count()==1, f'{dev}: el panel avisa de que falta la regla')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close(); continue
    ok([x['id'] for x in h if not x['snap'] and x['arch']]==['T1','T2'] and h[2]['snap'], f'{dev}: los 2 terminados salen del documento general, el abierto no {h}')
    ok(all(x['snap'] and not x['arch'] for x in m), f'{dev}: en la app siguen completos {m}')
    a=pg.evaluate("['T1','T2'].map(i=>{const d=window.__STORE['club/datos/torneos_archivo/'+i];return d&&JSON.parse(d.json).meta.title+'|'+(d.firma===firmaTexto(d.json))})")
    ok(a==['Torneo Uno|true','Torneo Dos|true'], f'{dev}: guardados aparte y con su firma {a}')
    ok(tam<pg.evaluate("JSON.stringify(datosComparablesNube(estadoCompletoParaNube(true))).length")-38000, f'{dev}: el documento general pesa ~40 KB menos ({tam})')
    if caso=='base':
      # copia de seguridad: lleva los torneos enteros
      pg.evaluate("guardarCopiaNube('manual-x','manual')"); pg.wait_for_timeout(1200)
      c=pg.evaluate("descomprimirTexto({fmt:window.__STORE['club/datos/copias/manual-x'].fmt,datos:window.__STORE['club/datos/copias/manual-x'].datos}).then(t=>JSON.parse(t).torneosHistorial.map(x=>!!x.snapshot))")
      ok(c==[True,True,True], f'{dev}: la copia de seguridad incluye los torneos completos {c}')
      pub=pg.evaluate("(window.__STORE['publico/datos'].torneosHistorial||[]).map(t=>t.id+':'+t.estado)"); ok(pub[:2]==['T1:finalizado','T2:finalizado'], f'{dev}: la web pública sigue recibiendo los terminados {pub}')
      pg.evaluate("goToClubGestion('datos')"); pg.wait_for_timeout(1000)
      ok(pg.locator('.nube-archivo').count()==1 and 'aparte: 2' in pg.inner_text('.nube-archivo'), f'{dev}: el panel lo indica ({pg.inner_text(".nube-archivo") if pg.locator(".nube-archivo").count() else "-"})')
      pg.evaluate("document.querySelector('.im-nube-panel details').open=true"); pg.locator('.im-nube-panel').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'archivo_{dev}.png')
      sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: sin descuadre ({sw})')
      # otro dispositivo (sin nada en local): recupera los torneos
      st=pg.evaluate("window.__STORE"); pg2,errs2=pagina(b,vw,vh,mov,st,admin=True); pg2.on('dialog',lambda d:(dl.append(d.message),d.accept()))
      pg2.goto('https://test.local/app.html'); pg2.wait_for_timeout(3000); pg2.evaluate(SALTAR); pg2.wait_for_timeout(1500)
      m2=pg2.evaluate(MEM); ok([x['tit'] for x in m2]==['Torneo Uno','Torneo Dos','Torneo Vivo'] and not any(x['arch'] for x in m2), f'{dev}: otro dispositivo los carga completos {m2}')
      h2=pg2.evaluate(HIST); ok([x['arch']!='' for x in h2]==[True,True,False], f'{dev}: y no los vuelve a meter en el documento general {h2}')
      # abrir un terminado: vuelve entero mientras está abierto; el que se cierra no es terminado, sigue entero
      ok(not [e for e in errs2 if 'hasPending' not in e], f'{dev}: sin errores en el 2.º dispositivo {errs2}'); pg2.close()
    if caso=='remoto':
      # otro dispositivo cambia un terminado: llega la ficha con otra firma -> se trae del archivo
      pg.evaluate("""(()=>{const S=window.__STORE;const d=S['club/datos/torneos_archivo/T1'];const s=JSON.parse(d.json);s.meta.title='Uno Corregido';const j=JSON.stringify(s);
        S['club/datos/torneos_archivo/T1']={firma:firmaTexto(j),json:j};const raw=JSON.parse(JSON.stringify(S['club/datos']));raw.torneosHistorial[0].archivado=firmaTexto(j);raw._rev=(raw._rev||0)+1;raw._disp='otro';S['club/datos']=raw;
        aplicarDatosDeNube(raw);fijarBaseNube(raw._rev);})()"""); pg.wait_for_timeout(2500)
      m=pg.evaluate(MEM); ok(m[0]['tit']=='Uno Corregido' and not m[0]['arch'], f'{dev}: un cambio hecho en otro dispositivo llega bien {m[0]}')
      a=pg.evaluate("JSON.parse(window.__STORE['club/datos/torneos_archivo/T1'].json).meta.title"); ok(a=='Uno Corregido', f'{dev}: y no se pisa el archivo con lo viejo ({a})')
      # fallo al traer: no se pierde nada ni se toca la web
      pg.evaluate("""(()=>{window.__DENY=['/torneos_archivo'];const S=window.__STORE;const raw=JSON.parse(JSON.stringify(S['club/datos']));raw.torneosHistorial[1].archivado='999.zz';raw._rev=(raw._rev||0)+1;S['club/datos']=raw;
        aplicarDatosDeNube(raw);fijarBaseNube(raw._rev);TallerApp.getState().clientes[0].nombre='Toca';TallerApp.saveLocal();programarSyncNube();})()"""); pg.wait_for_timeout(3000)
      h=pg.evaluate(HIST); ok(h[1]['arch']=='999.zz' and not h[1]['snap'] and pg.evaluate("JSON.stringify(window.__STORE['club/datos']).includes('Toca')"), f'{dev}: si no se puede traer, la ficha queda pendiente y el resto se guarda {h[1]}')
      ok(pg.evaluate("JSON.parse(window.__STORE['club/datos/torneos_archivo/T2'].json).meta.title")=='Torneo Dos', f'{dev}: el archivo queda intacto')
      n=len(dl); pg.evaluate("showSection('torneo')"); pg.wait_for_timeout(500); pg.evaluate("TorneoApp.irATab('historial')"); pg.wait_for_timeout(500)
      pg.locator('tr',has_text='Torneo Dos').locator('button.btn-primary').first.click(); pg.wait_for_timeout(500)
      ok(any('descargando' in x for x in dl[n:]) and pg.evaluate("TorneoApp.getTorneoActivoId()")=='T3', f'{dev}: un torneo sin descargar no se abre vacío, avisa {dl[n:]}')
    if caso=='abrir':
      pg.evaluate("showSection('torneo')"); pg.wait_for_timeout(500); pg.evaluate("TorneoApp.irATab('historial')"); pg.wait_for_timeout(500)
      pg.locator('tr',has_text='Torneo Uno').locator('button.btn-primary').first.click(); pg.wait_for_timeout(3500)
      ok(pg.evaluate("TorneoApp.getTorneoActivoId()")=='T1' and pg.evaluate("TorneoApp.getState().meta.title")=='Torneo Uno', f'{dev}: un terminado archivado se abre con sus datos')
      h=pg.evaluate(HIST); ok(h[0]['snap'] and not h[0]['arch'] and h[1]['arch'], f'{dev}: mientras está abierto vuelve entero al documento general {h}')
      pg.evaluate("TorneoApp.irATab('historial')"); pg.wait_for_timeout(400)
      pg.locator('tr',has_text='Torneo Vivo').locator('button.btn-primary').first.click(); pg.wait_for_timeout(3500)
      h=pg.evaluate(HIST); ok(h[0]['arch'] and not h[0]['snap'] and h[2]['snap'], f'{dev}: al cerrarlo vuelve a quedar aparte {h}')
      pg.evaluate("TorneoApp.irATab('historial')"); pg.wait_for_timeout(400)
      pg.locator('tr',has_text='Torneo Dos').locator('button.btn-danger').first.click(); pg.wait_for_timeout(3000)
      ok(not pg.evaluate("!!window.__STORE['club/datos/torneos_archivo/T2']") and pg.evaluate("!!window.__STORE['club/datos/torneos_archivo/T1']") and len(pg.evaluate(HIST))==2, f'{dev}: al eliminar un torneo se borra también su archivo (y solo el suyo)')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
