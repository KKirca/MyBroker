# MyAiBroker

Soğukkanlı, veriye dayalı bir yapay zeka destekli "Wall Street broker" sistemi. İki piyasada, iki farklı karakterle çalışır:

- **BIST (ağırlıklı pay):** uzun vadeli değer yatırımı. Sık al-sat yok; NAV/P/B/borç/makro analizine dayalı, zamanla pozisyon biriktiren (cost averaging) bir yaklaşım.
- **ABD hisseleri:** serbest karakter — tek kriter kârlılık. Kural bazlı, net stop-loss/hedef fiyatlı bir momentum/trend sistemi kullanır (disiplinsiz "her ne işe yararsa" yaklaşımı yerine).

Telegram üzerinden anlık sinyal/risk bildirimleri gönderir; risk yöneticisinden onay almadan hiçbir emir gönderilmez.

> **Durum:** Faz 0 — İskelet (scaffold) aşaması. Bu repo, `ROADMAP.md` dosyasındaki 14 günlük plana göre adım adım doldurulacak. Henüz gerçek para ile çalışmıyor.

## Ne yapıyor?

1. **Veri toplama** — Alpaca (ABD hisseleri) ve İş Yatırım AlgoLab veya alternatif bir kaynak (BIST) üzerinden fiyat/hacim verisi çeker.
2. **Sinyal motorları:**
   - `signals/bist_value_engine.py` — NAV iskontosu, P/B, borç trendi üzerinden bir değer skoru üretir (bkz. proje geçmişindeki Bakırcı GYO IPO analiz metodolojisi).
   - `signals/us_momentum_engine.py` — teknik indikatörlere (RSI/MACD/SMA) dayalı, net stop-loss/hedefli bir momentum sinyali üretir.
   - `signals/persona_engine.py` — her iki motorun çıktısını, Claude API ile "deneyimli broker" persona'sının BUY/HOLD/SELL/WATCH kararına ve risk/ödül yorumuna çevirir; ton asset class'a göre değişir (BIST: sabırlı/uzun vade, ABD: aktif/kısa-orta vade).
3. **Risk yöneticisi** (`src/risk/risk_manager.py`) — iki ayrı rejim uygular:
   - ABD: pozisyon tavanı + zorunlu stop-loss + günlük maksimum zarar kill-switch'i.
   - BIST: stop-loss yok; bunun yerine aylık bir "biriktirme bütçesi" tavanı.
4. **Bildirim** — Telegram bot üzerinden anlık push bildirimi.
5. **Emir yürütme** — ABD: önce paper (Alpaca), sonra küçük sermayeli canlı. BIST: varsayılan `signal_only` (bot önerir, sen/onaylı komut tetikler) — seyrek işlem sıklığı zaten tam otomasyonun getirisini düşürüyor.

## Mimari

```
src/
  data/        -> Alpaca (ABD) / BIST veri çekme modülleri
  signals/     -> bist_value_engine, us_momentum_engine, persona_engine (Claude)
  risk/        -> asset-class'a duyarlı risk yöneticisi (ABD: stop-loss, BIST: aylık bütçe)
  execution/   -> borsa/aracı kurum API'lerine emir gönderme (paper + live)
  notify/      -> Telegram bot entegrasyonu
tests/         -> risk yöneticisi birim testleri (7/7 geçiyor)
```

## Kurulum

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # API anahtarlarını ve BIST/ABD dağılımını doldur
python -m src.main
```

## Risk Bildirimi

Bu yazılım yatırım tavsiyesi değildir. Otomatik emir yürütme modülleri gerçek sermaye kaybına yol açabilir. BIST'te büyük pay ayırmak, TL bazlı enflasyon/devalüasyon riskine yoğunlaşmak anlamına gelir — getiriyi hem TL hem USD bazında takip edin. `risk/risk_manager.py` içindeki limitler devre dışı bırakılmadan canlıya alınmamalıdır. Geliştirici (proje sahibi), sistemi kullanmadan önce ilgili piyasaların (BIST, ABD) düzenleyici kurallarını ve aracı kurum API kullanım şartlarını kendisi doğrulamakla yükümlüdür.

## Lisans

MIT — bkz. `LICENSE`.
