"""Strategy evaluation (Lectures 3 and 4).

All functions take periodic *simple* returns as a pandas Series (or anything
pandas can turn into one). `periods_per_year` is 12 for monthly data and 252
for daily data.
"""

import numpy as np
import pandas as pd


def _series(r):
    return pd.Series(r, dtype=float).dropna()


def annualize_return(r, periods_per_year=12):
    """Geometric (compound) annual return."""
    r = _series(r)
    growth = (1 + r).prod()
    return float(growth ** (periods_per_year / len(r)) - 1)


def annualize_vol(r, periods_per_year=12):
    """Annualized volatility: the std scales with the square root of time."""
    return float(_series(r).std() * np.sqrt(periods_per_year))


def sharpe_ratio(r, rf=0.0, periods_per_year=12):
    """Annualized Sharpe ratio of excess returns.

    rf is the risk-free rate per period (a number or a Series aligned with r).
    """
    excess = _series(pd.Series(r, dtype=float) - rf)
    return float(excess.mean() / excess.std() * np.sqrt(periods_per_year))


def drawdown_series(r):
    """Drawdown at each date: % below the previous peak of the wealth index."""
    wealth = (1 + _series(r)).cumprod()
    peak = wealth.cummax()
    return wealth / peak - 1


def max_drawdown(r):
    """Worst peak-to-trough loss (a negative number)."""
    return float(drawdown_series(r).min())


def alpha_beta(r, market, rf=0.0, periods_per_year=12):
    """CAPM regression r - rf = alpha + beta (market - rf) + e.

    Returns (annualized alpha, beta, residuals).
    """
    df = pd.concat([pd.Series(r, dtype=float), pd.Series(market, dtype=float)], axis=1).dropna()
    y = df.iloc[:, 0] - rf
    x = df.iloc[:, 1] - rf
    beta = float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))
    alpha = float(y.mean() - beta * x.mean())
    resid = y - alpha - beta * x
    return alpha * periods_per_year, beta, resid


def information_ratio(r, market, rf=0.0, periods_per_year=12):
    """Annualized alpha divided by annualized idiosyncratic (residual) volatility."""
    alpha, _, resid = alpha_beta(r, market, rf, periods_per_year)
    return float(alpha / (resid.std() * np.sqrt(periods_per_year)))
