"""
BIST veri akışı (Gün 4).

Karar noktası: AlgoLab hesabı Gün 4'e kadar hazırsa onun veri akışını
kullan (get_algolab_price). Hazır değilse geçici fallback olarak
yfinance ile ".IS" sembollerinden gecikmeli veri çek (get_fallback_price)
ve BIST_EXECUTION_MODE=signal_only olarak kalsın — bu, otomatik emir
gönderilmediği, sadece Telegram'a bilgi/sinyal gittiği anlamına gelir.
"""
from src.config import settings


def get_algolab_price(symbol: str) -> float:
    """TODO (Gün 4, AlgoLab hesabı hazırsa): AlgoLab API entegrasyonu."""
    raise NotImplementedError("AlgoLab entegrasyonu henüz eklenmedi")


def get_fallback_price(symbol: str) -> float:
    """
    TODO (Gün 4, fallback): yfinance ile `f"{symbol}.IS"` sembolünden
    gecikmeli (real-time olmayan) veri çek. Örn: THYAO -> "THYAO.IS".
    """
    raise NotImplementedError("Fallback veri kaynağı henüz eklenmedi")


def get_bist_price(symbol: str) -> float:
    if settings.bist_execution_mode in ("paper", "live") and settings.algolab_api_key:
        return get_algolab_price(symbol)
    return get_fallback_price(symbol)
