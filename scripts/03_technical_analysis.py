import sqlite3

import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd

DB_PATH = "data/trading.db"


def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger(prices, period=20, std=2):
    mid = prices.rolling(period).mean()
    sigma = prices.rolling(period).std()
    upper = mid + std * sigma
    lower = mid - std * sigma
    return upper, mid, lower


def plot_full_analysis(symbol, df):
    fig = plt.figure(figsize=(16, 14))
    gs = gridspec.GridSpec(4, 1, figure=fig, hspace=0.05, height_ratios=[3, 1.5, 1.5, 1])
    fig.suptitle(f"Teknik Analiz: {symbol}", fontsize=15, fontweight="bold", y=0.98)

    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df.index, df["close"], color="#1565C0", lw=1.5, label="Kapanis")
    ax1.plot(df.index, df["sma20"], color="#FF9800", lw=1, label="SMA 20", ls="--")
    ax1.plot(df.index, df["sma50"], color="#9C27B0", lw=1, label="SMA 50", ls="--")
    ax1.plot(df.index, df["bb_mid"], color="gray", lw=0.8, ls=":")
    ax1.fill_between(df.index, df["bb_upper"], df["bb_lower"], alpha=0.12, color="#2196F3", label="Bollinger Bands")
    ax1.set_ylabel("Fiyat (TRY)", fontsize=10)
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, alpha=0.25)
    ax1.set_xticklabels([])

    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.plot(df.index, df["macd"], color="#1565C0", lw=1.2, label="MACD")
    ax2.plot(df.index, df["macd_signal"], color="#F44336", lw=1.2, label="Signal")
    bar_colors = ["#4CAF50" if v >= 0 else "#F44336" for v in df["macd_hist"]]
    ax2.bar(df.index, df["macd_hist"], color=bar_colors, alpha=0.7, width=1, label="Histogram")
    ax2.axhline(0, color="black", lw=0.5)
    ax2.set_ylabel("MACD", fontsize=10)
    ax2.legend(loc="upper left", fontsize=9)
    ax2.grid(True, alpha=0.25)
    ax2.set_xticklabels([])

    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(df.index, df["rsi"], color="#7B1FA2", lw=1.3, label="RSI(14)")
    ax3.axhline(70, color="#F44336", lw=1, ls="--", alpha=0.7)
    ax3.axhline(30, color="#4CAF50", lw=1, ls="--", alpha=0.7)
    ax3.axhline(50, color="gray", lw=0.8, ls=":")
    ax3.fill_between(df.index, 70, 100, alpha=0.05, color="red")
    ax3.fill_between(df.index, 0, 30, alpha=0.05, color="green")
    ax3.set_ylim(0, 100)
    ax3.set_ylabel("RSI", fontsize=10)
    ax3.legend(loc="upper left", fontsize=9)
    ax3.grid(True, alpha=0.25)
    ax3.set_xticklabels([])

    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    colors = ["#4CAF50" if c >= o else "#F44336" for c, o in zip(df["close"], df["open"])]
    ax4.bar(df.index, df["volume"], color=colors, alpha=0.8, width=1)
    ax4.set_ylabel("Hacim", fontsize=10)
    ax4.grid(True, alpha=0.25)

    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha="right")

    out = f"charts/{symbol.replace('.IS', '')}_technical.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Grafik: {out}")


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)

    for symbol in ["YKBNK.IS", "AKBNK.IS", "GARAN.IS"]:
        df = pd.read_sql(
            f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
            conn,
            parse_dates=["date"],
            index_col="date",
        )

        if df.empty:
            print(f"{symbol}: veri yok, atlaniyor.")
            continue

        df["rsi"] = calculate_rsi(df["close"])
        df["macd"], df["macd_signal"], df["macd_hist"] = calculate_macd(df["close"])
        df["bb_upper"], df["bb_mid"], df["bb_lower"] = calculate_bollinger(df["close"])
        df["sma20"] = df["close"].rolling(20).mean()
        df["sma50"] = df["close"].rolling(50).mean()
        df.dropna(inplace=True)

        print(f"\n{symbol} — Son Degerler:")
        print(f"  Fiyat : {df['close'].iloc[-1]:.2f} TRY")
        print(f"  RSI   : {df['rsi'].iloc[-1]:.2f}")
        print(f"  MACD  : {df['macd'].iloc[-1]:.4f}")

        plot_full_analysis(symbol, df)

    conn.close()
