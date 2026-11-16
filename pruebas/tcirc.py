exec(open('tportadas.py').read().split('with sync_playwright() as p:')[0])
def M(a,b,w): return {'id':a+b,'p1':a,'p2':b,'winner':w,'sets':[[21,10],[21,12]] if w==a else [[10,21],[12,21]]}
def ko(names):  # 8 jugadores, gana siempre el primero de cada partido
  P=[{'id':'p%d'%i,'name':n} for i,n in enumerate(names)]
  r1=[M('p0','p7','p0'),M('p3','p4','p3'),M('p1','p6','p1'),M('p2','p5','p2')]
  r2=[M('p0','p3','p0'),M('p1','p2','p1')]; r3=[M('p0','p1','p0')]
  return P,{'rounds':[r1,r2,r3]}
def cat(id,name,kind,P,K=None,groups=None,matches=None):
  return {'id':id,'name':name,'kind':kind,'enabled':True,'players':P,'groups':groups or [],'matches':matches or [],'knockout':K or {'rounds':[]}}
N1=['Ana Ruiz','Bea Gil','Carla Sanz','Dora Paz','Eva Mar','Fe Ros','Gema Lis','Hada Sol']
P,K=ko(N1); c1=cat('IF_catA','Individual Femenino Categoría A','single',P,K)
# dobles: liga de 3 parejas (un grupo)
PD=[{'id':'d1','name':'Luis Ortega / Raúl Ortega'},{'id':'d2','name':'Juan Pi / Leo Ra'},{'id':'d3','name':'Iker Ro / Max Tu'}]
gm=[dict(M('d1','d2','d1'),groupIndex=0),dict(M('d1','d3','d1'),groupIndex=0),dict(M('d2','d3','d2'),groupIndex=0)]
c2=cat('DM_catB','Dobles Masculino Categoría B','double',PD,groups=[{'name':'Grupo A','playerIds':['d1','d2','d3']}],matches=gm)
st1={'meta':{'title':'Jornada 1','date':'2026-09-27'},'config':{'courts':4,'matchMinutes':25,'bufferMinutes':5,'restMinutes':10,'startTime':'09:00'},'categories':[c1,c2]}
# jornada 2: Bea gana (cambio de nombres con tilde para Ana)
N2=['Bea Gil','Ána Ruiz','Carla Sanz','Dora Paz','Eva Mar','Fe Ros','Gema Lis','Ivet Nou']
P2,K2=ko(N2); K2['rounds'][2]=[M('p0','p1',None)]; K2['rounds'][2][0]['winner']=None  # final sin jugar => no cuenta todavía
st2={'meta':{'title':'Jornada 2','date':'2026-10-18'},'config':st1['config'],'categories':[cat('IF_catA','Individual Femenino Categoría A','single',P2,K2)]}
st2b=json.loads(json.dumps(st2)); st2b['categories'][0]['knockout']['rounds'][2]=[M('p0','p1','p0')]
hist=[{'id':'t1','nombre':'Jornada 1','fechaInicio':'2026-09-27','estado':'finalizado','snapshot':st1},{'id':'t2','nombre':'Jornada 2','fechaInicio':'2026-10-18','estado':'en_curso','snapshot':st2}]
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    seed={'club/datos':{'club':{'nombre':'Olimpia'},'torneosHistorial':hist,'torneoActivoId':'t2','torneo':st2,'taller':{'clientes':[],'articulos':[],'pedidos':[],'config':{}}}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('dialog',lambda d: d.accept())
    pg.route('**/*',ruta(HTML))
    pg.add_init_script('window.__SEED='+json.dumps(seed)+';window.__USER={email:"gerardoortega74@gmail.com",uid:"uadm",emailVerified:true};')
    pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500); pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(800)
    pg.evaluate("showSection('torneo')"); pg.wait_for_timeout(800)
    pg.evaluate("TorneoApp.irATab('circuito')"); pg.wait_for_timeout(600)
    clk=lambda sel: (pg.locator(sel).first.tap() if mov else pg.locator(sel).first.click())
    clk('.cir-nuevo'); pg.wait_for_timeout(400)
    for i in range(3): clk('.cir-j-anadir'); pg.wait_for_timeout(300)
    ok(pg.locator('.cir-jornada').count()==3, f'{dev}: 3 jornadas')
    pg.locator('.cir-j-torneo').nth(0).select_option('t1'); pg.wait_for_timeout(300)
    pg.locator('.cir-j-torneo').nth(1).select_option('t2'); pg.wait_for_timeout(300)
    pg.locator('.cir-j-fecha').nth(2).fill('2026-12-13'); pg.locator('.cir-j-fecha').nth(2).dispatch_event('change'); pg.wait_for_timeout(300)
    rk=pg.evaluate("rankingCircuito(circuitosCfg()[0])")
    f=next(r for r in rk if r['id']=='IF_catA')['filas']; d=next(r for r in rk if r['id']=='DM_catB')['filas']
    tot={x['nombre']:x['total'] for x in f}; print(dev,tot, {x['nombre']:x['total'] for x in d})
    ok(tot.get('Ana Ruiz')==100 and tot.get('Bea Gil')==80 and tot.get('Dora Paz')==60 and tot.get('Hada Sol')==40, f'{dev}: J1 puntos por ronda (100/80/60/40)')
    ok(f[0]['nombre']=='Ana Ruiz', f'{dev}: jornada 2 sin final jugada no cuenta todavía')
    dd={x['nombre']:x['total'] for x in d}
    ok(dd.get('Luis Ortega')==100 and dd.get('Raúl Ortega')==100 and dd.get('Juan Pi')==80 and dd.get('Iker Ro')==60, f'{dev}: dobles en liga: cada jugador suma {dd}')
    # termina la final de la jornada 2
    pg.evaluate("(s)=>{TorneoApp.setState(s)}", st2b); pg.evaluate("TorneoApp.irATab('circuito')"); pg.wait_for_timeout(500)
    rk=pg.evaluate("rankingCircuito(circuitosCfg()[0])"); f=next(r for r in rk if r['id']=='IF_catA')['filas']
    tot={x['nombre']:x['total'] for x in f}; print(dev,tot)
    ok(tot.get('Bea Gil')==180 and (tot.get('Ana Ruiz')==180 or tot.get('Ána Ruiz')==180) and len([x for x in f if x['nombre'].lower().startswith('ana')])==1, f'{dev}: suma las 2 jornadas y une «Ána/Ana» {tot}')
    ok(f[0]['pos']==1 and f[1]['pos']==1, f'{dev}: empate a puntos = mismo puesto')
    ok(tot.get('Hada Sol')==40 and tot.get('Ivet Nou')==40, f'{dev}: quien juega solo una jornada suma solo esa')
    pg.locator('.cir-cat').first.scroll_into_view_if_needed(); pg.screenshot(path=SP+f'cir_admin_{dev}.png')
    ok(pg.locator('.cir-tabla tbody tr').count()>=8, f'{dev}: tabla de clasificación en la app')
    ok(pg.evaluate("estadoPublicoParaNube().circuitos.length")==0, f'{dev}: sin marcar «Publicar» el circuito no sale')
    pg.locator('.cir-publicado').first.check(); pg.wait_for_timeout(400)
    pub=pg.evaluate("JSON.parse(JSON.stringify(estadoPublicoParaNube().circuitos))")
    ok(len(pub)==1 and pub[0]['jornadas'][0]['estado']=='jugada' and pub[0]['jornadas'][1]['estado']=='jugada' and pub[0]['jornadas'][2]['estado']=='proxima' and pub[0]['jornadas'][1]['fecha']=='2026-10-18', f'{dev}: se publica con estados de jornadas {[j["estado"] for j in pub[0]["jornadas"]]}')
    ok(not errs, f'{dev}: sin errores admin {errs}'); pg.close()
    # Página pública
    pub[0]['streamingUrl']='https://youtube.com/@x'; pub[0]['cuotas']='1 modalidad: 14 €\n2 modalidades: 20 €'; pub[0]['descripcion']='Circuito abierto para todos los niveles.'
    sd={'publico/datos':{'club':{'nombre':'Club Bádminton Olimpia'},'circuitos':pub,'torneosHistorial':[],'web':{}}}
    pg=b.new_page(viewport={'width':vw,'height':vh},is_mobile=mov,has_touch=mov); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.route('**/*',ruta(HTML)); pg.add_init_script('window.__SEED='+json.dumps(sd)+';')
    pg.goto('https://test.local/app.html?publico=1&circuito='+pub[0]['id']); pg.wait_for_timeout(3000)
    pg.evaluate("document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"); pg.wait_for_timeout(600)
    ok(pg.locator('.cir-hero h1').count()==1 and pg.locator('.cir-jor').count()==3, f'{dev}: página pública con portada y 3 jornadas')
    ok(pg.locator('.cir-tabla tbody tr').count()>=8, f'{dev}: clasificación pública')
    ok('se abrirá' in pg.inner_text('.cir-pub') and '14 €' in pg.inner_text('.cir-pub'), f'{dev}: inscripción: cuotas y aviso (próxima jornada sin torneo aún)')
    ok(pg.locator('a.cir-volver').count()==2 and pg.locator('a.cir-volver').first.get_attribute('href')=='./', f'{dev}: botón «Volver a la web del club» arriba y abajo')
    sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: sin scroll horizontal ({sw})')
    pg.screenshot(path=SP+f'cir_pub_{dev}.png', full_page=True)
    ok(not errs, f'{dev}: sin errores públicos {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
