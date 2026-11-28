// Bölüm 3 setleri: sabah şehir (durak), Atlas Holding girişi, İK ofisi. Her biri { scene, update(t, shot, cam, post, renderer) }
import * as THREE from 'three';
import { PX, ramp, hex, h2, fbm, texOf, cobbles, woodPlanks, plaster, billboard, glow, blob, mulberry } from './px.js';
import { mat, mesh, box } from './kit.js';
import { sky, particles } from './fx.js';
import { makeChar } from './chars.js';
import { T } from './story.js';
import { clamp, seg, ss, eio, lerp, track } from '/core/lib.js';

const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const solid = (col, o = {}) => new THREE.MeshStandardMaterial({ color: col, roughness: o.r ?? .85, metalness: o.m ?? 0, emissive: o.em ?? '#000000', emissiveIntensity: o.ei ?? 1 });
function frameOf(ch, name) { ch.frame(name); }
const walk = (t, f = 8) => ['w0', 'w1', 'w2', 'w3'][Math.floor(t * f) % 4];
const idle = (t, s = 0) => (Math.floor(t * 1.4 + s) % 2 ? 'idle1' : 'idle0');
const blinkOr = (t, base, s = 0) => (((t + s) % 3.7) < .12 ? 'blink' : base);

// —— Piksel yüzeyler ——
function asphalt(w = 96, h = 96, s = 1) { const P = new PX(w, h), C = ramp(['#1e2024', '#2a2c32', '#36383f', '#44464e'], .45); P.fill((x, y) => C(.45 + (fbm(x * .15, y * .15, s) - .5) * .7 + (h2(x, y, s) - .5) * .25, x, y)); return P.done(); }
function stoneWall(w = 96, h = 96, o = {}) { const C = ramp(o.cols ?? ['#7c7a76', '#9a9790', '#b4b0a8', '#cbc7bd'], .45), P = new PX(w, h); P.fill((x, y) => { const row = Math.floor(y / 12), off = row % 2 ? 12 : 0, j = (x + off) % 24 === 0 || y % 12 === 0; return j ? C(.12, x, y) : C(.55 + (fbm(x * .2, y * .2, o.seed ?? 3) - .5) * .5, x, y); }); return P.done(); }
function plainWall(cols, seed = 2) { const C = ramp(cols, .45), P = new PX(96, 96); P.fill((x, y) => C(.55 + (fbm(x * .12, y * .12, seed) - .5) * .35 + (h2(x, y, seed) - .5) * .12 - (y < 3 ? .3 : 0), x, y)); return P.done(); }
function sidewalk() { const C = ramp(['#6a665e', '#86827a', '#a19c92', '#b8b3a8'], .45), P = new PX(96, 96); P.fill((x, y) => (x % 24 === 0 || y % 24 === 0) ? C(.15, x, y) : C(.6 + (h2(x >> 2, y >> 2, 4) - .5) * .3 + (fbm(x * .3, y * .3, 9) - .5) * .3, x, y)); return P.done(); }
function carpet() { const C = ramp(['#2a3038', '#363e48', '#444e5a', '#525e6c'], .45), P = new PX(96, 96); P.fill((x, y) => C(.5 + ((x + y) % 4 === 0 ? -.12 : 0) + (fbm(x * .2, y * .2, 7) - .5) * .3, x, y)); return P.done(); }
function glassFacade(seed = 1) { const F = ramp(['#2a2e34', '#3e444c', '#575e68'], .45), G = ramp(['#1c3048', '#2e4c6c', '#4a7096', '#7aa0c4', '#bcd4ea'], .45), P = new PX(96, 96); P.fill((x, y) => { if (x % 24 < 2 || y % 32 < 2) return F(.6 - (x % 24 === 1 || y % 32 === 1 ? .3 : 0), x, y); const v = .45 + ((x % 24) + (32 - y % 32)) * .012 + (h2(x >> 3, y >> 4, seed) - .5) * .2; return G(v, x, y); }); return P.done(); }
function canopyTex(seed) { const P = new PX(44, 64), L = ramp(['#14301a', '#1e4a24', '#2e6a30', '#4a8a3a', '#78aa4a'], .22), B = ramp(['#2a1a10', '#40281a', '#5a3a24'], .22);
  for (let y = 40; y < 64; y++) for (let x = 20; x < 25; x++) P.set(x, y, B(.7 - (x - 20) * .15, x, y));
  P.fill((x, y) => { const dx = (x - 22) / 20, dy = (y - 22) / 21, r = dx * dx + dy * dy, n = fbm(x * .25, y * .25, seed); if (r + (n - .5) * .5 > 1) return null; return L(.75 - dy * .3 - dx * .25 + (n - .5) * .6, x, y); }); P.outline(.3); return texOf(P.done()); }
function signTex(text, w = 200, h = 26, col = '#e8d6a0') { // piksel tabela: düşük çözünürlükte yaz, eşikle
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.fillStyle = '#1a1c22'; g.fillRect(0, 0, w, h);
  g.font = '700 18px Cinzel'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(text, w / 2, h / 2 + 1);
  const d = g.getImageData(0, 0, w, h), C = hex(col); for (let i = 0; i < d.data.length; i += 4) { const on = d.data[i] > 120; d.data[i] = on ? C[0] : 26; d.data[i + 1] = on ? C[1] : 28; d.data[i + 2] = on ? C[2] : 34; d.data[i + 3] = 255; }
  g.putImageData(d, 0, 0); const t = new THREE.CanvasTexture(c); t.magFilter = t.minFilter = THREE.NearestFilter; t.colorSpace = THREE.SRGBColorSpace; return t; }
function tree(x, z, s = 1, seed = 1) { const b = billboard(canopyTex(seed), 44 / 24 * 1.5 * s, 64 / 24 * 1.5 * s); b.position.set(x, 0, z); return b; }
function aptBlock({ x, z, w, d, h, cols, seed = 1, ry = 0 }) {
  const g = new THREE.Group(), wm = mat(plainWall(cols, seed));
  const b = mesh(new THREE.BoxGeometry(w, h, d).translate(0, h / 2, 0), wm); g.add(b);
  const glass = solid('#5a7898', { r: .25, m: .3, em: '#20324a', ei: .4 }), frame = solid('#2a2a2e');
  for (let fy = 1.2; fy < h - .8; fy += 2.6) for (let fx = -w / 2 + 1; fx <= w / 2 - 1; fx += 1.8) {
    const win = new THREE.Mesh(new THREE.PlaneGeometry(.9, 1.2), (h2(fx * 7, fy * 3, seed) > .8) ? solid('#c8a060', { em: '#ffcf80', ei: .7 }) : glass); win.position.set(fx, fy, d / 2 + .01); g.add(win);
    const sill = new THREE.Mesh(new THREE.BoxGeometry(1.05, .08, .14), frame); sill.position.set(fx, fy - .64, d / 2 + .06); g.add(sill);
  }
  const roof = mesh(new THREE.BoxGeometry(w + .3, .3, d + .3).translate(0, h + .15, 0), mat(plainWall(['#4a4a4e', '#5c5c62', '#6e6e74'], seed + 9))); g.add(roof);
  g.position.set(x, 0, z); g.rotation.y = ry; return g;
}
function dayLights(scene, o = {}) {
  const sun = new THREE.DirectionalLight(o.sun ?? '#ffe2b8', o.si ?? 2.4); sun.position.set(...(o.sp ?? [-18, 22, 14])); sun.target.position.set(0, 0, 0);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -25, right: 25, top: 25, bottom: -25, near: 1, far: 120 }); sun.shadow.bias = -.0006; sun.shadow.normalBias = .02;
  const hemi = new THREE.HemisphereLight(o.hs ?? '#a8c4ec', o.hg ?? '#4a3e34', o.hi ?? 1.1);
  scene.add(sun, sun.target, hemi); return { sun, hemi };
}
function frontFill(scene, col = '#ffe8cc', i = 1.4, r = 8) { const L = new THREE.PointLight(col, i, r, 1.5); scene.add(L); return L; }

// ————————————————————————————————— ŞEHİR (sabah durak) —————————————————————————————————
export function buildCity() {
  const scene = new THREE.Scene(); scene.fog = new THREE.FogExp2('#b8c8d8', .016);
  const SK = sky({ top: '#3a6aa8', mid: '#7aa2d0', hor: '#e6d6bc', moonDir: V3(-.6, .35, -1), moonCol: '#fff4dc', moonI: 1.6 }); scene.add(SK.mesh);
  const L = dayLights(scene, { sp: [-20, 18, 10] });
  const road = mesh(new THREE.BoxGeometry(80, .1, 7).translate(0, -.05, 0), mat(asphalt())); scene.add(road);
  const lineM = solid('#e8e2d0'); for (let x = -40; x < 40; x += 3) { const l = new THREE.Mesh(new THREE.BoxGeometry(1.4, .02, .14), lineM); l.position.set(x, .01, 0); scene.add(l); }
  const swM = mat(sidewalk());
  const swN = mesh(new THREE.BoxGeometry(80, .22, 5).translate(0, .11, -6), swM); scene.add(swN);
  const swS = mesh(new THREE.BoxGeometry(80, .22, 4).translate(0, .11, 5.5), swM); scene.add(swS);
  const curbM = solid('#9a968c'); for (const z of [-3.5, 3.5]) { const c = new THREE.Mesh(new THREE.BoxGeometry(80, .24, .2), curbM); c.position.set(0, .12, z); c.receiveShadow = true; scene.add(c); }
  // binalar
  const B = [[-14, -12, 8, 6, 13, ['#a88a6a', '#c2a482', '#d8bc98', '#e8d0ae'], 1], [-5, -12, 7, 6, 16, ['#8a96a2', '#a2aeb8', '#bcc6ce', '#d2dae0'], 2], [4, -12, 8, 6, 11, ['#b8a088', '#cfb89e', '#e2ceb4', '#f0e0c8'], 3], [13, -12, 7, 6, 15, ['#9a7c6c', '#b49484', '#caac9a', '#dcc2b0'], 4], [22, -12, 8, 6, 12, ['#8e9a8a', '#a6b2a2', '#bec8ba', '#d2dccc'], 5], [-23, -12, 8, 6, 10, ['#a69a8a', '#beb2a2', '#d2c8b8', '#e4dccc'], 6]];
  for (const [x, z, w, d, h, c, s] of B) scene.add(aptBlock({ x, z, w, d, h, cols: c, seed: s }));
  [[-17, -4.6, 1, 1], [-8.5, -4.8, .9, 2], [8, -4.7, 1.05, 3], [16, -4.6, .95, 4], [-6, 5.6, .7, 5], [9, 5.5, .75, 6]].forEach(a => scene.add(tree(...a)));
  // durak
  const stop = new THREE.Group(), pole = solid('#2e3238', { m: .5, r: .4 });
  for (const x of [-1.6, 1.6]) { const p = new THREE.Mesh(new THREE.BoxGeometry(.1, 2.5, .1), pole); p.position.set(x, 1.25, -4.6); p.castShadow = true; stop.add(p); }
  const roofS = new THREE.Mesh(new THREE.BoxGeometry(3.6, .12, 1.5), solid('#3a4a5a', { m: .3 })); roofS.position.set(0, 2.55, -4.3); roofS.castShadow = true; stop.add(roofS);
  const backP = new THREE.Mesh(new THREE.BoxGeometry(3.2, 1.6, .05), new THREE.MeshStandardMaterial({ color: '#9ab8d0', transparent: true, opacity: .35, roughness: .1 })); backP.position.set(0, 1.4, -5); stop.add(backP);
  const bench = new THREE.Mesh(new THREE.BoxGeometry(2.4, .1, .45), solid('#6a4a2e')); bench.position.set(0, .5, -4.7); bench.castShadow = true; stop.add(bench);
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(.7, .5), new THREE.MeshStandardMaterial({ map: signTex('DURAK', 70, 50, '#f0e6c8') })); sign.position.set(1.95, 2.3, -4.6); stop.add(sign);
  const sp = new THREE.Mesh(new THREE.BoxGeometry(.08, 2.8, .08), pole); sp.position.set(1.95, 1.4, -4.65); stop.add(sp);
  scene.add(stop);
  const wallet = new THREE.Mesh(new THREE.BoxGeometry(.22, .05, .14), solid('#6a3a1c', { r: .6 })); wallet.position.set(-.3, .58, -4.6); wallet.rotation.y = .4; wallet.castShadow = true; scene.add(wallet);
  // otobüs
  const bus = new THREE.Group();
  { const body = new THREE.Mesh(new THREE.BoxGeometry(10, 2.6, 2.5), solid('#2a6aa8', { r: .5, m: .2 })); body.position.y = 1.75; body.castShadow = true; bus.add(body);
    const stripe = new THREE.Mesh(new THREE.BoxGeometry(10.02, .3, 2.52), solid('#e8e4d8')); stripe.position.y = .75; bus.add(stripe);
    const glass = solid('#1a2a3a', { r: .1, m: .5 }); const gw = new THREE.Mesh(new THREE.BoxGeometry(9.2, 1, 2.54), glass); gw.position.set(0, 2.25, 0); bus.add(gw);
    const top = new THREE.Mesh(new THREE.BoxGeometry(9.6, .25, 2.3), solid('#d8dce0')); top.position.y = 3.15; bus.add(top);
    for (const x of [-3.4, 3.2]) for (const z of [-1.2, 1.2]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.48, .48, .3, 12).rotateX(Math.PI / 2), solid('#141414')); w.position.set(x, .48, z); bus.add(w); }
    const rs = new THREE.Mesh(new THREE.PlaneGeometry(1.2, .35), new THREE.MeshStandardMaterial({ map: signTex('34', 40, 12, '#ffb040'), emissive: '#ffffff', emissiveMap: signTex('34', 40, 12, '#ffb040'), emissiveIntensity: .8 })); rs.position.set(5.01, 2.9, 0); rs.rotation.y = Math.PI / 2; bus.add(rs); }
  scene.add(bus);
  // karakterler
  const hero = makeChar('hero'), amca = makeChar('amca'), murat = makeChar('murat'); scene.add(hero.root, amca.root, murat.root);
  const aptDoor = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.3, .08), solid('#4a2e1c', { r: .6 })); aptDoor.position.set(4.5, 1.37, -8.98); scene.add(aptDoor);
  const aptLamp = new THREE.Mesh(new THREE.BoxGeometry(.2, .2, .1), solid('#ffe0a0', { em: '#ffd080', ei: 1.5 })); aptLamp.position.set(4.5, 2.8, -8.92); scene.add(aptLamp);
  amca.root.position.set(-.2, .22, -2.7); hero.root.position.set(-1.05, .22, -2.75);
  const fill = frontFill(scene, '#fff0d8', 1.2, 7);
  // sabah tozu
  const dust = particles(120, (i, t, o) => { const R = mulberry(i + 1); const a = R() * 30 - 15, b = R() * 6 - 5; o.x = a + Math.sin(t * .2 + i) * .6; o.y = .5 + R() * 4 + Math.sin(t * .3 + i * 2) * .3; o.z = b; o.a = .35 * (.5 + .5 * Math.sin(t * .7 + i)); o.s = .05; o.r = 1; o.g = .95; o.b = .8; }, { soft: true });
  scene.add(dust);
  const cam = track([[6, [12, 19, 27]], [11, [7, 15.5, 22.5]], [14, [5, 14, 20.5]], [17, [5, 16.5, 23.5]]]);
  const look = track([[6, [1, 1, -3]], [11, [-.5, .8, -3]], [17, [-.5, 1.3, -3.5]]]);
  return { scene, hero, update(t, shot, camera, post) {
    const id = shot.id;
    let cp, lk;
    if (id === 'recap') { const k = seg(t, 0, 5.0); cp = [lerp(4.2, 3.4, k), lerp(6.2, 5.6, k), lerp(9.8, 8.8, k)]; lk = [-.4, 1.3, -4.0]; }
    else { cp = track([[5.0, [7, 8, 7]], [8.6, [6.4, 5.4, 2.6]], [14.2, [5.6, 5.8, 3.2]]])(t); lk = track([[5.0, [1.6, 1, -6.5]], [8.6, [3.9, 1.1, -8.1]], [14.2, [3.0, 1.1, -7.6]]])(t); }
    camera.fov = 34; camera.position.set(...cp); camera.lookAt(...lk); camera.updateProjectionMatrix();
    bus.visible = false; wallet.visible = false; amca.root.visible = false;
    let hx = -.4, hz = -4.0, hf = 'fwd';
    if (id === 'street') {
      const u = seg(t, 5.0, 7.8); hx = lerp(-.4, 3.4, u); hz = lerp(-4.0, -7.9, u); hf = u < 1 ? walk(t, 12) : (t < 8.7 ? 'fwd' : 'idle0');
      if (t > 12.3) { const v = seg(t, 12.3, 14.2); hx = lerp(3.4, -3, v); hz = lerp(-7.9, -5, v); hf = walk(t, 14); }
    }
    hero.root.position.set(hx, .22, hz); hero.frame(hf); hero.face(camera, id === 'street' && t > 12.3);
    murat.root.visible = id === 'street' && t > T.muratOut;
    murat.root.position.set(lerp(4.5, 4.4, seg(t, T.muratOut, T.muratOut + .6)), .22, lerp(-8.85, -8.3, seg(t, T.muratOut, T.muratOut + .8)));
    murat.frame(t > 8.8 && t < 12.3 ? (Math.floor(t * 2.5) % 2 ? 'up' : 'up1') : (t < 8.7 ? 'head' : 'idle0')); murat.face(camera, true);
    fill.position.copy(hero.root.position).add(V3(.8, 1.4, 2));
    dust.userData.update?.(t);
    post.dof.focus = camera.position.distanceTo(hero.root.position.clone().add(V3(0, .8, 0))); post.dof.aper = 300; post.dof.maxCoc = 14;
    post.vig.uniforms.warm.value = .14; post.vig.uniforms.amt.value = .5; post.bloom.threshold = .92; post.bloom.strength = .35;
  } };
}

// ————————————————————————————————— ATLAS HOLDİNG GİRİŞİ —————————————————————————————————
export function buildGate() {
  const scene = new THREE.Scene(); scene.fog = new THREE.FogExp2('#c4ccd6', .02);
  const SK = sky({ top: '#3c6ca8', mid: '#86aad4', hor: '#e8dcc4', moonDir: V3(-.5, .4, -1), moonCol: '#fff4dc', moonI: 1.4 }); scene.add(SK.mesh);
  const L = dayLights(scene, { sp: [-16, 20, 12], si: 2.2 });
  const plaza = mesh(new THREE.BoxGeometry(50, .2, 30).translate(0, -.1, 4), mat(sidewalk())); scene.add(plaza);
  const facade = new THREE.Group(), stoneM = mat(stoneWall(96, 96, { seed: 5 })), glassM = mat(glassFacade(2), { rough: .25 });
  facade.add(mesh(new THREE.BoxGeometry(18, 22, 1).translate(0, 11, -4.5), glassM));
  facade.add(mesh(new THREE.BoxGeometry(6, 5.2, 1.4).translate(0, 2.6, -3.9), stoneM));   // giriş bloğu
  for (const x of [-9.4, 9.4]) facade.add(mesh(new THREE.BoxGeometry(1, 22.4, 1.4).translate(x, 11.2, -4.4), stoneM));
  const signM = new THREE.MeshStandardMaterial({ map: signTex('ATLAS HOLDİNG', 220, 26), emissive: '#ffffff', emissiveMap: signTex('ATLAS HOLDİNG', 220, 26), emissiveIntensity: .5 });
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(5.6, .66), signM); sign.position.set(0, 4.5, -3.18); facade.add(sign);
  // kapı (iki kanat, kayar)
  const doorM = new THREE.MeshStandardMaterial({ color: '#6a8aa8', roughness: .55, metalness: .1, transparent: true, opacity: .75 });
  const dl = new THREE.Mesh(new THREE.BoxGeometry(1.1, 2.6, .06), doorM), dr = dl.clone(); dl.position.set(-.55, 1.3, -3.17); dr.position.set(.55, 1.3, -3.17); facade.add(dl, dr);
  const dark = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 2.6), solid('#1a1e24', { em: '#3a3020', ei: .5 })); dark.position.set(0, 1.3, -3.21); facade.add(dark);
  const steps = mesh(new THREE.BoxGeometry(5, .16, 1.2).translate(0, .08, -2.6), stoneM); facade.add(steps);
  scene.add(facade);
  for (const x of [-3.6, 3.6]) { const p = new THREE.Mesh(new THREE.BoxGeometry(.7, .9, .7), solid('#6a6a70')); p.position.set(x, .45, -2.4); p.castShadow = true; scene.add(p); const tr = tree(x, -2.4, .5, x > 0 ? 3 : 4); tr.position.y = .9; scene.add(tr); }
  const hero = makeChar('hero'), guard = makeChar('guard'); scene.add(hero.root, guard.root);
  const fill = frontFill(scene, '#fff0d8', 1.3, 7);
  return { scene, hero, update(t, shot, camera, post) {
    const lt = t - 42;
    const cam = shot.id === 'choice' ? track([[50, [2.6, 4.4, 7.2]], [60, [3.6, 6.4, 11]]]) : track([[42, [4.2, 5.4, 10]], [50, [2.6, 4.4, 7.2]]]);
    camera.fov = 34; camera.position.set(...cam(t)); camera.lookAt(-.7, 1.6, -2.2); camera.updateProjectionMatrix();
    hero.root.visible = true; hero.root.position.set(-1.5, .02, -1.7); hero.frame(t > 48.8 ? 'head' : idle(t)); hero.face(camera);
    guard.root.position.set(-.2, .02, -2.0); guard.frame(t > 42.5 && t < 48.2 ? (Math.floor(t * 2) % 2 ? 'point' : 'idle0') : 'cross'); guard.face(camera, true);
    dl.position.x = -.55; dr.position.x = .55;
    fill.position.copy(hero.root.position).add(V3(.6, 1.4, 2));
    post.dof.focus = camera.position.distanceTo(hero.root.position.clone().add(V3(.6, .8, 0))); post.dof.aper = 300; post.dof.maxCoc = 14;
    const V = post.vig.uniforms; V.amt.value = .55; V.warm.value = .2; post.bloom.threshold = .92; post.bloom.strength = .35;
  } };
}

// ————————————————————————————————— İK OFİSİ —————————————————————————————————
export function buildOffice() {
  const scene = new THREE.Scene(); scene.fog = new THREE.FogExp2('#2a2620', .02);
  const floor = mesh(new THREE.BoxGeometry(8, .2, 7).translate(0, -.1, -.5), mat(woodPlanks(96, 96, { pw: 6, len: 64, seed: 11, cols: ['#3a2416', '#54341e', '#6e4628', '#8a5c34', '#a2703e'] })));
  scene.add(floor);
  const rug = mesh(new THREE.BoxGeometry(3.6, .02, 2.4).translate(.4, .01, -1.2), mat(carpet()), { cast: false }); scene.add(rug);
  const wallM = mat(plainWall(['#8a8070', '#a49884', '#bcb09a', '#d0c4ac'], 4));
  const back = mesh(new THREE.BoxGeometry(8, 4, .2).translate(0, 2, -3.9), wallM); scene.add(back);
  // sol duvar: kapı açıklığı (z -2.4 .. -1.2)
  const lw1 = mesh(new THREE.BoxGeometry(.2, 4, 1.4).translate(-3.9, 2, -3.2), wallM), lw2 = mesh(new THREE.BoxGeometry(.2, 4, 3.6).translate(-3.9, 2, 1.0), wallM), lw3 = mesh(new THREE.BoxGeometry(.2, 1.4, 1.2).translate(-3.9, 3.3, -1.9), wallM);
  scene.add(lw1, lw2, lw3);
  const skirt = solid('#3a2a1e'); for (const [w, d, x, z] of [[8, .06, 0, -3.78], [.06, 7, -3.78, -.5]]) { const s = new THREE.Mesh(new THREE.BoxGeometry(w, .14, d), skirt); s.position.set(x, .07, z); scene.add(s); }
  // pencere (arka duvar) + güneş
  const winGlass = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.8), solid('#bcd8f0', { em: '#d8ecff', ei: 1.4 })); winGlass.position.set(1.4, 2.2, -3.79); scene.add(winGlass);
  const wf = solid('#e8e0d0'); for (const [w, h, x, y] of [[2.6, .1, 1.4, 3.15], [2.6, .14, 1.4, 1.25], [.1, 1.9, .15, 2.2], [.1, 1.9, 2.65, 2.2], [.06, 1.8, 1.4, 2.2], [2.4, .06, 1.4, 2.2]]) { const f = new THREE.Mesh(new THREE.BoxGeometry(w, h, .1), wf); f.position.set(x, y, -3.74); scene.add(f); }
  const sun = new THREE.DirectionalLight('#ffe0b0', 2.0); sun.position.set(3, 6, -9); sun.target.position.set(0, 0, 0); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 1, far: 30 }); sun.shadow.bias = -.0008; scene.add(sun, sun.target);
  const hemi = new THREE.HemisphereLight('#e8dcc8', '#3a2a1e', .9); scene.add(hemi);
  const lamp = new THREE.PointLight('#ffc888', 6, 9, 1.6); lamp.position.set(.4, 3.4, -1); scene.add(lamp);
  // masa, sandalyeler, eşyalar
  const wood = mat(woodPlanks(48, 48, { pw: 48, len: 96, seed: 3, nails: false, cols: ['#2a1a10', '#40281a', '#5a3a24', '#704a2e'] }));
  const desk = new THREE.Group(); desk.add(mesh(new THREE.BoxGeometry(2.2, .1, 1.1).translate(0, .82, 0), wood));
  for (const [x, z] of [[-1, -.45], [1, -.45], [-1, .45], [1, .45]]) desk.add(mesh(new THREE.BoxGeometry(.08, .78, .08).translate(x, .39, z), wood));
  desk.add(mesh(new THREE.BoxGeometry(.08, .7, 1).translate(.6, .45, 0), wood));
  const mon = new THREE.Mesh(new THREE.BoxGeometry(.06, .45, .7), solid('#18181c')); mon.position.set(.85, 1.15, -.1); desk.add(mon);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(.62, .38), solid('#2a4a6a', { em: '#4a7aa8', ei: .8 })); scr.position.set(.81, 1.16, -.1); scr.rotation.y = -Math.PI / 2; desk.add(scr);
  const paper = new THREE.Mesh(new THREE.BoxGeometry(.3, .02, .4), solid('#f2eee4')); paper.position.set(-.2, .88, .1); paper.rotation.y = .3; desk.add(paper);
  const cup = new THREE.Mesh(new THREE.CylinderGeometry(.05, .045, .11, 10), solid('#c84a3a')); cup.position.set(-.7, .93, -.3); desk.add(cup);
  desk.position.set(.4, 0, -1.6); desk.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } }); scene.add(desk);
  const chairM = solid('#2a2a30'); for (const x of [-.95, 1.75]) { const c = new THREE.Group(); c.add(new THREE.Mesh(new THREE.BoxGeometry(.5, .08, .5), chairM).translateY(.48)); c.add(new THREE.Mesh(new THREE.BoxGeometry(.06, .7, .5), chairM).translateY(.85).translateX(x < 0 ? -.24 : .24)); c.add(new THREE.Mesh(new THREE.CylinderGeometry(.04, .04, .44, 6), chairM).translateY(.22)); c.position.set(x, 0, -1.6); c.traverse(o => o.isMesh && (o.castShadow = true)); scene.add(c); }
  // raf + bitki + çerçeve
  const shelf = mesh(new THREE.BoxGeometry(1.6, 1.9, .4).translate(-2.4, .95, -3.6), wood); scene.add(shelf);
  const bookC = ['#7a2a22', '#2a4a7a', '#3a6a3a', '#8a6a2a', '#5a2a5a']; for (let i = 0; i < 14; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(.08, .28 + h2(i, 2) * .08, .26), solid(bookC[i % 5])); b.position.set(-3.1 + (i % 7) * .2, i < 7 ? 1.12 : 1.62, -3.5); scene.add(b); }
  const pot = new THREE.Mesh(new THREE.CylinderGeometry(.22, .17, .4, 10), solid('#a86a4a')); pot.position.set(3.2, .2, -3.3); scene.add(pot);
  const plant = tree(3.2, -3.3, .45, 9); plant.position.y = .3; scene.add(plant);
  const frameP = new THREE.Mesh(new THREE.PlaneGeometry(1, .7), new THREE.MeshStandardMaterial({ map: signTex('ATLAS 1987', 90, 60, '#d8c28e') })); frameP.position.set(-.9, 2.5, -3.79); scene.add(frameP);
  // kapı kanadı (menteşe z=-2.4 tarafında) + koridor ışığı
  const doorG = new THREE.Group(), doorP = mesh(new THREE.BoxGeometry(.06, 2.6, 1.2).translate(0, 1.3, .6), wood); doorG.add(doorP); doorG.position.set(-3.86, 0, -2.4); scene.add(doorG);
  const hall = new THREE.SpotLight('#ffe8b0', 0, 16, .55, .35, 1.2); hall.position.set(-6.5, 2.4, -1.8); hall.target.position.set(1, 0, -1.4); hall.castShadow = true; hall.shadow.mapSize.set(1024, 1024); hall.shadow.bias = -.002; scene.add(hall, hall.target);
  const hallGlow = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 2.6), solid('#fff0c8', { em: '#fff0c8', ei: 0 })); hallGlow.position.set(-4.2, 1.3, -1.8); hallGlow.rotation.y = Math.PI / 2; scene.add(hallGlow);
  // karakterler: kahraman masanın solunda sağa bakar, Ali Bey sağda sola bakar
  const hero = makeChar('hero'), ali = makeChar('ali'), amca = makeChar('amca'), murat = makeChar('murat'); scene.add(hero.root, ali.root, amca.root, murat.root);
  const fill = frontFill(scene, '#ffe4c0', 1.4, 7);
  const dust = particles(60, (i, t, o) => { const R = mulberry(i + 3); o.x = R() * 3 + .2 + Math.sin(t * .3 + i) * .2; o.y = 1 + R() * 2.2 + Math.sin(t * .2 + i * 3) * .15; o.z = -3.4 + R() * 2.5; o.a = .45 * (.5 + .5 * Math.sin(t * .9 + i)); o.s = .03; o.r = 1; o.g = .92; o.b = .75; }, { soft: true }); scene.add(dust);
  return { scene, hero, update(t, shot, camera, post) {
    const id = shot.id, sep = id === 'sepia', sec = id === 'secret';
    let cp, lk = [-.6, 1.05, -1.7];
    if (id === 'office') cp = track([[14.2, [2.6, 5.2, 8.2]], [18.2, [2.0, 4.6, 7.4]], [19.4, [1.6, 4.4, 7.0]], [25, [1.9, 4.6, 7.4]]])(t), lk = track([[14.2, [.2, 1.05, -1.6]], [18.2, [-.4, 1.05, -1.7]], [19.4, [-.6, 1.1, -1.7]], [25, [-.4, 1.05, -1.6]]])(t);
    else if (sep) cp = [2.2, 4.8, 7.6], lk = [-1.0, 1.05, -1.7];
    else cp = track([[32.5, [1.0, 3.6, 6.2]], [42, [.4, 3.0, 5.0]]])(t), lk = [-1.1, 1.1, -.7];
    camera.fov = 36; camera.position.set(...cp); camera.lookAt(...lk); camera.updateProjectionMatrix();
    amca.root.visible = false;
    if (!sec) {
      hero.root.position.set(-.95, .02, -1.25); hero.frame(t < 18.6 || sep ? (Math.floor(t * 1.4) % 2 ? 'head' : 'idle0') : (t > 22 ? 'idle1' : 'idle0')); hero.face(camera);
      ali.root.visible = true; ali.root.position.set(1.75, .02, -1.65);
      ali.frame(sep ? 'idle0' : (t < 17.6 ? (Math.floor(t * 2) % 2 ? 'point' : 'idle0') : 'idle0')); ali.face(camera, true);
      const open = sep ? 1 : ss(seg(t, T.muratIn - .9, T.muratIn)); doorG.rotation.y = -open * 1.35; hall.intensity = open * 55; hallGlow.material.emissiveIntensity = open * 2.2;
      murat.root.visible = open > .2; const u = sep ? 1 : seg(t, T.muratIn, T.muratIn + 1.6);
      murat.root.position.set(lerp(-4.6, -2.3, u), .02, -1.85);
      murat.frame(sep ? (t > 27 ? 'cross' : 'idle0') : (u > 0 && u < 1 ? walk(t) : (t > 18.6 && t < 24 ? 'point' : 'idle0'))); murat.face(camera);
    } else {
      ali.root.visible = false; doorG.rotation.y = 0; hall.intensity = 0; hallGlow.material.emissiveIntensity = 0;
      murat.root.visible = true; murat.root.position.set(-.5, .02, -.75); murat.frame(t > 33 && t < 40.6 ? (Math.floor(t * 1.6) % 2 ? 'point' : 'idle0') : 'idle0'); murat.face(camera, true);
      hero.root.position.set(-1.8, .02, -.6); hero.frame(t > 38 ? 'head' : idle(t)); hero.face(camera);
    }
    fill.position.set(-.2, 1.6, .6); dust.userData.update?.(t);
    const foc = (id === 'office' && t > 18.6 && t < 24) ? murat.root.position : hero.root.position;
    post.dof.focus = camera.position.distanceTo(foc.clone().add(V3(0, .8, 0))); post.dof.aper = 240; post.dof.maxCoc = 14;
    const V = post.vig.uniforms; V.amt.value = .6; V.warm.value = .16; post.bloom.threshold = .9; post.bloom.strength = .4;
    if (sep) { V.sat.value = .05; V.warm.value = .55; V.amt.value = .85; }
  } };
}
