# CNC Lathe Context Notes

## Machine & Controller
- **Lathe type**: Router-based CNC lathe with rotating B-axis (tool rotation).
- **Controller**: FluidNC (GRBL-like firmware).
- **Coordinate system**:
  - **X-axis**: Horizontal, radial direction (toward/away from spindle center).
  - **Z-axis**: Longitudinal, along spindle axis (toward/away from chuck).
  - **B-axis**: Rotation of router/spindle around pivot center.

## Goals
- Implement **tip-centric probing and mapping**:
  - Calibrate tool tip radius (Rt).
  - Determine pivot center (router center in machine coordinates).
  - Probe surfaces (inside/outside bowls, platters).
  - Remap virtual toolpaths (Xv, Zv) into machine coordinates (Xm, Zm).

## Key Equations
- **Forward transform** (virtual → machine):
  \[
  X_m = X_0 + X_v + R_t \cdot \cos(B)
  \]
  \[
  Z_m = Z_0 + Z_v + R_t \cdot \sin(B)
  \]

- **Tip radius from two contacts**:
  \[
  R_t = \frac{X_2 - X_1}{\cos B_2 - \cos B_1}
  \quad \text{or} \quad
  R_t = \frac{Z_2 - Z_1}{\sin B_2 - \sin B_1}
  \]

- **Pivot center from contact**:
  \[
  X_0 = X_m - R_t \cdot \cos(B), \quad Z_0 = Z_m - R_t \cdot \sin(B)
  \]

## Tool Tip vs Router Center
- The **router center (pivot)** is fixed in machine space.
- The **tool tip** is offset from pivot by radius Rt, rotated by angle B.
- Calibration ensures we can transform between virtual surface coordinates and machine coordinates.

## Probing Workflows

### Outside of Bowl/Platter
- Rotate tool tip to face outward (B ≈ 270°).
- Jog tip to touch outside surface.
- Record (Xv, Zv) virtual point and (Xm, Zm) machine point.
- Repeat at multiple angles/locations to build surface map.

### Inside of Bowl
- Rotate tool tip inward (B ≈ 90°).
- Jog tip to touch inside surface.
- Record mapping as above.
- Ensure ΔZ ≈ 0 between rotated contacts to confirm same physical point.

## Mapping Strategy
- Build a **probe map**: list of correspondences between virtual surface points and machine coordinates.
- After tool change:
  - Recalibrate Rt using a known contact and stored pivot.
  - Reuse probe map to remap cutting toolpaths.

## Notes for Copilot
- Always assume FluidNC/GRBL-style G-code.
- Use `G0` for safe retracts (Z only).
- ΔZ is a validation metric, not part of Rt calculation.
- Probing sequence: contact → retract Z → rotate B → contact again.