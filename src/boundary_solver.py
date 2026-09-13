"""
Boundary-finding and continuation utilities for the serve
admissibility envelope.

V5-V7:
    Numerical location of net and service-line boundaries and
    continuation of admissibility boundaries across model parameters.
"""

import numpy as np
from scipy.optimize import brentq


def _find_sign_change_root(function, lower, upper, samples=401):
    """Find the first root of a scalar function in an interval."""
    grid = np.linspace(lower, upper, samples)
    values = np.asarray([function(x) for x in grid], dtype=float)

    for i in range(len(grid) - 1):
        f0, f1 = values[i], values[i + 1]

        if not (np.isfinite(f0) and np.isfinite(f1)):
            continue

        if f0 == 0.0:
            return grid[i]

        if f0 * f1 < 0.0:
            return brentq(function, grid[i], grid[i + 1])

    raise ValueError("No sign-change root found in the supplied interval.")


def find_net_boundary(clearance_function, angle_bounds=(-30.0, 10.0)):
    """
    Find the launch-angle boundary where net clearance is zero.

    The supplied function must accept an angle in degrees and return
    net clearance in metres.
    """
    return _find_sign_change_root(
        clearance_function,
        angle_bounds[0],
        angle_bounds[1],
    )


def find_service_boundary(
    landing_x_function,
    angle_bounds=(-30.0, 10.0),
    service_line=6.40,
):
    """
    Find the launch-angle boundary where landing reaches the service line.

    The supplied function must accept an angle in degrees and return
    landing distance measured from the net in metres.
    """
    return _find_sign_change_root(
        lambda angle: landing_x_function(angle) - service_line,
        angle_bounds[0],
        angle_bounds[1],
    )


def find_lateral_boundary(
    landing_y_function,
    target_y,
    angle_bounds=(-30.0, 10.0),
):
    """
    Find the launch-angle boundary where lateral landing reaches target_y.
    """
    return _find_sign_change_root(
        lambda angle: landing_y_function(angle) - target_y,
        angle_bounds[0],
        angle_bounds[1],
    )


def continue_boundary(
    parameter_values,
    boundary_function,
):
    """
    Evaluate a boundary function sequentially across parameter values.

    Parameters
    ----------
    parameter_values : array-like
        Ordered parameter values such as speeds or spin rates.
    boundary_function : callable
        Function mapping one parameter value to a boundary value.

    Returns
    -------
    numpy.ndarray
        Boundary values in the same order as parameter_values.
    """
    parameter_values = np.asarray(parameter_values, dtype=float)

    return np.asarray(
        [boundary_function(value) for value in parameter_values],
        dtype=float,
    )
