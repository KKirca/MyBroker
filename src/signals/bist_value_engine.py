"""
BIST Değer Yatırımı Motoru (Gün 5).

Kuzey'in kararı: BIST'te al-sat değil, uzun vadeli değer yatırımı karakteri.
Bu motor, `bakirci-gyo-ipo-analysis.md` notundaki metodolojiyi genelleştirir:
NAV (net aktif değer) iskontosu, P/B, borç trendi, ve makro bağlam (TCMB
faizi, enflasyon beklentisi, USD/TRY) üzerinden bir "değer skoru" üretir.

Bu motor SIK sinyal üretmek için tasarlanmadı — haftalık/aylık yeniden
değerlendirme öngörülüyor (bkz. ROADMAP.md Faz 2).
"""
from dataclasses import dataclass


@dataclass
class BistValueSnapshot:
    symbol: str
    price_try: float
    adjusted_nav_per_share_try: float | None   # NAV: şirketin varlıklarının makul değerinden borçlar düşülmüş hali
    price_to_book: float | None                # P/B: hisse fiyatının defter değerine oranı
    net_debt_try: float | None
    net_debt_trend: str | None                 # "azalıyor" | "artıyor" | "bilinmiyor"


@dataclass
class BistValueVerdict:
    symbol: str
    nav_discount_pct: float | None   # pozitif = NAV'a göre iskontolu (ucuz), negatif = primli
    notes: list[str]


def evaluate_value(snapshot: BistValueSnapshot) -> BistValueVerdict:
    """
    TODO (Gün 5): gerçek skorlama mantığını ekle.
    - nav_discount_pct = (adjusted_nav_per_share_try - price_try) / adjusted_nav_per_share_try
    - P/B ve borç trendini notes'a ekle
    - Makro bağlamı (enflasyon/USD-TRY) ayrı bir katman olarak persona_engine'e taşınacak
      (bu motor sadece şirket-özel değer analizini yapar; makro yorum Claude'a bırakılır)
    """
    raise NotImplementedError("Gün 5: BIST değer skorlama mantığı eklenecek")
