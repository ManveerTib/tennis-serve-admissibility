import numpy as np

from src.constants import (
    NET_DISTANCE,
    NET_HEIGHT_CENTER,
    NET_HEIGHT_POST,
    SERVICE_BOX_WIDTH,
    SERVICE_LINE_OFFSET,
)
from src.constraints import (
    net_height,
    is_inside_service_box,
    net_clearance,
    is_inside_service_depth,
    serve_is_legal,
)


def test_net_height_at_center():
    assert np.isclose(net_height(0.0), NET_HEIGHT_CENTER)


def test_net_height_at_post():
    assert np.isclose(
        net_height(SERVICE_BOX_WIDTH),
        NET_HEIGHT_POST,
    )


def test_net_height_is_symmetric():
    assert np.isclose(
        net_height(2.0),
        net_height(-2.0),
    )


def test_deuce_service_box_boundaries():
    assert is_inside_service_box(0.0, "deuce")
    assert is_inside_service_box(SERVICE_BOX_WIDTH, "deuce")
    assert not is_inside_service_box(-0.001, "deuce")


def test_ad_service_box_boundaries():
    assert is_inside_service_box(-SERVICE_BOX_WIDTH, "ad")
    assert is_inside_service_box(0.0, "ad")
    assert not is_inside_service_box(SERVICE_BOX_WIDTH + 0.001, "ad")


def test_invalid_service_side_raises_error():
    try:
        is_inside_service_box(0.0, "invalid")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for invalid target_side")


def test_net_clearance():
    y = 0.0
    z = NET_HEIGHT_CENTER + 0.10

    assert np.isclose(net_clearance(z, y), 0.10)


def test_service_depth_boundaries():
    service_line = NET_DISTANCE + SERVICE_LINE_OFFSET

    assert not is_inside_service_depth(NET_DISTANCE)
    assert not is_inside_service_depth(service_line)
    assert is_inside_service_depth(
        NET_DISTANCE + SERVICE_LINE_OFFSET / 2.0
    )


def test_legal_serve():
    service_line = NET_DISTANCE + SERVICE_LINE_OFFSET

    assert serve_is_legal(
        landing_x=NET_DISTANCE + 2.0,
        landing_y=2.0,
        net_z=NET_HEIGHT_CENTER + 0.10,
        net_y=0.0,
        target_side="deuce",
    )


def test_illegal_serve_fails_net_clearance():
    assert not serve_is_legal(
        landing_x=NET_DISTANCE + 2.0,
        landing_y=2.0,
        net_z=NET_HEIGHT_CENTER - 0.01,
        net_y=0.0,
        target_side="deuce",
    )


def test_illegal_serve_fails_service_depth():
    service_line = NET_DISTANCE + SERVICE_LINE_OFFSET

    assert not serve_is_legal(
        landing_x=service_line + 0.001,
        landing_y=2.0,
        net_z=NET_HEIGHT_CENTER + 0.10,
        net_y=0.0,
        target_side="deuce",
    )


def test_illegal_serve_fails_lateral_constraint():
    assert not serve_is_legal(
        landing_x=NET_DISTANCE + 2.0,
        landing_y=SERVICE_BOX_WIDTH + 0.001,
        net_z=NET_HEIGHT_CENTER + 0.10,
        net_y=0.0,
        target_side="deuce",
    )
