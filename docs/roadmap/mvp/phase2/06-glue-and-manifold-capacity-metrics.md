# GLUE & Manifold Capacity — Representation Geometry Metrics

## Goal
Quantify how “untangled” representations are, and link geometric properties to computational efficiency.

## Metrics
- Manifold capacity (estimates of separability/packing).
- Intrinsic dimension estimates per class/community.
- Radius, margin, and curvature‑like summaries per representation layer.
- Alignment with community labels and partitions (before/after embedding).

## Adapters
- `ManifoldMetricsPort` implementing:
  - Capacity estimators on embeddings/eigenvectors.
  - Layer‑wise geometry tracking during algorithms (e.g., Leiden levels).

## Outputs
- Tables + plots over seeds/time; hooks for the Vector/Matrix/Graph visualizers.
