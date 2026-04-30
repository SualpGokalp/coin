import os
import sqlite3

import pandas as pd

DB_PATH = "data/trading.db"


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prices (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol  TEXT NOT NULL,
            date    DATE NOT NULL,
            open    REAL,
            high    REAL,
            low     REAL,
            close   REAL,
            volume  INTEGER,
            UNIQUE(symbol, date)
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS signals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol      TEXT NOT NULL,
            date        DATE NOT NULL,
            signal_type TEXT,
            score       REAL,
            rsi         REAL,
            macd        REAL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol   TEXT NOT NULL,
            action   TEXT,
            price    REAL,
            quantity INTEGER,
            date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pnl      REAL,
            mode     TEXT DEFAULT 'demo'
        )
    """
    )

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prices_symbol ON prices(symbol)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(date)")
    conn.commit()
    print("Tablolar olusturuldu.")


def load_csv_to_db(conn, symbol):
    csv_path = f"data/{symbol.replace('.IS', '')}_prices.csv"
    if not os.path.exists(csv_path):
        print(f"CSV bulunamadi: {csv_path}")
        return

    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)
    df.columns = [c.lower() for c in df.columns]

    date_col = "date" if "date" in df.columns else df.columns[0]
    df.rename(columns={date_col: "date"}, inplace=True)
    df["symbol"] = symbol
    df["date"] = pd.to_datetime(df["date"]).dt.date

    cols = [c for c in ["symbol", "date", "open", "high", "low", "close", "volume"] if c in df.columns]
    df[cols].to_sql("prices", conn, if_exists="append", index=False)
    print(f"{symbol}: {len(df)} satir yuklendi.")


def verify_database(conn):
    cursor = conn.cursor()
    print("\nVERITABANI OZETI")
    print("=" * 55)
    cursor.execute(
        """
        SELECT symbol, COUNT(*) as rows,
               MIN(date) as first_date,
               MAX(date) as last_date,
               ROUND(AVG(close), 2) as avg_close
        FROM prices
        GROUP BY symbol
    """
    )
    for row in cursor.fetchall():
        symbol, rows, first_date, last_date, avg_close = row
        print(f"{symbol:14} | {rows:4} satir | {first_date} -> {last_date} | Ort: {avg_close} TRY")
    print("=" * 55)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    for stock in ["YKBNK.IS", "AKBNK.IS", "GARAN.IS"]:
        load_csv_to_db(conn, stock)

    verify_database(conn)
    conn.close()
