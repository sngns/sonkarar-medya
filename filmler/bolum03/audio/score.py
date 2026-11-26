# Bölüm 3 — sentetik müzik + efektler (telifsiz, numpy). 96 bpm, Re minör.
# Çıktı: music.wav ve sfx.wav (48 kHz stereo, 60 sn)
import numpy as np, soundfile as sf, os
from scipy.signal import butter, sosfilt
SR = 48000; DUR = 60.0; N = int(SR * DUR); B = 60 / 96
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(3)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b, o=2): return sosfilt(butter(o, [a, b], 'band', fs=SR, output='sos'), x)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR))
def adsr(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, min(n, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
class Track:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, x, t, g=1.0, pan=0.0):
        i = int(t * SR); x = x[:max(0, N - i)]
        if i < 0 or len(x) == 0: return
        s.L[i:i + len(x)] += x * g * np.sqrt((1 - pan) / 2) * 1.414
        s.R[i:i + len(x)] += x * g * np.sqrt((1 + pan) / 2) * 1.414
    def st(s): return np.stack([s.L, s.R], 1)

# —— Enstrümanlar ——
def celesta(m, d=1.6):
    t = tt(d); f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * dk) for k, a, dk in [(1, 1, 2.2), (2.01, .35, 5), (3.98, .18, 9), (5.4, .08, 14)])
    return x * adsr(len(t), .003, .3) * .5
def harp(m, d=2.2):
    t = tt(d); f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * k * t + k) * np.exp(-t * (1.2 + k * .9)) for k, a in [(1, 1), (2, .45), (3, .22), (4, .1), (5, .05)])
    return x * adsr(len(t), .004, .25) * .45
def pad(ms, d, cut=1800, g=.12, att=.8):
    t = tt(d); x = np.zeros(len(t))
    for m in ms:
        for det in (-.12, 0, .12):
            ph = 2 * np.pi * hz(m + det) * t; x += (2 * ((ph / (2 * np.pi)) % 1) - 1) * .33
    return lp(x, cut, 2) * adsr(len(t), att, min(1.2, d * .4)) * g
def strings(ms, d, g=.14):
    t = tt(d); x = np.zeros(len(t))
    for m in ms:
        vib = 1 + .004 * np.sin(2 * np.pi * 5.2 * t)
        for det in (-.08, .08):
            ph = np.cumsum(2 * np.pi * hz(m + det) * vib / SR); x += (2 * ((ph / (2 * np.pi)) % 1) - 1) * .3
    return lp(hp(x, 120), 2600, 2) * adsr(len(t), 1.0, min(1.5, d * .4)) * g
def choir(ms, d, g=.12):
    t = tt(d); x = np.zeros(len(t))
    for m in ms:
        ph = np.cumsum(2 * np.pi * hz(m) * (1 + .006 * np.sin(2 * np.pi * 4.6 * t)) / SR); s = (2 * ((ph / (2 * np.pi)) % 1) - 1)
        x += bp(s, 500, 1100) * .7 + bp(s, 250, 600) * .5
    return x * adsr(len(t), 1.2, 1.2) * g
def horn(m, d, g=.18):
    t = tt(d); ph = np.cumsum(2 * np.pi * hz(m) * (1 + .003 * np.sin(2 * np.pi * 5 * t)) / SR); s = 2 * ((ph / (2 * np.pi)) % 1) - 1
    return lp(s, 900, 2) * adsr(len(t), .25, .8) * g
def timpani(m=38, d=2.5):
    t = tt(d); f = hz(m) * (1 + .15 * np.exp(-t * 12))
    x = np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-t * 1.6) + lp(noise(d), 300) * np.exp(-t * 30) * .4
    return x * .8
def framedrum(d=.4):
    t = tt(d); return (np.sin(2 * np.pi * 95 * t) * np.exp(-t * 14) + bp(noise(d), 200, 1200) * np.exp(-t * 35) * .4) * .5
def tick(hi=True):
    t = tt(.06); return bp(noise(.06), 2500 if hi else 1800, 6000) * np.exp(-t * 120) * .35
def bell(m, d=3):
    t = tt(d); f = hz(m)
    return sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * dk) for k, a, dk in [(1, 1, 1.0), (2.76, .5, 2), (5.4, .25, 4), (8.9, .1, 7)]) * .35

M = Track()
# Kanca 0–3.2: celesta motifi + pad, 3.2'de kesme
motif = [74, 77, 81, 79, 77, 76, 74]
for i, m in enumerate(motif): M.add(celesta(m), .25 + i * B * .5, .55, pan=.2 * ((i % 2) * 2 - 1))
p = pad([50, 57, 62, 65], 3.2, 1400, .1, .6); p[-int(.03 * SR):] *= np.linspace(1, 0, int(.03 * SR)); M.add(p, 0)
# 4.0 kart: timpani + Si♭ akoru şişer
M.add(timpani(34), 4.0, .7); M.add(pad([46, 53, 58, 62], 2.2, 1600, .11, .3), 4.0)
# 6–17 geri sarım: harp ostinatosu Dm Bb F C, 8'likler
prog = [[50, 57, 62, 65, 69], [46, 53, 58, 62, 65], [41, 48, 53, 57, 60], [48, 55, 60, 64, 67]]
t0 = 6.0; bar = 4 * B
for k in range(int((17 - t0) / bar) + 1):
    ch = prog[k % 4]; base = t0 + k * bar
    if base >= 17: break
    M.add(pad(ch[:4], bar + .3, 1500, .07, .4), base)
    pat = [0, 2, 3, 4, 3, 2, 1, 2]
    for j, q in enumerate(pat):
        ts = base + j * B / 2
        if ts < 17: M.add(harp(ch[q] + 12), ts, .5, pan=-.3 + .6 * (j / 7))
M.add(bell(86), 14.0, .5)
# 17–24 giriş: el davulu + harp devam
t0 = 17.0
for k in range(3):
    ch = prog[(k + 1) % 4]; base = t0 + k * bar
    M.add(pad(ch[:4], bar + .3, 1700, .08, .3), base)
    for j in range(8):
        ts = base + j * B / 2
        if ts < 24: M.add(harp(ch[[0, 2, 3, 4, 3, 2, 1, 2][j]] + 12), ts, .45, pan=.3 - .6 * (j / 7))
    for j in range(4):
        ts = base + j * B
        if ts < 24: M.add(framedrum(), ts, .5 if j % 2 == 0 else .3)
# 24–28.5 sepya: yalnız harp, seyrek, kısık
for j, m in enumerate([62, 65, 69, 67, 65, 62, 60]): M.add(harp(m, 3), 24.2 + j * B * 1.0, .35)
# 28.5–38 ofis: yaylı pad + saat
for base, ch in [(28.5, [50, 57, 62, 65]), (31.0, [43, 55, 58, 62]), (33.5, [45, 52, 57, 61]), (36.0, [50, 57, 62, 65])]:
    M.add(strings(ch, 2.8 if base < 36 else 1.6), base)
for i, ts in enumerate(np.arange(28.5, 37.6, B)): M.add(tick(i % 2 == 0), ts, .6)
# 38–50 dönüm: 41 koro + boynuz, 45 timpani
M.add(choir([46, 53, 58, 62], 4.2), 41.0); M.add(choir([45, 52, 57, 61], 5.2), 45.0)
M.add(horn(58, 1.8), 41.2); M.add(horn(57, 2.4), 43.0); M.add(horn(62, 3.0), 45.2)
M.add(timpani(38), 45.0, .75); M.add(timpani(33), 48.8, .5)
M.add(strings([38, 50], 12, .08), 38.3)
# 50–60 seçim: celesta motifi yinelenir, pad, menü imleç tıkları
M.add(pad([50, 57, 62, 65], 10, 1400, .09, 1.0), 50.0)
for r in range(2):
    for i, m in enumerate(motif): M.add(celesta(m), 50.4 + r * 4.6 + i * B * .5, .5, pan=.2 * ((i % 2) * 2 - 1))
M.add(bell(81), 56.0, .4)
music = M.st()
fade = np.ones(N); fade[int(58.8 * SR):] = np.linspace(1, 0, N - int(58.8 * SR)); music *= fade[:, None]
music /= np.abs(music).max() + 1e-9; music *= .8

# —— Efektler ——
S = Track()
def amb_city(d): x = lp(noise(d), 500) * .5 + bp(noise(d), 1500, 4000) * .05; return x * adsr(len(x), .4, .4)
def amb_room(d): x = lp(noise(d), 180) * .5 + np.sin(2 * np.pi * 60 * tt(d)) * .02; return x * adsr(len(x), .3, .3)
def birds(t0, t1):
    for ts in np.arange(t0, t1, .9):
        if rng.random() < .55:
            t = tt(.12); f = 3200 + rng.random() * 1500; S.add(np.sin(2 * np.pi * (f + 800 * np.sin(2 * np.pi * 18 * t)) * t) * np.exp(-t * 25) * .08, ts + rng.random() * .4, pan=rng.uniform(-.7, .7))
def step(stone=True):
    t = tt(.12); return (bp(noise(.12), 300 if stone else 150, 2500 if stone else 900) * np.exp(-t * 45) + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 40) * .4) * .5
def chime():
    t = tt(.7); return (np.sin(2 * np.pi * 1760 * t) + .5 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 6) * .12
def creak(d=.9):
    t = tt(d); f = 180 + 120 * np.sin(2 * np.pi * .8 * t); x = np.sin(np.cumsum(2 * np.pi * f / SR)) * (1 + .5 * np.sign(np.sin(2 * np.pi * 34 * t)))
    return bp(x, 200, 2000) * adsr(len(t), .05, .3) * .25
def handle():
    t = tt(.25); return (bp(noise(.25), 1500, 6000) * np.exp(-t * 40) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 30) * .3) * .4
def bus(d=7):
    t = tt(d); x = np.sin(2 * np.pi * (48 + 10 * t / d) * t) * .4 + lp(noise(d), 250) * .6
    return x * np.clip(1.2 - t / d, 0, 1) * adsr(len(t), .5, 1.5) * .6
def freeze():
    t = tt(.5); return (np.sin(2 * np.pi * 220 * t * (1 - t)) * np.exp(-t * 8) + hp(noise(.5), 3000) * np.exp(-t * 20) * .3) * .35
def whoosh(d=.6):
    t = tt(d); x = bp(noise(d), 400, 3000) * np.sin(np.pi * t / d) ** 2; return x * .3
def paper():
    t = tt(.35); return bp(noise(.35), 2000, 8000) * np.sin(np.pi * t / .35) * .15
def doorslide(d=.8):
    t = tt(d); return (bp(noise(d), 300, 1500) * .3 + np.sin(2 * np.pi * 120 * t) * .05) * adsr(len(t), .1, .3)

S.add(amb_room(3.2), 0, .5); S.add(chime(), .35); S.add(freeze(), 3.2, .9)
S.add(whoosh(.8), 3.6, .5)
S.add(amb_city(11), 6.0, .45); birds(6.0, 17.0); S.add(bus(7.5), 6.0, .9, pan=.3)
S.add(amb_city(11.5), 17.0, .4); birds(17.0, 24.0)
for k in range(10): S.add(step(), 17.0 + k * .5, .35, pan=-.4 + k * .05)   # 0–4 sn yürüyüş
for k in range(5): S.add(step(), 21.3 + k * .5, .3)
S.add(doorslide(), 20.6, .5); S.add(chime(), 24.4)
S.add(amb_city(4.5) * .6, 24.0, .3); S.add(doorslide(), 26.0, .6)
S.add(amb_room(9.1), 28.5, .45); S.add(chime(), 29.0)
for ts in (29.6, 31.4, 33.0): S.add(paper(), ts, .8)
S.add(handle(), 37.85, .9); S.add(creak(1.0), 38.05, .9); S.add(whoosh(.5), 38.0, .4)
S.add(amb_room(22), 38.0, .4)
for k in range(4): S.add(step(False), 39.3 + k * .45, .4, pan=-.5)
for ts in (40.6, 44.8, 52.5): S.add(chime(), ts)
for ts in np.arange(52.5, 60, 1.25): S.add(tick(), ts, .4)
sfx = S.st(); sfx /= np.abs(sfx).max() + 1e-9; sfx *= .7
sf.write(os.path.join(OUT, 'music.wav'), music.astype(np.float32), SR)
sf.write(os.path.join(OUT, 'sfx.wav'), sfx.astype(np.float32), SR)
print('ok', music.shape, sfx.shape)
