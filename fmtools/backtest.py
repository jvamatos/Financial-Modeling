"""Vectorized backtesting (Lecture 4)."""

import numpy as np
import pandas as pd


def sma_signal(prices, window=20):
    """1 when the price is above its `window`-day SMA, else 0.

    The first window-1 days have no SMA and get position 0.
    """
    prices = pd.Series(prices, dtype=float)
    sma = prices.rolling(window).mean()
    return (prices > sma).astype(int)


def transaction_costs(position, cost=0.005):
    """Cost per period: `cost` for each unit change in position.

    Entering (0 -> 1) and exiting (1 -> 0) are two changes; +1 -> -1 counts as 2.
    """
    return pd.Series(position, dtype=float).diff(1).abs().fillna(0) * cost


def backtest_signal(prices, position, cost=0.0):
    """Log returns of a strategy that holds `position` (decided at each close).

    The position is shifted one day, so the position decided with today's
    close earns tomorrow's return. Without that shift the backtest has
    look-ahead bias. Returns a DataFrame with the asset's log return, the
    strategy's gross and net log returns and both cumulative wealth paths.
    """
    prices = pd.Series(prices, dtype=float)
    position = pd.Series(position, dtype=float).reindex(prices.index)
    log_rtn = np.log(prices).diff(1)
    gross = position.shift(1) * log_rtn
    # same convention as the Lecture 4 notebook: the cost is charged on the
    # day the position changes
    net = gross - transaction_costs(position, cost)
    out = pd.DataFrame({"log_rtn": log_rtn, "strategy_gross": gross, "strategy_net": net}).dropna()
    out["bh_cum"] = np.exp(out["log_rtn"].cumsum())
    out["strategy_cum"] = np.exp(out["strategy_net"].cumsum())
    return out
