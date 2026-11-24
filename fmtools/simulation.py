"""Monte Carlo and Markov chains (Lecture 5)."""

import numpy as np
import pandas as pd


def mc_standard_error(samples):
    """Standard error of a Monte Carlo mean: std / sqrt(M). Halving it needs 4x the draws."""
    samples = np.asarray(samples, dtype=float)
    return float(samples.std(ddof=1) / np.sqrt(len(samples)))


def estimate_transition_matrix(states, n_states=None):
    """Transition matrix P[i, j] = P(next state = j | state = i), from a series of states 0..N-1."""
    s = np.asarray(pd.Series(states).dropna(), dtype=int)
    n = n_states or int(s.max()) + 1
    counts = np.zeros((n, n))
    np.add.at(counts, (s[:-1], s[1:]), 1)
    rows = counts.sum(axis=1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(rows > 0, counts / rows, 0.0)


def simulate_markov_chain(P, T, start=0, burn_in=100, rng=None):
    """Simulate T periods of a Markov chain with transition matrix P.

    The first `burn_in` periods are thrown away so the result does not depend
    on the arbitrary starting state.
    """
    P = np.asarray(P, dtype=float)
    if not np.allclose(P.sum(axis=1), 1):
        raise ValueError("each row of the transition matrix must sum to 1")
    rng = np.random.default_rng(rng)
    n = P.shape[0]
    states = np.empty(T + burn_in, dtype=int)
    states[0] = start
    for t in range(1, T + burn_in):
        states[t] = rng.choice(n, p=P[states[t - 1]])
    return states[burn_in:]
