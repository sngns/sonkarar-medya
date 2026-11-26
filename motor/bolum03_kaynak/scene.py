"""Bölüm 1 – Otobüs durağı. SVG kare üretici."""
import math

W, H = 1080, 1920
OUT = "#16181D"  # outline

# ---------------------------------------------------------------- helpers
def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------------------------------------------------------------- world parts
def sky():
    return f'''
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#8EC5F0"/><stop offset="0.7" stop-color="#CFE6F7"/><stop offset="1" stop-color="#F6E3C8"/>
 </linearGradient>
</defs>
<rect x="-3000" y="-2000" width="10000" height="3100" fill="url(#sky)"/>'''

def cloud(x, y, s):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="#fff" stroke="{OUT}" stroke-width="5">'
            '<path d="M0,60 a45,45 0 0 1 60,-50 a60,60 0 0 1 110,0 a45,45 0 0 1 55,50 z"/></g>')

BUILD_COLORS = ["#E9B872", "#D98B6A", "#C9CED6", "#9FB4C7", "#E6D3B3", "#B9A38B", "#DDB4A0", "#A7C1A8"]

def building(x, w, h, col, seed):
    base = 1000
    y = base - h
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" stroke="{OUT}" stroke-width="6"/>']
    s.append(f'<rect x="{x-8}" y="{y-14}" width="{w+16}" height="18" fill="#8a7a6a" stroke="{OUT}" stroke-width="5"/>')
    cols = max(2, int(w // 70))
    gap = w / cols
    rows = int((h - 120) // 95)
    for r in range(rows):
        for c in range(cols):
            wx = x + c * gap + gap * 0.22
            wy = y + 40 + r * 95
            lit = ((seed * 7 + r * 3 + c * 5) % 9) == 0
            s.append(f'<rect x="{wx:.0f}" y="{wy}" width="{gap*0.56:.0f}" height="58" rx="4" '
                     f'fill="{"#FFE9A8" if lit else "#5E7A94"}" stroke="{OUT}" stroke-width="4"/>')
    return "\n".join(s)

def shop(x, w, name, col):
    # ground-floor shop band on a building
    return (f'<rect x="{x}" y="900" width="{w}" height="100" fill="#3a3f4a" stroke="{OUT}" stroke-width="5"/>'
            f'<rect x="{x+10}" y="860" width="{w-20}" height="46" rx="6" fill="{col}" stroke="{OUT}" stroke-width="5"/>'
            f'<text x="{x+w/2}" y="893" font-family="Poppins" font-weight="700" font-size="28" fill="#fff" text-anchor="middle">{name}</text>')

def tree(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-12" y="-40" width="24" height="160" fill="#7A5236" stroke="{OUT}" stroke-width="5"/>'
            f'<circle cx="0" cy="-90" r="85" fill="#5DAA5B" stroke="{OUT}" stroke-width="6"/>'
            f'<circle cx="-55" cy="-40" r="55" fill="#4E9A4E" stroke="{OUT}" stroke-width="6"/>'
            f'<circle cx="60" cy="-45" r="58" fill="#4E9A4E" stroke="{OUT}" stroke-width="6"/></g>')

def street_static():
    s = [sky()]
    s += [cloud(-300, 120, 1.4), cloud(500, 220, 1.1), cloud(1300, 90, 1.5), cloud(2200, 200, 1.2), cloud(2900, 130, 1.3)]
    xs = [-500, -180, 120, 420, 760, 1060, 1380, 1700, 2000, 2330, 2650, 2950, 3250]
    hs = [520, 680, 430, 600, 740, 480, 650, 560, 700, 450, 620, 540, 660]
    for i, x in enumerate(xs):
        s.append(building(x, 300, hs[i], BUILD_COLORS[i % len(BUILD_COLORS)], i))
    s.append(shop(140, 260, "FIRIN", "#C0392B"))
    s.append(shop(1080, 260, "ECZANE", "#2E8B57"))
    s.append(shop(2020, 260, "MARKET", "#2563EB"))
    # far sidewalk
    s.append(f'<rect x="-2000" y="995" width="8000" height="45" fill="#C9C3B8" stroke="{OUT}" stroke-width="5"/>')
    for x in (-200, 650, 1500, 2400, 3200):
        s.append(tree(x, 930, 0.9))
    # road
    s.append(f'<rect x="-2000" y="1040" width="8000" height="260" fill="#4A4E57"/>')
    for x in range(-2000, 6000, 220):
        s.append(f'<rect x="{x}" y="1165" width="120" height="14" rx="4" fill="#F4F1E8"/>')
    # curb + near sidewalk
    s.append(f'<rect x="-2000" y="1300" width="8000" height="34" fill="#E2DCCF" stroke="{OUT}" stroke-width="6"/>')
    s.append(f'<rect x="-3000" y="1334" width="10000" height="2500" fill="#D8D0C2"/>')
    for x in range(-2000, 6000, 260):
        s.append(f'<line x1="{x}" y1="1334" x2="{x-160}" y2="1920" stroke="#B9B0A1" stroke-width="5"/>')
    s.append(f'<line x1="-2000" y1="1560" x2="6000" y2="1560" stroke="#B9B0A1" stroke-width="5"/>')
    # bus stop (pole + sign + bench) on near sidewalk
    s.append(f'''<g transform="translate(1520,0)">
 <rect x="-10" y="760" width="20" height="600" fill="#9AA3AE" stroke="{OUT}" stroke-width="5"/>
 <rect x="-95" y="700" width="190" height="120" rx="14" fill="#1F6FEB" stroke="{OUT}" stroke-width="6"/>
 <text x="0" y="752" font-family="Poppins" font-weight="700" font-size="34" fill="#fff" text-anchor="middle">DURAK</text>
 <text x="0" y="798" font-family="Poppins" font-weight="700" font-size="34" fill="#FFD43B" text-anchor="middle">34 · 42K</text>
</g>''')
    return "\n".join(s)

STREET = street_static()

def bus(x, door_open=0.0, blink=False):
    # bus body 1150 wide, bottom on road y 1260
    d = door_open
    s = [f'<g transform="translate({x},0)">']
    s.append(f'<rect x="0" y="780" width="1150" height="440" rx="40" fill="#E94B3C" stroke="{OUT}" stroke-width="8"/>')
    s.append(f'<rect x="0" y="1120" width="1150" height="70" fill="#C0392B" stroke="{OUT}" stroke-width="6"/>')
    s.append(f'<rect x="30" y="800" width="1090" height="60" rx="10" fill="#222" stroke="{OUT}" stroke-width="5"/>')
    s.append(f'<text x="575" y="845" font-family="Poppins" font-weight="700" font-size="40" fill="#FFB020" text-anchor="middle">42K  ·  MERKEZ</text>')
    for i in range(5):
        wx = 250 + i * 175
        s.append(f'<rect x="{wx}" y="880" width="150" height="150" rx="14" fill="#AFD3EE" stroke="{OUT}" stroke-width="6"/>')
        if i in (1, 3):  # passengers
            s.append(f'<circle cx="{wx+75}" cy="975" r="32" fill="#E8B48F" stroke="{OUT}" stroke-width="5"/>'
                     f'<rect x="{wx+35}" y="1005" width="80" height="30" rx="12" fill="#4B6584" stroke="{OUT}" stroke-width="5"/>')
    # front windshield + driver (left side = front, bus faces left)
    s.append(f'<rect x="20" y="880" width="200" height="220" rx="22" fill="#AFD3EE" stroke="{OUT}" stroke-width="6"/>')
    s.append(f'<circle cx="150" cy="975" r="34" fill="#C98E6B" stroke="{OUT}" stroke-width="5"/>'
             f'<path d="M116,965 q34,-40 68,0 z" fill="#333" stroke="{OUT}" stroke-width="4"/>'
             f'<rect x="108" y="1008" width="84" height="40" rx="14" fill="#2C3E50" stroke="{OUT}" stroke-width="5"/>')
    # door (front-ish, between windshield and windows)
    dw = 0  # door panels slide
    s.append(f'<rect x="230" y="880" width="0" height="0"/>')
    # wheels
    for wx in (230, 920):
        s.append(f'<circle cx="{wx}" cy="1215" r="70" fill="#222" stroke="{OUT}" stroke-width="8"/>'
                 f'<circle cx="{wx}" cy="1215" r="30" fill="#BBB" stroke="{OUT}" stroke-width="6"/>')
    # headlight + indicator
    s.append(f'<rect x="-6" y="1110" width="40" height="40" rx="8" fill="#FFF3B0" stroke="{OUT}" stroke-width="5"/>')
    if blink:
        s.append(f'<circle cx="20" cy="1080" r="16" fill="#FFA500" stroke="{OUT}" stroke-width="4"/>')
    s.append('</g>')
    return "\n".join(s)

def old_man(x, y, s=1.0, reach=0.0):
    """Kaldırımda düşmüş yaşlı amca. reach: uzanan kolu kaldırma 0..1"""
    a = -20 - 50 * reach
    return f'''<g transform="translate({x},{y}) scale({s})">
 <ellipse cx="0" cy="150" rx="260" ry="30" fill="#000" opacity="0.12"/>
 <!-- legs -->
 <path d="M-20,110 L180,120 L200,150 L-30,150 Z" fill="#7A8190" stroke="{OUT}" stroke-width="7" stroke-linejoin="round"/>
 <path d="M180,118 l50,-8 l12,40 l-60,2 z" fill="#3B2A20" stroke="{OUT}" stroke-width="6"/>
 <!-- torso (sitting, leaning back on one arm) -->
 <path d="M-90,-40 Q-40,-80 20,-50 L40,130 L-110,130 Z" fill="#8B5E3C" stroke="{OUT}" stroke-width="7" stroke-linejoin="round"/>
 <path d="M-60,-40 L-30,40 L0,-45" fill="none" stroke="#6E4A2E" stroke-width="6"/>
 <!-- back arm on ground -->
 <path d="M-95,0 L-170,110 L-140,125 L-70,30" fill="#8B5E3C" stroke="{OUT}" stroke-width="7" stroke-linejoin="round"/>
 <circle cx="-160" cy="122" r="18" fill="#E2B08C" stroke="{OUT}" stroke-width="5"/>
 <!-- reaching arm -->
 <g transform="translate(20,-20) rotate({a})">
  <rect x="0" y="-20" width="130" height="40" rx="18" fill="#8B5E3C" stroke="{OUT}" stroke-width="7"/>
  <circle cx="145" cy="0" r="22" fill="#E2B08C" stroke="{OUT}" stroke-width="5"/>
 </g>
 <!-- head -->
 <circle cx="-40" cy="-120" r="62" fill="#E2B08C" stroke="{OUT}" stroke-width="7"/>
 <path d="M-100,-140 Q-40,-205 20,-140 L25,-128 L-105,-128 Z" fill="#6D6A63" stroke="{OUT}" stroke-width="6"/>
 <rect x="-108" y="-140" width="138" height="16" rx="6" fill="#55524C" stroke="{OUT}" stroke-width="5"/>
 <path d="M-62,-92 q22,14 44,0" fill="#E9E6E0" stroke="{OUT}" stroke-width="5"/>
 <circle cx="-58" cy="-118" r="6" fill="{OUT}"/><circle cx="-20" cy="-118" r="6" fill="{OUT}"/>
 <path d="M-74,-128 l22,-8 M-4,-128 l-22,-8" stroke="{OUT}" stroke-width="5"/>
 <ellipse cx="-38" cy="-70" rx="11" ry="13" fill="#7a2e2e" stroke="{OUT}" stroke-width="5"/>
 <!-- cane + spilled oranges -->
 <path d="M80,160 L330,60 q20,-10 25,12" fill="none" stroke="#7A5236" stroke-width="16" stroke-linecap="round"/>
 <path d="M80,160 L330,60 q20,-10 25,12" fill="none" stroke="{OUT}" stroke-width="4" stroke-linecap="round" opacity="0.6"/>
 <path d="M-260,90 l70,-10 l20,70 l-80,8 z" fill="#F2EBDD" stroke="{OUT}" stroke-width="6"/>
 <circle cx="-300" cy="150" r="22" fill="#F39C12" stroke="{OUT}" stroke-width="5"/>
 <circle cx="-350" cy="130" r="20" fill="#F39C12" stroke="{OUT}" stroke-width="5"/>
 <circle cx="-410" cy="155" r="22" fill="#F39C12" stroke="{OUT}" stroke-width="5"/>
</g>'''

# ---------------------------------------------------------------- POV hands
SKIN, SKIN_D = "#F2B58E", "#D9946B"

def hand(cx, cy, rot, mirror, pose):
    """pose: open | fist | point | hold"""
    sx = -1 if mirror else 1
    g = [f'<g transform="translate({cx},{cy}) rotate({rot}) scale({sx},1)">']
    # forearm
    g.append(f'<path d="M-90,520 L-70,120 Q0,90 70,120 L95,520 Z" fill="{SKIN}" stroke="{OUT}" stroke-width="8" stroke-linejoin="round"/>')
    g.append(f'<rect x="-100" y="330" width="200" height="200" rx="20" fill="#2F3B52" stroke="{OUT}" stroke-width="8"/>')  # sleeve
    if pose == "open":
        g.append(f'<rect x="-85" y="-10" width="170" height="160" rx="60" fill="{SKIN}" stroke="{OUT}" stroke-width="8"/>')
        for i, (fx, fl, fr) in enumerate([(-62, 120, -12), (-22, 145, -4), (18, 140, 4), (56, 110, 12)]):
            g.append(f'<g transform="translate({fx},20) rotate({fr})"><rect x="-19" y="{-fl}" width="38" height="{fl+20}" rx="19" '
                     f'fill="{SKIN}" stroke="{OUT}" stroke-width="7"/></g>')
        g.append(f'<g transform="translate(-80,90) rotate(-55)"><rect x="-20" y="-95" width="40" height="110" rx="20" fill="{SKIN}" stroke="{OUT}" stroke-width="7"/></g>')
        g.append(f'<rect x="-82" y="10" width="164" height="60" rx="30" fill="{SKIN}"/>')
    elif pose in ("fist", "hold"):
        g.append(f'<rect x="-90" y="0" width="180" height="170" rx="55" fill="{SKIN}" stroke="{OUT}" stroke-width="8"/>')
        for i in range(4):
            g.append(f'<rect x="{-88+i*44}" y="-12" width="44" height="70" rx="22" fill="{SKIN}" stroke="{OUT}" stroke-width="7"/>')
        g.append(f'<path d="M-90,60 q-30,-10 -20,-60 q40,10 50,50" fill="{SKIN}" stroke="{OUT}" stroke-width="7"/>')
    elif pose == "point":
        g.append(f'<rect x="-90" y="0" width="180" height="170" rx="55" fill="{SKIN}" stroke="{OUT}" stroke-width="8"/>')
        for i in range(1, 4):
            g.append(f'<rect x="{-88+i*44}" y="-12" width="44" height="70" rx="22" fill="{SKIN}" stroke="{OUT}" stroke-width="7"/>')
        g.append(f'<rect x="-88" y="-190" width="46" height="230" rx="23" fill="{SKIN}" stroke="{OUT}" stroke-width="7"/>')
        g.append(f'<path d="M-90,60 q-30,-10 -20,-60 q40,10 50,50" fill="{SKIN}" stroke="{OUT}" stroke-width="7"/>')
    g.append('</g>')
    return "\n".join(g)

def phone(cx, cy, rot, t_now):
    return f'''<g transform="translate({cx},{cy}) rotate({rot})">
 <rect x="-170" y="-300" width="340" height="600" rx="40" fill="#1C1E24" stroke="{OUT}" stroke-width="8"/>
 <rect x="-150" y="-270" width="300" height="540" rx="26" fill="#2B3A55"/>
 <text x="0" y="-160" font-family="Poppins" font-weight="700" font-size="76" fill="#fff" text-anchor="middle">{t_now}</text>
 <text x="0" y="-110" font-family="Poppins" font-size="26" fill="#C9D3E6" text-anchor="middle">Salı, 25 Kasım</text>
 <rect x="-135" y="-60" width="270" height="150" rx="22" fill="#F4F6FA"/>
 <rect x="-118" y="-42" width="44" height="44" rx="10" fill="#E3262F"/>
 <text x="-62" y="-10" font-family="Poppins" font-weight="700" font-size="22" fill="#222">TAKVİM</text>
 <text x="-118" y="34" font-family="Poppins" font-weight="700" font-size="25" fill="#111">İş görüşmesi</text>
 <text x="-118" y="70" font-family="Poppins" font-size="23" fill="#E3262F">09:30 · 35 dk kaldı</text>
</g>'''

def hands(pose, t, shake=0.0):
    bob = math.sin(t * 2.2) * 10
    jx = math.sin(t * 37) * shake * 14
    jy = math.cos(t * 41) * shake * 10
    if pose == "phone":
        return (hand(330 + jx, 1700 + bob + jy, 18, False, "hold") +
                hand(750 + jx, 1700 + bob + jy, -18, True, "hold") +
                phone(540 + jx, 1500 + bob + jy, 0, "08:55"))
    if pose == "open":
        return hand(170 + jx, 1580 + bob + jy, -14, False, "open") + hand(910 + jx, 1580 + bob + jy, 14, True, "open")
    if pose == "fist":
        return hand(200 + jx, 1640 + bob + jy, -10, False, "fist") + hand(880 + jx, 1640 + bob + jy, 10, True, "fist")
    if pose == "point_left":
        return hand(260 + jx, 1560 + bob, -32, False, "point") + hand(930, 1720 + bob, 12, True, "fist")
    if pose == "point_right":
        return hand(150, 1720 + bob, -12, False, "fist") + hand(820 + jx, 1560 + bob, 32, True, "point")
    return ""

# ---------------------------------------------------------------- UI overlays
def top_banner():
    return f'''<g transform="translate(40,70)">
 <rect x="6" y="8" width="560" height="160" rx="18" fill="#000" opacity="0.25"/>
 <rect x="0" y="0" width="560" height="160" rx="18" fill="#16181D" stroke="#FFC531" stroke-width="5"/>
 <text x="30" y="46" font-family="Poppins" font-weight="700" font-size="26" fill="#FFC531">BÖLÜM 1 · SAAT 08:55</text>
 <text x="30" y="100" font-family="Poppins" font-weight="700" font-size="46" fill="#FFFFFF">İŞ GÖRÜŞMESİ GÜNÜ</text>
 <text x="30" y="140" font-family="Poppins" font-size="26" fill="#C9CED6">Görüşmeye 35 dakika var.</text>
</g>'''

def subtitle(text, y=1180, size=66, pop=1.0):
    lines = text.split("\n")
    s = [f'<g transform="translate(540,{y}) scale({pop})">']
    for i, ln in enumerate(lines):
        yy = (i - (len(lines) - 1) / 2) * (size * 1.15)
        s.append(f'<text x="0" y="{yy:.0f}" font-family="Poppins" font-weight="700" font-size="{size}" text-anchor="middle" '
                 f'fill="#FFD43B" stroke="{OUT}" stroke-width="16" stroke-linejoin="round" paint-order="stroke">{esc(ln)}</text>')
    s.append('</g>')
    return "\n".join(s)

def speech_box(tag, tag_col, text, y=1040, appear=1.0):
    lines = text.split("\n")
    h = 70 + 62 * len(lines)
    op = ease(appear)
    s = [f'<g transform="translate(90,{y + (1-op)*40:.0f})" opacity="{op:.2f}">',
         f'<rect x="0" y="0" width="900" height="{h}" rx="22" fill="#16181D" opacity="0.88" stroke="{tag_col}" stroke-width="6"/>',
         f'<rect x="24" y="-30" width="{40 + 24*len(tag)}" height="58" rx="14" fill="{tag_col}" stroke="{OUT}" stroke-width="5"/>',
         f'<text x="{44 + 12*len(tag)}" y="10" font-family="Poppins" font-weight="700" font-size="32" fill="#16181D" text-anchor="middle">{esc(tag)}</text>']
    for i, ln in enumerate(lines):
        s.append(f'<text x="450" y="{78 + i*62}" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">{esc(ln)}</text>')
    s.append('</g>')
    return "\n".join(s)

def ab_pills(appear=1.0):
    op = ease(appear)
    return f'''<g opacity="{op:.2f}">
 <g transform="translate(40,270)"><rect width="470" height="78" rx="39" fill="#E3262F" stroke="#fff" stroke-width="5"/>
  <text x="235" y="52" font-family="Poppins" font-weight="700" font-size="36" fill="#fff" text-anchor="middle">A · AMCA</text></g>
 <g transform="translate(570,270)"><rect width="470" height="78" rx="39" fill="#2563EB" stroke="#fff" stroke-width="5"/>
  <text x="235" y="52" font-family="Poppins" font-weight="700" font-size="36" fill="#fff" text-anchor="middle">B · OTOBÜS</text></g>
</g>'''

def watermark():
    return ('<text x="1040" y="1890" font-family="Poppins" font-weight="700" font-size="30" fill="#fff" opacity="0.7" '
            f'text-anchor="end" stroke="{OUT}" stroke-width="6" paint-order="stroke">@sonkarar.senin</text>')

# ---------------------------------------------------------------- end card
def end_card(t, world_snapshot):
    """t: seconds since end card start"""
    a1 = ease(t / 0.4)
    a2 = ease((t - 0.3) / 0.4)
    a3 = ease((t - 0.6) / 0.4)
    a4 = ease((t - 1.0) / 0.4)
    pulse = 1 + 0.04 * math.sin(t * 6)
    arrow = 10 * math.sin(t * 7)
    return f'''{world_snapshot}
<rect width="{W}" height="{H}" fill="#14161B" opacity="0.82"/>
<g opacity="{a1:.2f}" transform="translate(540,{330 - (1-a1)*40:.0f})">
 <text x="0" y="0" font-family="Poppins" font-weight="700" font-size="96" fill="#fff" text-anchor="middle">ŞİMDİ NE</text>
 <text x="0" y="110" font-family="Poppins" font-weight="700" font-size="96" fill="#fff" text-anchor="middle">YAPMALIYIM?</text>
</g>
<g opacity="{a2:.2f}">
 <g transform="translate(70,560)">
  <rect width="440" height="440" rx="28" fill="#FCEAEA" stroke="#E3262F" stroke-width="12"/>
  <clipPath id="ca"><rect width="440" height="440" rx="28"/></clipPath>
  <g clip-path="url(#ca)"><rect width="440" height="440" fill="#D8D0C2"/>{old_man(250, 230, 0.75, 1.0)}</g>
  <circle cx="220" cy="0" r="52" fill="#E3262F" stroke="#fff" stroke-width="8"/>
  <text x="220" y="20" font-family="Poppins" font-weight="700" font-size="58" fill="#fff" text-anchor="middle">A</text>
 </g>
 <g transform="translate(570,560)">
  <rect width="440" height="440" rx="28" fill="#E8F0FE" stroke="#2563EB" stroke-width="12"/>
  <clipPath id="cb"><rect width="440" height="440" rx="28"/></clipPath>
  <g clip-path="url(#cb)"><rect width="440" height="440" fill="#4A4E57"/><g transform="translate(-40,-560) scale(0.8)">{bus(100, blink=True)}</g></g>
  <circle cx="220" cy="0" r="52" fill="#2563EB" stroke="#fff" stroke-width="8"/>
  <text x="220" y="20" font-family="Poppins" font-weight="700" font-size="58" fill="#fff" text-anchor="middle">B</text>
 </g>
</g>
<g opacity="{a3:.2f}">
 <g transform="translate(70,1060)"><rect width="940" height="150" rx="24" fill="#E3262F" stroke="#fff" stroke-width="6"/>
  <text x="470" y="64" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">A – Amcaya yardım et,</text>
  <text x="470" y="118" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">iş görüşmesini kaçır!</text></g>
 <text x="540" y="1270" font-family="Poppins" font-weight="700" font-size="40" fill="#FFC531" text-anchor="middle">YA DA</text>
 <g transform="translate(70,1310)"><rect width="940" height="150" rx="24" fill="#2563EB" stroke="#fff" stroke-width="6"/>
  <text x="470" y="64" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">B – Otobüse bin,</text>
  <text x="470" y="118" font-family="Poppins" font-weight="700" font-size="44" fill="#fff" text-anchor="middle">birinin yardım etmesini um!</text></g>
</g>
<g opacity="{a4:.2f}">
 <g transform="translate(540,1580) scale({pulse:.3f})">
  <text x="0" y="0" font-family="Poppins" font-weight="700" font-size="58" fill="#FFD43B" text-anchor="middle" stroke="{OUT}" stroke-width="12" paint-order="stroke">Yorumlara A veya B yaz!</text>
 </g>
 <text x="540" y="1660" font-family="Poppins" font-size="36" fill="#E6E8EC" text-anchor="middle">En çok oy alan seçenekle devam ediyorum.</text>
 <path transform="translate(540,{1730+arrow:.0f})" d="M-30,0 L30,0 L0,40 Z" fill="#FFD43B" stroke="{OUT}" stroke-width="5"/>
</g>
{watermark()}'''
