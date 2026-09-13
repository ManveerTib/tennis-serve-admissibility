import numpy as np
import pytest

from src.validation import (
    assert_close,
    assert_finite,
    assert_fraction,
    assert_monotonic,
    assert_positive_width,
    check_spin_reversal_symmetry,
)


def test_assert_close_passes_for_close_values():
    assert_close(1.0, 1.0 + 1e-9)


def test_assert_close_rejects_different_values():
    with pytest.raises(AssertionError):
        assert_close(1.0, 1.1)


def test_assert_monotonic_decreasing():
    assert_monotonic(
        [5.0, 4.0, 3.0, 2.0],
        direction="decreasing",
    )


def test_assert_monotonic_increasing():
    assert_monotonic(
        [1.0, 2.0, 3.0, 4.0],
        direction="increasing",
    )


def test_assert_monotonic_rejects_wrong_direction():
    with pytest.raises(AssertionError):
        assert_monotonic(
            [1.0, 3.0, 2.0],
            direction="increasing",
        )


def test_assert_fraction():
    assert_fraction(0.5)


def test_assert_fraction_rejects_invalid_value():
    with pytest.raises(AssertionError):
        assert_fraction(1.1)


def test_assert_positive_width():
    assert_positive_width([0.1, 0.5, 1.0])


def test_assert_positive_width_rejects_zero():
    with pytest.raises(AssertionError):
        assert_positive_width([0.1, 0.0, 1.0])


def test_assert_finite():
    assert_finite([1.0, 2.0, 3.0])


def test_assert_finite_rejects_nan():
    with pytest.raises(AssertionError):
        assert_finite([1.0, np.nan, 3.0])


def test_spin_reversal_symmetry():
    positive = np.array([1.0, 2.0, 3.0])
    negative = np.array([1.0, 2.0, 3.0])

    error = check_spin_reversal_symmetry(
        positive,
        negative,
    )

    assert np.isclose(error, 0.0)


def test_spin_reversal_symmetry_rejects_large_error():
    positive = np.array([1.0, 2.0, 3.0])
    negative = np.array([1.0, 2.0, 4.0])

    with pytest.raises(AssertionError):
        check_spin_reversal_symmetry(
            positive,
            negative,
            atol=1e-6,
        )
