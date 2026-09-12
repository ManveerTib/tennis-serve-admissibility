"""
Physical and court constants for the tennis serve model.
"""

# -------------------------
# Physical constants
# -------------------------

G = 9.81  # gravitational acceleration, m/s^2


# -------------------------
# Court geometry
# -------------------------

NET_DISTANCE = 11.885          # baseline to net, m
SERVICE_LINE_DISTANCE = 18.285 # baseline to service line, m
NET_HEIGHT_CENTER = 0.914      # center of net, m


# -------------------------
# Initial serve conditions
# -------------------------

CONTACT_HEIGHT = 3.0           # initial test value, m

SERVE_SPEED_KMH = 200.0
SERVE_SPEED_MS = SERVE_SPEED_KMH / 3.6
