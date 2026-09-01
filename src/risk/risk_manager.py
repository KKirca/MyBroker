"""
Risk yöneticisi — MyAiBroker'ın "fren sistemi".

Kural: execution/ katmanındaki hiçbir modül, bu sınıftan onay almadan
borsaya emir göndermez. Bu dosya proje boyunca en çok test edilmesi
gereken dosyadır (bkz. tests/test_risk_manager.py, Gün 7-8, Gün 14 go-live
kapısı).

İki farklı karakter, iki farklı risk mantığı:
- "us_equity": aktif, stop-loss'lu tarz. Pozisyon tavanı + günlük maksimum
  zarar kill-switch'i var (Kuzey: "karakter önemsiz, kâr etsin" — ama
  disiplin için stop-loss zorunlu tutuluyor).
- "bist": uzun vadeli değer yatırımı. Stop-loss mantığı YOK — bunun
  yerine aylık bir "biriktirme bütçesi" (cost averaging) tavanı var.
"""
from dataclasses import dataclass
from datetime import date


@dataclass
class TradeProposal:
    symbol: str
    asset_class: str          # "us_equity" | "bist"
    side: str                 # "buy" | "sell"
    notional_usd: float
    stop_loss_pct: float = 0.0   # sadece "us_equity" için zorunlu


@dataclass
class RiskDecision:
    approved: bool
    reason: str
    adjusted_notional_usd: float = 0.0


class RiskManager:
    def __init__(self, max_position_size_usd: float, max_daily_loss_usd: float,
                 max_bist_monthly_contribution_usd: float, global_kill_switch: bool):
        self.max_position_size_usd = max_position_size_usd
        self.max_daily_loss_usd = max_daily_loss_usd
        self.max_bist_monthly_contribution_usd = max_bist_monthly_contribution_usd
        self.global_kill_switch = global_kill_switch

        self._daily_realized_pnl_usd = 0.0
        self._pnl_reset_date = date.today()

        self._bist_month_spent_usd = 0.0
        self._bist_month_key = (date.today().year, date.today().month)

    def _roll_daily_window(self) -> None:
        if date.today() != self._pnl_reset_date:
            self._daily_realized_pnl_usd = 0.0
            self._pnl_reset_date = date.today()

    def _roll_monthly_window(self) -> None:
        key = (date.today().year, date.today().month)
        if key != self._bist_month_key:
            self._bist_month_spent_usd = 0.0
            self._bist_month_key = key

    def record_realized_pnl(self, pnl_usd: float) -> None:
        self._roll_daily_window()
        self._daily_realized_pnl_usd += pnl_usd

    def _evaluate_us_equity(self, proposal: TradeProposal) -> RiskDecision:
        self._roll_daily_window()

        if self._daily_realized_pnl_usd <= -abs(self.max_daily_loss_usd):
            return RiskDecision(approved=False, reason="Günlük maksimum zarar limitine ulaşıldı — bugün için ABD emirleri durduruldu.")

        if proposal.side == "buy" and proposal.stop_loss_pct <= 0:
            return RiskDecision(approved=False, reason="ABD pozisyonları için stop-loss yüzdesi zorunlu (disiplin kuralı) — belirtilmedi.")

        capped_notional = min(proposal.notional_usd, self.max_position_size_usd)
        if capped_notional <= 0:
            return RiskDecision(approved=False, reason="Pozisyon büyüklüğü sıfır veya negatif.")

        return RiskDecision(approved=True, reason="Onaylandı (ABD — aktif tarz).", adjusted_notional_usd=capped_notional)

    def _evaluate_bist(self, proposal: TradeProposal) -> RiskDecision:
        self._roll_monthly_window()

        if proposal.side == "sell":
            # Uzun vadeli tarzda satış nadir olmalı; risk yöneticisi engellemez
            # ama persona motorunun gerekçe sunması beklenir (bkz. Gün 5-6).
            return RiskDecision(approved=True, reason="BIST satış onaylandı (uzun vadeli tarzda istisnai olmalı).",
                                 adjusted_notional_usd=proposal.notional_usd)

        remaining_budget = self.max_bist_monthly_contribution_usd - self._bist_month_spent_usd
        if remaining_budget <= 0:
            return RiskDecision(approved=False, reason="Bu ayki BIST biriktirme bütçesi doldu — yeni alım ay sonuna kadar durduruldu.")

        capped_notional = min(proposal.notional_usd, remaining_budget)
        return RiskDecision(approved=True, reason="Onaylandı (BIST — uzun vadeli biriktirme).", adjusted_notional_usd=capped_notional)

    def record_bist_contribution(self, spent_usd: float) -> None:
        self._roll_monthly_window()
        self._bist_month_spent_usd += spent_usd

    def evaluate(self, proposal: TradeProposal) -> RiskDecision:
        if self.global_kill_switch:
            return RiskDecision(approved=False, reason="GLOBAL_KILL_SWITCH aktif — hiçbir gerçek emir gönderilmiyor.")

        if proposal.asset_class == "us_equity":
            return self._evaluate_us_equity(proposal)
        elif proposal.asset_class == "bist":
            return self._evaluate_bist(proposal)
        else:
            return RiskDecision(approved=False, reason=f"Bilinmeyen asset_class: {proposal.asset_class}")
