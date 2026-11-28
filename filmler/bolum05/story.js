// Bölüm 5 "Yeni Müdür" — 2. hikâye, 2. bölüm (B kazandı: cüzdan sahibine götürüldü)
export const DUR = 60;
export const EP = 5, TITLE = 'Yeni Müdür';
export const SHOTS = [
  { id: 'recap', a: 0, b: 5.0 },       // durak, oy kartı
  { id: 'street', a: 5.0, b: 14.2 },   // Lale Sk.: cüzdan teslim
  { id: 'office', a: 14.2, b: 25.0 },  // geç kaldı → yeni müdür Murat Bey
  { id: 'sepia', a: 25.0, b: 30.0 },   // A'yı seçseydin…
  { id: 'card', a: 30.0, b: 32.5 },    // "Öğle arası…"
  { id: 'secret', a: 32.5, b: 42.0 },  // Murat Bey sırrı verir
  { id: 'gate', a: 42.0, b: 50.0 },    // Cem (güvenlik) sorar
  { id: 'choice', a: 50.0, b: 60.0 },  // seçim menüsü
];
export const T = { vote: 0.15, voteEnd: 4.8, muratOut: 7.4, muratIn: 18.3, menu: 52.3, cta: 56.0 };
export const CARD = { a: 30.0, b: 32.5, pre: '', sub: 'Öğle arası…' };
export const SEPIA = { a: 25.0, b: 30.0, text: 'A’yı seçseydin…' };
export const ITEM = null;
export const FADES = [[5.0, .2, .25], [14.2, .25, .3], [25.0, .25, .3], [30.0, .3, .35], [32.5, .3, .4], [42.0, .25, .3], [50.0, .25, .4]];
export const VO = [
  { id: 'n0', t: 0.2, sub: 'Cüzdanı sahibine götürdüm… ama sahibi kim çıktı, tahmin bile edemezsiniz!' },
  { id: 'k1', t: 5.3, who: 'Kerem', sub: 'Murat Demir siz misiniz? Cüzdanınız durakta düşmüştü.' },
  { id: 'm1', t: 8.8, who: 'Murat Bey', sub: 'Aman! Her şey yerinde… Sağ ol delikanlı!' },
  { id: 'n1', t: 12.4, sub: 'Teşekkürü bile dinlemeden koştum.' },
  { id: 'a1', t: 14.5, who: 'Ali Bey · İK', sub: 'Kerem! İlk günden yarım saat geç mi?!' },
  { id: 'm2', t: 18.6, who: 'Murat Bey', sub: 'Bırakın Ali Bey. Ben yeni genel müdürünüzüm… ve bu çocuk sabah cüzdanımı getirdi.' },
  { id: 'm3', t: 25.4, who: 'Murat Bey', sub: 'Bu sabah cüzdanım çalındı. İçinde beş bin lira vardı…' },
  { id: 'm4', t: 32.9, who: 'Murat Bey', sub: 'Sana bir sır vereyim: Hüseyin Bey emekli oluyor. Şirketi oğluna değil, bana bırakıyor. Kimseye söyleme.' },
  { id: 'c1', t: 42.5, who: 'Cem · Güvenlik', sub: 'Kerem, seni içeri ben soktum, unutma. Babam şirketi kime bırakıyor, duydun mu?' },
  { id: 'p1', t: 48.9, sub: 'Bana iyiliği dokunan adam… ama müdüre söz verdim.', inner: true },
  { id: 'n3', t: 56.4, sub: 'Sence ne yapmalıyım? Yorumlara A ya da B yaz!' },
];
export const VOTE = { side: 'B', text: 'Cüzdanı sahibine götür' };
export const CHOICE = [{ k: 'A', t: 'GERÇEĞİ SÖYLE', col: '#e0483c' }, { k: 'B', t: 'SIRRI SAKLA', col: '#3c7ae0' }];
export const shotAt = t => SHOTS.find(s => t >= s.a && t < s.b) || SHOTS[SHOTS.length - 1];
