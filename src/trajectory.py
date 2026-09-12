"""
Trajectory calculations for the tennis serve model.

V1:
Gravity-only projectile motion.
"""


def projectile_derivative(t, state, g=9.81):
    """
    Return derivatives for a 2D projectile.

    State:
        [x, z, vx, vz]

    Returns:
        [dx/dt, dz/dt, dvx/dt, dvz/dt]
    """

    x, z, vx, vz = state

    return [
        vx,
        vz,
        0.0,
        -g
    ]
