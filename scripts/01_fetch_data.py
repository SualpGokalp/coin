import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

STOCKS = ["YKBNK.IS", "AKBNK.IS", "GARAN.IS"]
START = "2022-01-01"
END = "2024-12-31"


def fetch_stock(symbol, start, end):
    print(f"Downloading {symbol}...", end=" ")
    df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)

    if df.empty:
        print("No data")
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index = pd.to_datetime(df.index)
    print(f"OK — {len(df)} rows ({df.index[0].date()} -> {df.index[-1].date()})")
    return df


def plot_stock(symbol, df):
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle(f"{symbol} — Fiyat & Hacim", fontsize=14, fontweight="bold")

    axes[0].plot(df.index, df["Close"], color="#2196F3", linewidth=1.5, label="Close")
    axes[0].fill_between(df.index, df["Low"], df["High"], alpha=0.15, color="#2196F3")
    axes[0].set_ylabel("Fiyat (TRY)", fontsize=10)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    colors = ["#4CAF50" if c >= o else "#F44336" for c, o in zip(df["Close"], df["Open"])]
    axes[1].bar(df.index, df["Volume"], color=colors, alpha=0.8, width=1)
    axes[1].set_ylabel("Hacim", fontsize=10)
    axes[1].grid(True, alpha=0.3)

    daily_change = df["Close"].pct_change() * 100
    pos = daily_change.clip(lower=0)
    neg = daily_change.clip(upper=0)
    axes[2].fill_between(df.index, pos, 0, color="#4CAF50", alpha=0.7, label="Artis")
    axes[2].fill_between(df.index, neg, 0, color="#F44336", alpha=0.7, label="Dusus")
    axes[2].axhline(0, color="black", linewidth=0.5)
    axes[2].set_ylabel("Gunluk Degisim %", fontsize=10)
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.tight_layout()

    out = f"charts/{symbol.replace('.IS', '')}_price.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Grafik: {out}")


if __name__ == "__main__":
    os.makedirs("charts", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    all_data = {}
    for stock in STOCKS:
        data = fetch_stock(stock, START, END)
        if data is not None:
            all_data[stock] = data
            data.to_csv(f"data/{stock.replace('.IS', '')}_prices.csv")
            plot_stock(stock, data)

    print(f"\n{len(all_data)}/{len(STOCKS)} hisse basariyla indirildi.")
