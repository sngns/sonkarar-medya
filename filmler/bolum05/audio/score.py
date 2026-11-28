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
motif = [74, 77, 81, 79, 77, 76, 74]
prog = [[50, 57, 62, 65, 69], [46, 53, 58, 62, 65], [41, 48, 53, 57, 60], [48, 55, 60, 64, 67]]
bar = 4 * B
# 0–4.4 kanca: çan + yükselen pad
M.add(bell(86), 0.2, .5); M.add(pad([46, 53, 58, 62], 4.4, 1600, .09, .3), 0)
for i, m in enumerate(motif[:4]): M.add(celesta(m), .6 + i * B * .5, .45)
# 4.4–13.5 sokak: harp ostinato + davul
for k in range(4):
    ch = prog[k % 4]; base = 4.4 + k * bar
    if base >= 13.5: break
    M.add(pad(ch[:4], bar + .3, 1600, .07, .4), base)
    for j, q in enumerate([0, 2, 3, 4, 3, 2, 1, 2]):
        ts = base + j * B / 2
        if ts < 13.5: M.add(harp(ch[q] + 12), ts, .45, pan=-.3 + .6 * (j / 7))
    for j in range(4):
        ts = base + j * B
        if ts < 13.5: M.add(framedrum(), ts, .4 if j % 2 == 0 else .25)
# 13.5–25 ofis: gerilim → 18.3 kapı, koro+boynuz
M.add(strings([50, 57, 62, 65], 4.6), 13.5); M.add(timpani(38), 18.3, .6)
for base, ch in [(18.6, [41, 53, 57, 60]), (21.1, [46, 53, 58, 62])]:
    M.add(choir(ch, 2.8, .1), base); M.add(pad(ch, 2.7, 2200, .08, .4), base)
M.add(horn(65, 1.6), 18.8); M.add(horn(69, 2.4), 21.2)
# 25–30 sepya
for j, m in enumerate([62, 65, 69, 67, 65, 62, 60, 58]): M.add(harp(m, 3), 25.2 + j * B * .95, .35)
# 30–32.5 kart
M.add(timpani(34), 30.0, .6); M.add(pad([46, 53, 58, 62], 2.6, 1600, .1, .3), 30.0)
# 32.5–42 sır: alçak yaylı + saat
M.add(strings([38, 50, 53, 57], 9.5, .09), 32.5)
for i, ts in enumerate(np.arange(32.5, 41.8, B)): M.add(tick(i % 2 == 0), ts, .5)
# 42–50 kapı: tik hızlanır
ts = 42.0; step = B
while ts < 49.6: M.add(tick(int(ts * 10) % 2 == 0), ts, .55); ts += step; step = max(B / 2.2, step * .97)
M.add(strings([38, 45, 50], 8, .08), 42.0); M.add(timpani(33), 48.8, .5)
# 50–60 seçim
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

S.add(amb_city(13.5), 0, .45); birds(0, 13.5); S.add(chime(), 4.8); S.add(chime(), 8.4)
for k in range(7): S.add(step(), 4.5 + k * .4, .35)
t = tt(.4); S.add(bp(noise(.4), 400, 2500) * np.exp(-t * 12) * .4, 6.5, .6)   # apartman kapısı
for k in range(6): S.add(step(), 11.1 + k * .35, .35, pan=-.4)
S.add(amb_room(16.5), 13.5, .45); S.add(chime(), 14.0); S.add(handle(), 17.4, .9); S.add(creak(1.0), 17.6, .8); S.add(chime(), 18.6)
S.add(amb_room(5) * .6, 25.0, .3); S.add(chime(), 25.4); S.add(whoosh(.8), 29.7, .5)
S.add(amb_room(9.5), 32.5, .4); S.add(chime(), 32.9)
S.add(amb_city(18), 42.0, .4); birds(42.0, 60.0); S.add(chime(), 42.5)
for ts in np.arange(52.3, 60, 1.25): S.add(tick(), ts, .4)
sfx = S.st(); sfx /= np.abs(sfx).max() + 1e-9; sfx *= .7
sf.write(os.path.join(OUT, 'music.wav'), music.astype(np.float32), SR)
sf.write(os.path.join(OUT, 'sfx.wav'), sfx.astype(np.float32), SR)
print('ok', music.shape, sfx.shape)
