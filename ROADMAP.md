# MyAiBroker — 14 Günlük Yol Haritası (v2 — kripto çıkarıldı)

Başlangıç: **2026-09-01** · Hedef go-live tarihi: **2026-09-14** · Değerlendirme: **2026-09-15**

**v2 kapsam güncellemesi (2026-09-01):** Kripto tamamen kaldırıldı. Sadece BIST (ağırlıklı pay, uzun vadeli değer yatırımı karakteri) ve ABD hisseleri (serbest karakter, tek kriter kârlılık). Gerekçe ve risk/ödül tartışması: proje dokümanı `myaibroker-roadmap.md` (Cowork projesi) ve sohbet geçmişi.

Kural: Her kutuyu, o günün işi bitince işaretle (`- [ ]` → `- [x]`). GitHub'da bu dosya repo kök dizininde durursa ilerleme herkese (ve sana) görünür kalır. Gerçek zamanlı "tık tık" deneyimi istiyorsan aynı maddeleri bir **GitHub Projects (Kanban) board**'una da issue olarak açabilirsin — checkbox'lar orada tıklanabilir.

---

## Faz 0 — Kurulum (Gün 0, bugün)

- [ ] GitHub repo oluştur (`myaibroker`), bu iskeleti push'la
- [ ] Telegram bot oluştur (@BotFather) → `TELEGRAM_BOT_TOKEN` al
- [ ] Alpaca hesabı aç, paper trading API anahtarı al (canlı hesap onayı günler sürebilir — bugün başvur ki Gün 9'da hazır olsun)
- [ ] İş Yatırım (veya AlgoLab destekleyen başka bir aracı kurum) hesabı için başvuru başlat — KYC süresi riski var, en erken günde başlatılmalı (BIST varsayılan modu zaten `signal_only`, bu yüzden hesap gecikirse proje bloklanmaz)
- [ ] Anthropic API anahtarı al
- [ ] `.env` dosyasını doldur (asla commit etme — `.gitignore` içinde zaten var), `BIST_ALLOCATION_PCT` / `US_ALLOCATION_PCT` değerlerini kendi tercihine göre ayarla

## Faz 1 — Veri + Bildirim İskeleti (Gün 1-3)

- [ ] **Gün 1:** Telegram bot "merhaba dünya" — bot sana manuel tetiklenen bir test mesajı göndersin
- [ ] **Gün 2:** Alpaca'dan canlı fiyat çekme (`src/data/alpaca_feed.py`) çalışır durumda
- [ ] **Gün 3:** BIST fiyat verisi — AlgoLab hesabı hazırsa onun veri akışı, değilse geçici/ücretsiz bir kaynak (ör. Yahoo Finance `.IS` sembolleri) ile başla

## Faz 2 — Sinyal Motorları (Gün 4-8)

- [ ] **Gün 4:** Teknik indikatör modülü (`src/signals/indicators.py`) — RSI, MACD, hareketli ortalama, hacim anomalisi (ABD motoru için altyapı)
- [ ] **Gün 5:** BIST değer motoru (`src/signals/bist_value_engine.py`) — NAV iskontosu, P/B, borç trendi skorlaması. Referans: proje geçmişindeki Bakırcı GYO IPO analiz metodolojisi
- [ ] **Gün 6:** ABD momentum motoru (`src/signals/us_momentum_engine.py`) + persona motoru entegrasyonu (`src/signals/persona_engine.py`) — asset class'a göre ton değişimi (BIST: sabırlı/uzun vade, ABD: aktif/net stop-loss)
- [ ] **Gün 7:** Risk yöneticisi (`src/risk/risk_manager.py`) — ABD: pozisyon tavanı + stop-loss + günlük zarar kill-switch; BIST: aylık biriktirme bütçesi tavanı
- [ ] **Gün 8:** Uçtan uca entegrasyon testi — birkaç BIST + birkaç ABD sembolü için sinyal → risk kontrolü → Telegram bildirimi (hepsi paper/simülasyon)

## Faz 3 — Emir Yürütme (Gün 9-11)

- [ ] **Gün 9:** Alpaca **paper** hesabı üzerinden ABD için otomatik emir gönderme, risk yöneticisinden geçerek
- [ ] **Gün 10:** BIST için karar noktası: varsayılan `signal_only` kalır (bot önerir, sen tetiklersin); AlgoLab hazır ve isteğe bağlıysa `manual_confirm` modunu dene
- [ ] **Gün 11:** Tampon/backtest günü — son 30-90 günlük veriyle ABD momentum motorunun sanity check'i, BIST değer motorunun geçmiş NAV/fiyat verisiyle geriye dönük tutarlılık kontrolü

## Faz 4 — Sağlamlaştırma (Gün 12-13)

- [ ] **Gün 12:** Hata yönetimi + loglama + "bot çöktü" uyarı mekanizması (health-check → Telegram)
- [ ] **Gün 13:** README/mimari diyagram/risk bildirimi son hali; GitHub Projects board'unu bu checklist ile senkronize et

## Faz 5 — Go-Live Kapısı (Gün 14)

**Kural:** Aşağıdaki koşullar sağlanmadan `GLOBAL_KILL_SWITCH=false` yapılmaz:

- [ ] Risk yöneticisi testleri (`tests/test_risk_manager.py`) yeşil
- [ ] En az 5 günlük ABD paper trading kaydı var ve kill-switch en az bir kez gerçekten devreye girip pozisyonu kapattığı test edildi
- [ ] BIST değer motoru en az bir tam döngü (veri çek → skor → persona yorumu) hatasız tamamladı

**Kademeli canlıya geçiş (önerilen):**

- [ ] ABD bacağını küçük ve sabit bir sermaye tavanıyla (ör. $50-100) canlıya al
- [ ] BIST bacağını `signal_only` (veya en fazla `manual_confirm`) modunda tut — uzun vadeli karakteri zaten tam otomasyon gerektirmiyor, asıl değer doğru analizde
- [ ] `v1.0` tag'i at, GitHub release notu yaz

---

## Bütçe Notu

Aylık $10-30 bandı: Alpaca ve AlgoLab'ın kendisi ücretsizdir — bütçe küçük bir VPS/sunucu (bot 7/24 çalışsın diye, ~$5-10/ay) ve kullanım bazlı Claude API maliyetine (muhtemelen aylık birkaç dolar, bu ölçekte) gitmeli. BIST için ayrı, ücretli bir üçüncü parti veri aboneliği (Foreks/Matriks gibi) genelde bu bütçeyi aşar — bu yüzden plan, BIST verisini aracı kurumun kendi (bedava) veri akışından almayı öngörüyor.

## Bilinen Riskler / Blokajlar

| Risk | Etki | Azaltma |
|---|---|---|
| Alpaca canlı hesap onayı gecikir | ABD bacağı Gün 14'te live olamaz | Hesabı Gün 0'da aç, gecikirse ABD bacağı paper'da kalır |
| AlgoLab/BIST hesap KYC süreci uzar | BIST otomasyonu gecikir | Varsayılan zaten `signal_only` — proje bloklanmaz, sadece elle işlem yaparsın |
| BIST'e ağırlıklı sermaye = TL/enflasyon riski yoğunlaşması | Nominal kazanç, reel kayıp olabilir | Getiriyi TL + USD bazında raporla, makro bağlamı persona yorumuna dahil et |
| "ABD'de karakter önemsiz, kâr etsin" disiplinsiz uygulanırsa | Gürültüyü sinyal sanma, aşırı risk | Kural bazlı momentum sistemi + zorunlu stop-loss (risk yöneticisi bunu zorunlu kılıyor) |
| Kod hatası risk yöneticisini bypass eder | Gerçek sermaye kaybı | Kill-switch varsayılan `true`; canlıya geçiş kod incelemesi + testle şartlı |
