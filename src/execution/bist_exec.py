"""
BIST emir yürütme (Gün 10 — koşullu).

Kuzey'in BIST için "uzun vadeli değer yatırımı" kararı sonrası bu modülün
varsayılan modu artık `signal_only`: bot sadece Telegram'a bildirim/öneri
gönderir, gerçek işlem kararı ve tetiklemesi kullanıcıda kalır. Seyrek
işlem sıklığı zaten tam otomasyonun getirisini düşürüyor — asıl değer
zamanlı emirde değil, doğru analizde.

`manual_confirm` modunda (ileri faz): Telegram'dan gelen bir onay mesajı
üzerine emir gönderilir. `live` modu (tam otomasyon) ancak haftalarca
signal_only/manual_confirm sonrası, ROADMAP.md Faz 5 kapısından geçtikten
sonra açılmalı.
"""
from src.config import settings
from src.risk.risk_manager import RiskManager, TradeProposal, RiskDecision


def place_order(risk_manager: RiskManager, proposal: TradeProposal) -> RiskDecision:
    if settings.bist_execution_mode == "signal_only":
        return RiskDecision(approved=False, reason="BIST signal_only modda — otomatik emir gönderilmiyor, karar kullanıcıda.")

    decision = risk_manager.evaluate(proposal)
    if not decision.approved:
        return decision

    if settings.bist_execution_mode == "manual_confirm":
        """TODO (ileri faz): Telegram üzerinden onay iste, onaylanırsa devam et."""
        raise NotImplementedError("manual_confirm modu için Telegram onay akışı eklenecek")

    """TODO (Gün 10-11, sadece AlgoLab hazır ve Faz 5 kapısı geçildiyse): AlgoLab emir gönderimi."""
    raise NotImplementedError("live modu: AlgoLab emir gönderimi eklenecek")
