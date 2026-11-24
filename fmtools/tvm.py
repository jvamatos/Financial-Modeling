"""Time value of money (Lecture 1)."""

import numpy as np
from scipy.optimize import brentq


def pv(cash_flow, rate, t):
    """Present value of a single cash flow received at time t."""
    return cash_flow / (1 + rate) ** t


def fv(amount, rate, t):
    """Future value at time t of an amount invested today."""
    return amount * (1 + rate) ** t


def npv(rate, cash_flows):
    """NPV of cash flows at t = 0, 1, 2, ...

    Unlike Excel's NPV(), the first cash flow is at t = 0 and is not
    discounted. This is the convention used in the course notebooks.
    """
    cash_flows = np.asarray(cash_flows, dtype=float)
    t = np.arange(len(cash_flows))
    return float(np.sum(cash_flows / (1 + rate) ** t))


def irr(cash_flows, low=-0.99, high=10.0):
    """Internal rate of return: the rate at which NPV = 0.

    Searches for a root of NPV between `low` and `high`. Raises ValueError if
    NPV has the same sign at both ends (no IRR in the interval, or cash flows
    with several sign changes that need a narrower interval).
    """
    f = lambda r: npv(r, cash_flows)
    if f(low) * f(high) > 0:
        raise ValueError("NPV does not change sign between low and high; no IRR found there.")
    return float(brentq(f, low, high))


def annuity_pv(payment, rate, n):
    """PV of n equal payments at the end of each period."""
    if rate == 0:
        return payment * n
    return payment * (1 - (1 + rate) ** -n) / rate


def annuity_payment(principal, rate, n):
    """Periodic payment that repays `principal` over n periods (e.g. a loan)."""
    if rate == 0:
        return principal / n
    return principal * rate / (1 - (1 + rate) ** -n)
