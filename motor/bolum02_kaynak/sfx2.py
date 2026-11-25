"""Sentetik müzik + efekt bandı (telifsiz, kodla üretildi)."""
import numpy as np, json, os, wave
SR = 44100
TOTAL = 31.0
T = {}
if os.path.exists("timing.json"):
    T.update(json.load(open("timing.json")))
TOTAL = T["end"]
N = int(SR * TOTAL)
out = np.zeros((N, 2))
rng = np.random.default_rng(7)

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    sig = sig[: max(0, N - i)]
    l, r = gain * (1 - max(0, pan)), gain * (1 + min(0, pan))
    out[i:i + len(sig), 0] += sig * l
    out[i:i + len(sig), 1] += sig * r

def env(n, a=0.01, r=0.2):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def tone(f, d, kind="sine"):
    t = np.arange(int(d * SR)) / SR
    if kind == "sine": return np.sin(2 * np.pi * f * t)
    if kind == "saw": return 2 * ((f * t) % 1) - 1
    if kind == "sq": return np.sign(np.sin(2 * np.pi * f * t))

def lp(x, k=0.05):
    y = np.zeros_like(x); a = 0
    for i in range(len(x)):
        a += k * (x[i] - a); y[i] = a
    return y

def noise(d): return rng.standard_normal(int(d * SR))


th = np.sin(2 * np.pi * np.cumsum(np.linspace(90, 30, int(0.35 * SR))) / SR) * env(int(0.35 * SR), 0.001, 0.3)
def whoosh(d=0.45):
    n = noise(d); e = np.sin(np.linspace(0, np.pi, len(n))) ** 2
    return (lp(n, 0.25) - lp(n, 0.03)) * e
# 1) özet: yumuşak pad + uzaklaşan otobüs
d = T["s2"]
pad = sum(tone(f, d, "sine") for f in (146.83, 174.61, 220.0)) / 3
add(pad * np.minimum(1, np.arange(len(pad)) / SR / 1.0), 0, 0.10)
rum = lp(noise(4.5), 0.01) * 6 + 0.4 * tone(48, 4.5, "saw")
add(rum * np.linspace(0.8, 0.0, len(rum)), 0, 0.3, pan=0.4)
# kart: küçük "ding"
add(tone(1318.5, 0.6) * env(int(0.6 * SR), 0.002, 0.55) + 0.5 * tone(1975.5, 0.6) * env(int(0.6 * SR), 0.002, 0.5), T["cardAt"], 0.12)
# 2) geri bakış: sepya, yavaş arp + rüzgâr + otobüs içi uğultu
add(whoosh(0.8), T["s2"] - 0.2, 0.7)
fd = T["s3"] - T["s2"]
arp = np.zeros(int(fd * SR)); notes = [220.0, 261.63, 329.63, 261.63]
for k in range(int(fd / 0.5)):
    sg = tone(notes[k % 4], 0.48) * env(int(0.48 * SR), 0.01, 0.4); i = int(k * 0.5 * SR); arp[i:i + len(sg)] += sg[: len(arp) - i]
add(arp, T["s2"], 0.10)
add(lp(noise(fd), 0.01) * 5 + 0.3 * tone(45, fd, "saw"), T["s2"], 0.18)
# 3) şirket: gerilim nabzı
beat = 0.5; t = T["s3"]; bass = [73.42, 73.42, 87.31, 65.41]; b = 0
while t < T["s8"]:
    intense = t > T["notice"]
    s_ = tone(bass[(b // 4) % 4], beat * 0.9, "saw") * env(int(beat * 0.9 * SR), 0.005, 0.25)
    add(lp(s_, 0.08), t, 0.16 if intense else 0.10)
    k_ = np.sin(2 * np.pi * np.cumsum(np.linspace(140, 45, int(0.18 * SR))) / SR) * env(int(0.18 * SR), 0.001, 0.15)
    add(k_, t, 0.4 if intense else 0.22)
    add(noise(0.03) * env(int(0.03 * SR), 0.001, 0.02), t + beat / 2, 0.07, pan=0.4)
    t += beat; b += 1
add(whoosh(), T["s3"] - 0.1, 0.8)
# tanıma anı: vuruş + sting
add(th + 0.3 * lp(noise(0.35), 0.05) * env(int(0.35 * SR), 0.001, 0.3), T["notice"], 0.9)
st = sum(tone(f, 1.4, "saw") for f in (146.83, 185.0, 220.0)) / 3 * env(int(1.4 * SR), 0.005, 1.1)
add(lp(st, 0.2), T["notice"] + 0.05, 0.3)
pad_d = T["s8"] - T["s6"]
pad2 = sum(tone(f, pad_d, "saw") for f in (293.66, 349.23, 440.0, 554.37)) / 4
add(lp(pad2, 0.03) * np.linspace(0.0, 1.0, len(pad2)) ** 1.5, T["s6"], 0.16)
add(whoosh(0.8), T["s6"] - 0.1, 0.5)
# final
rs = noise(1.2) * np.linspace(0, 1, int(1.2 * SR)) ** 2
add(lp(rs, 0.3) - lp(rs, 0.05), T["s8"] - 1.2, 0.5)
add(th, T["s8"], 1.0)
loop_d = T["end"] - T["s8"]; arp = np.zeros(int(loop_d * SR)); notes = [293.66, 349.23, 440.0, 349.23]
for k in range(int(loop_d / 0.25)):
    sg = tone(notes[k % 4], 0.22) * env(int(0.22 * SR), 0.005, 0.18); i = int(k * 0.25 * SR); arp[i:i + len(sg)] += sg[: len(arp) - i]
add(arp, T["s8"] + 0.3, 0.12)
out /= max(1e-9, np.abs(out).max()) / 0.8
out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
with wave.open("bed.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", TOTAL)
