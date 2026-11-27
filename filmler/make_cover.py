# Kapak üretici (1080×1920). Tüm yazılar Instagram profil ızgarası güvenli alanında: orta 1080×1440 (y 240–1680), ±50 px pay.
# Kullanım: python make_cover.py <arka_plan.jpg> <çıktı.jpg> <bölüm_no> "<başlık>" "<kanca satır 1>" ["<kanca satır 2>"]
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = '/home/claude/sonkarar-medya/filmler/bolum03/fonts/'
SAFE_T, SAFE_B = 290, 1630
bg, out, ep, title, *hook = sys.argv[1:]
im = Image.open(bg).convert('RGB').resize((1080, 1920)); W, H = im.size
d = ImageDraw.Draw(im, 'RGBA')
for y in range(0, 760): d.line([(0, y), (W, y)], fill=(4, 6, 14, int(225 * (1 - y / 760) ** .8)))
for y in range(1150, H): d.line([(0, y), (W, y)], fill=(4, 6, 14, int(235 * ((y - 1150) / (H - 1150)) ** .8)))
def font(name, size, wght):
    f = ImageFont.truetype(F + name, size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
def ctext(y, t, f, fill, sh=9):
    w = d.textlength(t, font=f); x = (W - w) / 2
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((x, y), t, font=f, fill=(0, 0, 0, 235))
    g = g.filter(ImageFilter.GaussianBlur(sh)); im.paste(g, (0, 0), g); ImageDraw.Draw(im).text((x, y), t, font=f, fill=fill)
    bb = ImageDraw.Draw(im).textbbox((x, y), t, font=f); assert SAFE_T - 50 <= bb[1] and bb[3] <= SAFE_B + 50, (t, bb)
ctext(SAFE_T, f'BÖLÜM {ep}', font('Cinzel.ttf', 50, 600), '#e2c989')
ctext(SAFE_T + 66, title, font('CormorantGaramond-Italic.ttf', 120, 600), '#f6f0e2')
fh = font('Cinzel.ttf', 92, 800); lh = 108
y0 = SAFE_B - 80 - lh * len(hook)
for i, L in enumerate(hook): ctext(y0 + i * lh, L, fh, '#ffd88a')
ctext(SAFE_B - 70, 'Son karar senin: A mı, B mi?', font('CormorantGaramond-Italic.ttf', 58, 600), '#f3ead6')
im.save(out, quality=92)
# önizleme: profil ızgarası kırpımı
im.crop((0, 240, 1080, 1680)).resize((300, 400)).save(out.replace('.jpg', '_grid.jpg'))
print('ok', out)
