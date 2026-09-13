"""
Sensitivity and perturbation analysis for the serve admissibility model.

V8:
    Local finite-difference sensitivity and factorial robustness utilities.
"""

import itertools
import numpy as np


def finite_difference_sensitivity(
    function,
    x0,
    step,
):
    """
    Estimate a local derivative using a centered finite difference.

    Returns
    -------
    float
        Approximate derivative df/dx at x0.
    """
    x0 = float(x0)
    step = float(step)

    if step <= 0:
        raise ValueError("step must be positive")

    return (function(x0 + step) - function(x0 - step)) / (2.0 * step)


def perturbation_grid(center, perturbations):
    """
    Construct a one-dimensional perturbation grid around a nominal value.
    """
    center = float(center)
    perturbations = np.asarray(perturbations, dtype=float)
    return center + perturbations


def full_factorial_levels(levels):
    """
    Generate the Cartesian product of supplied perturbation levels.

    Parameters
    ----------
    levels : dict
        Mapping parameter name -> iterable of tested values.

    Returns
    -------
    list of dict
        One dictionary per factorial-design combination.
    """
    names = list(levels.keys())
    values = [list(levels[name]) for name in names]

    return [
        dict(zip(names, combination))
        for combination in itertools.product(*values)
    ]


def robustness_fraction(results):
    """
    Calculate the fraction of tested cases satisfying a condition.

    Parameters
    ----------
    results : array-like
        Boolean legality/robustness results.

    Returns
    -------
    float
        Fraction of True results.
    """
    results = np.asarray(results, dtype=bool)

    if results.size == 0:
        raise ValueError("results must not be empty")

    return float(np.mean(results))


def marginal_effect(results, factor_values, factor_name):
    """
    Estimate the difference in success rate between the highest and
    lowest tested level of one factor.

    This is a perturbation-design summary, not a formal global
    variance-decomposition statistic.
    """
    if len(results) != len(factor_values):
        raise ValueError("results and factor_values must have equal length")

    results = np.asarray(results, dtype=bool)
    factor_values = np.asarray(factor_values)

    unique = np.unique(factor_values)
    if unique.size < 2:
        raise ValueError("factor must have at least two levels")

    low = unique.min()
    high = unique.max()

    low_rate = np.mean(results[factor_values == low])
    high_rate = np.mean(results[factor_values == high])

    return {
        "factor": factor_name,
        "low_level": low,
        "high_level": high,
        "low_success_rate": float(low_rate),
        "high_success_rate": float(high_rate),
        "effect_percentage_points": float(100.0 * (high_rate - low_rate)),
    }
