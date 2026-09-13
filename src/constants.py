"""
Physical and court constants for the tennis serve model.
"""

import numpy as np


# -------------------------
# Physical constants
# -------------------------

G = 9.81                    # gravitational acceleration, m/s^2

BALL_MASS = 0.0575          # tennis ball mass, kg
BALL_DIAMETER = 0.067       # tennis ball diameter, m
BALL_RADIUS = BALL_DIAMETER / 2.0
BALL_AREA = np.pi * BALL_RADIUS**2


# -------------------------
# Aerodynamic constants
# -------------------------

AIR_DENSITY = 1.21          # air density, kg/m^3

DRAG_COEFFICIENT = 0.55    # provisional constant drag coefficient


# -------------------------
# Court geometry
# -------------------------

NET_DISTANCE = 11.885               # baseline to net, m
SERVICE_LINE_OFFSET = 6.40          # net to service line, m
SERVICE_LINE_DISTANCE = 18.285      # baseline to service line, m

NET_HEIGHT_CENTER = 0.914            # center of net, m
NET_HEIGHT_POST = 1.07               # net post height, m

SERVICE_BOX_WIDTH = 4.115            # half-width of singles court/service box, m


# -------------------------
# Initial serve conditions
# -------------------------

CONTACT_HEIGHT = 3.0                 # initial test value, m

SERVE_SPEED_KMH = 200.0
SERVE_SPEED_MS = SERVE_SPEED_KMH / 3.6
