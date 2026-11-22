_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import urllib.parse, io, sys
from PIL import Image, ImageDraw
im=Image.new('RGB',(600,900),'#D8C7A8'); dr=ImageDraw.Draw(im); dr.ellipse((150,60,450,480),outline='white',width=14); dr.line((300,480,300,860),fill='white',width=14)
bf=io.BytesIO(); im.save(bf,'JPEG',quality=70); FOTO='data:image/jpeg;base64,'+base64.b64encode(bf.getvalue()).decode()
SALTAR="document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"
BLOB="(async()=>{const i=document.querySelector('.im-enc-img');const r=await fetch(i.src);const b=await r.blob();return await new Promise(ok=>{const f=new FileReader();f.onload=()=>ok(f.result);f.readAsDataURL(b)})})()"
caso=sys.argv[1]
def sem(tel=None, sol=None):
  sd=json.loads(json.dumps(seed(sol))); t=sd['club/datos']['taller']
  t['pedidos'][0].update({'marcaModelo':'Yonex Astrox 88D Pro','cordajeId':'s088','cordajeIdH':'y1','tensionVertical':11.5,'tensionHorizontal':12,'pretensado':True,'notas':'Cuidado con el ojal 7, está tocado','fotoAntes':FOTO,
     'articulosAdicionales':[{'articuloId':'g1','cantidad':1,'precioUnitario':3,'nombre':'Grip Toalla Azul'}]})
  if tel: t['config']['telefonoEncordador']=tel
  return sd
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    if caso=='manual':
      pg,errs=pagina(b,vw,vh,mov,sem(),admin=True)
      pg.add_init_script("window.open=(u)=>{window.__abierto=u;return null}")
      pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(400)
      pg.evaluate("showSection('taller')"); pg.wait_for_timeout(900)
      c=pg.locator('.im-raqueta',has_text='Astrox 88D').first; c.scroll_into_view_if_needed()
      c.locator('summary, button',has_text='Más opciones').first.click(); pg.wait_for_timeout(300)
      pg.locator('.im-enc-abrir').first.click(); pg.wait_for_timeout(1500)
      ok(pg.locator('.im-enc').count()==1 and (pg.locator('.im-enc-img').get_attribute('src') or '').startswith('blob:'), f'{dev}: «Avisar al encordador» abre la ficha con su imagen')
      d=pg.evaluate(BLOB); open(SP+f'ficha_{dev}.png','wb').write(base64.b64decode(d.split(',')[1]))
      w,h=Image.open(SP+f'ficha_{dev}.png').size; ok(w==900 and h>1200, f'{dev}: imagen con la foto incluida ({w}×{h})')
      sw=pg.evaluate("document.documentElement.scrollWidth"); ok(sw<=vw+1, f'{dev}: sin descuadre ({sw})'); pg.screenshot(path=SP+f'enc_modal_{dev}.png')
      pg.locator('.im-enc-tel').fill('611 22 33 44'); pg.locator('.im-enc-texto').click(); pg.wait_for_timeout(300)
      u=urllib.parse.unquote(pg.evaluate("window.__abierto||''")); print('  ',u.replace('\n',' | ')[:420])
      ok(u.startswith('https://wa.me/34611223344?text=') and all(x in u for x in ('Raqueta: Yonex Astrox 88D Pro','Verticales: CORDAJE TOPO PA2055','Horizontales: Yonex BG65 · Blanco','Verticales 11,5 kg · Horizontales 12 kg','Pretensado: Sí','Grip Toalla Azul','ojal 7')), f'{dev}: el texto lleva raqueta, cordajes y tensión, al teléfono escrito')
      ok(pg.evaluate("TallerApp.getState().config.telefonoEncordador")=='611 22 33 44', f'{dev}: el teléfono se recuerda para la próxima')
      pg.evaluate("window.__abierto=''"); pg.locator('.im-enc-enviar').click(); pg.wait_for_timeout(1500)
      av=pg.inner_text('.im-enc-aviso'); ok(('descargada' in av or 'copiada' in av) and 'wa.me/34611223344' in pg.evaluate("window.__abierto||''"), f'{dev}: enviar prepara la imagen y abre el chat ({av[:60]})')
      pg.locator('.im-enc-cerrar').click(); ok(pg.locator('.im-enc').count()==0, f'{dev}: se cierra')
      pg.evaluate("TallerApp.irATab('config')"); pg.wait_for_timeout(600)
      ok(pg.locator('.im-cfg-encordador').input_value()=='611 22 33 44', f'{dev}: el teléfono aparece en Configuración')
      pg.locator('.im-cfg-encordador').fill(''); pg.locator('.im-cfg-encordador-ok').click(); pg.wait_for_timeout(300)
      ok(pg.evaluate("TallerApp.getState().config.telefonoEncordador")=='', f'{dev}: y se puede quitar')
    if caso=='nuevo':
      for tel in (None,'611223344'):
        pg,errs=pagina(b,vw,vh,mov,sem(tel),admin=True); pg.on('dialog',lambda d:d.accept())
        pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(400)
        pg.evaluate("showSection('taller')"); pg.wait_for_timeout(600)
        pg.evaluate("TallerApp.pedidoDesdeCorreo({clienteId:'c1'}); TallerApp.irATab('nuevo')"); pg.wait_for_timeout(700)
        pg.locator('button',has_text='Guardar en la cola').first.scroll_into_view_if_needed(); pg.locator('button',has_text='Guardar en la cola').first.click(); pg.wait_for_timeout(1500)
        n=pg.evaluate("TallerApp.getState().pedidos.length")
        if tel: ok(n==2 and pg.locator('.im-enc').count()==1 and pg.locator('.im-enc-tel').input_value()=='611223344', f'{dev}: con encordador puesto, al guardar una raqueta nueva sale la ficha para mandársela')
        else: ok(n==2 and pg.locator('.im-enc').count()==0, f'{dev}: sin encordador en Configuración, todo como antes')
        if tel: pg.locator('.im-enc-cerrar').click(); ok(pg.locator('.im-enc').count()==0, f'{dev}: «Ahora no» la cierra')
        ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
      continue
    if caso=='solicitud':
      sol={'s1':{'nombre':'Marta','apellidos':'Gil','telefono':'600333444','raqueta':'Victor Thruster K','cordajeId':'s123','cordajeNombre':'x','color':'Rosa-Blanco','cordajeIdH':'','cordajeNombreH':'','colorH':'','tension':11,'tensionH':11,'pretensado':False,'foto':FOTO,'comentarios':'','consentimiento':True,'creadoEn':AHORA-600000}}
      pg,errs=pagina(b,vw,vh,mov,sem('611223344',sol),admin=True)
      pg.goto('https://test.local/app.html'); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(400)
      pg.evaluate("showSection('taller'); TallerApp.irATab('cola')"); pg.wait_for_timeout(900)
      pg.locator('.im-solic-card').locator('button', has_text='Aceptar').click(); pg.wait_for_timeout(1800)
      ok(pg.locator('.im-enc').count()==1, f'{dev}: al aceptar una solicitud del QR sale la ficha para el encordador')
      d=pg.evaluate(BLOB); open(SP+f'ficha_sol_{dev}.png','wb').write(base64.b64decode(d.split(',')[1]))
      pg.locator('.im-enc-cerrar').click(); pg.wait_for_timeout(500)
      ok(pg.locator('.im-enc').count()==0 and 'seguimiento' in pg.inner_text('#tallerModalRoot'), f'{dev}: y después, el enlace de seguimiento para el cliente, como antes')
    ok(not [e for e in errs if 'hasPending' not in e], f'{dev}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
