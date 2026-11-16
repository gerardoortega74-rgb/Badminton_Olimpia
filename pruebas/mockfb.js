// Mock mínimo de Firebase compat (app + firestore + auth) para pruebas locales.
(function(){
  const S = window.__STORE = {};
  const seed = window.__SEED || {}; for (const k in seed) S[k] = JSON.parse(JSON.stringify(seed[k]));
  window.__DENY = window.__DENY || [];
  const denegado = p => (window.__DENY||[]).some(r => new RegExp(r).test(p));
  const err = () => { const e = new Error('Missing or insufficient permissions.'); e.code = 'permission-denied'; return e; };
  const clone = v => v === undefined ? undefined : JSON.parse(JSON.stringify(v));
  const listeners = [];
  const notify = () => setTimeout(() => listeners.slice().forEach(l => l.fire()), 0);
  let n = 0; const nid = () => 'm' + Date.now().toString(36) + (n++);
  function mkSnap(path){ const d = S[path]; return { id: path.split('/').pop(), exists: d !== undefined, data: () => clone(d), ref: docRef(path), metadata: { hasPendingWrites: false, fromCache: false } }; }
  function matchW(d, ws){ return ws.every(([f,op,v]) => { const x = d ? d[f] : undefined; return op==='=='?x===v: op==='in'?v.includes(x): op==='>='?x>=v: op==='<='?x<=v: op==='>'?x>v: op==='<'?x<v: op==='array-contains'?(x||[]).includes(v):true; }); }
  function qSnap(path, ws){ const pre = path + '/'; const docs = Object.keys(S).filter(k => k.startsWith(pre) && !k.slice(pre.length).includes('/') && matchW(S[k], ws)).map(mkSnap); return { docs, size: docs.length, empty: !docs.length, forEach: f => docs.forEach(f), metadata: { hasPendingWrites: false, fromCache: false }, docChanges: () => [] }; }
  function docRef(path){
    return { id: path.split('/').pop(), path,
      collection: c => colRef(path + '/' + c),
      get: () => denegado(path) ? Promise.reject(err()) : Promise.resolve(mkSnap(path)),
      set: (d, o) => { if (denegado(path)) return Promise.reject(err()); S[path] = (o && o.merge) ? Object.assign({}, S[path] || {}, clone(d)) : clone(d); notify(); return Promise.resolve(); },
      update: d => { if (denegado(path)) return Promise.reject(err()); S[path] = Object.assign({}, S[path] || {}, clone(d)); notify(); return Promise.resolve(); },
      delete: () => { if (denegado(path)) return Promise.reject(err()); delete S[path]; notify(); return Promise.resolve(); },
      onSnapshot: (ok, ko) => { const l = { fire: () => { if (denegado(path)) { ko && ko(err()); return; } ok(mkSnap(path)); } }; listeners.push(l); setTimeout(l.fire, 0); return () => { const i = listeners.indexOf(l); if (i >= 0) listeners.splice(i, 1); }; } };
  }
  function colRef(path, ws){ ws = ws || [];
    return { id: path.split('/').pop(), path,
      doc: id => docRef(path + '/' + (id || nid())),
      add: d => { const p = path + '/' + nid(); if (denegado(p)) return Promise.reject(err()); S[p] = clone(d); notify(); return Promise.resolve(docRef(p)); },
      where: (f, op, v) => colRef(path, ws.concat([[f, op, v]])),
      orderBy: () => colRef(path, ws), limit: () => colRef(path, ws),
      get: () => denegado(path) ? Promise.reject(err()) : Promise.resolve(qSnap(path, ws)),
      onSnapshot: (ok, ko) => { const l = { fire: () => { if (denegado(path + '/x')) { ko && ko(err()); return; } ok(qSnap(path, ws)); } }; listeners.push(l); setTimeout(l.fire, 0); return () => { const i = listeners.indexOf(l); if (i >= 0) listeners.splice(i, 1); }; } };
  }
  const db = { collection: c => colRef(c), doc: p => docRef(p),
    runTransaction: fn => { const t = { get: r => r.get(), set: (r, d, o) => { r.set(d, o); return t; }, update: (r, d) => { r.update(d); return t; } }; return Promise.resolve().then(() => fn(t)); },
    enablePersistence: () => Promise.resolve(), settings: () => {} };
  let user = window.__USER ? Object.assign({ getIdToken: () => Promise.resolve('t') }, window.__USER) : null;
  const authL = [];
  const auth = { get currentUser(){ return user; },
    onAuthStateChanged: f => { authL.push(f); setTimeout(() => f(user), 0); return () => {}; },
    signInWithEmailAndPassword: (e) => { user = { email: e, uid: 'u_' + e, emailVerified: true, getIdToken: () => Promise.resolve('t') }; authL.forEach(f => f(user)); return Promise.resolve({ user }); },
    createUserWithEmailAndPassword: (e) => Promise.resolve({ user: { email: e, uid: 'u_' + e } }),
    sendPasswordResetEmail: () => Promise.resolve(),
    signOut: () => { user = null; authL.forEach(f => f(null)); return Promise.resolve(); },
    setPersistence: () => Promise.resolve() };
  const fsFn = () => db; fsFn.FieldValue = { serverTimestamp: () => Date.now(), delete: () => null, arrayUnion: (...a) => a, increment: x => x };
  const authFn = () => auth; authFn.Auth = { Persistence: { LOCAL: 'local' } };
  const app = { firestore: fsFn, auth: authFn };
  window.firebase = { apps: [], initializeApp: () => { window.firebase.apps.push(app); return app; }, firestore: fsFn, auth: authFn, app: () => app };
})();
