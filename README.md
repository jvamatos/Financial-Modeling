# 2270 Financial Modelling

Course materials for **2270 Financial Modelling** (Masters in Finance, T2): designing models for financial decisions and building them in Python.

## Contents

| # | Topic | Materials | Summary |
|---|-------|-----------|---------|
| 1 | Principles of financial modelling & basic financial calculations (time value of money, PV/FV, IRR) | [Slides](lectures/01-financial-calculations/Lecture1_Intro.pdf) · [Notebook](lectures/01-financial-calculations/Lecture1_financial_calculations.ipynb) | [Resumo](summaries/01-financial-calculations.md) |
| 2 | Data structures & NumPy; bond valuation | [Part 1: Python & NumPy](lectures/02-numpy-and-bond-valuation/Lecture2_python_numpy.ipynb) · [Part 2: Bond valuation](lectures/02-numpy-and-bond-valuation/Lecture2_bond_valuation.ipynb) | [Resumo](summaries/02-numpy-and-bond-valuation.md) |
| 3 | Getting data via APIs (FRED, CoinGecko) & pandas; portfolio strategies (1/n) | [Part 1: APIs & pandas](lectures/03-data-apis-and-portfolios/Lecture3_apis_pandas.ipynb) · [Part 2: Portfolio strategies](lectures/03-data-apis-and-portfolios/Lecture3_portfolio_strategies.ipynb) | [Resumo](summaries/03-data-apis-and-portfolios.md) |
| 4 | Portfolio backtesting | [Notebook](lectures/04-backtesting/Lecture4_backtesting.ipynb) | [Resumo](summaries/04-backtesting.md) |
| 5 | Event studies; Monte Carlo simulation (Markov chains, retirement, LBO); valuing a private loan | [Monte Carlo](lectures/05-event-studies-and-monte-carlo/Lecture5_monte_carlo.ipynb) · [Practice: private loan](lectures/05-event-studies-and-monte-carlo/Lecture5_private_loan.ipynb) | [Resumo](summaries/05-event-studies-and-monte-carlo.md) |

**Reference:** [Formula sheet](reference/2270_Formulae.pdf)

**Summaries:** [all lecture summaries](summaries/README.md) (in Portuguese), including the DataCamp Python basics. The event-study part of Lecture 5 is covered in its summary; its notebook isn't in the repository yet.

## Repository layout

```
lectures/
  01-financial-calculations/
  02-numpy-and-bond-valuation/
  03-data-apis-and-portfolios/
  04-backtesting/
  05-event-studies-and-monte-carlo/
reference/          formula sheet and other handouts
summaries/          revision summaries per lecture (notes, traps, practice questions)
fmtools/            tested helper functions for every lecture (to check your answers)
tests/              tests for fmtools
requirements.txt    Python packages used by the notebooks
```

## Running the notebooks

The notebooks are saved with their outputs (printed results and charts), so you can read the results on GitHub without running anything. A few cells are left without output: the blank Practice cells in Lecture 2 (you fill them in) and the FRED API cells in Lecture 3, which need your own key.

The notebooks run as-is in Google Colab. To run them locally:

```bash
pip install -r requirements.txt
jupyter lab
```

### FRED API key (Lecture 3)

Lecture 3 uses the FRED API, which needs a free personal key from
<https://fred.stlouisfed.org/docs/api/api_key.html>. Either paste it into the
notebook where it says `PASTE_YOUR_KEY_HERE`, or set it as an environment
variable so it never ends up in the notebook:

```bash
export FRED_API_KEY=your_key_here
```

Don't commit your own key to the repository.

Lecture 5 reads FRED series (`USREC`, `GS5`) as CSV files from
`fred.stlouisfed.org/graph/fredgraph.csv`, which needs no key.

## Checking your answers with `fmtools`

The notebooks build every calculation step by step. `fmtools` has the same
calculations as small, tested functions, so you can check a result you
computed by hand (or reuse them in the group assignment once you understand
them):

```python
import fmtools as fm

fm.npv(0.07, [-1000, 300, 400, 500])         # Lecture 1 (first cash flow at t = 0)
fm.irr([-97, 6, 6.24, 6.49, 6.75, 128.69])   # Lecture 5 private loan, about 10.75%
fm.bond_price(1000, 0.06, 2, 0.07, freq=2)   # Lecture 2
fm.modified_duration(1000, 0.05, 10, 0.07)
fm.sharpe_ratio(monthly_returns, rf=rf)      # Lectures 3-4, annualized with sqrt(12)
fm.max_drawdown(monthly_returns)
fm.backtest_signal(prices, fm.sma_signal(prices, 20), cost=0.005)   # Lecture 4
est, evt = fm.event_window_indices(returns.index, '2024-11-06')    # Lecture 5
fm.car_with_ci(fm.abnormal_returns(returns, est, evt))
fm.simulate_markov_chain(P, T=100, rng=17)
```

| Module | Lecture | Functions |
|---|---|---|
| `tvm` | 1 | `pv`, `fv`, `npv`, `irr`, `annuity_pv`, `annuity_payment` |
| `bonds` | 2 | `bond_cash_flows`, `bond_price`, `macaulay_duration`, `modified_duration` |
| `performance` | 3–4 | `annualize_return`, `annualize_vol`, `sharpe_ratio`, `drawdown_series`, `max_drawdown`, `alpha_beta`, `information_ratio` |
| `backtest` | 4 | `sma_signal`, `transaction_costs`, `backtest_signal` (always shifts the position one day) |
| `event_study` | 5 | `event_window_indices`, `abnormal_returns` (constant-return or market model), `car_with_ci` |
| `simulation` | 5 | `estimate_transition_matrix`, `simulate_markov_chain`, `mc_standard_error` |

In Colab, clone the repository first (`!git clone https://github.com/jvamatos/Financial-Modeling` and
`%cd Financial-Modeling`). To run the tests locally:

```bash
pytest
```

They also run on GitHub on every push.
