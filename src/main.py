"""
MyAiBroker giriş noktası.

Şu an sadece iskelet — Faz 1-4 tamamlandıkça buraya zamanlanmış
(APScheduler ile) iki ayrı döngü eklenecek:
  - BIST döngüsü: düşük frekans (haftalık/aylık) — değer motoru + persona -> Telegram
  - ABD döngüsü: yüksek frekans (günlük/gün içi) — momentum motoru + persona ->
    risk kontrolü -> (varsa) paper/live emir -> Telegram
"""
from src.config import settings
from src.risk.risk_manager import RiskManager


def build_risk_manager() -> RiskManager:
    return RiskManager(
        max_position_size_usd=settings.max_position_size_usd,
        max_daily_loss_usd=settings.max_daily_loss_usd,
        max_bist_monthly_contribution_usd=settings.max_bist_monthly_contribution_usd,
        global_kill_switch=settings.global_kill_switch,
    )


def main() -> None:
    risk_manager = build_risk_manager()
    print(f"MyAiBroker başlatıldı. GLOBAL_KILL_SWITCH={risk_manager.global_kill_switch}")
    print(f"BIST modu: {settings.bist_execution_mode} | Dağılım: BIST %{settings.bist_allocation_pct} / ABD %{settings.us_allocation_pct}")
    # TODO: Faz 1-4 ilerledikçe veri/sinyal/execution modüllerini buraya bağla.


if __name__ == "__main__":
    main()
