_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import base64,sys
SALTAR="document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"
LOGO='data:image/png;base64,'+base64.b64encode(os.urandom(60000)).decode()
caso=sys.argv[1]
def sem():
  sd=json.loads(json.dumps(seed())); sd['club/datos']['club']={'nombre':'Club Prueba','localidad':'X','logo':LOGO,'tecnicos':[],'temporadaInicio':'','temporadaFin':''}
  st={'meta':{'title':'Viejo','date':'2026-01-01'},'categories':[],'config':{}}
  sd['club/datos']['torneosHistorial']=[{'id':'T1','nombre':'Viejo','fechaInicio':'2026-01-01','fechaFin':'2026-01-02','estado':'finalizado','snapshot':dict(st,relleno='y'*30000)},{'id':'T3','nombre':'Vivo','fechaInicio':'','fechaFin':'','estado':'en_curso','snapshot':st}]
  sd['club/datos']['torneoActivoId']='T3'; sd['club/datos']['torneo']=st; sd['club/datos']['_rev']=5
  return sd
CL="(()=>{const c=window.__STORE['club/datos'].club;return {logo:(c.logo||'').length,marca:c.logoAparte||''}})()"
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    pg,errs=pagina(b,vw,vh,mov,sem(),admin=True); dl=[]; pg.on('dialog',lambda d:(dl.append(d.message),d.accept()))
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(5000)
    c=pg.evaluate(CL); ok(c['logo']==0 and c['marca'], f'{dev}: sin tocar nada, el logo sale solo del documento general {c}')
    ok(pg.evaluate("window.__STORE['club/datos/taller_fotos/_club_logo'].foto")==LOGO, f'{dev}: guardado aparte, idéntico')
    ok(pg.evaluate("clubGlobal.logo")==LOGO, f'{dev}: en la app sigue el logo')
    h=pg.evaluate("window.__STORE['club/datos'].torneosHistorial.map(t=>!!t.snapshot+':'+!!t.archivado)"); ok(h==['false:true','true:false'], f'{dev}: y el torneo terminado también, sin tocar nada {h}')
    ok(pg.evaluate("window.__STORE['publico/datos'].club.logo")==LOGO, f'{dev}: la web sigue teniendo el logo')
    if caso=='base':
      pg.evaluate("guardarCopiaNube('manual-x','manual')"); pg.wait_for_timeout(1200)
      ok(pg.evaluate("(l)=>descomprimirTexto({fmt:window.__STORE['club/datos/copias/manual-x'].fmt,datos:window.__STORE['club/datos/copias/manual-x'].datos}).then(t=>JSON.parse(t).club.logo===l)",LOGO), f'{dev}: la copia de seguridad lleva el logo')
      pg.evaluate("goToClubGestion('datos')"); pg.wait_for_timeout(1000)
      ok(pg.locator('.nube-logo-aparte').count()==1 and pg.locator('.nube-archivo').count()==1, f'{dev}: el panel lo indica ({pg.inner_text(".nube-logo-aparte") if pg.locator(".nube-logo-aparte").count() else "-"})')
      pg.evaluate("document.querySelector('.im-nube-panel details').open=true"); pg.locator('.im-nube-panel').scroll_into_view_if_needed(); pg.screenshot(path=SP+f'logo_{dev}.png')
      st=pg.evaluate("window.__STORE"); pg2,errs2=pagina(b,vw,vh,mov,st,admin=True)
      pg2.goto('https://test.local/app.html'); pg2.wait_for_timeout(3000); pg2.evaluate(SALTAR); pg2.wait_for_timeout(4000)
      ok(pg2.evaluate("clubGlobal.logo")==LOGO and pg2.evaluate("!clubGlobal.logoAparte"), f'{dev}: otro dispositivo carga el logo')
      ok(pg2.evaluate("(l)=>[...document.querySelectorAll('img')].some(i=>i.src===l)",LOGO), f'{dev}: y lo pinta en pantalla')
      c=pg2.evaluate(CL); ok(c['logo']==0 and c['marca'], f'{dev}: y no lo vuelve a meter en el documento general {c}')
      ok(not [e for e in errs2 if 'hasPending' not in e], f'{dev}: sin errores 2.º {errs2}'); pg2.close()
    if caso=='cambio':
      L2='data:image/png;base64,'+base64.b64encode(os.urandom(3000)).decode()
      pg.evaluate("(l)=>{clubGlobal.logo=l;logoClubPendiente=null;saveClubGlobal()}",L2); pg.wait_for_timeout(4000)
      c2=pg.evaluate(CL); ok(pg.evaluate("window.__STORE['club/datos/taller_fotos/_club_logo'].foto")==L2 and c2['logo']==0 and c2['marca'] and c2['marca']!=c['marca'], f'{dev}: al cambiar el logo se actualiza aparte {c2}')
      ok(pg.evaluate("window.__STORE['publico/datos'].club.logo")==L2, f'{dev}: y en la web')
      # quitar
      pg.evaluate("(()=>{clubGlobal.logo='';logoClubPendiente=null;saveClubGlobal()})()"); pg.wait_for_timeout(3500)
      c3=pg.evaluate(CL); ok(c3=={'logo':0,'marca':''} and pg.evaluate("window.__STORE['publico/datos'].club.logo")=='', f'{dev}: al quitarlo desaparece de verdad {c3}')
    if caso=='fallo':
      # dispositivo nuevo que no consigue leer el logo: no lo borra a los demás ni de la web
      st=pg.evaluate("window.__STORE"); pg2,errs2=pagina(b,vw,vh,mov,st,admin=True); pg2.add_init_script("window.__DENY=['_club_logo']")
      pg2.goto('https://test.local/app.html'); pg2.wait_for_timeout(3000); pg2.evaluate(SALTAR); pg2.wait_for_timeout(1000)
      pg2.evaluate("(()=>{TallerApp.getState().clientes[0].nombre='Toca';TallerApp.saveLocal();programarSyncNube()})()"); pg2.wait_for_timeout(4000)
      c=pg2.evaluate(CL); ok(c['marca'] and pg2.evaluate("JSON.stringify(window.__STORE['club/datos']).includes('Toca')"), f'{dev}: si no puede leer el logo, guarda lo demás y deja la marca {c}')
      ok(pg2.evaluate("window.__STORE['publico/datos'].club.logo")==LOGO and pg2.evaluate("window.__STORE['club/datos/taller_fotos/_club_logo'].foto")==LOGO, f'{dev}: la web y el logo guardado quedan intactos')
      ok(not [e for e in errs2 if 'hasPending' not in e], f'{dev}: sin errores 2.º {errs2}'); pg2.close()
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
