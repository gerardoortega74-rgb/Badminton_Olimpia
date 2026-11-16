_t=open('/home/claude/test/tform2.py').read(); exec(_t[:_t.index("with sync_playwright() as p:")])
import re
SALTAR="document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Saltar')b.click()})"
STUB={'xlsx':'window.XLSX={ok:1};','pdf.min':'window.pdfjsLib={GlobalWorkerOptions:{}};','tesseract':'window.Tesseract={createWorker:()=>Promise.resolve({recognize:()=>Promise.resolve({data:{text:"hola"}})})};'}
with sync_playwright() as p:
  b=p.chromium.launch()
  for vw,vh,mov,dev in ((390,844,True,'mov'),(1366,700,False,'pc')):
    for q in ('raqueta=1','publico=1','tiendaonline=1','tallerpublico=1',''):
      pg,errs=pagina(b,vw,vh,mov,json.loads(json.dumps(seed())),admin=(q=='')); ped=[]
      def lib(r):
        ped.append(r.request.url)
        for k,v in STUB.items():
          if k in r.request.url: return r.fulfill(body=v,content_type='text/javascript')
        r.fulfill(status=404,body='')
      pg.route(re.compile(r'cdnjs|jsdelivr'),lib)
      pg.goto('https://test.local/app.html'+('?'+q if q else '')); pg.wait_for_timeout(3000); pg.evaluate(SALTAR); pg.wait_for_timeout(600)
      pes=[u for u in ped if 'xlsx' in u or 'pdf' in u or 'tesseract' in u]
      txt=len(pg.inner_text('body').strip())
      if q:
        ok(not pes and txt>40, f'{dev} ?{q}: no descarga Excel/PDF/OCR y la página se ve ({txt} car.) {pes}')
      else:
        ok(len(pes)==3 and pg.evaluate("!!window.XLSX&&!!pdfjsLib.GlobalWorkerOptions.workerSrc&&!!window.Tesseract"), f'{dev} app: las carga en segundo plano y quedan listas {len(pes)}')
        ok(pg.evaluate("esperarLibreria('Tesseract')")==True and pg.evaluate("esperarLibreria('pdfjsLib')")==True, f'{dev} app: lector de fotos y PDF disponibles')
        ok(pg.evaluate("esperarLibreria('XLSX')")==True, f'{dev} app: Excel disponible')
      ok(not [e for e in errs if 'hasPending' not in e], f'{dev} ?{q}: sin errores {errs}'); pg.close()
  b.close()
print('TOTAL',sum(R),'/',len(R))
