"""Event studies (Lecture 5)."""

import numpy as np
import pandas as pd


def event_window_indices(index, event_date, estimation_window=(-100, -11), event_window=(-10, 10)):
    """Integer positions of the estimation and event windows.

    Windows are in trading days relative to the event (day 0) and include
    both ends, as in the lecture: (-100, -11) is 90 days.
    If the event date is not a trading day, the next trading day is day 0.
    """
    index = pd.DatetimeIndex(index)
    if index.tz is not None:
        index = index.tz_localize(None)
    day0 = int(index.searchsorted(pd.Timestamp(event_date)))
    if day0 >= len(index):
        raise ValueError("event_date is after the last date in the data")
    est = range(day0 + estimation_window[0], day0 + estimation_window[1] + 1)
    evt = range(day0 + event_window[0], day0 + event_window[1] + 1)
    if est.start < 0 or evt.stop > len(index):
        raise ValueError("not enough data around the event for these windows")
    return est, evt


def abnormal_returns(returns, est_idx, evt_idx, market=None):
    """Abnormal returns in the event window, one column per stock.

    With market=None this is the constant-return model: normal return = mean
    in the estimation window. With a market return series it is the market
    model: normal return = alpha + beta * market, both estimated per stock in
    the estimation window.
    """
    returns = pd.DataFrame(returns)
    est = returns.iloc[list(est_idx)]
    evt = returns.iloc[list(evt_idx)]
    if market is None:
        return evt - est.mean(axis=0)

    market = pd.Series(market).reindex(returns.index)
    m_est = market.iloc[list(est_idx)]
    m_evt = market.iloc[list(evt_idx)]
    ar = {}
    for col in returns.columns:
        y = est[col]
        ok = y.notna() & m_est.notna()
        beta = np.cov(m_est[ok], y[ok], ddof=1)[0, 1] / np.var(m_est[ok], ddof=1)
        alpha = y[ok].mean() - beta * m_est[ok].mean()
        ar[col] = evt[col] - (alpha + beta * m_evt)
    return pd.DataFrame(ar)


def car_with_ci(ar, z=1.96):
    """Average CAR across stocks with the lecture's confidence band.

    The band is CAR ± z * (cross-sectional std of AR on that day) * sqrt(horizon).
    Returns a DataFrame with columns car, low and high.
    """
    car = ar.cumsum().mean(axis=1)
    std = ar.std(axis=1)
    horizon = np.arange(1, len(ar) + 1)
    half = z * std * np.sqrt(horizon)
    return pd.DataFrame({"car": car, "low": car - half, "high": car + half})
