import sys; sys.argv=['x']
exec(open('tform2.py').read().split('with sync_playwright() as p:')[0])
SP2=SP
from playwright.sync_api import sync_playwright
# foto de prueba: mitad izquierda roja, derecha azul (3000x2000)
from PIL import Image
im=Image.new('RGB',(3000,2000),(220,30,30)); im.paste((30,30,220),(1500,0,3000,2000)); b=io.BytesIO(); im.save(b,'JPEG',quality=90)
DU='data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
from playwright.sync_api import sync_playwright
JS="""(modo)=>{window.__reelEsperaMs=5; window.__reelReintentoMs=5; let cont=0; const log=[]; let polls=0;
 const W=(o,st)=>Promise.resolve(new Response(JSON.stringify(o),{status:st||200}));
 window.tokenMeta=()=>'TK'; const r=redesCfg(); r.paginaId='P1'; r.instagramId='IG1';
 window.fetch=(u,o)=>{ const m=(o&&o.method)||'GET'; log.push(m+' '+u.split('?')[0]+(u.includes('video_url=')?' [video_url]':''));
  if(u.includes('rupload')) return modo==='ruok'?W({success:true}):Promise.reject(new TypeError('Failed to fetch'));
  if(u.includes('graph-video')) return modo==='gvcors'?Promise.reject(new TypeError('Failed to fetch')):W({id:'V9'});
  if(u.includes('/P1/videos')) return W({id:'V9'});
  if(u.includes('IG1/media_publish')) return W({id:'M1'});
  if(u.includes('IG1/media')) return W({id:'C1'});
  if(u.includes('/V9')&&m==='DELETE') return W({success:true});
  if(u.includes('/V9')) { polls++; return W(polls<3?{status:{video_status:'processing'}}:{source:'https://video.fbcdn.net/x.mp4',status:{video_status:'ready'}}); }
  if(u.includes('/C1')) { if(modo==='falla1'){cont++; if(cont===1) return W({status_code:'ERROR',status:'Error: Media upload has failed with error code 2207076'});} if(modo==='fallasiempre') return W({status_code:'ERROR',status:'Error: 2207076'}); return W({status_code:'FINISHED'}); }
  return W({error:{message:'?'}},400); };
 return publicarReelInstagram({id:'n',titulo:'T',texto:'x'}, new Blob(['x'],{type:'video/mp4'}), ()=>{}).then(res=>({res,log}),e=>({err:e.message,log}));}"""
with sync_playwright() as p:
  br=p.chromium.launch()
  pg,errs=pagina(br,1366,860,False,seed(),admin=True)
  pg.goto('https://test.local/app.html'); pg.wait_for_timeout(2500)
  for modo in ('cors','gvcors','ruok','falla1','fallasiempre'):
    o=pg.evaluate(JS,modo); print(modo,o)
    if modo=='falla1': ok(o.get('res',{}).get('mediaId')=='M1' and sum('[video_url]' in l for l in o['log'])==2, 'si Instagram falla una vez, reintenta y publica'); continue
    if modo=='fallasiempre': ok('no pudo procesar' in o.get('err','') and sum('[video_url]' in l for l in o['log'])==3, 'tras 3 fallos avisa'); continue
    if modo=='ruok': ok(o.get('res',{}).get('mediaId')=='M1' and not any('videos' in l for l in o['log']), 'si la subida directa funciona, no usa Facebook')
    else:
      ok(o.get('res',{}).get('mediaId')=='M1', f'{modo}: publica el reel en Instagram por Facebook')
      ok(any('[video_url]' in l for l in o['log']) and any(l.startswith('DELETE') for l in o['log']), f'{modo}: usa video_url y borra el vídeo oculto de Facebook')
  ok(not errs, f'sin errores {errs[:2]}')
print('TOTAL', sum(R), '/', len(R))
