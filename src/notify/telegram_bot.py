"""
Telegram bildirim modülü (Gün 1).

@BotFather üzerinden bot oluşturup TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID
değerlerini .env'e ekledikten sonra bu modül doğrudan çalışır.
"""
import requests
from src.config import settings


def send_message(text: str) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        raise RuntimeError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID .env içinde tanımlı değil")

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    resp = requests.post(url, json={"chat_id": settings.telegram_chat_id, "text": text}, timeout=10)
    return resp.ok


if __name__ == "__main__":
    # Gün 1 doğrulama: python -m src.notify.telegram_bot
    ok = send_message("MyAiBroker: Telegram bağlantısı çalışıyor. (Faz 1 / Gün 1)")
    print("Gönderildi" if ok else "Gönderilemedi — token/chat_id kontrol et")
