import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.analysis_agent import AnalysisAgent
from agents.base_agent import BaseAgent
from agents.data_agent import DataAgent
from agents.signal_agent import SignalAgent


class OrchestratorAgent(BaseAgent):
    SYMBOLS = ["YKBNK.IS", "AKBNK.IS", "GARAN.IS"]

    def __init__(self, db_path="data/trading.db"):
        super().__init__("OrchestratorAgent")
        self.data_agent = DataAgent(db_path)
        self.analysis_agent = AnalysisAgent(db_path)
        self.signal_agent = SignalAgent()

    def run(self, fetch_fresh=False):
        self.status = "running"
        self.log("Pipeline basliyor...")

        if fetch_fresh:
            self.log("Adim 1: Taze veri cekiliyor")
            self.data_agent.run(self.SYMBOLS)

        self.log("Adim 2: Teknik analiz")
        analyses = self.analysis_agent.run(self.SYMBOLS)

        self.log("Adim 3: Sinyal uretimi")
        signals = self.signal_agent.run(analyses)

        self.log("Adim 4: Rapor olusturuluyor")
        self._print_report(analyses, signals)
        self._plot_dashboard(analyses, signals)

        self.status = "done"
        return signals

    def _print_report(self, analyses, signals):
        print("\n" + "=" * 60)
        print("AJAN SISTEMI RAPORU")
        print("=" * 60)
        emoji = {"STRONG_BUY": "[++]", "BUY": "[+]", "NEUTRAL": "[ ]", "SELL": "[-]", "STRONG_SELL": "[--]"}

        for symbol, sig in signals.items():
            a = analyses.get(symbol, {})
            tag = emoji.get(sig["signal"], "[ ]")
            print(
                f"{tag} {symbol:14} | {sig['signal']:12} | "
                f"Skor: {sig['score']:6.1f} | "
                f"RSI: {a.get('rsi', 0):5.1f} | "
                f"Fiyat: {a.get('close', 0):7.2f} TRY"
            )
        print("=" * 60)

    def _plot_dashboard(self, analyses, signals):
        symbols = list(signals.keys())
        scores = [signals[s]["score"] for s in symbols]
        colors = ["#4CAF50" if s > 0 else "#F44336" for s in scores]

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle("Ajan Dashboard", fontsize=13, fontweight="bold")

        bars = axes[0].barh(symbols, scores, color=colors, height=0.5)
        axes[0].axvline(0, color="black", lw=1)
        axes[0].axvline(40, color="green", ls="--", alpha=0.5)
        axes[0].axvline(-40, color="red", ls="--", alpha=0.5)
        axes[0].set_xlabel("Sinyal Skoru")
        axes[0].set_title("Guncel Sinyaller")
        axes[0].grid(True, alpha=0.3, axis="x")
        for bar, score in zip(bars, scores):
            axes[0].text(
                score + (1 if score >= 0 else -1),
                bar.get_y() + bar.get_height() / 2,
                f"{score:.1f}",
                va="center",
                fontsize=10,
            )

        rsi_vals = [analyses[s].get("rsi", 50) for s in symbols]
        rsi_colors = []
        for r in rsi_vals:
            if r < 30:
                rsi_colors.append("#4CAF50")
            elif r > 70:
                rsi_colors.append("#F44336")
            else:
                rsi_colors.append("#2196F3")

        axes[1].barh(symbols, rsi_vals, color=rsi_colors, height=0.5)
        axes[1].axvline(30, color="green", ls="--", alpha=0.6, label="Oversold")
        axes[1].axvline(70, color="red", ls="--", alpha=0.6, label="Overbought")
        axes[1].axvline(50, color="gray", ls=":", alpha=0.5)
        axes[1].set_xlabel("RSI Degeri")
        axes[1].set_title("RSI Karsilastirmasi")
        axes[1].set_xlim(0, 100)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis="x")

        plt.tight_layout()
        os.makedirs("charts", exist_ok=True)
        plt.savefig("charts/agent_dashboard.png", dpi=120, bbox_inches="tight")
        plt.close()
        print("  Grafik: charts/agent_dashboard.png")


if __name__ == "__main__":
    orchestrator = OrchestratorAgent()
    signals = orchestrator.run(fetch_fresh=False)
    print("\nAjan pipeline tamamlandi!")
