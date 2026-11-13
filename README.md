# 2270 Financial Modelling

Course materials for **2270 Financial Modelling** (Masters in Finance, T2): designing models for financial decisions and building them in Python.

## Contents

| # | Topic | Materials |
|---|-------|-----------|
| 1 | Principles of financial modelling & basic financial calculations (time value of money, PV/FV, IRR) | [Slides](lectures/01-financial-calculations/Lecture1_Intro.pdf) · [Notebook](lectures/01-financial-calculations/Lecture1_financial_calculations.ipynb) |
| 2 | Data structures & NumPy; bond valuation | [Part 1: Python & NumPy](lectures/02-numpy-and-bond-valuation/Lecture2_python_numpy.ipynb) · [Part 2: Bond valuation](lectures/02-numpy-and-bond-valuation/Lecture2_bond_valuation.ipynb) |
| 3 | Getting data via APIs (FRED, CoinGecko) & pandas; portfolio strategies (1/n) | [Part 1: APIs & pandas](lectures/03-data-apis-and-portfolios/Lecture3_apis_pandas.ipynb) · [Part 2: Portfolio strategies](lectures/03-data-apis-and-portfolios/Lecture3_portfolio_strategies.ipynb) |
| 4 | Portfolio backtesting | [Notebook](lectures/04-backtesting/Lecture4_backtesting.ipynb) |

**Reference:** [Formula sheet](reference/2270_Formulae.pdf)

## Repository layout

```
lectures/
  01-financial-calculations/
  02-numpy-and-bond-valuation/
  03-data-apis-and-portfolios/
  04-backtesting/
reference/          formula sheet and other handouts
requirements.txt    Python packages used by the notebooks
```

## Running the notebooks

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
