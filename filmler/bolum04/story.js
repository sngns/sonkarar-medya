// Bölüm 4 "Bulunan Cüzdan" — 1. hikâyenin sonu (B kazandı: itiraf) + 2. hikâyenin başlangıcı
export const DUR = 60;
export const EP = 4, TITLE = 'Bulunan Cüzdan';
export const SHOTS = [
  { id: 'recap', a: 0, b: 3.4 },       // ofis, "Geçen bölüm B" oy kartı
  { id: 'confess', a: 3.4, b: 16.0 },  // itiraf → amca işe alır
  { id: 'sepia', a: 16.0, b: 21.5 },   // A'yı seçseydin…
  { id: 'card', a: 21.5, b: 24.5 },    // Hikâye 1 sonu → Bölüm 4 kartı
  { id: 'stop', a: 24.5, b: 36.0 },    // ertesi sabah durak, cüzdan
  { id: 'bus', a: 36.0, b: 44.0 },     // otobüs gelir
  { id: 'hold', a: 44.0, b: 50.0 },    // cüzdan elde, kimse görmedi
  { id: 'choice', a: 50.0, b: 60.0 },  // seçim menüsü
];
export const T = { vote: 0.15, voteEnd: 3.2, stand: 4.2, aliShock: 8.0, amcaJoy: 9.4, busIn: 36.0, busStop: 39.0, pick: 29.0, menu: 52.3, cta: 56.0 };
export const CARD = { a: 21.5, b: 24.5, pre: '— Hikâye 1 sona erdi —', sub: 'Ertesi sabah…' };
export const SEPIA = { a: 16.0, b: 21.5, text: 'A’yı seçseydin…' };
export const ITEM = { a: 30.4, b: 35.6, title: 'EŞYA BULUNDU: Cüzdan', lines: ['5.000 TL nakit', 'Kimlik: MURAT DEMİR', 'Adres: Lale Sk. No 7'] };
export const FADES = [[3.4, .2, .25], [16.0, .25, .3], [21.5, .3, .35], [24.5, .3, .45], [50.0, .25, .4]];
export const VO = [
  { id: 'p1', t: 3.8, who: 'Kerem', sub: 'Özür dilerim… Benim adım Emre değil. Ben Kerem.' },
  { id: 'a1', t: 7.9, who: 'Ali Bey · İK', sub: 'Ne?!' },
  { id: 'h1', t: 9.3, who: 'Hüseyin Amca', sub: 'Beni yerden kaldıran adamın adı lazım bana, Emre’nin değil. Yarın başlıyorsun Kerem!' },
  { id: 'h2', t: 16.5, who: 'Hüseyin Amca', sub: 'Emre Kaya mı? Emre benim yeğenim evladım… Dün İzmir’e taşındı.' },
  { id: 'n1', t: 25.2, sub: 'İşteki ilk günüm. Bu sefer erken çıktım.' },
  { id: 'p2', t: 31.0, sub: 'Beş bin lira… ve bir kimlik. Murat Demir.', inner: true },
  { id: 'p3', t: 37.2, sub: 'Otobüs geldi. Adres iki sokak ötede… ama ilk günümde geç kalamam!', inner: true },
  { id: 'p4', t: 45.0, sub: 'Kimse görmedi…', inner: true },
  { id: 'n3', t: 56.4, sub: 'Sence ne yapmalıyım? Yorumlara A ya da B yaz!' },
];
export const VOTE = { pct: 100, side: 'B', text: 'Her şeyi itiraf et' };
export const CHOICE = [{ k: 'A', t: 'PARAYI AL', col: '#e0483c' }, { k: 'B', t: 'SAHİBİNE GÖTÜR', col: '#3c7ae0' }];
export const shotAt = t => SHOTS.find(s => t >= s.a && t < s.b) || SHOTS[SHOTS.length - 1];
