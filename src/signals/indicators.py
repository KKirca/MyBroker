"""
Teknik analiz indikatörleri (Gün 5).

TODO: `ta` kütüphanesi ile RSI, MACD, SMA/EMA ve hacim anomalisi hesapla.
Girdi: pandas DataFrame (kolonlar: open, high, low, close, volume).
Çıktı: aynı DataFrame + indikatör kolonları.
"""
import pandas as pd


def add_core_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO (Gün 5): ta.momentum.RSIIndicator, ta.trend.MACD,
    ta.trend.SMAIndicator ekle. Şimdilik placeholder.
    """
    raise NotImplementedError("Gün 5: teknik indikatörler eklenecek")
