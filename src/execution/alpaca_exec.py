"""
Alpaca emir yürütme (Gün 10). Her çağrı önce RiskManager.evaluate()
onayından geçmek ZORUNDADIR.
"""
from src.risk.risk_manager import RiskManager, TradeProposal, RiskDecision


def place_order(risk_manager: RiskManager, proposal: TradeProposal) -> RiskDecision:
    decision = risk_manager.evaluate(proposal)
    if not decision.approved:
        return decision

    """TODO (Gün 10): alpaca-py TradingClient ile paper hesapta emir gönder."""
    raise NotImplementedError("Gün 10: Alpaca emir gönderimi eklenecek")
