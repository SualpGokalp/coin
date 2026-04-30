import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
    df["bb_lower"] = sma20 - 2 * std20
    df["sma20"] = sma20
    df["sma50"] = df["close"].rolling(50).mean()
    return df.dropna()


def run_backtest(df, initial_capital=100_000, commission=0.001, slippage=0.0005, risk_pct=1.0, stop_loss_pct=2.0, take_profit_pct=5.0):
    capital = initial_capital
    equity = [capital]
    trades = []
    in_pos = False
    entry_p = 0
    entry_d = None
    quantity = 0

    for i in range(1, len(df)):
        row = df.iloc[i]
        close = row["close"]

        if in_pos:
            sl_price = entry_p * (1 - stop_loss_pct / 100)
            tp_price = entry_p * (1 + take_profit_pct / 100)
            exit_reason = None
            exit_price = close

            if close <= sl_price:
                exit_reason = "STOP_LOSS"
                exit_price = sl_price * (1 - slippage)
            elif close >= tp_price:
                exit_reason = "TAKE_PROFIT"
                exit_price = tp_price * (1 + slippage)
            elif row.get("rsi", 50) > 70 and df.iloc[i - 1].get("rsi", 50) <= 70:
                exit_reason = "RSI_OVERBOUGHT"

            if exit_reason:
                gross_pnl = (exit_price - entry_p) * quantity
                fee = exit_price * quantity * commission
                net_pnl = gross_pnl - fee
                capital += entry_p * quantity + net_pnl

                trades.append(
                    {
                        "entry_date": entry_d,
                        "exit_date": row.name,
                        "entry_price": entry_p,
                        "exit_price": exit_price,
                        "quantity": quantity,
                        "pnl": net_pnl,
                        "pnl_pct": (exit_price - entry_p) / entry_p * 100,
                        "reason": exit_reason,
                    }
                )
                in_pos = False

        else:
            rsi_ok = row.get("rsi", 50) < 35
            macd_ok = row.get("macd", 0) > row.get("macd_signal", 0)

            if rsi_ok and macd_ok and capital > 10_000:
                risk_amt = capital * (risk_pct / 100)
                sl_diff = close * (stop_loss_pct / 100)
                qty = int(risk_amt / sl_diff)
                cost = close * qty * (1 + commission + slippage)

                if qty > 0 and cost < capital:
                    capital -= cost
                    entry_p = close * (1 + slippage)
                    entry_d = row.name
                    quantity = qty
                    in_pos = True

        pos_val = (close - entry_p) * quantity if in_pos else 0
        equity.append(capital + entry_p * quantity + pos_val if in_pos else capital)

    return pd.DataFrame(trades), pd.Series(equity, index=df.index[: len(equity)])


def plot_backtest_results(symbol, df, trades, equity):
    fig = plt.figure(figsize=(16, 12))
    gs = plt.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3)
    fig.suptitle(f"Backtest Sonuclari: {symbol}", fontsize=14, fontweight="bold")

    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity.values, color="#1565C0", lw=2, label="Portfoy Degeri")
    ax1.axhline(equity.iloc[0], color="gray", ls="--", alpha=0.5, label="Baslangic")
    ax1.fill_between(equity.index, equity.iloc[0], equity.values, where=(equity >= equity.iloc[0]), alpha=0.15, color="green")
    ax1.fill_between(equity.index, equity.iloc[0], equity.values, where=(equity < equity.iloc[0]), alpha=0.15, color="red")

    if not trades.empty:
        for _, t in trades.iterrows():
            color = "#4CAF50" if t["pnl"] > 0 else "#F44336"
            ax1.axvline(t["entry_date"], color=color, alpha=0.2, lw=0.8)

    ax1.set_ylabel("Sermaye (TRY)")
    ax1.set_title("Equity Curve")
    ax1.legend()
    ax1.grid(True, alpha=0.25)

    if not trades.empty:
        ax2 = fig.add_subplot(gs[1, 0])
        pnl_vals = trades["pnl"].values
        colors = ["#4CAF50" if p > 0 else "#F44336" for p in pnl_vals]
        ax2.bar(range(len(pnl_vals)), pnl_vals, color=colors, alpha=0.8)
        ax2.axhline(0, color="black", lw=0.8)
        ax2.set_xlabel("Islem #")
        ax2.set_ylabel("PnL (TRY)")
        ax2.set_title("Islem Bazinda PnL")
        ax2.grid(True, alpha=0.25)

        ax3 = fig.add_subplot(gs[1, 1])
        wins = trades[trades["pnl"] > 0]["pnl"]
        loses = trades[trades["pnl"] < 0]["pnl"]
        if len(wins):
            ax3.hist(wins, bins=15, color="#4CAF50", alpha=0.7, label=f"Kazanan ({len(wins)})")
        if len(loses):
            ax3.hist(loses, bins=15, color="#F44336", alpha=0.7, label=f"Kaybeden ({len(loses)})")
        ax3.axvline(0, color="black", lw=1)
        ax3.set_xlabel("PnL (TRY)")
        ax3.set_ylabel("Islem Sayisi")
        ax3.set_title("Kazanan / Kaybeden Dagilimi")
        ax3.legend()
        ax3.grid(True, alpha=0.25)

        ax4 = fig.add_subplot(gs[2, :])
        peak = equity.cummax()
        drawdown = ((equity - peak) / peak) * 100
        ax4.fill_between(equity.index, drawdown, 0, color="red", alpha=0.4)
        ax4.plot(equity.index, drawdown, color="darkred", lw=0.8)
        ax4.set_ylabel("Drawdown %")
        ax4.set_title("Drawdown (Tepe Noktadan Dusus)")
        ax4.grid(True, alpha=0.25)

        import matplotlib.dates as mdates

        ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha="right")

    out = f"charts/{symbol.replace('.IS', '')}_backtest.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  Grafik: {out}")


def print_backtest_stats(symbol, initial_capital, trades, equity):
    final = equity.iloc[-1]
    total_r = (final - initial_capital) / initial_capital * 100

    print(f"\n{'=' * 60}")
    print(f"BACKTEST SONUCLARI: {symbol}")
    print(f"{'=' * 60}")
    print(f"Baslangic Sermaye   : {initial_capital:>12,.0f} TRY")
    print(f"Final Sermaye       : {final:>12,.0f} TRY")
    print(f"Toplam Getiri       : {total_r:>11.2f} %")

    if not trades.empty:
        winners = trades[trades["pnl"] > 0]
        losers = trades[trades["pnl"] < 0]
        win_rate = len(winners) / len(trades) * 100

        peak = equity.cummax()
        drawdown = ((equity - peak) / peak) * 100
        max_dd = drawdown.min()

        avg_win = winners["pnl"].mean() if len(winners) else 0
        avg_loss = losers["pnl"].mean() if len(losers) else 0
        rr_ratio = abs(avg_win / avg_loss) if avg_loss else 0

        print(f"Toplam Islem        : {len(trades):>12}")
        print(f"Kazanan             : {len(winners):>12}  (%{win_rate:.1f})")
        print(f"Kaybeden            : {len(losers):>12}")
        print(f"Ortalama Kazanc     : {avg_win:>12,.2f} TRY")
        print(f"Ortalama Kayip      : {avg_loss:>12,.2f} TRY")
        print(f"Risk/Reward Orani   : {rr_ratio:>12.2f}")
        print(f"Max Drawdown        : {max_dd:>11.2f} %")

    print(f"{'=' * 60}")


if __name__ == "__main__":
    conn = sqlite3.connect("data/trading.db")
    INITIAL = 100_000

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
        trades, equity = run_backtest(df, initial_capital=INITIAL)
        print_backtest_stats(symbol, INITIAL, trades, equity)
        plot_backtest_results(symbol, df, trades, equity)

    conn.close()
