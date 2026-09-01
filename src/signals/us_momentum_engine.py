"""
ABD Aktif/Momentum Motoru (Gün 6).

Kuzey'in talimatı: ABD tarafında karakter önemsiz, tek kriter kâr. Claude'un
önerisi: disiplinsiz "her ne işe yararsa" yaklaşımı yerine kural bazlı,
net stop-loss ve hedef fiyatlı bir trend/momentum sistemi (RSI + MACD +
hareketli ortalama kesişimi, bkz. indicators.py). Hiçbir yöntem kâr garantisi
vermez — bu motorun amacı rastgele gürültüyü değil, tanımlı ve test
edilebilir bir kenarı (edge) takip etmektir.
"""
from dataclasses import dataclass


@dataclass
class MomentumSignal:
    symbol: str
    direction: str            # "long" | "flat" | "short" (short: Faz sonrası, v1'de kullanılmıyor)
    suggested_stop_loss_pct: float
    suggested_target_pct: float
    confidence_notes: list[str]


def evaluate_momentum(indicator_row) -> MomentumSignal:
    """
    TODO (Gün 6): indicators.add_core_indicators() çıktısındaki RSI/MACD/SMA
    kolonlarını kullanarak bir yön (direction) ve risk/ödül (stop-loss,
    hedef) öner. Örn. kural: SMA(20) > SMA(50) ve RSI 40-65 bandındaysa
    "long", MACD histogramı negatife dönerse "flat".
    """
    raise NotImplementedError("Gün 6: ABD momentum kural seti eklenecek")
