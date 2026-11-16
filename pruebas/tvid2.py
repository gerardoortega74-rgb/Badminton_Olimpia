import json
exec(open('/home/claude/test/tform2.py').read().split("# foto de prueba")[0])
WEBM=open(SP+'prueba_intro.webm','rb').read()
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,860,False,'pc')):
    for q in ('tiendaonline=1','raqueta=1','tallerpublico=1&pedido=x'):
      pg,errs=pagina(b,vw,vh,mov,seed())
      pg.route('**/intro_idermay.mp4*',lambda r: r.fulfill(body=WEBM,content_type='video/webm'))
      pg.goto('https://test.local/app.html?'+q,wait_until='commit'); pg.wait_for_selector('.idv-intro',timeout=8000); pg.wait_for_timeout(2500)
      src=pg.evaluate("document.querySelector('.idv-video').currentSrc")
      ok(pg.evaluate("document.querySelector('.idv-video').currentTime")>0.8 and 'v=2' in src, f'{dev} {q}: se reproduce el vídeo nuevo')
      pg.wait_for_timeout(9000)
      ok(pg.locator('.idv-intro').count()==0, f'{dev} {q}: se retira al acabar')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev} {q}: sin errores {errs}'); pg.close()
  b.close()
print(sum(R),'/',len(R))
