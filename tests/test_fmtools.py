"""Tests for fmtools. Run with:  pytest

Several expected values are numbers that appear in the course notebooks, so
a passing test also means the helper agrees with the lecture.
"""

import numpy as np
import pandas as pd
import pytest

import fmtools as fm


# --- Lecture 1: time value of money ----------------------------------------

def test_npv_first_cash_flow_not_discounted():
    assert fm.npv(0.10, [-100, 110]) == pytest.approx(0.0)


def test_irr_recovers_rate():
    cfs = [-1000, 300, 400, 500]
    r = fm.irr(cfs)
    assert fm.npv(r, cfs) == pytest.approx(0.0, abs=1e-8)


def test_irr_raises_without_sign_change():
    with pytest.raises(ValueError):
        fm.irr([100, 100, 100])


def test_annuity_and_loan_payment_are_inverses():
    pmt = fm.annuity_payment(20_000, 0.005, 60)
    assert fm.annuity_pv(pmt, 0.005, 60) == pytest.approx(20_000)


def test_pv_fv_roundtrip():
    assert fm.pv(fm.fv(100, 0.07, 10), 0.07, 10) == pytest.approx(100)


# --- Lecture 2: bonds --------------------------------------------------------

def test_par_bond_prices_at_face():
    assert fm.bond_price(1000, 0.07, 10, 0.07) == pytest.approx(1000)


def test_lecture2_semiannual_example():
    # 2-year bond, 6% semiannual coupon, discounted at 7%
    expected = sum(30 / 1.035 ** t for t in range(1, 5)) + 1000 / 1.035 ** 4
    assert fm.bond_price(1000, 0.06, 2, 0.07, freq=2) == pytest.approx(expected)


def test_zero_coupon_duration_equals_maturity():
    assert fm.macaulay_duration(1000, 0.0, 10, 0.07) == pytest.approx(10)


def test_modified_duration_approximates_price_change():
    p0 = fm.bond_price(1000, 0.05, 10, 0.07)
    p1 = fm.bond_price(1000, 0.05, 10, 0.0701)
    approx = -fm.modified_duration(1000, 0.05, 10, 0.07) * 0.0001
    assert (p1 - p0) / p0 == pytest.approx(approx, rel=1e-3)


# --- Lectures 3-4: performance and backtesting -----------------------------

def test_sharpe_scales_with_sqrt_time():
    r = pd.Series([0.01, 0.02, -0.01, 0.03, 0.00, 0.015])
    monthly = r.mean() / r.std()
    assert fm.sharpe_ratio(r) == pytest.approx(monthly * np.sqrt(12))


def test_max_drawdown():
    r = pd.Series([0.10, -0.50, 0.20])   # 1 -> 1.1 -> 0.55 -> 0.66
    assert fm.max_drawdown(r) == pytest.approx(-0.5)


def test_alpha_beta_on_exact_line():
    rng = np.random.default_rng(0)
    m = pd.Series(rng.normal(0.01, 0.04, 120))
    r = 0.002 + 1.5 * m
    alpha, beta, _ = fm.alpha_beta(r, m)
    assert beta == pytest.approx(1.5)
    assert alpha == pytest.approx(0.002 * 12)


def test_backtest_uses_yesterdays_position():
    prices = pd.Series([100, 110, 99, 120.0])
    position = pd.Series([1, 0, 1, 0])
    bt = fm.backtest_signal(prices, position)
    log_rtn = np.log(prices).diff()
    # day 1 earns with day-0 position (1), day 2 with day-1 position (0), ...
    assert list(bt["strategy_gross"]) == pytest.approx([log_rtn[1], 0.0, log_rtn[3]])


def test_round_trip_costs_two_trades():
    tc = fm.transaction_costs([0, 1, 1, 0], cost=0.005)
    assert tc.sum() == pytest.approx(0.01)


def test_sma_signal_needs_full_window():
    s = fm.sma_signal(pd.Series(np.arange(1.0, 31.0)), window=20)
    assert s.iloc[:19].sum() == 0 and s.iloc[19:].all()


# --- Lecture 5: event studies -----------------------------------------------

def _fake_returns(n=200, k=5, jump_day=150, jump=0.05, seed=1):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2024-01-01", periods=n)
    r = pd.DataFrame(rng.normal(0.0005, 0.01, (n, k)), index=idx)
    r.iloc[jump_day] += jump
    return r, idx[jump_day]


def test_event_windows_match_lecture_lengths():
    r, day0 = _fake_returns()
    est, evt = fm.event_window_indices(r.index, day0)
    assert len(est) == 90 and len(evt) == 21
    assert r.index[evt[10]] == day0


def test_car_detects_a_jump():
    r, day0 = _fake_returns(jump=0.15)
    est, evt = fm.event_window_indices(r.index, day0)
    res = fm.car_with_ci(fm.abnormal_returns(r, est, evt))
    jump = res["car"].iloc[10] - res["car"].iloc[9]
    assert jump == pytest.approx(0.15, abs=0.02)
    assert res["low"].iloc[10] > 0      # significant on the event day


def test_market_model_removes_market_move():
    rng = np.random.default_rng(2)
    idx = pd.bdate_range("2024-01-01", periods=200)
    m = pd.Series(rng.normal(0, 0.01, 200), index=idx)
    m.iloc[150] += 0.05                                 # the whole market jumps
    stocks = pd.DataFrame({c: 1.2 * m + rng.normal(0, 0.002, 200) for c in "ABC"})
    est, evt = fm.event_window_indices(idx, idx[150])
    ar = fm.abnormal_returns(stocks, est, evt, market=m)
    assert abs(ar.iloc[10].mean()) < 0.005             # no stock-specific effect


# --- Lecture 5: Monte Carlo and Markov chains ------------------------------

def test_transition_matrix_rows_sum_to_one():
    states = [0, 0, 1, 1, 1, 0, 0, 0, 1, 0]
    P = fm.estimate_transition_matrix(states)
    assert np.allclose(P.sum(axis=1), 1)
    assert P[1, 1] == pytest.approx(2 / 4)


def test_markov_chain_long_run_share():
    P = np.array([[0.9, 0.1], [0.3, 0.7]])
    s = fm.simulate_markov_chain(P, 50_000, rng=0)
    # stationary share of state 1: 0.1 / (0.1 + 0.3) = 0.25
    assert s.mean() == pytest.approx(0.25, abs=0.01)


def test_markov_chain_rejects_bad_matrix():
    with pytest.raises(ValueError):
        fm.simulate_markov_chain(np.array([[0.5, 0.4], [0.3, 0.7]]), 10)


def test_mc_standard_error_shrinks_with_sqrt_m():
    rng = np.random.default_rng(3)
    se1 = fm.mc_standard_error(rng.normal(size=10_000))
    se2 = fm.mc_standard_error(rng.normal(size=40_000))
    assert se1 / se2 == pytest.approx(2, rel=0.05)


# --- Lecture 5: private loan notebook ---------------------------------------

def test_private_loan_promised_yield():
    # 100 face, issued at 97, 6% cash + 4% PIK, 5 years: notebook prints 10.75%
    t = np.arange(1, 6)
    balances = 100 * 1.04 ** (t - 1)
    flows = np.zeros(6)
    flows[0] = -97
    flows[1:] = 0.06 * balances
    flows[-1] += 100 * 1.04 ** 5
    assert fm.irr(flows) == pytest.approx(0.1075, abs=5e-5)
