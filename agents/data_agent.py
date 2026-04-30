import sqlite3

import pandas as pd
import yfinance as yf

from agents.base_agent import BaseAgent


class DataAgent(BaseAgent):
    def __init__(self, db_path="data/trading.db"):
        super().__init__("DataAgent")
        self.db_path = db_path

    def run(self, symbols, start="2022-01-01", end=None):
        self.status = "running"
        self.log(f"Veri cekiliyor: {symbols}")
        conn = sqlite3.connect(self.db_path)
        results = {}

        for symbol in symbols:
            try:
                df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
                if not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df.reset_index(inplace=True)
                    df.columns = [c.lower() for c in df.columns]
                    df["symbol"] = symbol
                    df["date"] = pd.to_datetime(df["date"]).dt.date
                    cols = [c for c in ["symbol", "date", "open", "high", "low", "close", "volume"] if c in df.columns]
                    df[cols].to_sql("prices", conn, if_exists="append", index=False)
                    results[symbol] = len(df)
                    self.log(f"{symbol}: {len(df)} satir kaydedildi.")
            except Exception as e:
                self.log(f"{symbol}: HATA - {e}", "ERROR")

        conn.close()
        self.status = "done"
        self.result = results
        return results
