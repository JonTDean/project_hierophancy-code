# Phase 2 — Geometry & Manifold Program (Overview)
**Date:** 2025-11-06

## Goal
Integrate Euclidean and non‑Euclidean geometry methods to analyze, embed, flatten, and reconstruct manifolds represented through our Matrix/Vector/Graph primitives.

## Why
Community detection reveals discrete structure. Many datasets also live on (or near) low‑dimensional manifolds. Phase 2 adds continuous geometric structure—geodesics, Laplacians, curvature, local charts—to complement discrete partitions and enable faithful embeddings and reconstructions.

## Scope
- Manifold embeddings: Laplacian Eigenmaps, Diffusion Maps, Isomap (graph‑geodesic MDS), Spectral embeddings.
- Reconstruction: flattening via discrete flows and autoencoding (FlatNet‑style), inverse maps.
- Geometry estimation: kNN/ε‑graphs, local tangent/SVD charts, Riemannian metric approximation.
- Curvature and flows: curvature‑aware weights, (Forman/Ollivier) Ricci summaries, optional Ricci flow.
- Evaluation: Trustworthiness/Continuity, geodesic distortion, reconstruction error, injectivity checks.
- Visualization: coordinated Graph / Matrix / Eigenvector / Embedding scatter views.

## Architectural Fit (Ports/Adapters)
- Ports (proposals):
  - `EmbeddingPort`: `fit_transform(G|A|X) -> Embedding, Model` (with `inverse_transform` optional).
  - `GeodesicPort`: `pairwise_geodesic(G) -> DistMatrix` (graph shortest‑paths / diffusion distance).
  - `LaplacianPort`: `operators(G) -> L, L_rw, L_sym`.
  - `ChartPort`: local PCA/SVD charts and metric estimators on neighborhoods.
  - `CurvaturePort`: graph curvature metrics (summary per node/edge/community).
  - `FlatteningFlowPort`: layer‑wise flattening + reconstruction (FlatNet‑style).
  - `ManifoldMetricsPort`: trustworthiness/continuity/distortion/ARI vs partition & γ‑scans.
- Adapters: concrete implementations (`src/lib/adapter/{embeddings,geometry,curvature,flows,metrics}/...`).

## Deliverables
- Ten design docs (this set), stub ports, typed dataclasses for results, example notebooks/tests.
- Reusable visualizer hooks for embeddings and eigenvectors.

## References
- Bronstein et al., *Geometric Deep Learning: going beyond Euclidean data*, 2017 (survey).
- Psenka et al., *Representation Learning via Manifold Flattening and Reconstruction*, JMLR 2024.
- Chou et al., *Geometry Linked to Untangling Efficiency (GLUE)*, bioRxiv 2024/2025.
