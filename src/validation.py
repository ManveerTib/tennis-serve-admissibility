"""
Validation and numerical-quality checks for the serve model.

V1-V10:
    Reusable assertions for physical, numerical, geometric,
    and empirical-analysis checks.
"""

import numpy as np


def assert_close(actual, expected, atol=1e-8, rtol=1e-8, label="value"):
    """Raise AssertionError unless actual and expected are sufficiently close."""
    if not np.allclose(actual, expected, atol=atol, rtol=rtol):
        raise AssertionError(
            f"{label} mismatch: actual={actual}, expected={expected}"
        )


def assert_monotonic(values, direction="decreasing", label="values"):
    """Assert monotonic non-increasing or non-decreasing behavior."""
    values = np.asarray(values, dtype=float)

    differences = np.diff(values)

    if direction == "decreasing":
        valid = np.all(differences <= 0.0)
    elif direction == "increasing":
        valid = np.all(differences >= 0.0)
    else:
        raise ValueError("direction must be 'increasing' or 'decreasing'")

    if not valid:
        raise AssertionError(f"{label} is not monotonic {direction}")


def assert_fraction(value, label="fraction"):
    """Assert that a reported fraction lies between zero and one."""
    value = float(value)

    if not 0.0 <= value <= 1.0:
        raise AssertionError(f"{label} must lie in [0, 1], got {value}")


def assert_positive_width(widths, label="widths"):
    """Assert that all admissibility widths are strictly positive."""
    widths = np.asarray(widths, dtype=float)

    if not np.all(widths > 0.0):
        raise AssertionError(f"{label} contains non-positive values")


def assert_finite(values, label="values"):
    """Assert that all supplied numerical values are finite."""
    values = np.asarray(values)

    if not np.all(np.isfinite(values)):
        raise AssertionError(f"{label} contains non-finite values")


def check_spin_reversal_symmetry(
    positive_values,
    negative_values,
    atol=1e-6,
):
    """
    Check approximate symmetry under spin reversal.

    Parameters
    ----------
    positive_values, negative_values : array-like
        Corresponding quantities evaluated at +spin and -spin.
    atol : float
        Absolute tolerance for the maximum discrepancy.

    Returns
    -------
    float
        Maximum absolute discrepancy.
    """
    positive_values = np.asarray(positive_values, dtype=float)
    negative_values = np.asarray(negative_values, dtype=float)

    if positive_values.shape != negative_values.shape:
        raise ValueError("Arrays must have matching shapes")

    error = float(np.max(np.abs(positive_values - negative_values)))

    if error > atol:
        raise AssertionError(
            f"Spin-reversal symmetry failed: max error={error}"
        )

    return error
