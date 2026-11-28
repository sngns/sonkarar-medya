// Son Karar Senin — piksel karakterler (3/4 yandan, sağa bakar). Her poz bir parametre nesnesi; atlas'a paketlenir.
import * as THREE from 'three';
import { PX, ramp, hex, texOf, billboard, blob } from './px.js';

export const SPX = 1 / 30;
const FW = 34, FH = 50;
const INK = hex('#1a1016');
const R = cols => ramp(cols, .22);
const SKIN = R(['#b87a62', '#dea282', '#f3c9a6', '#ffe2c8']);
const SKIN_T = R(['#8a5a40', '#b47a58', '#d69a74', '#efbb92']);   // esmer ten

// Karakter görünümleri
export const LOOKS = {
  // Kahraman: turuncu-kırmızı mont (hiçbir sette olmayan doygun renk), kot, koyu saç
  hero: { coat: R(['#3a0e0a', '#6e1e12', '#a8331c', '#d8542a', '#f07a3a']), shirt: R(['#8a8f98', '#c2c7cf', '#eef0f3']), pants: R(['#141c2e', '#22304e', '#34487a', '#4a64a0']), shoe: R(['#1a1410', '#3a2e26', '#5a4a3e']),
    skin: SKIN, hair: R(['#140c08', '#2a1a10', '#40281a', '#5a3a24']), hairStyle: 'short', long: false },
  // Ali Bey (İK): koyu takım, kel, açık ten, kravat lacivert
  ali: { coat: R(['#0e1016', '#1a1e28', '#2a303e', '#3c4456', '#525c72']), shirt: R(['#b8c2d2', '#dfe6f0', '#f6f8fb']), tie: R(['#0e1a3a', '#1e3470', '#3a58a8']), pants: R(['#0e1016', '#1a1e28', '#2a303e']), shoe: R(['#0c0a08', '#221c16', '#3a3028']),
    skin: SKIN, hair: null, hairStyle: 'bald', long: true },
  // Hüseyin amca: kahverengi takım, fötr şapka, beyaz bıyık, gri saç
  amca: { coat: R(['#20140c', '#3c2616', '#5c3c24', '#7e5634', '#9c7048']), shirt: R(['#a89c84', '#d2c6ac', '#efe6d0']), tie: R(['#3a0c0c', '#6a1a16', '#9a2c22']), pants: R(['#20140c', '#3c2616', '#5c3c24']), shoe: R(['#140c08', '#2a1a10', '#40281a']),
    skin: SKIN, hair: R(['#6d6a70', '#9c99a0', '#c8c6cc', '#eceaf0']), hairStyle: 'side', hat: R(['#141210', '#2a2620', '#403a30', '#5a5244']), mustache: true, long: true },
  // Murat Bey (yeni genel müdür): lacivert takım, kırmızı kravat, siyah saç ve bıyık, gözlük
  murat: { coat: R(['#0a0e1c', '#141c34', '#20304e', '#2e4470', '#405a8c']), shirt: R(['#b8c2d2', '#dfe6f0', '#f6f8fb']), tie: R(['#4a0a0a', '#7a1414', '#b02a22']), pants: R(['#0a0e1c', '#141c34', '#20304e']), shoe: R(['#0c0a08', '#221c16', '#3a3028']),
    skin: SKIN, hair: R(['#08060a', '#16121a', '#262030', '#3a3242']), hairStyle: 'short', mustache: true, glasses: true, long: true },
  // Güvenlik: lacivert üniforma, şapka, esmer
  guard: { coat: R(['#0a1020', '#142040', '#1e3060', '#2c4480', '#3e5aa0']), shirt: R(['#5a78a8', '#8aa8d0', '#c0d4ec']), tie: R(['#0a0a10', '#1a1a24', '#2a2a38']), pants: R(['#0a1020', '#142040', '#1e3060']), shoe: R(['#0c0a08', '#221c16', '#3a3028']),
    skin: SKIN_T, hair: R(['#100a06', '#20140c', '#302014']), hairStyle: 'short', cap: R(['#0a1020', '#142040', '#22346a']), badge: true, long: false },
};

// p: { step 0..3 | -1, bob, arm:'low'|'fwd'|'up'|'paper'|'cross'|'head'|'point'|'help', sit, lie, kneel, blink, look(-1..1 baş), sweat }
function drawPerson(P, E, L, p) {
  const by = (p.bob || 0) + (p.sit ? 9 : 0) + (p.kneel ? 7 : 0);
  if (p.lie) return drawLying(P, L, p);
  const hx = 16, hy = 11 + by;
  const top = 18 + by, bot = L.long ? 38 + (p.sit ? 6 : 0) : 35 + (p.sit ? 6 : 0);
  // —— Bacaklar ——
  if (p.sit) {   // oturan: uyluk öne yatay, baldır aşağı
    for (let x = 14; x < 26; x++) for (let y = top + 15; y < top + 19; y++) P.set(x, y, L.pants(.65 - (y - top - 15) * .15 - (x > 23 ? .1 : 0), x, y));
    for (let y = top + 19; y < 48; y++) for (let x = 22; x < 26; x++) P.set(x, y, L.pants(.45 - (x === 22 ? .15 : 0), x, y));
    P.rect(22, 47, 6, 2, L.shoe(.4, 0, 0)); P.rect(23, 47, 5, 1, L.shoe(.75, 0, 0));
  } else if (p.kneel) {
    for (let x = 12; x < 24; x++) for (let y = 42; y < 46; y++) P.set(x, y, L.pants(.55 - (y - 42) * .12, x, y));
    for (let y = 38; y < 46; y++) for (let x = 21; x < 25; x++) P.set(x, y, L.pants(.7 - (x === 21 ? .2 : 0), x, y));
    P.rect(9, 45, 5, 2, L.shoe(.5, 0, 0));
  } else {
    const st = p.step ?? -1;
    const legs = st < 0 ? [[12, 0], [18, 0]] : [[[10, 0], [20, -1]], [[13, -1], [17, 0]], [[20, -1], [10, 0]], [[17, 0], [13, -1]]][st];
    legs.forEach(([lx, ly], i) => {
      for (let y = bot - 2; y < 47 + ly; y++) for (let x = lx; x < lx + 4; x++) P.set(x, y, L.pants((i ? .55 : .8) - (x === lx ? .25 : 0) - (y > 44 ? .1 : 0), x, y));
      P.rect(lx, 47 + ly, 5, 2, L.shoe(.35, 0, 0)); P.rect(lx + 1, 47 + ly, 4, 1, L.shoe(.7, 0, 0));
    });
  }
  // —— Gövde (ceket) ——
  const shL = 10, shR = 22;
  P.poly([[shL, top], [shR, top], [shR + 1, bot], [shL - 1, bot]], (x, y) => {
    const u = (y - top) / (bot - top), s = (x - shL) / (shR - shL);
    let v = .7 - s * .45 + (1 - u) * .1; if (s > .6 && s < .66) v -= .25; return L.coat(v, x, y);
  });
  // gömlek yakası + kravat
  P.poly([[17, top], [21, top], [20, top + 7], [18, top + 7]], (x, y) => L.shirt(.8 - (x - 17) * .1, x, y));
  if (L.tie) { P.rect(19, top + 1, 1, 9, L.tie(.6, 0, 0)); P.set(18, top + 1, L.tie(.4, 0, 0)); }
  if (L.badge) { P.rect(12, top + 4, 2, 2, hex('#e2c262')); P.set(12, top + 4, hex('#fff0b0')); }
  if (L === LOOKS.hero) { P.rect(17, top + 2, 4, 1, L.shirt(.5, 0, 0)); P.rect(19, top + 3, 1, bot - top - 4, L.coat(.25, 0, 0)); }   // fermuar
  P.rect(shL - 1, bot - 1, shR - shL + 3, 1, L.coat(.15, 0, 0));
  // —— Baş ——
  const look = p.look || 0;
  P.ellipse(hx + 1, hy, 5.5, 6, (x, y, dx, dy) => L.skin(.62 - dx * .12 - dy * .28 + (dx > .6 ? -.18 : 0), x, y));
  // boyun
  P.rect(hx - 1, hy + 5, 4, 2, L.skin(.35, 0, 0));
  // saç / şapka
  if (L.hairStyle === 'short') { P.ellipse(hx - .5, hy - 3.5, 6, 3.5, (x, y, dx, dy) => L.hair(.6 - dy * .3 + ((x * 3 + y) % 4 === 0 ? -.15 : 0), x, y)); for (let y = hy - 3; y < hy + 3; y++) P.set(hx - 5, y, L.hair(.4, 0, y)); P.rect(hx - 4, hy - 1, 3, 3, L.hair(.45, 0, 0)); }
  if (L.hairStyle === 'bald') { P.set(hx - 1, hy - 4, L.skin(.95, 0, 0)); P.set(hx, hy - 4, L.skin(.9, 0, 0)); P.rect(hx - 5, hy - 1, 2, 3, hex('#4a3a34')); }
  if (L.hairStyle === 'side') { P.ellipse(hx - 3, hy + 1, 3, 4, (x, y, dx, dy) => L.hair(.7 - dy * .2, x, y)); }
  if (L.hat) { P.ellipse(hx + .5, hy - 4.2, 6, 3, (x, y, dx, dy) => L.hat(.65 - dy * .35, x, y)); P.rect(hx - 6, hy - 2, 14, 1, L.hat(.3, 0, 0)); P.rect(hx - 4, hy - 3, 10, 1, hex('#5a1e18')); }
  if (L.cap) { P.ellipse(hx, hy - 4, 6, 2.8, (x, y, dx, dy) => L.cap(.65 - dy * .3, x, y)); P.rect(hx + 2, hy - 2, 7, 1, L.cap(.2, 0, 0)); P.set(hx, hy - 5, hex('#e2c262')); }
  // kaşlar, gözler, burun, bıyık
  const ey = hy - 1 - look;
  P.rect(hx + 2, ey - 2, 3, 1, L.hair ? L.hair(.2, 0, 0) : hex('#5a4038'));
  if (p.blink) P.set(hx + 4, ey, L.skin(.2, 0, 0)); else { P.set(hx + 4, ey, INK); P.set(hx + 4, ey - 1, INK); }
  P.set(hx + 1, ey, INK);
  P.rect(hx + 5, ey + 1, 2, 2, L.skin(.82, 0, 0)); P.set(hx + 6, ey + 2, L.skin(.45, 0, 0));
  if (L.mustache) { P.rect(hx + 2, ey + 3, 5, 1, L.hair(.95, 0, 0)); P.set(hx + 1, ey + 4, L.hair(.8, 0, 0)); P.set(hx + 6, ey + 4, L.hair(.8, 0, 0)); }
  else P.rect(hx + 3, ey + 4, 2, 1, hex('#9a5a48'));
  if (L.glasses) { P.rect(hx + 2, ey - 1, 4, 1, hex('#1a1a20')); P.rect(hx + 3, ey, 2, 1, hex('#bcd4ea')); P.set(hx + 1, ey - 1, hex('#1a1a20')); }
  if (p.sweat) { P.set(hx - 2, hy - 2, hex('#cfe8ff')); P.set(hx - 2, hy - 1, hex('#9cc8f0')); E && E.set(hx - 2, hy - 2, hex('#6a8aa8')); }
  // —— Kollar ——
  const arm = p.arm || 'low';
  const sl = pts => pts.forEach(([x, y]) => { P.set(x, y, L.coat(.78, x, y)); P.set(x, y + 1, L.coat(.48, x, y)); P.set(x - 1, y + 1, L.coat(.35, x, y)); });
  const hand = (x, y, w = 2, h = 2) => P.rect(x, y, w, h, L.skin(.6, 0, 0));
  if (arm === 'low') { sl([[21, top + 2], [22, top + 4], [22, top + 6], [22, top + 8], [22, top + 10]]); hand(21, top + 12); }
  if (arm === 'fwd' || arm === 'point') { sl([[21, top + 2], [23, top + 3], [25, top + 4], [26, top + 5]]); hand(27, top + 5, arm === 'point' ? 3 : 2, 2); if (arm === 'point') P.rect(29, top + 5, 2, 1, L.skin(.7, 0, 0)); }
  if (arm === 'up') { sl([[21, top + 1], [22, top - 1], [23, top - 3], [24, top - 5], [24, top - 7]]); hand(23, top - 10, 3, 3); }
  if (arm === 'paper') { sl([[21, top + 3], [23, top + 5], [24, top + 7]]); hand(25, top + 7); P.rect(25, top + 1, 6, 8, hex('#f4f0e6')); P.rect(26, top + 3, 4, 1, hex('#8a8a90')); P.rect(26, top + 5, 3, 1, hex('#8a8a90')); }
  if (arm === 'cross') { for (let x = 12; x < 23; x++) { P.set(x, top + 8, L.coat(.85, x, 0)); P.set(x, top + 9, L.coat(.55, x, 0)); } hand(21, top + 7); hand(12, top + 8); }
  if (arm === 'head') { sl([[21, top + 1], [22, top - 1], [21, top - 3]]); hand(19, hy - 2, 3, 3); }
  if (arm === 'help') { sl([[21, top + 3], [23, top + 5], [25, top + 7], [26, top + 9]]); hand(27, top + 10, 3, 2); }
  if (arm === 'desk') { sl([[21, top + 3], [23, top + 5], [25, top + 6]]); hand(26, top + 6, 3, 2); }
  if (!['cross'].includes(arm)) P.set(9, top + 9, L.skin(.35, 0, 0));
}

// Yerde yatan / oturan amca (sağa bakar), yatay bir figür
function drawLying(P, L, p) {
  const HR = L.hair || (() => hex("#5a4038"));
  const y0 = 38;
  // bacaklar (uzanmış)
  for (let x = 16; x < 31; x++) for (let y = y0 + 4; y < y0 + 8; y++) P.set(x, y, L.pants(.6 - (y - y0 - 4) * .12, x, y));
  P.rect(30, y0 + 3, 3, 5, L.shoe(.45, 0, 0));
  // gövde (geriye yaslanmış, eğik)
  P.poly([[8, y0 - 8], [15, y0 - 10], [18, y0 + 8], [8, y0 + 8]], (x, y) => L.coat(.65 - (x - 8) * .03, x, y));
  // destek kolu
  P.rect(6, y0 + 2, 3, 6, L.coat(.4, 0, 0)); P.rect(5, y0 + 7, 3, 2, L.skin(.5, 0, 0));
  // uzanan kol (yukarı, yardım ister)
  const k = p.reach ?? 1;
  for (let i = 0; i < 7; i++) { const x = 16 + i, y = Math.round(y0 - 8 - i * k * .9); P.set(x, y, L.coat(.8, x, y)); P.set(x, y + 1, L.coat(.5, x, y)); }
  P.rect(23, Math.round(y0 - 8 - 7 * k * .9) - 1, 2, 2, L.skin(.6, 0, 0));
  // baş
  const hx = 12, hy = y0 - 15;
  P.ellipse(hx, hy, 5, 5.5, (x, y, dx, dy) => L.skin(.6 - dx * .12 - dy * .25, x, y));
  if (L.hat) { P.ellipse(hx - .5, hy - 4, 5.5, 2.8, (x, y, dx, dy) => L.hat(.65 - dy * .35, x, y)); P.rect(hx - 6, hy - 2, 12, 1, L.hat(.3, 0, 0)); }
  P.set(hx + 3, hy - 1, INK); P.set(hx, hy - 1, INK); P.rect(hx + 1, hy + 2, 4, 1, HR(.95, 0, 0));
  P.rect(hx + 1, hy + 4, 2, 1, hex('#7a2e2e'));
  // baston
  for (let i = 0; i < 14; i++) P.set(20 + i, y0 + 9 - Math.round(i * .2), hex('#5a3b24'));
}

const BASE = {
  idle0: {}, idle1: { bob: 1 }, blink: { blink: 1 },
  w0: { step: 0 }, w1: { step: 1, bob: -1 }, w2: { step: 2 }, w3: { step: 3, bob: -1 },
  fwd: { arm: 'fwd' }, point: { arm: 'point' }, up: { arm: 'up' }, up1: { arm: 'up', bob: 1 }, cross: { arm: 'cross' }, head: { arm: 'head', sweat: 1 },
  sit0: { sit: 1, arm: 'desk' }, sit1: { sit: 1, arm: 'desk', bob: 1 }, sitBlink: { sit: 1, arm: 'desk', blink: 1 },
  sitSweat: { sit: 1, arm: 'desk', sweat: 1 }, sitSweat1: { sit: 1, arm: 'desk', sweat: 1, bob: 1 }, sitHead: { sit: 1, arm: 'head', sweat: 1 },
  sitPaper: { sit: 1, arm: 'paper' }, sitPaper1: { sit: 1, arm: 'paper', bob: 1 }, sitLook: { sit: 1, arm: 'desk', look: 1 },
  help: { kneel: 1, arm: 'help' }, lie: { lie: 1, reach: 1 }, lie1: { lie: 1, reach: .7 },
};

function atlas(table, L) {
  const names = Object.keys(table), n = names.length;
  const P = new PX(FW * n, FH), E = new PX(FW * n, FH);
  names.forEach((k, i) => {
    const p1 = new PX(FW, FH), e1 = new PX(FW, FH);
    drawPerson(p1, e1, L, table[k]); p1.outline(.3);
    for (let y = 0; y < FH; y++) for (let x = 0; x < FW; x++) { const c = p1.get(x, y); if (c) P.set(i * FW + x, y, c); const e = e1.get(x, y); if (e) E.set(i * FW + x, y, e); }
  });
  const tex = texOf(P.done()), em = texOf(E.done());
  for (const t of [tex, em]) t.repeat.set(1 / n, 1);
  return { tex, em, names, n, canvas: P.c };
}

export function makeChar(kind) {
  const A = atlas(BASE, LOOKS[kind]);
  const mesh = billboard(A.tex, FW * SPX, FH * SPX, { em: A.em, emCol: '#ffffff', emI: 1.2 });
  const root = new THREE.Group(); root.add(mesh); root.userData.char = kind;
  const sh = blob(.42, .55); sh.position.y = .015; root.add(sh);
  return {
    root, mesh, atlas: A,
    frame(name) { const i = A.names.indexOf(name); if (i < 0) throw new Error('frame ' + name); A.tex.offset.x = A.em.offset.x = i / A.n; },
    face(cam, flip = false) { root.rotation.y = Math.atan2(cam.position.x - root.position.x, cam.position.z - root.position.z); mesh.scale.x = flip ? -1 : 1; },
  };
}
export { atlas, BASE, drawPerson, FW, FH };
