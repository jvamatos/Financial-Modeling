"""Small, tested helpers for the 2270 Financial Modelling course.

The notebooks write these calculations out step by step, which is the point
of the course. This package has the same calculations in one place so you can
check your own answers, or reuse them in the group assignment once you
understand how they work.

    from fmtools import npv, irr, bond_price, sharpe_ratio
"""

from .tvm import pv, fv, npv, irr, annuity_pv, annuity_payment
from .bonds import bond_cash_flows, bond_price, macaulay_duration, modified_duration
from .performance import (
    annualize_return,
    annualize_vol,
    sharpe_ratio,
    max_drawdown,
    drawdown_series,
    alpha_beta,
    information_ratio,
)
from .backtest import sma_signal, backtest_signal, transaction_costs
from .event_study import event_window_indices, abnormal_returns, car_with_ci
from .simulation import estimate_transition_matrix, simulate_markov_chain, mc_standard_error

__all__ = [
    "pv", "fv", "npv", "irr", "annuity_pv", "annuity_payment",
    "bond_cash_flows", "bond_price", "macaulay_duration", "modified_duration",
    "annualize_return", "annualize_vol", "sharpe_ratio", "max_drawdown",
    "drawdown_series", "alpha_beta", "information_ratio",
    "sma_signal", "backtest_signal", "transaction_costs",
    "event_window_indices", "abnormal_returns", "car_with_ci",
    "estimate_transition_matrix", "simulate_markov_chain", "mc_standard_error",
]
