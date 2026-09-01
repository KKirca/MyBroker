"""
Risk yöneticisi testleri — Gün 7-8'de genişletilecek, Gün 14 go-live
kapısının şartlarından biri budur (bkz. ROADMAP.md, Faz 5).
"""
from src.risk.risk_manager import RiskManager, TradeProposal


def make_us_proposal(notional_usd: float = 50.0, stop_loss_pct: float = 0.03) -> TradeProposal:
    return TradeProposal(
        symbol="AAPL",
        asset_class="us_equity",
        side="buy",
        notional_usd=notional_usd,
        stop_loss_pct=stop_loss_pct,
    )


def make_bist_proposal(notional_usd: float = 50.0) -> TradeProposal:
    return TradeProposal(
        symbol="THYAO",
        asset_class="bist",
        side="buy",
        notional_usd=notional_usd,
    )


def make_rm(**overrides) -> RiskManager:
    defaults = dict(max_position_size_usd=100, max_daily_loss_usd=25,
                     max_bist_monthly_contribution_usd=100, global_kill_switch=False)
    defaults.update(overrides)
    return RiskManager(**defaults)


def test_kill_switch_blocks_everything():
    rm = make_rm(global_kill_switch=True)
    decision = rm.evaluate(make_us_proposal())
    assert decision.approved is False
    assert "KILL_SWITCH" in decision.reason


def test_us_position_size_is_capped():
    rm = make_rm()
    decision = rm.evaluate(make_us_proposal(notional_usd=500))
    assert decision.approved is True
    assert decision.adjusted_notional_usd == 100


def test_us_requires_stop_loss():
    rm = make_rm()
    decision = rm.evaluate(make_us_proposal(stop_loss_pct=0))
    assert decision.approved is False
    assert "stop-loss" in decision.reason


def test_us_daily_loss_limit_blocks_new_trades():
    rm = make_rm()
    rm.record_realized_pnl(-30)
    decision = rm.evaluate(make_us_proposal())
    assert decision.approved is False
    assert "zarar limitine" in decision.reason


def test_bist_monthly_budget_is_capped():
    rm = make_rm(max_bist_monthly_contribution_usd=100)
    decision = rm.evaluate(make_bist_proposal(notional_usd=500))
    assert decision.approved is True
    assert decision.adjusted_notional_usd == 100


def test_bist_budget_exhausted_blocks_new_contributions():
    rm = make_rm(max_bist_monthly_contribution_usd=100)
    rm.record_bist_contribution(100)
    decision = rm.evaluate(make_bist_proposal(notional_usd=10))
    assert decision.approved is False
    assert "bütçesi doldu" in decision.reason


def test_bist_has_no_stop_loss_requirement():
    rm = make_rm()
    proposal = make_bist_proposal(notional_usd=20)
    assert proposal.stop_loss_pct == 0.0
    decision = rm.evaluate(proposal)
    assert decision.approved is True
