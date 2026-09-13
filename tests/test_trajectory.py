import numpy as np

from src.trajectory import (
    projectile_derivative,
    trajectory_with_drag,
)


def test_projectile_derivative():
    state = np.array([0.0, 3.0, 50.0, 10.0])

    derivative = projectile_derivative(0.0, state)

    expected = np.array([
        50.0,
        10.0,
        0.0,
        -9.81,
    ])

    assert np.allclose(derivative, expected)


def test_projectile_has_no_horizontal_acceleration():
    state = np.array([0.0, 3.0, 50.0, 10.0])

    derivative = projectile_derivative(0.0, state)

    assert np.isclose(derivative[2], 0.0)


def test_projectile_gravity_acceleration():
    state = np.array([0.0, 3.0, 50.0, 10.0])

    derivative = projectile_derivative(0.0, state)

    assert np.isclose(derivative[3], -9.81)


def test_drag_reduces_horizontal_velocity():
    state = np.array([0.0, 3.0, 55.5556, 10.0])

    derivative = trajectory_with_drag(0.0, state)

    assert derivative[2] < 0.0


def test_drag_reduces_vertical_velocity():
    state = np.array([0.0, 3.0, 55.5556, 10.0])

    derivative = trajectory_with_drag(0.0, state)

    assert derivative[3] < -9.81


def test_zero_velocity_has_only_gravity():
    state = np.array([0.0, 3.0, 0.0, 0.0])

    derivative = trajectory_with_drag(0.0, state)

    expected = np.array([
        0.0,
        0.0,
        0.0,
        -9.81,
    ])

    assert np.allclose(derivative, expected)
