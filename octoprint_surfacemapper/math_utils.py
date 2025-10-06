def angle_delta(B1, B2):
    """Return the smallest difference between two angles in radians."""
    delta = (B2 - B1) % (2 * math.pi)
    if delta > math.pi:
        delta -= 2 * math.pi
    return abs(delta)
def compute_tangent_and_normal(pt1, pt2):
    """Given two probe points (Xt, Zt), compute tangent and normal vectors."""
    dx = pt2[0] - pt1[0]
    dz = pt2[1] - pt1[1]
    tangent = (dx, dz)
    # Normal is perpendicular: (-dz, dx)
    normal = (-dz, dx)
    return tangent, normal

def compute_B_from_normal(normal):
    """Compute B (radians) so tool is tangent to surface (normal direction)."""
    # atan2 returns angle of normal vector
    return math.atan2(normal[1], normal[0])

def adaptive_step_size(B_prev, B_curr, base_step, min_step=0.01, max_step=1.0):
    """
    Adjust step size based on rate of change of B (radians).
    The step size decreases as delta_B increases, and increases as delta_B decreases.
    sensitivity: higher values make step size more sensitive to changes in B.
    """
    sensitivity = 0.2  # You can tune this value
    delta_B = angle_delta(B_prev, B_curr)
    # Compute a scaling factor inversely proportional to delta_B
    scale = 1.0 / (1.0 + sensitivity * delta_B)
    step = base_step * scale
    # Clamp to min and max
    step = max(min_step, min(step, max_step))
    return step
import math

def tip_to_machine(Xt, Zt, B_rad, X0, Z0, R):
    """Convert tip coordinates to machine coordinates. B_rad and R are in radians."""
    Xm = X0 + Xt + R * math.cos(B_rad)
    Zm = Z0 + Zt + R * math.sin(B_rad)
    return Xm, Zm, B_rad

def machine_to_tip(Xm, Zm, B_rad, X0, Z0, R):
    """Convert machine coordinates to tip coordinates. B_rad and R are in radians."""
    Xt = Xm - X0 - R * math.cos(B_rad)
    Zt = Zm - Z0 - R * math.sin(B_rad)
    return Xt, Zt, B_rad
