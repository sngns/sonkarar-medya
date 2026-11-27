# Son Karar Senin — günlük bölüm üretim hattı

Bu depo, "Son Karar Senin" (Instagram: sonkarar.senin, YouTube Shorts, TikTok) A/B seçimli hikâye serisinin
medya dosyalarını, 3D motorunu ve bölüm kayıtlarını tutar. Sahibi Berkay. Dil: Türkçe.

## Format
- Birinci şahıs (POV) gerçekçi 3D sahne, 1080×1920, ~30 sn. Ekranda sadece ana karakterin elleri görünür.
- Üstte bölüm bandı ("BÖLÜM N · SAAT ..." + başlık), sarı konuşma altyazıları, karakter konuşma kutuları,
  sonda "ŞİMDİ NE YAPMALIYIM?" A (kırmızı) / B (mavi) final ekranı + "Yorumlara A veya B yaz!".
- A/B etiketlerinde MESAFE YAZILMAZ (Berkay istemedi): sadece "A · AMCA" / "B · OTOBÜS" gibi.
- Konular: günlük hayat ikilemleri, vicdan, sosyal ikilem, hayatta kalma/felaket, anlık kararlar (spor vb.).
  Güvenlik içeren konularda (deprem, yangın vb.) doğru davranış sonraki bölümde mutlaka gösterilir.

## Devam kuralı (Berkay ile anlaşıldı)
- Ana hikâye ÇOĞUNLUĞUN seçtiği şıktan devam eder.
- Sonraki bölümün başında ilk ~3 sn: "Geçen bölüm: %X A dedi!" + kısa hatırlatma.
- Kazanan şıkkın sonucu (beklenmedik bir dönüşle), sonra yeni ikilem ve A/B ekranı.
- Azınlık için 5–8 sn'lik "B'yi seçseydin ne olurdu?" kısa sahnesi eklenir.
- Bir hikâye 2–3 bölümde kapanır, sonra yeni hikâye başlar.

## Günlük döngü
- 13:00 (Europe/Istanbul) üretim, 19:00 yayın. Berkay onay vermeden HİÇBİR ŞEY herkese açık yayınlanmaz.
- Yayın: Metricool (blogId 8342778; instagram, tiktok, youtube bağlı). Video için `media` alanına bu deponun
  raw URL'si verilir: https://raw.githubusercontent.com/sngns/sonkarar-medya/main/bolumNN/video.mp4
  - Instagram: instagramData.type = "REEL", kapak videoThumbnailUrl ile.
  - YouTube: youtubeData.type = "short", madeForKids false, kategori ENTERTAINMENT. Kanal doğrulanmadığı için
    videoThumbnailUrl GÖNDERME (tüm gönderi reddedilir) → kapak, videonun İLK KARESİ olarak videoya gömülür.
  - TikTok: tiktokData.isAigc = true (seslendirme yapay zekâ). Hesap kişisel bağlıysa gönderi TikTok'ta
    "AWAITING_CONFIRMATION" durumunda kalır; Berkay'a uygulamadan son "Paylaş"ı yapmasını hatırlat.
  - Onay öncesi gönderi Metricool'da `draft: true` olarak 19:00'a kurulur; Berkay onaylayınca draft:false yapılır.
- Yorum/oy sayımı: Instagram yorumları Windsor.ai (instagram hesabı 17841433706735929) veya Metricool
  analitiği; TikTok/YouTube yorumları erişilebildiği kadar. Hangi kaynağın sayılabildiğini Berkay'a dürüstçe söyle.
- Windsor ile YouTube yüklemesi "rate-limited" hatası verdi; YouTube için Metricool kullan.

## Seslendirme
- ElevenLabs bağlayıcısı, model eleven_v4. Sesler: ana karakter "Naim Işık" (h1meLSDvtheYylUdAmYa),
  yaşlı erkek "Seyfullah Kartal" (mF7tIc9VLrznhGooGjaT), kalın erkek "Bir Pare Sound" (J17lijyP1BHYcM7ld0Rg).
  Ses kimliklerini kullanmadan önce creative_list_voices ile doğrula.
- Ücretsiz kuyruk bazen "busy" döner: aynı turda tekrar deneme; sonraki turda dene.
- Dosyalar elevenlabsusercontent.com'dan indirilir (izinli alan adı). Ana karakter replikleri tek seferde üretilip
  ffmpeg silencedetect ile bölünür.

## 3D motor (motor/)
- three.js 0.170 + puppeteer-core + /usr/bin/google-chrome (swiftshader). `cd motor && npm i`.
- motor/a/: man.glb (iskeletli insan modeli, three.js örnek deposundan), city.hdr (şehir ışığı), tuğla dokuları.
- motor/bolum01_kaynak/: Bölüm 1'in tam kaynağı — çalışan örnek. Yeni bölüm için bu dosyaları kopyala ve
  sahneyi/zaman çizelgesini değiştir:
  - real.html: sahne (sokak, binalar, otobüs, karakterler), `aim/ikArm/placePOV` ile poz ve POV eller,
    `window.renderFrame(t)` zaman çizelgesi (TM objesi), post-process (GTAO, bloom, renk grade).
    Çalıştırırken real.html ile aynı klasörde `a/` olmalı (motor/a'yı kopyala ya da symlink).
  - rframes.mjs: `node rframes.mjs 720 1280 30 0 23 frames` → kareleri üretir (~2.5 sn/kare, ~30 dk).
    Uzun render'ı arka planda çalıştır, ilerlemeyi `ls frames | wc -l` ile izle.
  - overlay.py + scene.py: 2D katmanlar ve final ekranı (rsvg-convert). Final kartları için end_bg.jpg,
    thumb_a.jpg, thumb_b.jpg gerekir (render karelerinden kırp).
  - sfx.py: telifsiz sentetik müzik/efekt bandı.
- Birleştirme: 720p kareler lanczos ile 1080×1920'ye ölçeklenir, overlay bindirilir, final ekranı eklenir,
  sesler yerleştirilip müzik altında kısılır, loudnorm -14 LUFS.
- Karakter kısıtı: tek gerçekçi insan modeli var (man.glb). Farklı karakterler bunun renk/doku varyasyonu.
  Kadın/çocuk gereken hikâyelerden şimdilik kaçın ya da Berkay'a söyle.
- Kontrol: final videodan kare örnekleri al ve gözle bak (eller görünüyor mu, karakterler havada mı, altyazı
  karakterin üstüne biniyor mu).

## Bölüm kayıtları
Her bölüm `bolumNN/` klasöründe: video.mp4, kapak.jpg, meta.json (hikâye, A/B metinleri, gönderi kimlikleri,
oy sonuçları).

## YENİ ÜRETİM HATTI (Bölüm 3 v2'den itibaren — Berkay, 2026-11-26)
- Süre ~60 sn. Stil: Lemo-Opuscar `hd-2d` (2.5D piksel diorama). /video-uretim kuralları: önce storyboard (6–9 kare) → Berkay onayı → render.
- Kaynak şablonu: filmler/bolum03/ (story.js = zaman çizelgesi ve replikler, sets.js = setler, chars.js = piksel karakterler, ui.js = bölüm bandı/diyalog kutusu/oy kartı/seçim menüsü, audio/score.py müzik+efekt, audio/mix.py miks). Yeni bölüm: klasörü kopyala, story.js + sets.js değiştir.
- POV eller yok; A/B ekranı RPG seçim menüsü ("ŞİMDİ NE YAPMALIYIM?" ▶ A/B) + "YORUMLARA A VEYA B YAZ!".
- Komutlar (lemo-opuscar kökünden, PATH başında /home/claude/bin ffmpeg 7):
  still: node core/render/still.mjs <film> <t...> --size 1080x1920 --q ss=1
  test: node <film>/tools/render_range.mjs a b --workers 2 (~0.6 kare/sn)
  tam: node core/render/video.mjs <film> --fps 24 --workers 2 --size 1080x1920 --q ss=1 (~40 dk, arka planda)
  kapak: ?noui=1&ss=2 ile still → `python filmler/make_cover.py still.jpg bolumNN/kapak.jpg N "Başlık" "KANCA 1" "KANCA 2"` → videonun başına 1 kare olarak ekle, ses 42 ms geciktir
  KAPAK KURALI (Berkay): Instagram profil ızgarası ortadaki 1080×1440'ı gösterir (y 240–1680). Başlık, bölüm no ve tüm yazılar bu alanın içinde olmalı; make_cover.py bunu kontrol eder, _grid.jpg önizlemesine bak.
  mux: sh core/render/mux.sh video.mp4 mix.wav final.mp4 24 0  (−14 LUFS)
- Teslim öncesi ZORUNLU kontrol: blackdetect, silencedetect, freezedetect (v1'de 10 sn görüntüsüz/sessiz boşluk hatası olmuştu; parça birleştirme yapma).
