"""
Alpaca veri akışı (Gün 3). ABD hisseleri için market data + hesap erişimi.
ALPACA_PAPER=true iken paper trading ortamına bağlanır.
"""
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from src.config import settings


def get_data_client() -> StockHistoricalDataClient:
    return StockHistoricalDataClient(settings.alpaca_api_key, settings.alpaca_api_secret)


def get_latest_quote(symbol: str = "AAPL"):
    """TODO (Gün 3): hata yönetimi + retry ekle."""
    client = get_data_client()
    request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
    return client.get_stock_latest_quote(request)
