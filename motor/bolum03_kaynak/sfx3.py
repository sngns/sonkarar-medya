"""Sentetik müzik + efekt bandı (telifsiz, kodla üretildi)."""
import numpy as np, json, os, wave
SR = 44100
TOTAL = 31.0
T = json.load(open("timing.json")); AT = json.load(open("vo_at.json"))
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
# 1) giriş: hafif gerilim pad + sokak uğultusu
d = T["s1"]
pad = sum(tone(f, d, "sine") for f in (146.83, 174.61, 220.0)) / 3
add(pad * np.minimum(1, np.arange(len(pad)) / SR / 0.8), 0, 0.10)
add(lp(noise(d), 0.01) * 4, 0, 0.12)
# 2) B'yi seçseydin: sepya arp + kapı kapanma vuruşu
add(whoosh(0.8), T["s1"] - 0.2, 0.7)
fd = T["s2"] - T["s1"]
arp = np.zeros(int(fd * SR)); notes = [220.0, 261.63, 329.63, 261.63]
for k in range(int(fd / 0.5)):
    sg = tone(notes[k % 4], 0.48) * env(int(0.48 * SR), 0.01, 0.4); i = int(k * 0.5 * SR); arp[i:i + len(sg)] += sg[: len(arp) - i]
add(arp, T["s1"], 0.10)
add(th, T["s2"] - 0.6, 0.6)
# 3) ofis: klima uğultusu + saat tik-tak + gerilim nabzı
od = T["end"] - T["s2"]
add(lp(noise(od), 0.004) * 6 + 0.15 * tone(60, od, "sine"), T["s2"], 0.07)
add(whoosh(), T["s2"] - 0.1, 0.8)
t = T["s2"]
while t < T["s8"]:
    add(noise(0.025) * env(int(0.025 * SR), 0.001, 0.02), t, 0.06, pan=-0.3); t += 0.5
beat = 0.5; t = T["s3"]; bass = [73.42, 73.42, 87.31, 65.41]; b = 0
while t < T["s8"]:
    intense = t > T["s4"]
    s_ = tone(bass[(b // 4) % 4], beat * 0.9, "saw") * env(int(beat * 0.9 * SR), 0.005, 0.25)
    add(lp(s_, 0.08), t, 0.15 if intense else 0.08)
    k_ = np.sin(2 * np.pi * np.cumsum(np.linspace(140, 45, int(0.18 * SR))) / SR) * env(int(0.18 * SR), 0.001, 0.15)
    add(k_, t, 0.38 if intense else 0.18)
    t += beat; b += 1
# kapı: kapı kolu + gıcırtı
add(noise(0.06) * env(int(0.06 * SR), 0.001, 0.05), T["s4"] + 0.15, 0.35, pan=0.5)
cr = tone(1, 1.0)
fr = np.linspace(420, 260, int(1.0 * SR)); creak = np.sign(np.sin(2 * np.pi * np.cumsum(fr + 30 * np.sin(np.arange(len(fr)) / SR * 40)) / SR)) * env(len(fr), 0.05, 0.4)
add(lp(creak, 0.08), T["s4"] + 0.3, 0.12, pan=0.5)
add(whoosh(), T["s4"] - 0.1, 0.8)
# amca görünür: sting
st = sum(tone(f, 1.4, "saw") for f in (146.83, 185.0, 220.0)) / 3 * env(int(1.4 * SR), 0.005, 1.1)
add(lp(st, 0.2), T["s4"] + 1.0, 0.28)
# kurucu ortaya çıkar: vuruş
add(th + 0.3 * lp(noise(0.35), 0.05) * env(int(0.35 * SR), 0.001, 0.3), T["s5"] + 0.15, 0.9)
add(th + 0.3 * lp(noise(0.35), 0.05) * env(int(0.35 * SR), 0.001, 0.3), AT["n3"], 0.9)
pad_d = T["s8"] - T["s6"]
pad2 = sum(tone(f, pad_d, "saw") for f in (293.66, 349.23, 440.0, 554.37)) / 4
add(lp(pad2, 0.03) * np.linspace(0.0, 1.0, len(pad2)) ** 1.5, T["s6"], 0.16)
add(whoosh(0.8), T["s5"] - 0.1, 0.5)
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
