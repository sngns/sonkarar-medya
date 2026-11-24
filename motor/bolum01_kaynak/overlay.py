"""Gerçekçi bölüm için 2D katmanlar: başlık bandı, altyazılar, konuşma kutuları, A/B, final ekranı."""
import sys, os, json, base64, subprocess, math
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import top_banner, subtitle, speech_box, ab_pills, watermark, ease, esc, OUT

W, H, FPS = 1080, 1920, 30
T = dict(s1=0.0, s2=3.6, s3=7.2, s4=9.4, s5=13.4, s6=16.4, s7=20.0, s8=23.0, end=31.0)
if os.path.exists("timing.json"):
    T.update(json.load(open("timing.json")))

SUBS = [("s1", 0.3, "s2", "Bugün hayatımın en önemli\niş görüşmesi var.", 700),
        ("s2", 0.4, "s3", "Bu otobüsü kaçırırsam\nasla yetişemem.", 700),
        ("s3", 0.25, "s4", "Amca?!", 600),
        ("s6", 0.5, "s7", "Etrafta kimse yok...\notobüs de kalkıyor!", 640),
        ("s7", 0.2, "s8", "Kararı size bırakıyorum!", 640)]

def notif(t):
    """S1: telefon bildirimi kartı kayarak gelir"""
    k = ease((t - 0.4) / 0.4) * (1 - ease((t - (T["s2"] - 0.3)) / 0.3))
    if k <= 0: return ""
    y = 1250 + (1 - k) * 80
    return f'''<g transform="translate(150,{y:.0f})" opacity="{k:.2f}">
 <rect x="0" y="0" width="780" height="190" rx="36" fill="#F4F6FA" opacity="0.96"/>
 <rect x="32" y="32" width="64" height="64" rx="14" fill="#E3262F"/>
 <text x="64" y="76" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" text-anchor="middle">25</text>
 <text x="120" y="62" font-family="Poppins" font-weight="700" font-size="28" fill="#555">TAKVİM · şimdi</text>
 <text x="120" y="112" font-family="Poppins" font-weight="700" font-size="40" fill="#111">İş görüşmesi · 09:30</text>
 <text x="120" y="160" font-family="Poppins" font-size="34" fill="#E3262F">35 dakika kaldı</text>
</g>'''

def b64(path):
    return "data:image/jpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()

def overlay_svg(t):
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    p.append(top_banner())
    if t < T["s2"]:
        p.append(notif(t))
    if t >= T["s6"]:
        p.append(ab_pills((t - T["s6"]) / 0.4))
    if T["s4"] + 0.3 <= t < T["s5"]:
        p.append(speech_box("AMCA", "#FFC531", "Evladım... ne olur yardım et,\nkalkamıyorum...", 520, (t - T["s4"] - 0.3) / 0.3))
    if T["s5"] + 0.4 <= t < T["s6"]:
        p.append(speech_box("ŞOFÖR", "#7FD1FF", "Biniyorsan bin,\nkalkıyoruz!", 560, (t - T["s5"] - 0.4) / 0.3))
    for a, off, b, txt, y in SUBS:
        st, en = T[a] + off, T[b]
        if st <= t < en:
            pop = 1.0 + 0.18 * (1 - ease((t - st) / 0.18))
            p.append(subtitle(txt, y=y, size=74 if len(txt) < 12 else 66, pop=pop))
    p.append(watermark())
    p.append("</svg>")
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
  <text x="470" y="64" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">A – Amcaya yardım et,</text>
  <text x="470" y="118" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">iş görüşmesini kaçır!</text></g>
 <text x="540" y="1270" font-family="Poppins" font-weight="700" font-size="40" fill="#FFC531" text-anchor="middle">YA DA</text>
 <g transform="translate(70,1310)"><rect width="940" height="150" rx="24" fill="#2563EB" stroke="#fff" stroke-width="6"/>
  <text x="470" y="64" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">B – Otobüse bin,</text>
  <text x="470" y="118" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">birinin yardım etmesini um!</text></g></g>
<g opacity="{a4:.2f}">
 <g transform="translate(540,1580) scale({pulse:.3f})"><text x="0" y="0" font-family="Poppins" font-weight="700" font-size="58" fill="#FFD43B" text-anchor="middle" stroke="{OUT}" stroke-width="12" paint-order="stroke">Yorumlara A veya B yaz!</text></g>
 <text x="540" y="1660" font-family="Poppins" font-size="36" fill="#E6E8EC" text-anchor="middle">En çok oy alan seçenekle devam ediyorum.</text>
 <path transform="translate(540,{1730 + arrow:.0f})" d="M-30,0 L30,0 L0,40 Z" fill="#FFD43B" stroke="{OUT}" stroke-width="5"/></g>
{watermark()}
</svg>'''

def job(i):
    t = i / FPS
    if t < T["s8"]:
        out = f"ov/o{i:05d}.png"
        if not os.path.exists(out):
            subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", out], input=overlay_svg(t).encode(), check=True)
    else:
        out = f"end/e{i:05d}.png"
        if not os.path.exists(out):
            svg = end_svg(t - T["s8"], ASSETS["bg"], ASSETS["a"], ASSETS["b"])
            subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", out], input=svg.encode(), check=True)

ASSETS = {}
if __name__ == "__main__":
    os.makedirs("ov", exist_ok=True); os.makedirs("end", exist_ok=True)
    ASSETS.update(bg=b64("end_bg.jpg"), a=b64("thumb_a.jpg"), b=b64("thumb_b.jpg"))
    n = int(round(T["end"] * FPS))
    with Pool(1) as pool:
        pool.map(job, range(n), chunksize=10)
