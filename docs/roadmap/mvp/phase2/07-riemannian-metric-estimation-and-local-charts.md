# Local Charts & Riemannian Metric Estimation

## Goal
Approximate local tangent spaces and Riemannian metrics from samples/graphs.

## Methods
- For each node, take kNN neighborhood; perform local PCA/SVD for tangent estimation.
- Estimate metric tensor via local covariance; use for curvature‑related estimates and geodesic refinement.
- Stitch local charts to produce consistent coordinates (Procrustes alignment / overlap transition maps).

## Port
- `ChartPort`:
  - `fit(X or G)` returns local bases, chart radii, and consistency diagnostics.

## Uses
- Improve geodesic estimation; seed flattening flows; drive curvature‑aware edge reweighting.
