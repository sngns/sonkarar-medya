// 2D katman (1080×1920): üst bölüm bandı, bölüm kartı, diyalog kutusu, iç ses / anlatıcı altyazısı, oy kartı, seçim menüsü, geçişler
import { VO, T, VOTE, CHOICE, EP, TITLE, CARD, SEPIA, ITEM, FADES } from './story.js';

const cv = document.getElementById('ov'), g = cv.getContext('2d');
const W = 1080, H = 1920;
let DURS = {};
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const GOLD = '#e2c989';

export async function overlayReady() {
  await Promise.all(['500 40px Cinzel', '700 40px Cinzel', 'italic 500 40px "Cormorant Garamond"', '600 40px "Cormorant Garamond"', '500 40px "Cormorant Garamond"', '700 40px "Cormorant Garamond"'].map(f => document.fonts.load(f)));
  try { DURS = await (await fetch('voices/dur.json')).json(); } catch { DURS = {}; }
}
const dur = v => DURS[v.id] || Math.max(1.6, v.sub.length / 15);

function ornament(cx, y, w, a) {
  g.save(); g.globalAlpha = a; g.fillStyle = GOLD; g.lineWidth = 2;
  for (const s of [-1, 1]) { const gr = g.createLinearGradient(cx, 0, cx + s * w, 0); gr.addColorStop(0, 'rgba(226,201,137,1)'); gr.addColorStop(1, 'rgba(226,201,137,0)'); g.strokeStyle = gr; g.beginPath(); g.moveTo(cx + s * 18, y); g.lineTo(cx + s * w, y); g.stroke(); g.beginPath(); g.arc(cx + s * 30, y, 3, 0, 7); g.fill(); }
  g.strokeStyle = GOLD; g.beginPath(); g.moveTo(cx, y - 9); g.lineTo(cx + 9, y); g.lineTo(cx, y + 9); g.lineTo(cx - 9, y); g.closePath(); g.stroke();
  g.restore();
}
function spaced(text, x, y, sp) { const ws = [...text].map(c => g.measureText(c).width), tot = ws.reduce((a, b) => a + b, 0) + sp * (ws.length - 1); let cx = x - tot / 2; [...text].forEach((c, i) => { g.fillText(c, cx + ws[i] / 2, y); cx += ws[i] + sp; }); }
function glowText(fn, col, blur) { g.save(); g.shadowColor = col; g.shadowBlur = blur; fn(); g.restore(); fn(); }
function wrap(text, maxW) { const words = text.split(' '), lines = []; let cur = ''; for (const w of words) { const n = cur ? cur + ' ' + w : w; if (g.measureText(n).width > maxW && cur) { lines.push(cur); cur = w; } else cur = n; } if (cur) lines.push(cur); return lines; }

// RPG kutusu (diyalog ve seçim menüsünün ortak çerçevesi)
function frameBox(x, y, bw, bh) {
  const bgr = g.createLinearGradient(0, y, 0, y + bh); bgr.addColorStop(0, 'rgba(14,18,34,.88)'); bgr.addColorStop(1, 'rgba(6,8,18,.92)');
  g.fillStyle = bgr; g.fillRect(x, y, bw, bh);
  g.strokeStyle = 'rgba(214,190,130,.92)'; g.lineWidth = 3; g.strokeRect(x + 1.5, y + 1.5, bw - 3, bh - 3);
  g.strokeStyle = 'rgba(214,190,130,.35)'; g.lineWidth = 1.5; g.strokeRect(x + 10.5, y + 10.5, bw - 21, bh - 21);
  for (const [cx, cy] of [[x, y], [x + bw, y], [x, y + bh], [x + bw, y + bh]]) { g.fillStyle = GOLD; g.beginPath(); g.moveTo(cx, cy - 10); g.lineTo(cx + 10, cy); g.lineTo(cx, cy + 10); g.lineTo(cx - 10, cy); g.fill(); }
}

// —— Üst bölüm bandı (her sahnede, kart hariç) ——
function topBand(t) {
  g.save(); const sh = g.createLinearGradient(0, 0, 0, 230); sh.addColorStop(0, 'rgba(4,6,14,.7)'); sh.addColorStop(1, 'rgba(4,6,14,0)'); g.fillStyle = sh; g.fillRect(0, 0, W, 230);
  g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#d8c28e'; g.font = '500 32px Cinzel'; spaced('BÖLÜM ' + EP, W / 2, 118, 9);
  g.font = 'italic 600 46px "Cormorant Garamond"'; g.fillStyle = '#f6f0e2'; glowText(() => g.fillText(TITLE, W / 2, 168), 'rgba(0,0,0,.8)', 10);
  g.restore();
}

// —— Bölüm kartı ——
function chapterCard(t) {
  const c0 = CARD.a, c1 = CARD.b, a0 = ss(seg(t, c0 + .05, c0 + .6)), a1 = ss(seg(t, c0 + .4, c0 + 1.0)), out = 1 - ss(seg(t, c1 - .35, c1));
  const bg = g.createRadialGradient(W / 2, H / 2, 60, W / 2, H / 2, 1200); bg.addColorStop(0, '#11172a'); bg.addColorStop(1, '#020308');
  g.fillStyle = bg; g.fillRect(0, 0, W, H); g.textAlign = 'center'; g.textBaseline = 'middle';
  g.globalAlpha = a0 * out; g.fillStyle = '#d8c28e'; g.font = '500 44px Cinzel'; spaced('BÖLÜM  ' + EP, W / 2, 850, 12);
  if (CARD.pre) { g.font = 'italic 500 50px "Cormorant Garamond"'; g.fillStyle = '#b8ae98'; g.fillText(CARD.pre, W / 2, 700); }
  ornament(W / 2, 910, 260 * (.4 + .6 * a0), a0 * out);
  g.globalAlpha = a1 * out; g.fillStyle = '#f3ead6'; g.font = 'italic 500 104px "Cormorant Garamond"';
  glowText(() => g.fillText(TITLE, W / 2, 1010 - (1 - a1) * 12), 'rgba(255,190,110,.35)', 28);
  g.font = 'italic 500 54px "Cormorant Garamond"'; g.fillStyle = '#cfc6b2'; g.globalAlpha = ss(seg(t, c0 + .9, c0 + 1.3)) * out; g.fillText(CARD.sub, W / 2, 1120);
  g.globalAlpha = 1;
}

// —— Diyalog kutusu ——
function dialog(t, v, frozen) {
  const nx = VO.find(w => w.who && w.t > v.t), d = dur(v), end = Math.min(v.end ?? v.t + d + .9, nx ? nx.t - .05 : 1e9), a = ss(seg(t, v.t - .1, v.t + .25)) * (1 - ss(seg(t, end - .3, end)));
  if (a <= 0) return;
  const bw = 980, bh = 300, x = (W - bw) / 2, y = 1430 + (1 - a) * 18;
  g.save(); g.globalAlpha = a; if (frozen) g.filter = 'saturate(.2) brightness(.8)';
  frameBox(x, y, bw, bh);
  g.font = '600 44px "Cormorant Garamond"'; const nw = g.measureText(v.who).width + 64;
  g.fillStyle = 'rgba(10,12,24,.96)'; g.fillRect(x + 40, y - 34, nw, 64); g.strokeStyle = 'rgba(214,190,130,.92)'; g.lineWidth = 2; g.strokeRect(x + 41, y - 33, nw - 2, 62);
  g.fillStyle = '#e8d5a4'; g.textAlign = 'left'; g.textBaseline = 'middle'; g.fillText(v.who, x + 72, y - 2);
  g.font = '500 58px "Cormorant Garamond"'; g.fillStyle = '#f4efe4';
  const tt = frozen ? Math.min(t, T.freeze) : t, n = v.sub.length, shown = Math.floor(n * clamp((tt - v.t + .05) / (d * .92)));
  const lines = wrap(v.sub, bw - 150); let k = shown;
  lines.forEach((L, i) => { const s = L.slice(0, Math.max(0, k)); k -= L.length + 1; g.fillText(s, x + 72, y + 96 + i * 74); });
  if (shown >= n && Math.floor(t * 2.5) % 2 === 0) { g.fillStyle = GOLD; const tx = x + bw - 62, ty = y + bh - 44; g.beginPath(); g.moveTo(tx - 12, ty - 7); g.lineTo(tx + 12, ty - 7); g.lineTo(tx, ty + 8); g.fill(); }
  g.restore();
}

// —— Altyazı (anlatıcı / iç ses) ——
function subtitle(t, v) {
  const d = dur(v), a = ss(seg(t, v.t - .35, v.t)) * (1 - ss(seg(t, v.t + d + .4, v.t + d + .8)));
  if (a <= 0) return;
  g.save(); g.globalAlpha = a; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  g.font = `italic 500 ${v.inner ? 60 : 56}px "Cormorant Garamond"`;
  const text = v.inner ? `“${v.sub}”` : v.sub, lines = wrap(text, 900), y0 = 1560 - (lines.length - 1) * 36;
  const sh = g.createLinearGradient(0, y0 - 110, 0, y0 + lines.length * 72 + 30); sh.addColorStop(0, 'rgba(0,0,0,0)'); sh.addColorStop(.5, 'rgba(0,0,0,.45)'); sh.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = sh; g.fillRect(0, y0 - 110, W, lines.length * 72 + 140);
  g.shadowColor = 'rgba(0,0,0,.95)'; g.shadowBlur = 12; g.shadowOffsetY = 2; g.fillStyle = v.inner ? '#ffe9b8' : '#f6f0e2';
  lines.forEach((L, i) => g.fillText(L, W / 2, y0 + i * 72));
  if (v.inner && lines.length) { g.font = '500 30px Cinzel'; g.fillStyle = 'rgba(216,194,142,.85)'; g.shadowBlur = 6; spaced('İÇ SES', W / 2, y0 - 66, 6); }
  g.restore();
}

// —— Seçim hatırlatma kartı (oran YOK — Berkay): "Bunu seçmemi istediniz" ——
function voteCard(t) {
  const a = ss(seg(t, T.vote, T.vote + .4)) * (1 - ss(seg(t, T.voteEnd - .4, T.voteEnd)));
  if (a <= 0) return;
  const bw = 860, bh = 250, x = (W - bw) / 2, y = 330 - (1 - a) * 20;
  g.save(); g.globalAlpha = a; frameBox(x, y, bw, bh); g.textAlign = 'center'; g.textBaseline = 'middle';
  g.font = '500 32px Cinzel'; g.fillStyle = '#d8c28e'; spaced('BUNU SEÇMEMİ İSTEDİNİZ', W / 2, y + 62, 5);
  ornament(W / 2, y + 108, 220, a);
  g.font = 'italic 600 64px "Cormorant Garamond"'; g.fillStyle = '#ffe2a8'; glowText(() => g.fillText(`${VOTE.side} · ${VOTE.text}`, W / 2, y + 170), 'rgba(255,190,90,.45)', 20);
  g.restore();
}

// —— "B'yi seçseydin…" bandı ——
function sepiaTag(t) {
  const a = ss(seg(t, SEPIA.a, SEPIA.a + .3)) * (1 - ss(seg(t, SEPIA.b - .4, SEPIA.b))); if (a <= 0) return;
  g.save(); g.globalAlpha = a; g.textAlign = 'center'; g.textBaseline = 'middle'; frameBox(170, 300, 740, 110);
  g.font = 'italic 600 56px "Cormorant Garamond"'; g.fillStyle = '#9ec4ff'; g.fillText(SEPIA.text, W / 2, 356); g.restore();
}

// —— Seçim menüsü ——
function choiceMenu(t) {
  const a = ss(seg(t, T.menu, T.menu + .4)); if (a <= 0) return;
  const bw = 900, bh = 420, x = (W - bw) / 2, y = 300 + (1 - a) * 24;
  g.save(); g.globalAlpha = a; frameBox(x, y, bw, bh); g.textAlign = 'center'; g.textBaseline = 'middle';
  g.font = '700 46px Cinzel'; g.fillStyle = '#f3e2b0'; spaced('ŞİMDİ NE YAPMALIYIM?', W / 2, y + 74, 4);
  ornament(W / 2, y + 128, 300, a);
  const sel = Math.floor((t - T.menu) / 1.25) % 2;   // imleç iki vuruşta bir gidip gelir
  CHOICE.forEach((c, i) => {
    const cy = y + 210 + i * 110, on = sel === i;
    g.fillStyle = on ? 'rgba(255,255,255,.07)' : 'rgba(0,0,0,0)'; g.fillRect(x + 50, cy - 46, bw - 100, 92);
    g.fillStyle = c.col; g.fillRect(x + 150, cy - 36, 72, 72); g.strokeStyle = 'rgba(255,255,255,.6)'; g.lineWidth = 2; g.strokeRect(x + 151, cy - 35, 70, 70);
    g.font = '700 52px Cinzel'; g.fillStyle = '#fff'; g.fillText(c.k, x + 186, cy + 3);
    g.textAlign = 'left'; g.font = '700 54px Cinzel'; g.fillStyle = on ? '#fff4d6' : '#c8bea6'; g.fillText(c.t, x + 260, cy + 4); g.textAlign = 'center';
    if (on) { g.fillStyle = GOLD; const px = x + 96 + Math.sin(t * 8) * 5; g.beginPath(); g.moveTo(px - 14, cy - 18); g.lineTo(px + 14, cy); g.lineTo(px - 14, cy + 18); g.fill(); }
  });
  const c = ss(seg(t, T.cta, T.cta + .4));
  if (c > 0) { g.globalAlpha = c; g.font = '700 52px Cinzel'; g.fillStyle = '#ffd88a'; glowText(() => spaced('YORUMLARA A VEYA B YAZ!', W / 2, y + bh + 100, 2), 'rgba(0,0,0,.9)', 14); }
  g.restore();
}

// —— RPG eşya kutusu ——
function itemBox(t) {
  if (!ITEM) return; const a = ss(seg(t, ITEM.a, ITEM.a + .35)) * (1 - ss(seg(t, ITEM.b - .35, ITEM.b))); if (a <= 0) return;
  const bw = 900, bh = 150 + ITEM.lines.length * 64, x = (W - bw) / 2, y = 330 + (1 - a) * 20;
  g.save(); g.globalAlpha = a; frameBox(x, y, bw, bh); g.textAlign = 'left'; g.textBaseline = 'middle';
  g.font = '700 40px Cinzel'; g.fillStyle = '#ffd88a'; glowText(() => g.fillText('★ ' + ITEM.title, x + 56, y + 66), 'rgba(255,190,90,.5)', 16);
  g.font = '500 50px "Cormorant Garamond"'; g.fillStyle = '#f4efe4';
  ITEM.lines.forEach((L, i) => { const k = ss(seg(t, ITEM.a + .5 + i * .45, ITEM.a + .8 + i * .45)); g.globalAlpha = a * k; g.fillText('• ' + L, x + 70, y + 140 + i * 64); });
  g.restore();
}
function blackout(t) {
  let a = 0;
  for (const [c, o, i] of FADES) { if (t < c && t > c - o) a = Math.max(a, ss((t - (c - o)) / o)); if (t >= c && t < c + i) a = Math.max(a, 1 - ss((t - c) / i)); }
  a = Math.max(a, ss(seg(t, 59.4, 60))); if (a > 0) { g.fillStyle = `rgba(0,0,0,${a})`; g.fillRect(0, 0, W, H); }
}
// kapı açılışında koridor ışığı patlaması
function flash(t) { const a = Math.max(0, Math.exp(-(t - T.doorOpen - .25) / .25)) * (t > T.doorOpen + .25 ? .35 : 0); if (a > .01) { g.fillStyle = `rgba(255,236,190,${a})`; g.fillRect(0, 0, W, H); } }

export const TEXTS = () => VO.map(v => ({ id: v.id, t: v.t, d: dur(v), text: v.sub }));
export function drawOverlay(t, shot) {
  g.clearRect(0, 0, W, H);
  if (shot.id === 'card') { chapterCard(t); blackout(t); return; }
  flash(t);
  topBand(t);
  const frozen = shot.id === 'hook' && t > T.freeze;
  for (const v of VO) { if (v.who) dialog(t, v, frozen && v.id === 'h1'); else subtitle(t, v); }
  voteCard(t); sepiaTag(t); itemBox(t); choiceMenu(t);
  blackout(t);
}
