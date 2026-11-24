"""Sentetik müzik + efekt bandı (telifsiz, kodla üretildi)."""
import numpy as np, json, os, wave
SR = 44100
TOTAL = 31.0
T = dict(s1=0.0, s2=3.6, s3=7.2, s4=9.4, s5=13.4, s6=16.4, s7=20.0, s8=23.0, end=TOTAL)
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

# --- music bed: tense pulse in D minor, tempo 120 → speeds after s3
bpm = 120
beat = 60 / bpm
t = 0.0
bass_notes = [73.42, 73.42, 87.31, 65.41]  # D2 D2 F2 C2
bar = 0
while t < T["s8"]:
    f = bass_notes[bar % 4]
    for b in range(4):
        if t >= T["s8"]: break
        intense = t > T["s3"]
        g = 0.18 if intense else 0.11
        s = tone(f, beat * 0.9, "saw") * env(int(beat * 0.9 * SR), 0.005, 0.25)
        add(lp(s, 0.08), t, g)
        # kick
        k = np.sin(2 * np.pi * np.cumsum(np.linspace(140, 45, int(0.18 * SR))) / SR) * env(int(0.18 * SR), 0.001, 0.15)
        add(k, t, 0.45 if intense else 0.3)
        # clock tick on off-beat
        tick = noise(0.03) * env(int(0.03 * SR), 0.001, 0.02)
        add(tick, t + beat / 2, 0.08, pan=0.4)
        t += beat
    bar += 1
# high tension string pad after s6
pad_d = T["s8"] - T["s6"]
pad = sum(tone(f, pad_d, "saw") for f in (293.66, 349.23, 440.0, 554.37)) / 4
pad = lp(pad, 0.03) * np.linspace(0.0, 1.0, len(pad)) ** 1.5
add(pad, T["s6"], 0.16)

# --- bus arrival: engine rumble + brake hiss
d = T["s3"] - T["s2"]
rum = lp(noise(d), 0.01) * 6 + 0.4 * tone(48, d, "saw")
e = np.interp(np.arange(len(rum)) / SR, [0, 1.8, 2.6, d], [0.1, 1.0, 0.6, 0.35])
add(rum * e, T["s2"], 0.35, pan=-0.3)
hiss = noise(0.7) * env(int(0.7 * SR), 0.02, 0.5)
add(lp(hiss, 0.6) - lp(hiss, 0.15), T["s2"] + 2.5, 0.35, pan=-0.2)
# idle until end card
idle_d = T["s8"] - T["s3"]
idle = lp(noise(idle_d), 0.008) * 5 + 0.3 * tone(42, idle_d, "saw")
add(lp(idle, 0.05), T["s3"], 0.15)

# --- whooshes on whip pans
def whoosh(d=0.45):
    n = noise(d); e = np.sin(np.linspace(0, np.pi, len(n))) ** 2
    return (lp(n, 0.25) - lp(n, 0.03)) * e
add(whoosh(), T["s3"] - 0.1, 0.9)
add(whoosh(), T["s5"] - 0.1, 0.7)
add(whoosh(0.8), T["s6"] - 0.1, 0.5)

# --- thud + sting at fall
th = np.sin(2 * np.pi * np.cumsum(np.linspace(90, 30, int(0.35 * SR))) / SR) * env(int(0.35 * SR), 0.001, 0.3)
add(th + 0.3 * lp(noise(0.35), 0.05) * env(int(0.35 * SR), 0.001, 0.3), T["s3"], 1.0)
st = sum(tone(f, 1.2, "saw") for f in (146.83, 155.56, 220.0)) / 3 * env(int(1.2 * SR), 0.005, 1.0)
add(lp(st, 0.2), T["s3"] + 0.05, 0.35)

# --- horn when driver speaks
hn = (tone(370, 0.5, "sq") + tone(466, 0.5, "sq")) * env(int(0.5 * SR), 0.01, 0.08)
add(lp(hn, 0.15), T["s5"] + 0.05, 0.12)
add(lp(hn, 0.15), T["s5"] + 0.6, 0.12)

# --- end card: riser + hit + soft loop
rs = noise(1.2) * np.linspace(0, 1, int(1.2 * SR)) ** 2
add(lp(rs, 0.3) - lp(rs, 0.05), T["s8"] - 1.2, 0.5)
hit = th[: int(0.35 * SR)]
add(hit, T["s8"], 1.0)
loop_d = T["end"] - T["s8"]
arp = np.zeros(int(loop_d * SR))
notes = [293.66, 349.23, 440.0, 349.23]
for k in range(int(loop_d / 0.25)):
    s = tone(notes[k % 4], 0.22) * env(int(0.22 * SR), 0.005, 0.18)
    i = int(k * 0.25 * SR); arp[i:i + len(s)] += s[: len(arp) - i]
add(arp, T["s8"] + 0.3, 0.12)

out /= max(1e-9, np.abs(out).max()) / 0.8
out[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
with wave.open("bed.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("ok", TOTAL)
