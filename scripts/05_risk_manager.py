import matplotlib.pyplot as plt
import numpy as np


def calculate_position_size(portfolio, risk_pct, entry, stop_loss):
    risk_amount = portfolio * (risk_pct / 100)
    risk_per_share = abs(entry - stop_loss)
    if risk_per_share == 0:
        return None
    quantity = int(risk_amount / risk_per_share)
    total_inv = quantity * entry
    return {
        "quantity": quantity,
        "total_inv": total_inv,
        "risk_amount": risk_amount,
        "portfolio_pct": (total_inv / portfolio) * 100,
    }


def plot_risk_scenarios():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Risk Yonetimi Senaryolari", fontsize=13, fontweight="bold")

    portfolio = 100_000
    risk_pcts = np.linspace(0.5, 5, 50)
    max_losses = [portfolio * (r / 100) for r in risk_pcts]

    axes[0].fill_between(risk_pcts, 0, max_losses, alpha=0.3, color="red")
    axes[0].plot(risk_pcts, max_losses, color="red", lw=2)
    axes[0].axvline(1, color="green", ls="--", lw=1.5, label="Onerilen: %1")
    axes[0].axvline(2, color="orange", ls="--", lw=1.5, label="Maksimum: %2")
    axes[0].set_xlabel("Risk Yuzdesi (%)")
    axes[0].set_ylabel("Maksimum Kayip (TRY)")
    axes[0].set_title("Risk % -> Maksimum Kayip")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    starting = 100_000
    scenarios = {"%1 risk": 1, "%2 risk": 2, "%5 risk": 5}
    colors = ["green", "orange", "red"]

    for (label, risk), color in zip(scenarios.items(), colors):
        capital = starting
        history = [capital]
        for _ in range(20):
            capital -= capital * (risk / 100)
            history.append(capital)
        pct_left = (history[-1] / starting) * 100
        axes[1].plot(history, color=color, lw=2, label=f"{label} -> %{pct_left:.0f} kaldi")

    axes[1].axhline(starting, color="black", ls=":", alpha=0.5)
    axes[1].set_xlabel("Pes Pese Kaybeden Islem Sayisi")
    axes[1].set_ylabel("Kalan Sermaye (TRY)")
    axes[1].set_title("20 Kaybeden Islem Sonrasi Sermaye")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("charts/risk_scenarios.png", dpi=120, bbox_inches="tight")
    plt.close()
    print("  Grafik: charts/risk_scenarios.png")


if __name__ == "__main__":
    print("POSITION SIZING ORNEKLERI\n")

    portfolio = 100_000
    entry = 10.50
    stop_loss = 10.00

    for risk_pct in [0.5, 1.0, 2.0]:
        result = calculate_position_size(portfolio, risk_pct, entry, stop_loss)
        if result:
            print(f"Risk %{risk_pct:.1f}:")
            print(f"  Alinacak Lot   : {result['quantity']:,}")
            print(f"  Toplam Yatirim : {result['total_inv']:,.2f} TRY")
            print(f"  Max Kayip      : {result['risk_amount']:,.2f} TRY")
            print(f"  Portfoy %      : %{result['portfolio_pct']:.1f}")
            print()

    plot_risk_scenarios()
