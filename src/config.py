"""
Merkezi konfigürasyon yükleyici.
.env dosyasındaki tüm ayarları tek bir yerden okur, geri kalan modüller
buradan import eder — API anahtarları kod içinde asla hardcode edilmez.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Claude
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Alpaca (ABD hisseleri)
    alpaca_api_key: str = os.getenv("ALPACA_API_KEY", "")
    alpaca_api_secret: str = os.getenv("ALPACA_API_SECRET", "")
    alpaca_paper: bool = os.getenv("ALPACA_PAPER", "true").lower() == "true"

    # BIST / AlgoLab
    algolab_username: str = os.getenv("ALGOLAB_USERNAME", "")
    algolab_password: str = os.getenv("ALGOLAB_PASSWORD", "")
    algolab_api_key: str = os.getenv("ALGOLAB_API_KEY", "")
    bist_execution_mode: str = os.getenv("BIST_EXECUTION_MODE", "signal_only")

    # Sermaye dağılımı (bilgi amaçlı)
    bist_allocation_pct: float = float(os.getenv("BIST_ALLOCATION_PCT", "65"))
    us_allocation_pct: float = float(os.getenv("US_ALLOCATION_PCT", "35"))

    # ABD risk limitleri — aktif, stop-loss'lu tarz
    max_position_size_usd: float = float(os.getenv("MAX_POSITION_SIZE_USD", "100"))
    max_daily_loss_usd: float = float(os.getenv("MAX_DAILY_LOSS_USD", "25"))

    # BIST risk limiti — uzun vadeli biriktirme tarzı
    max_bist_monthly_contribution_usd: float = float(os.getenv("MAX_BIST_MONTHLY_CONTRIBUTION_USD", "100"))

    # Bu kod içinde asla ezilmemeli (override edilmemeli)
    global_kill_switch: bool = os.getenv("GLOBAL_KILL_SWITCH", "true").lower() == "true"


settings = Settings()
