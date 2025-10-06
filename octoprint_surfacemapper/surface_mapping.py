import math
from .math_utils import tip_to_machine, compute_tangent_and_normal, compute_B_from_normal, adaptive_step_size

class SurfaceMapping:
    def __init__(self, safe_retract):
        self.safe_retract = safe_retract
        self.probe_points = []  # List of (Xt, Zt, B)

    def record_point(self, Xt, Zt, B):
        self.probe_points.append((Xt, Zt, B))

    def retract_above_surface(self, Xt, Zt, B, X0, Z0, R):
        # Move tip to SafeRetract units away from surface, opposite B
        Xm, Zm, _ = tip_to_machine(Xt, Zt, B, X0, Z0, R)
        Xm_retract = Xm - self.safe_retract * math.cos(B)
        Zm_retract = Zm - self.safe_retract * math.sin(B)
        return Xm_retract, Zm_retract, B

    def probe_surface(self, start, end, X0, Z0, R, initial_step, min_step, max_step):
        """
        start, end: (Xt, Zt, B) tuples
        initial_step: initial step size from GUI
        min_step, max_step: min/max step sizes from GUI
        """
        from .math_utils import machine_to_tip
        current = start
        prev_B = start[2]
        step = initial_step
        while True:
            if not self.probe_and_record(current, X0, Z0, R):
                self.handle_probe_failure(current)
                break

            # Check if at end point
            if self.is_at_end(current, end):
                # Probe the end point for accuracy
                if not self.probe_and_record(end, X0, Z0, R):
                    self.handle_probe_failure(end)
                    break
                break

            # Compute next probe location using last actual probed location
            last_actual = self.probe_points[-1] if len(self.probe_points) > 0 else current
            tangent, normal = compute_tangent_and_normal(last_actual, current)
            next_B = compute_B_from_normal(normal)
            # Update step size using last step, clamping handled in adaptive_step_size
            step = adaptive_step_size(prev_B, next_B, step, min_step, max_step)
            # Step along tangent from last actual probed location
            next_Xt = last_actual[0] + tangent[0] * step / math.hypot(*tangent)
            next_Zt = last_actual[1] + tangent[1] * step / math.hypot(*tangent)
            current = (next_Xt, next_Zt, next_B)
            prev_B = next_B
    def probe_and_record(self, tip_coords, X0, Z0, R):
        """
        Move to retract position, probe, and record contact if successful.
        Returns True if probe succeeded, False otherwise.
        """
        Xm_retract, Zm_retract, B = self.retract_above_surface(*tip_coords, X0, Z0, R)
        self.send_gcode_move(Xm_retract, Zm_retract, B)
        probe_result = self.send_grbl_probe(Xm_retract, Zm_retract, B)
        if probe_result:
            self.record_probe_contact(X0, Z0, R)
            return True
        return False
        # Integrate with OctoPrint GUI to indicate failure
        # For now, just print an error
        print(f"Probe failed at point: {failed_point}")

    def get_probe_contact_position(self):
        # Integrate with OctoPrint to get actual machine coordinates at probe contact
        # For now, this is a stub returning the commanded position
        # Replace with code to query OctoPrint for actual position after probe
        return (0.0, 0.0, 0.0)

    def send_gcode_move(self, Xm, Zm, B):
        # Stub: Implement OctoPrint G-code sending here
        pass

    def send_grbl_probe(self, Xm, Zm, B):
        # Stub: Implement GRBL probe command sending here
        return True  # Simulate successful probe

    def is_at_end(self, current, end, tol=1e-3):
        # Check if current probe location is at or past the end point
        return math.hypot(current[0] - end[0], current[1] - end[1]) < tol
