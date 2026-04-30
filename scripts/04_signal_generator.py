import sqlite3

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def score_rsi(rsi):
    if pd.isna(rsi):
        return 0
    if rsi < 20:
        return 100
    if rsi < 30:
        return 80
    if rsi < 40:
        return 40
    if rsi < 50:
        return 10
    if rsi < 60:
        return -10
    if rsi < 70:
        return -40
    if rsi < 80:
        return -80
    return -100


def score_macd(macd, signal, histogram):
    if pd.isna(macd):
        return 0
    score = 0
    if macd > signal:
        score += 40
    if histogram > 0:
        score += 60
    return max(-100, min(100, score if macd > signal else -score))


def score_bollinger(close, upper, lower, mid):
    if pd.isna(upper) or (upper - lower) == 0:
        return 0
    pos = (close - lower) / (upper - lower)
    if pos < 0.1:
        return 100
    if pos < 0.25:
        return 60
    if pos < 0.4:
        return 20
    if pos < 0.6:
        return 0
    if pos < 0.75:
        return -20
    if pos < 0.9:
        return -60
    return -100


def score_moving_average(close, sma20, sma50):
    score = 0
    if not pd.isna(sma20) and close > sma20:
        score += 25
    if not pd.isna(sma50) and close > sma50:
        score += 35
    if not pd.isna(sma20) and not pd.isna(sma50) and sma20 > sma50:
        score += 40
    return score - 50


def generate_signals_for_df(df):
    results = []
    for _, row in df.iterrows():
        rsi_s = score_rsi(row.get("rsi", np.nan))
        macd_s = score_macd(row.get("macd", np.nan), row.get("macd_signal", np.nan), row.get("macd_hist", np.nan))
        bb_s = score_bollinger(row["close"], row.get("bb_upper", np.nan), row.get("bb_lower", np.nan), row.get("bb_mid", np.nan))
        ma_s = score_moving_average(row["close"], row.get("sma20", np.nan), row.get("sma50", np.nan))

        avg = np.mean([rsi_s, macd_s, bb_s, ma_s])

        if avg >= 75:
            sig = "STRONG_BUY"
        elif avg >= 40:
            sig = "BUY"
        elif avg <= -75:
            sig = "STRONG_SELL"
        elif avg <= -40:
            sig = "SELL"
        else:
            sig = "NEUTRAL"

        results.append({"score": round(avg, 2), "signal": sig, "rsi_score": rsi_s, "macd_score": macd_s, "bb_score": bb_s, "ma_score": ma_s})

    return pd.DataFrame(results, index=df.index)


def plot_signals(symbol, df, signals):
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True, gridspec_kw={"height_ratios": [3, 1.5, 1]})
    fig.suptitle(f"Sinyal Analizi: {symbol}", fontsize=14, fontweight="bold")

    axes[0].plot(df.index, df["close"], color="#1565C0", lw=1.2, label="Kapanis")
    axes[0].fill_between(df.index, df["bb_lower"], df["bb_upper"], alpha=0.1, color="gray")

    buy_idx = signals[signals["signal"].isin(["BUY", "STRONG_BUY"])].index
    sell_idx = signals[signals["signal"].isin(["SELL", "STRONG_SELL"])].index

    axes[0].scatter(buy_idx, df.loc[buy_idx, "close"], marker="^", color="#4CAF50", s=80, zorder=5, label="BUY")
    axes[0].scatter(sell_idx, df.loc[sell_idx, "close"], marker="v", color="#F44336", s=80, zorder=5, label="SELL")
    axes[0].set_ylabel("Fiyat (TRY)")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.25)

    colors = ["#4CAF50" if s >= 0 else "#F44336" for s in signals["score"]]
    axes[1].bar(signals.index, signals["score"], color=colors, alpha=0.75, width=1)
    axes[1].axhline(40, color="green", lw=1, ls="--", alpha=0.6, label="Buy esigi")
    axes[1].axhline(-40, color="red", lw=1, ls="--", alpha=0.6, label="Sell esigi")
    axes[1].axhline(0, color="black", lw=0.5)
    axes[1].set_ylabel("Sinyal Skoru")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.25)

    axes[2].plot(df.index, df["rsi"], color="#7B1FA2", lw=1.2)
    axes[2].axhline(70, color="red", lw=0.8, ls="--")
    axes[2].axhline(30, color="green", lw=0.8, ls="--")
    axes[2].set_ylim(0, 100)
    axes[2].set_ylabel("RSI")
    axes[2].grid(True, alpha=0.25)

    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    out = f"charts/{symbol.replace('.IS', '')}_signals.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Grafik: {out}")


def add_indicators(df):
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    df["rsi"] = 100 - 100 / (1 + gain / loss)

    ema12 = df["close"].ewm(span=12).mean()
    ema26 = df["close"].ewm(span=26).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    sma20 = df["close"].rolling(20).mean()
    std20 = df["close"].rolling(20).std()
    df["bb_upper"] = sma20 + 2 * std20
    df["bb_mid"] = sma20
    df["bb_lower"] = sma20 - 2 * std20
    df["sma20"] = sma20
    df["sma50"] = df["close"].rolling(50).mean()
    return df.dropna()


if __name__ == "__main__":
    conn = sqlite3.connect("data/trading.db")

    for symbol in ["YKBNK.IS", "AKBNK.IS", "GARAN.IS"]:
        df = pd.read_sql(
            f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
            conn,
            parse_dates=["date"],
            index_col="date",
        )
        if df.empty:
            continue

        df = add_indicators(df)
        signals = generate_signals_for_df(df)

        latest = signals.iloc[-1]
        print(f"\n{symbol} — GUNCEL SINYAL:")
        print(f"  Sinyal     : {latest['signal']}")
        print(f"  Skor       : {latest['score']:.2f}")
        print(f"  RSI score  : {latest['rsi_score']}")
        print(f"  MACD score : {latest['macd_score']}")
        print(f"  BB score   : {latest['bb_score']}")
        print(f"  MA score   : {latest['ma_score']}")

        print(f"\n  Sinyal Dagilimi ({len(signals)} gun):")
        for sig_type, count in signals["signal"].value_counts().items():
            pct = count / len(signals) * 100
            print(f"    {sig_type:12} : {count:4} gun (%{pct:.1f})")

        plot_signals(symbol, df, signals)

    conn.close()
