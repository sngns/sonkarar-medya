// Bölüm 3 "Sahte İsim" — zaman çizelgesi (tek doğruluk kaynağı)
export const DUR = 60;
export const SHOTS = [
  { id: 'hook', a: 0, b: 4.0 },        // ofis, amca kapıda soruyor, kare donar
  { id: 'card', a: 4.0, b: 6.0 },      // bölüm kartı + "45 dakika önce…"
  { id: 'city', a: 6.0, b: 17.0 },     // sabah şehir dioraması (özet) + %67 A
  { id: 'gate', a: 17.0, b: 24.0 },    // Atlas Holding girişi
  { id: 'sepia', a: 24.0, b: 28.5 },   // B'yi seçseydin…
  { id: 'office', a: 28.5, b: 38.0 },  // görüşme
  { id: 'door', a: 38.0, b: 50.0 },    // kapı açılır, amca girer, kurucu
  { id: 'choice', a: 50.0, b: 60.0 },  // açılış karesi + seçim menüsü
];
export const T = {
  freeze: 3.2, vote: 14.0, guardStep: 19.0, heroIn: 21.0, sepiaClose: 26.2,
  doorOpen: 38.0, amcaIn: 39.2, aliStand: 45.0, menu: 52.5, cta: 56.0,
};
// id = ses dosyası; who: konuşma kutusu ismi (yoksa altyazı); inner: iç ses (italik, tırnaklı)
export const VO = [
  { id: 'h1', t: 0.4, who: 'Hüseyin Amca', sub: 'Adın neydi senin evladım?', end: 3.2 },
  { id: 'n1', t: 6.4, sub: 'Sabah otobüs durağında düşen bir amcaya yardım ettim, otobüsü kaçırdım.' },
  { id: 'n2', t: 10.6, sub: 'Şirkette güvenlik, gelmeyen birinin adıyla girmemi önerdi.' },
  { id: 'p1', t: 18.2, sub: 'Tamam… bugünlük adım Emre Kaya.', inner: true },
  { id: 'g1', t: 24.5, who: 'Güvenlik', sub: 'Dürüstlüğün için sağ ol… ama kurallar kurallar.' },
  { id: 'a1', t: 29.0, who: 'Ali Bey · İK', sub: 'Emre Kaya… Özgeçmişinizde beş yıl yazılım tecrübesi yazıyor.' },
  { id: 'p2', t: 34.0, sub: 'Beş yıl mı? Ben daha staj bile yapmadım…', inner: true },
  { id: 'h2', t: 40.6, who: 'Hüseyin Amca', sub: 'Evladım! Sabah bana yardım eden delikanlı sensin!' },
  { id: 'a2', t: 44.8, who: 'Ali Bey · İK', sub: 'Hüseyin Bey! Buyurun efendim… Kendisi Emre Kaya.' },
  { id: 'p3', t: 48.6, sub: 'Şirketin kurucusu… sabahki amca mıymış?!', inner: true },
  { id: 'p4', t: 52.7, sub: 'Ya yalana devam edeceğim… ya da her şeyi itiraf.', inner: true },
  { id: 'n3', t: 56.5, sub: 'Sence ne yapmalıyım? Yorumlara A ya da B yaz!' },
];
export const VOTE = { pct: 67, side: 'A', text: 'Onun adıyla gir' };
export const CHOICE = [{ k: 'A', t: 'YALANA DEVAM', col: '#e0483c' }, { k: 'B', t: 'İTİRAF ET', col: '#3c7ae0' }];
export const shotAt = t => SHOTS.find(s => t >= s.a && t < s.b) || SHOTS[SHOTS.length - 1];
