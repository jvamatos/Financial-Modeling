"""Bond valuation and duration (Lecture 2, Part 2)."""

import numpy as np


def bond_cash_flows(face, coupon_rate, maturity, freq=1):
    """Times (in years) and cash flows of a plain-vanilla bond.

    coupon_rate is annual; freq is the number of coupons per year.
    """
    n = int(round(maturity * freq))
    times = np.arange(1, n + 1) / freq
    cfs = np.full(n, face * coupon_rate / freq, dtype=float)
    cfs[-1] += face
    return times, cfs


def bond_price(face, coupon_rate, maturity, ytm, freq=1):
    """Price of a bond, discounting at ytm/freq per period."""
    times, cfs = bond_cash_flows(face, coupon_rate, maturity, freq)
    periods = times * freq
    return float(np.sum(cfs / (1 + ytm / freq) ** periods))


def macaulay_duration(face, coupon_rate, maturity, ytm, freq=1):
    """Macaulay duration in years: PV-weighted average time of the cash flows."""
    times, cfs = bond_cash_flows(face, coupon_rate, maturity, freq)
    pvs = cfs / (1 + ytm / freq) ** (times * freq)
    return float(np.sum(times * pvs) / np.sum(pvs))


def modified_duration(face, coupon_rate, maturity, ytm, freq=1):
    """Modified duration: % price change for a 1-unit change in ytm.

    dP/P ≈ -modified_duration * dy
    """
    return macaulay_duration(face, coupon_rate, maturity, ytm, freq) / (1 + ytm / freq)
