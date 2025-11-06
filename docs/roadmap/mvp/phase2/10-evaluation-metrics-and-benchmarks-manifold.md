# Evaluation & Benchmarks

## Metrics
- Trustworthiness / Continuity (local/global preservation).
- Mean geodesic distortion (graph geodesics vs. embedded Euclidean).
- Reconstruction error (when decoder exists).
- Injectivity violations (nearest‑neighbor inverses), crowding/tearing diagnostics.
- Runtime, memory, and determinism under seeds.

## Datasets
- Synthetic: Swiss roll, S‑curve, torus, spheres with noise; SBM graphs with manifold node positions.
- Domain: plug‑and‑play via Graph I/O (CSV, JSON, NetworkX).

## CI
- Regressions on metrics; track eigen‑spectrum changes; standardized plots as artifacts.
