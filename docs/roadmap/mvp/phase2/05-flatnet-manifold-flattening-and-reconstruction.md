# Manifold Flattening & Reconstruction (FlatNet‑style)

## Goal
Adopt a discrete geometric‑flow approach to flatten and reconstruct embedded submanifolds from samples, yielding interpretable encoder/decoder pairs.

## Plan
- `FlatteningFlowPort`:
  - `init(X)` or graph‑based inputs that yield local charts.
  - Iteratively construct maps that reduce extrinsic curvature (local models → global “convexification”).
  - Produce encoder `f` and decoder `g`; provide `reconstruction_error` utilities.
- Graph integration:
  - Use local neighborhoods (kNN on ambient or graph) to fit curvature terms per node.
  - Optionally regularize by edge weights/community structure.

## Acceptance
- On synthetic manifolds (Swiss roll, S‑curve, torus), achieve low reconstruction error and low geodesic distortion compared to spectral baselines.
