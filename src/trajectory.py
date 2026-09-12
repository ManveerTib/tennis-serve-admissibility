"""
Trajectory calculations for the tennis serve model.

V1:
    Gravity-only projectile motion.

V2:
    Gravity + quadratic aerodynamic drag.
"""

import numpy as np


def projectile_derivative(t, state, g=9.81):
    """
    Return derivatives for a 2D gravity-only projectile.

    State:
        [x, z, vx, vz]

    Returns:
        [dx/dt, dz/dt, dvx/dt, dvz/dt]
    """
    x, z, vx, vz = state

    return np.array([
        vx,
        vz,
        0.0,
        -g
    ])


def drag_acceleration(
    vx,
    vz,
    mass,
    area,
    air_density,
    drag_coefficient
):
    """
    Calculate acceleration caused by quadratic aerodynamic drag.

    Parameters
    ----------
    vx, vz : float
        Velocity components in m/s.
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
    ax, az : float
        Drag-induced acceleration components in m/s^2.
    """

    speed = np.sqrt(vx**2 + vz**2)

    if speed == 0:
        return 0.0, 0.0

    drag_factor = (
        -0.5
        * air_density
        * drag_coefficient
        * area
        * speed
        / mass
    )

    ax = drag_factor * vx
    az = drag_factor * vz

    return ax, az


def trajectory_with_drag(
    t,
    state,
    g=9.81,
    mass=0.0575,
    area=np.pi * (0.067 / 2)**2,
    air_density=1.21,
    drag_coefficient=0.55
):
    """
    Return derivatives for a 2D tennis-ball trajectory
    including gravity and quadratic aerodynamic drag.

    State:
        [x, z, vx, vz]
    """

    x, z, vx, vz = state

    ax_drag, az_drag = drag_acceleration(
        vx,
        vz,
        mass,
        area,
        air_density,
        drag_coefficient
    )

    return np.array([
        vx,
        vz,
        ax_drag,
        -g + az_drag
    ])
