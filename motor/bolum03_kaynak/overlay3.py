"""Bölüm 3 katmanları."""
import sys, os, json, base64, subprocess, math
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import subtitle, speech_box, watermark, ease, esc, OUT
W, H, FPS = 1080, 1920, 30
T = json.load(open("timing.json")); AT = json.load(open("vo_at.json"))

def banner(t):
    inside = t >= T["s2"]
    alt = "Görüşme odası. Ali Bey bekliyor." if inside else "Kapıdan 'Emre Kaya' olarak giriyorum."
    return f'''<g transform="translate(40,70)">
 <rect x="6" y="8" width="600" height="160" rx="18" fill="#000" opacity="0.25"/>
 <rect x="0" y="0" width="600" height="160" rx="18" fill="#16181D" stroke="#FFC531" stroke-width="5"/>
 <text x="30" y="46" font-family="Poppins" font-weight="700" font-size="26" fill="#FFC531">BÖLÜM 3 · SAAT 09:52</text>
 <text x="30" y="100" font-family="Poppins" font-weight="700" font-size="46" fill="#FFFFFF">SAHTE İSİM</text>
 <text x="30" y="140" font-family="Poppins" font-size="26" fill="#C9CED6">{alt}</text>
</g>'''

def recap(t):
    k = ease(t / 0.35) * (1 - ease((t - (T["s1"] - 0.35)) / 0.35))
    if k <= 0: return ""
    sc = 0.9 + 0.1 * ease(t / 0.35)
    return f'''<g opacity="{k:.2f}" transform="translate(540,{470}) scale({sc:.3f})">
 <rect x="-460" y="-150" width="920" height="300" rx="30" fill="#16181D" opacity="0.92" stroke="#FFC531" stroke-width="7"/>
 <text x="0" y="-80" font-family="Poppins" font-weight="700" font-size="40" fill="#FFC531" text-anchor="middle">GEÇEN BÖLÜM</text>
 <text x="0" y="20" font-family="Poppins" font-weight="700" font-size="92" fill="#fff" text-anchor="middle"><tspan fill="#FF4B55">%67 A</tspan> dedi!</text>
 <text x="0" y="96" font-family="Poppins" font-weight="700" font-size="36" fill="#C9CED6" text-anchor="middle">Gelmeyen adayın adıyla giriyorum...</text>
</g>'''

def flash_tag(t):
    k = ease((t - T["s1"]) / 0.3) * (1 - ease((t - (T["s2"] - 0.3)) / 0.3))
    if k <= 0: return ""
    return f'''<g opacity="{k:.2f}" transform="translate(540,330)">
 <rect x="-400" y="-50" width="800" height="100" rx="50" fill="#2563EB" stroke="#fff" stroke-width="6"/>
 <text x="0" y="18" font-family="Poppins" font-weight="700" font-size="50" fill="#fff" text-anchor="middle">B'Yİ SEÇSEYDİN...</text></g>'''

def pills(appear):
    op = ease(appear)
    return f'''<g opacity="{op:.2f}">
 <g transform="translate(30,270)"><rect width="500" height="78" rx="39" fill="#E3262F" stroke="#fff" stroke-width="5"/>
  <text x="250" y="52" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" text-anchor="middle">A · YALANA DEVAM</text></g>
 <g transform="translate(550,270)"><rect width="500" height="78" rx="39" fill="#2563EB" stroke="#fff" stroke-width="5"/>
  <text x="250" y="52" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" text-anchor="middle">B · İTİRAF ET</text></g></g>'''

SUBS = [  # (start, end, text, y)
 (AT["n1"], T["s1"], "Tamam... bugünlük\nadım Emre Kaya.", 1250),
 (AT["n2"], T["s4"], "Beş yıl mı? Ben daha\nstaj bile yapmadım...", 1480),
 (AT["n3"], AT["n4"], "Şirketin kurucusu...\nsabahki amca mıymış?!", 1480),
 (AT["n4"], T["s7"], "Ya yalana devam edeceğim...\nya da her şeyi itiraf edeceğim.", 1480),
 (T["s7"], T["s8"], "Kararı size bırakıyorum!", 1480),
]
BOXES = [
 (AT["g1"] + 0.05, T["s2"], "GÜVENLİK", "#7FD1FF", "Dürüstlüğün için sağ ol\nkardeşim... ama kurallar\nkurallar.", 1120),
 (AT["i1"] + 0.05, T["s3"] + 0.2, "ALİ BEY · İK", "#7FD1FF", "Emre Kaya... Özgeçmişinizde\nbeş yıl yazılım tecrübesi\nyazıyor. Etkileyici.", 380),
 (AT["a1"] + 0.05, T["s5"], "HÜSEYİN AMCA", "#FFC531", "Evladım! Sabah bana yardım\neden delikanlı sensin!\nAdın neydi senin?", 380),
 (AT["i2"] + 0.05, T["s6"], "ALİ BEY · İK", "#7FD1FF", "Hüseyin Bey! Buyurun efendim...\nKendisi Emre Kaya,\nbugünkü adayımız.", 380),
]

def overlay_svg(t):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    p.append(banner(t))
    if t < T["s1"]: p.append(recap(t))
    if T["s1"] <= t < T["s2"]: p.append(flash_tag(t))
    if t >= T["s6"]: p.append(pills((t - T["s6"]) / 0.4))
    for st, en, tag, col, txt, y in BOXES:
        if st <= t < en: p.append(speech_box(tag, col, txt, y, (t - st) / 0.3))
    for st, en, txt, y in SUBS:
        if st <= t < en:
            pop = 1.0 + 0.18 * (1 - ease((t - st) / 0.18))
            p.append(subtitle(txt, y=y, size=74 if len(txt) < 12 else 62, pop=pop))
    p.append(watermark()); p.append("</svg>")
    return "".join(p)

def end_svg(t, bg, thA, thB):
    a1 = ease(t / 0.4); a2 = ease((t - 0.3) / 0.4); a3 = ease((t - 0.6) / 0.4); a4 = ease((t - 1.0) / 0.4)
    pulse = 1 + 0.04 * math.sin(t * 6); arrow = 10 * math.sin(t * 7)
    def card(x, col, img, letter):
        return f'''<g transform="translate({x},560)">
  <clipPath id="c{letter}"><rect width="440" height="440" rx="28"/></clipPath>
  <image href="{img}" width="440" height="440" preserveAspectRatio="xMidYMid slice" clip-path="url(#c{letter})"/>
  <rect width="440" height="440" rx="28" fill="none" stroke="{col}" stroke-width="12"/>
  <circle cx="220" cy="0" r="52" fill="{col}" stroke="#fff" stroke-width="8"/>
  <text x="220" y="20" font-family="Poppins" font-weight="700" font-size="58" fill="#fff" text-anchor="middle">{letter}</text></g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<image href="{bg}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="#14161B" opacity="0.78"/>
<g opacity="{a1:.2f}" transform="translate(540,{330 - (1 - a1) * 40:.0f})">
 <text x="0" y="0" font-family="Poppins" font-weight="700" font-size="96" fill="#fff" text-anchor="middle">ŞİMDİ NE</text>
 <text x="0" y="110" font-family="Poppins" font-weight="700" font-size="96" fill="#fff" text-anchor="middle">YAPMALIYIM?</text></g>
<g opacity="{a2:.2f}">{card(70, "#E3262F", thA, "A")}{card(570, "#2563EB", thB, "B")}</g>
<g opacity="{a3:.2f}">
 <g transform="translate(70,1060)"><rect width="940" height="150" rx="24" fill="#E3262F" stroke="#fff" stroke-width="6"/>
  <text x="470" y="64" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">A – Yalana devam et:</text>
  <text x="470" y="118" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">"Evet, ben Emre Kaya!"</text></g>
 <text x="540" y="1270" font-family="Poppins" font-weight="700" font-size="40" fill="#FFC531" text-anchor="middle">YA DA</text>
 <g transform="translate(70,1310)"><rect width="940" height="150" rx="24" fill="#2563EB" stroke="#fff" stroke-width="6"/>
  <text x="470" y="64" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">B – Her şeyi itiraf et,</text>
  <text x="470" y="118" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">gerçek adını söyle!</text></g></g>
<g opacity="{a4:.2f}">
 <g transform="translate(540,1580) scale({pulse:.3f})"><text x="0" y="0" font-family="Poppins" font-weight="700" font-size="58" fill="#FFD43B" text-anchor="middle" stroke="{OUT}" stroke-width="12" paint-order="stroke">Yorumlara A veya B yaz!</text></g>
 <text x="540" y="1660" font-family="Poppins" font-size="36" fill="#E6E8EC" text-anchor="middle">En çok oy alan seçenekle hikâye son buluyor.</text>
 <path transform="translate(540,{1730 + arrow:.0f})" d="M-30,0 L30,0 L0,40 Z" fill="#FFD43B" stroke="{OUT}" stroke-width="5"/></g>
{watermark()}
</svg>'''

def b64(path): return "data:image/jpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()
ASSETS = {}
def job(i):
    t = i / FPS
    if t < T["s8"]:
        out = f"ov/o{i:05d}.png"
        if not os.path.exists(out):
            subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", out], input=overlay_svg(t).encode(), check=True)
    else:
        out = f"end/e{i:05d}.png"
        if not os.path.exists(out):
            if not ASSETS: ASSETS.update(bg=b64("end_bg.jpg"), a=b64("thumb_a.jpg"), b=b64("thumb_b.jpg"))
            subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", out], input=end_svg(t - T["s8"], ASSETS["bg"], ASSETS["a"], ASSETS["b"]).encode(), check=True)

if __name__ == "__main__":
    os.makedirs("ov", exist_ok=True); os.makedirs("end", exist_ok=True)
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    n = int(round(T["end"] * FPS)); ns = int(math.ceil(T["s8"] * FPS))
    rng = range(ns) if only == "ov" else range(ns, n) if only == "end" else range(n)
    with Pool(1) as pool: pool.map(job, rng, chunksize=10)
