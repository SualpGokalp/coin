import sqlite3

import pandas as pd

from agents.base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    def __init__(self, db_path="data/trading.db"):
        super().__init__("AnalysisAgent")
        self.db_path = db_path

    def _add_indicators(self, df):
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

    def run(self, symbols):
        self.status = "running"
        conn = sqlite3.connect(self.db_path)
        analyses = {}

        for symbol in symbols:
            df = pd.read_sql(
                f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
                conn,
                parse_dates=["date"],
                index_col="date",
            )
            if df.empty:
                continue

            df = self._add_indicators(df)
            latest = df.iloc[-1]

            analyses[symbol] = {
                "close": latest["close"],
                "rsi": latest["rsi"],
                "macd": latest["macd"],
                "macd_signal": latest["macd_signal"],
                "bb_upper": latest["bb_upper"],
                "bb_lower": latest["bb_lower"],
                "sma20": latest["sma20"],
                "sma50": latest["sma50"],
            }
            self.log(f"{symbol}: RSI={latest['rsi']:.2f}, MACD={latest['macd']:.4f}")

        conn.close()
        self.status = "done"
        self.result = analyses
        return analyses
