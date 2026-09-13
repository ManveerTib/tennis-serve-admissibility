import numpy as np

from src.aerodynamics import (
    drag_acceleration,
    lift_coefficient,
    magnus_acceleration,
)
from src.constants import (
    BALL_AREA,
    BALL_MASS,
    BALL_RADIUS,
)


def test_drag_points_opposite_velocity():
    velocity = np.array([55.5556, 0.0])

    acceleration = drag_acceleration(velocity)

    assert acceleration[0] < 0.0
    assert acceleration[1] == 0.0


def test_drag_is_zero_at_zero_velocity():
    velocity = np.array([0.0, 0.0])

    acceleration = drag_acceleration(velocity)

    assert np.allclose(acceleration, np.zeros(2))


def test_lift_coefficient_is_zero_without_spin():
    assert lift_coefficient(55.5556, 0.0) == 0.0


def test_lift_coefficient_is_positive_with_spin():
    value = lift_coefficient(55.5556, BALL_RADIUS * 100.0)

    assert value > 0.0


def test_magnus_acceleration_zero_without_spin():
    velocity = np.array([55.5556, 0.0, 0.0])
    omega = np.array([0.0, 0.0, 0.0])

    acceleration = magnus_acceleration(velocity, omega)

    assert np.allclose(acceleration, np.zeros(3))


def test_magnus_direction():
    velocity = np.array([55.5556, 0.0, 0.0])
    omega = np.array([0.0, 100.0, 0.0])

    acceleration = magnus_acceleration(velocity, omega)

    assert acceleration[2] < 0.0
    assert np.isclose(acceleration[0], 0.0)
    assert np.isclose(acceleration[1], 0.0)
