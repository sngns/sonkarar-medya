# Bölüm 3 miks: sesler (story.js zamanları) + müzik + efekt, satır başına otomatik kısma → mix.wav
import numpy as np, soundfile as sf, json, re, os
from scipy.signal import butter, sosfilt
D = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(D); SR = 48000; N = SR * 60
story = open(os.path.join(P, 'story.js'), encoding='utf-8').read()
VO = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\{ id: '(\w+)', t: ([\d.]+)", story)]
VO = [v for v in VO if v[0] in ('h1','n1','n2','p1','g1','a1','p2','h2','a2','p3','p4','n3')]
rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)
def comp(x, thr=.25, ratio=3):
    a = np.abs(x); g = np.where(a > thr, (thr + (a - thr) / ratio) / (a + 1e-9), 1); return x * g
voice = np.zeros(N); duck = np.ones(N)
for k, t in VO:
    f = os.path.join(P, 'voices', f'{k}.wav')
    if not os.path.exists(f): print('yok:', k); continue
    x, sr = sf.read(f); x = x if x.ndim == 1 else x.mean(1)
    x = comp(x / (np.abs(x).max() + 1e-9)); x *= 10 ** (-17 / 20) / rms(x)
    if k in ('p1', 'p2', 'p3', 'p4'):   # iç ses: biraz yakın ve yumuşak
        x = sosfilt(butter(2, 7000, 'low', fs=SR, output='sos'), x)
    i = int(t * SR); x = x[:N - i]; voice[i:i + len(x)] += x
    a, b = max(0, i - int(.15 * SR)), min(N, i + len(x) + int(.25 * SR)); duck[a:b] = np.minimum(duck[a:b], 10 ** (-9 / 20))
k = int(.12 * SR); duck = np.convolve(duck, np.ones(k) / k, 'same')
mus, _ = sf.read(os.path.join(D, 'music.wav')); fx, _ = sf.read(os.path.join(D, 'sfx.wav'))
mus = mus[:N] * (10 ** (-20 / 20) / rms(mus[:N])); fx = fx[:N] * (10 ** (-27 / 20) / rms(fx[:N]))
mix = mus * duck[:, None] + fx * (.5 + .5 * duck[:, None]) + voice[:, None]
mix = np.tanh(mix * 1.1) / 1.1
sf.write(os.path.join(P, 'mix.wav'), mix.astype(np.float32), SR)
for k, t in VO: print(k, t)
print('mix ok', mix.shape, 'peak', float(np.abs(mix).max()))
