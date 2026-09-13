"""
Court-geometry and serve-legality constraints.

V4:
    Net geometry, service-box boundaries, landing depth,
    net clearance, and overall serve legality.
"""

import numpy as np

from .constants import (
    NET_DISTANCE,
    NET_HEIGHT_CENTER,
    NET_HEIGHT_POST,
    SERVICE_BOX_WIDTH,
    SERVICE_LINE_OFFSET,
)


def net_height(y):
    """
    Return the net height at lateral position y.

    The model uses linear interpolation from the center of the
    net to the post height, then clips the value at the post height.

    Parameters
    ----------
    y : float or array-like
        Lateral court coordinate in metres.

    Returns
    -------
    float or numpy.ndarray
        Net height in metres.
    """

    y = np.asarray(y)

    return (
        NET_HEIGHT_CENTER
        + (NET_HEIGHT_POST - NET_HEIGHT_CENTER)
        * np.minimum(np.abs(y) / SERVICE_BOX_WIDTH, 1.0)
    )


def is_inside_service_box(y, target_side="deuce"):
    """
    Determine whether a landing point is inside the requested
    singles service box laterally.

    Parameters
    ----------
    y : float
        Lateral landing coordinate in metres.
    target_side : {"deuce", "ad"}
        Target service-box side.

    Returns
    -------
    bool
        True if y lies inside the requested service box.
    """

    if target_side == "deuce":
        return 0.0 <= y <= SERVICE_BOX_WIDTH

    if target_side == "ad":
        return -SERVICE_BOX_WIDTH <= y <= 0.0

    raise ValueError("target_side must be 'deuce' or 'ad'")


def net_clearance(z, y):
    """
    Calculate vertical clearance above the net.

    Parameters
    ----------
    z : float
        Ball height at the net crossing, in metres.
    y : float
        Lateral coordinate at the net crossing, in metres.

    Returns
    -------
    float
        Ball height above the local net height, in metres.
    """

    return z - net_height(y)


def is_inside_service_depth(x):
    """
    Determine whether a landing point lies between the net
    and the service line.

    Parameters
    ----------
    x : float
        Longitudinal landing coordinate measured from the net,
        with the receiving court extending in the positive x direction.

    Returns
    -------
    bool
        True if the point is strictly between the net and service line.
    """

    return NET_DISTANCE < x < NET_DISTANCE + SERVICE_LINE_OFFSET


def serve_is_legal(
    landing_x,
    landing_y,
    net_z,
    net_y,
    target_side="deuce",
):
    """
    Determine whether a modeled serve satisfies the geometric
    legality constraints.

    A serve is legal in this model if:
        1. The ball clears the local net height.
        2. It lands between the net and service line.
        3. It lands inside the requested service box laterally.

    Parameters
    ----------
    landing_x : float
        Longitudinal landing position measured from the baseline
        coordinate system used by the trajectory model.
    landing_y : float
        Lateral landing position in metres.
    net_z : float
        Ball height at the net crossing in metres.
    net_y : float
        Lateral coordinate at the net crossing in metres.
    target_side : {"deuce", "ad"}
        Target service-box side.

    Returns
    -------
    bool
        True if all modeled legality constraints are satisfied.
    """

    return (
        net_clearance(net_z, net_y) > 0.0
        and is_inside_service_depth(landing_x)
        and is_inside_service_box(landing_y, target_side)
    )
