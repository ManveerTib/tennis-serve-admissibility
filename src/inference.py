"""
Empirical inference utilities for serve-speed analysis.

V9:
    Distribution summaries, bootstrap confidence intervals,
    standardized group differences, and logistic speed-response models.
"""

import numpy as np
from scipy.optimize import minimize
from scipy.stats import ks_2samp


def distribution_summary(values):
    """Return standard descriptive statistics for a numeric sample."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if values.size == 0:
        raise ValueError("values must contain at least one finite observation")

    return {
        "n": int(values.size),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values, ddof=1)) if values.size > 1 else 0.0,
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "p95": float(np.percentile(values, 95)),
        "p99": float(np.percentile(values, 99)),
    }


def bootstrap_median_difference(
    group_a,
    group_b,
    n_bootstrap=5000,
    seed=0,
):
    """
    Bootstrap a median difference (group_a median - group_b median).
    """
    a = np.asarray(group_a, dtype=float)
    b = np.asarray(group_b, dtype=float)

    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]

    if len(a) == 0 or len(b) == 0:
        raise ValueError("Both groups must contain observations")

    rng = np.random.default_rng(seed)
    estimates = np.empty(n_bootstrap)

    for i in range(n_bootstrap):
        a_sample = rng.choice(a, size=len(a), replace=True)
        b_sample = rng.choice(b, size=len(b), replace=True)
        estimates[i] = np.median(a_sample) - np.median(b_sample)

    return {
        "estimate": float(np.median(a) - np.median(b)),
        "ci_low": float(np.percentile(estimates, 2.5)),
        "ci_high": float(np.percentile(estimates, 97.5)),
        "bootstrap_estimates": estimates,
    }


def cohens_d(group_a, group_b):
    """Calculate Cohen's d using the pooled sample standard deviation."""
    a = np.asarray(group_a, dtype=float)
    b = np.asarray(group_b, dtype=float)

    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]

    if len(a) < 2 or len(b) < 2:
        raise ValueError("Each group needs at least two observations")

    pooled_sd = np.sqrt(
        ((len(a) - 1) * np.var(a, ddof=1)
         + (len(b) - 1) * np.var(b, ddof=1))
        / (len(a) + len(b) - 2)
    )

    return float((np.mean(a) - np.mean(b)) / pooled_sd)


def ks_test(group_a, group_b):
    """Return the two-sample Kolmogorov-Smirnov test result."""
    result = ks_2samp(group_a, group_b)

    return {
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
    }


def _logistic_nll(beta, x, y):
    """Negative log-likelihood for logistic regression."""
    eta = beta[0] + beta[1] * x
    log_likelihood = np.sum(
        y * eta - np.logaddexp(0.0, eta)
    )
    return -log_likelihood


def fit_logistic_speed(
    speed_kmh,
    outcome,
    reference_speed=170.0,
    scale=10.0,
):
    """
    Fit a logistic model with centered/scaled serve speed.

    Model:
        logit(P(win)) = beta0 + beta1 * (speed-reference_speed)/scale

    Returns fitted coefficients and odds ratio per scale unit.
    """
    speed_kmh = np.asarray(speed_kmh, dtype=float)
    outcome = np.asarray(outcome, dtype=float)

    mask = np.isfinite(speed_kmh) & np.isfinite(outcome)
    speed = speed_kmh[mask]
    y = outcome[mask]

    if len(speed) == 0:
        raise ValueError("No finite observations")

    x = (speed - reference_speed) / scale

    result = minimize(
        _logistic_nll,
        x0=np.zeros(2),
        args=(x, y),
        method="L-BFGS-B",
    )

    if not result.success:
        raise RuntimeError(result.message)

    intercept, slope = result.x

    return {
        "intercept": float(intercept),
        "slope_per_scale": float(slope),
        "odds_ratio_per_scale": float(np.exp(slope)),
        "reference_speed": float(reference_speed),
        "scale": float(scale),
        "n": int(len(y)),
        "optimization_result": result,
    }


def predict_logistic_speed(
    speed_kmh,
    model,
):
    """Predict win probability from a fitted logistic speed model."""
    x = (
        np.asarray(speed_kmh, dtype=float) - model["reference_speed"]
    ) / model["scale"]

    eta = model["intercept"] + model["slope_per_scale"] * x

    return 1.0 / (1.0 + np.exp(-eta))
