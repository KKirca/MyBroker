"""
Persona motoru (Gün 6) — MyBroker/MyAiBroker projesinin "deneyimli Wall
Street broker" persona'sını Claude API üzerinden nihai sinyale bağlar.

Bu katman, alttaki iki farklı motorun (bist_value_engine, us_momentum_engine)
ham çıktısını alıp asset_class'a göre TONU değiştirir:
  - "bist"      -> uzun vadeli, sabırlı, NAV/makro odaklı yorum; sık al-sat
                    önerisi ÜRETMEZ.
  - "us_equity" -> kısa/orta vadeli, net stop-loss/hedef fiyatlı, aktif yorum.

Her iki durumda da çıktı formatı projenin talimatlarıyla tutarlı:
  BUY (+ hedef fiyat) / HOLD (neden) / SELL (risk faktörleri) /
  WATCH (neden henüz değil) — + risk/ödül profili + karşıt (contrarian) görüş.
"""
from anthropic import Anthropic
from src.config import settings

SYSTEM_PROMPT_BASE = """Sen 25 yıllık deneyime sahip, Berkshire Hathaway
tarzı değer yatırımcısı bir Wall Street bankeri gibi davranan bir sinyal
motorusun. Doğrudan konuş, riski gözden kaçırma ama hesaplı risk almaktan
kaçınma. Her çıktıda: karar (BUY/HOLD/SELL/WATCH), gerekçe, risk/ödül
profili ve varsa karşıt (contrarian) görüş yer almalı."""

ASSET_CLASS_INSTRUCTIONS = {
    "bist": (
        "Bu sembolü UZUN VADELİ DEĞER YATIRIMI bakış açısıyla değerlendir. "
        "NAV iskontosu/primi, P/B, borç trendi ve makro bağlamı (enflasyon, "
        "TCMB faizi, USD/TRY) dikkate al. Kısa vadeli al-sat sinyali üretme; "
        "pozisyon önerini 'zamanla biriktir' (cost averaging) mantığıyla ver. "
        "Getiriyi hem TL hem USD bazında yorumla (enflasyon/devalüasyon riski)."
    ),
    "us_equity": (
        "Bu sembolü kısa/orta vadeli, teknik momentum ve risk/ödül odaklı bir "
        "bakış açısıyla değerlendir. Net bir stop-loss yüzdesi ve hedef fiyat ver."
    ),
}


def generate_signal(symbol: str, asset_class: str, engine_summary: str) -> str:
    """
    TODO (Gün 6): engine_summary (bist_value_engine veya us_momentum_engine
    çıktısının özeti) ile birlikte Claude API'ye gönder, yapılandırılmış
    (BUY/HOLD/SELL/WATCH) bir yanıt al. Şimdilik iskelet.
    """
    if asset_class not in ASSET_CLASS_INSTRUCTIONS:
        raise ValueError(f"Bilinmeyen asset_class: {asset_class}")

    client = Anthropic(api_key=settings.anthropic_api_key)
    system_prompt = SYSTEM_PROMPT_BASE + "\n\n" + ASSET_CLASS_INSTRUCTIONS[asset_class]
    raise NotImplementedError("Gün 6: Claude API çağrısı tamamlanacak")
