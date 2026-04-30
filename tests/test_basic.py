import sys

sys.path.insert(0, ".")


def test_imports():
    import numpy as np
    import pandas as pd
    import yfinance as yf

    assert pd.__version__
    assert np.__version__
    assert yf.__version__


def test_rsi_range():
    import pandas as pd

    prices = pd.Series([10, 11, 10.5, 12, 11.5, 13, 12, 14, 13.5, 15, 14, 16, 15, 17, 16, 18, 17, 19, 18, 20])
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rsi = 100 - 100 / (1 + gain / loss)
    valid = rsi.dropna()
    assert len(valid) > 0
    assert valid.between(0, 100).all()


def test_position_sizing():
    portfolio = 100_000
    risk_pct = 1.0
    entry = 10.50
    stop_loss = 10.00

    risk_amount = portfolio * (risk_pct / 100)
    risk_per_share = abs(entry - stop_loss)
    quantity = int(risk_amount / risk_per_share)

    assert quantity == 2000
    assert risk_amount == 1000.0


def test_signal_scoring():
    scores = []
    rsi = 25
    if rsi < 30:
        scores.append(80)
    avg = sum(scores) / len(scores)
    assert avg == 80
