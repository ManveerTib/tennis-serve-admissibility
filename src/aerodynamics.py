"""
Aerodynamic calculations for the tennis serve model.

V2:
    Quadratic aerodynamic drag.

V3:
    Spin-dependent Magnus acceleration.
"""

import numpy as np

from .constants import (
    AIR_DENSITY,
    BALL_AREA,
    BALL_MASS,
    BALL_RADIUS,
    DRAG_COEFFICIENT,
)


def drag_acceleration(
    velocity,
    mass=BALL_MASS,
    area=BALL_AREA,
    air_density=AIR_DENSITY,
    drag_coefficient=DRAG_COEFFICIENT,
):
    """
    Calculate the acceleration caused by quadratic aerodynamic drag.

    Parameters
    ----------
    velocity : array-like
        Velocity vector in m/s.
    mass : float
        Ball mass in kg.
    area : float
        Ball cross-sectional area in m^2.
    air_density : float
        Air density in kg/m^3.
    drag_coefficient : float
        Dimensionless drag coefficient.

    Returns
    -------
    numpy.ndarray
        Drag-induced acceleration vector in m/s^2.
    """

    velocity = np.asarray(velocity, dtype=float)
    speed = np.linalg.norm(velocity)

    if speed == 0.0:
        return np.zeros_like(velocity)

    drag_factor = (
        -0.5
        * air_density
        * drag_coefficient
        * area
        * speed
        / mass
    )

    return drag_factor * velocity


def lift_coefficient(speed, spin_speed):
    """
    Calculate the provisional spin-dependent lift coefficient.

    Parameters
    ----------
    speed : float
        Ball speed in m/s.
    spin_speed : float
        Surface spin speed r*omega in m/s.

    Returns
    -------
    float
        Dimensionless lift coefficient.
    """

    if speed <= 0.0 or spin_speed <= 0.0:
        return 0.0

    return 1.0 / (2.0 + speed / spin_speed)


def magnus_acceleration(
    velocity,
    omega,
    mass=BALL_MASS,
    area=BALL_AREA,
    air_density=AIR_DENSITY,
):
    """
    Calculate the 3D Magnus acceleration.

    The direction follows the model convention

        omega_hat x velocity_hat.

    Parameters
    ----------
    velocity : array-like
        Ball velocity vector in m/s.
    omega : array-like
        Angular-velocity vector in rad/s.
    mass : float
        Ball mass in kg.
    area : float
        Ball cross-sectional area in m^2.
    air_density : float
        Air density in kg/m^3.

    Returns
    -------
    numpy.ndarray
        Magnus acceleration vector in m/s^2.
    """

    velocity = np.asarray(velocity, dtype=float)
    omega = np.asarray(omega, dtype=float)

    speed = np.linalg.norm(velocity)
    spin_rate = np.linalg.norm(omega)

    if speed == 0.0 or spin_rate == 0.0:
        return np.zeros(3)

    velocity_hat = velocity / speed
    omega_hat = omega / spin_rate

    spin_speed = BALL_RADIUS * spin_rate
    lift_coefficient_value = lift_coefficient(speed, spin_speed)

    magnus_direction = np.cross(omega_hat, velocity_hat)

    force_magnitude = (
        0.5
        * air_density
        * area
        * lift_coefficient_value
        * speed**2
    )

    return (
        force_magnitude
        * magnus_direction
        / mass
    )
