<div align="center">

# 📈 Multi-Agent Trading System

**A multi-agent algorithmic-trading research prototype for Borsa İstanbul (BIST) equities —
from market data to technical analysis, signals, risk sizing, and backtesting.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![matplotlib](https://img.shields.io/badge/matplotlib-11557C?style=flat-square)
![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/status-research%20prototype-orange?style=flat-square)

</div>

> ⚠️ **Disclaimer / Feragatname:** This is an **educational research project**. It does **not** place real orders and is **not** financial advice.
> *Bu bir eğitim/araştırma projesidir; gerçek emir göndermez ve yatırım tavsiyesi değildir.*

---

## 📌 Overview

A modular pipeline that turns raw price data into ranked trading signals, wrapped in a small
**multi-agent architecture**. Each stage is an independent agent sharing a common `BaseAgent`
contract (logging + status), coordinated by an `OrchestratorAgent`.

It was built as a *learn-by-building* project, so the repo also ships a detailed, phase-by-phase
Turkish guide — [`TRADING_SYSTEM_GUIDE.md`](TRADING_SYSTEM_GUIDE.md) — that walks through the
logic and the math behind every step.

## 🏗️ Architecture

```
                 ┌──────────────────── OrchestratorAgent ────────────────────┐
  yfinance  ──▶  │  DataAgent  ──▶  AnalysisAgent  ──▶  SignalAgent           │  ──▶  signals
   (BIST)        │  (SQLite)        (RSI/MACD/BB)       (composite score)     │        + charts
                 └────────────────────────────────────────────────────────────┘
```

- **`DataAgent`** — downloads OHLCV data via `yfinance` and stores it in SQLite (`data/trading.db`).
- **`AnalysisAgent`** — computes **RSI(14)**, **MACD(12/26/9)**, **Bollinger Bands(20, 2σ)**, and **SMA20/50**.
- **`SignalAgent`** — blends the indicators into a **−100 … +100** score → `STRONG_BUY / BUY / HOLD / SELL / STRONG_SELL`.
- **`OrchestratorAgent`** — runs the whole pipeline, prints a report, and saves a matplotlib dashboard.

## ✅ What's implemented

- 📥 Market-data ingestion (yfinance → SQLite)
- 📊 Technical indicators: RSI, MACD, Bollinger Bands, SMA
- 🎯 Composite signal scoring with tunable thresholds
- 🛡️ Risk management: position sizing from account risk % + stop-loss distance
- ⏮️ Backtesting engine: commission, slippage, stop-loss & take-profit, equity curve
- 🧩 Multi-agent orchestration with shared logging/status
- ✅ Unit tests (`pytest`) + `pre-commit` hooks

## 🧭 Roadmap (not yet built)

- [ ] Interactive web dashboard (Plotly + Flask/Streamlit)
- [ ] Broker API integration for paper / live trading
- [ ] Strategy configuration & parameter optimization
- [ ] Portfolio-level backtesting across multiple symbols

## 🛠️ Tech Stack

`Python` · `pandas` · `numpy` · `yfinance` · `SQLite` · `matplotlib` · `scikit-learn` · `pytest` · `pre-commit`

## 📂 Project Structure

```
agents/     base_agent · data_agent · analysis_agent · signal_agent · orchestrator
scripts/    01_fetch_data → 06_backtesting   (standalone, step-by-step)
tests/      pytest suite
TRADING_SYSTEM_GUIDE.md   detailed Turkish build guide
```

## 🚀 Quick Start

```bash
# 1) install core dependencies
pip install yfinance pandas numpy matplotlib scikit-learn pytest

# 2) fetch market data into SQLite (data/trading.db)
python scripts/01_fetch_data.py

# 3) run the full agent pipeline: analysis → signals → dashboard
python -m agents.orchestrator

# explore individual stages
python scripts/03_technical_analysis.py
python scripts/06_backtesting.py

# run the tests
pytest
```

> First run? The orchestrator reads data already stored in `data/trading.db`.
> Fetch it first (step 2), or set `fetch_fresh=True` in the orchestrator's `__main__` block.

Default watchlist (BIST banks): `YKBNK.IS`, `AKBNK.IS`, `GARAN.IS` — edit `OrchestratorAgent.SYMBOLS` to change it.

## 🧮 How signals are scored

Each indicator casts a weighted vote, and the votes are averaged into a single score:

| Indicator | Bullish (buy) | Bearish (sell) |
|-----------|---------------|----------------|
| **RSI**   | `< 30` (oversold) | `> 70` (overbought) |
| **MACD**  | above signal line | below signal line |
| **Bollinger position** | near the lower band | near the upper band |

The averaged score maps to the final label, e.g. `≥ 60 → STRONG_BUY`, `≤ −60 → STRONG_SELL`.

---

<div align="center">
<sub>⚠️ Educational project — not investment advice. Trading carries risk of loss.</sub>
</div>
