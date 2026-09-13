"""
Trajectory calculations for the tennis serve model.

V1:
    Gravity-only projectile motion.

V2:
    Gravity + quadratic aerodynamic drag.
"""

import numpy as np

from .constants import (
    G,
    BALL_MASS,
    BALL_AREA,
    AIR_DENSITY,
    DRAG_COEFFICIENT,
)

from .aerodynamics import drag_acceleration


def projectile_derivative(t, state, g=G):
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


def trajectory_with_drag(
    t,
    state,
    g=G,
    mass=BALL_MASS,
    area=BALL_AREA,
    air_density=AIR_DENSITY,
    drag_coefficient=DRAG_COEFFICIENT
):
    """
    Return derivatives for a 2D tennis-ball trajectory
    including gravity and quadratic aerodynamic drag.

    State:
        [x, z, vx, vz]
    """

    x, z, vx, vz = state

    drag = drag_acceleration(
        np.array([vx, vz]),
        mass=mass,
        area=area,
        air_density=air_density,
        drag_coefficient=drag_coefficient
    )

    return np.array([
        vx,
        vz,
        drag[0],
        -g + drag[1]
    ])
