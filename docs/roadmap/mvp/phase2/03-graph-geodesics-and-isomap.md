# Geodesic Distances & Isomap

## Goal
Estimate manifold geodesics from the graph and use them for distance‑preserving embeddings.

## Components
- `GeodesicPort` with algorithms:
  - Shortest paths on weighted graphs (Dijkstra/Johnson, sparse).
  - kNN graph + reciprocal symmetrization + edge weights via metric in ambient space (optional).
  - Diffusion distances (via eigenpairs of the Markov operator).
- `IsomapAdapter(EmbeddingPort)`:
  - 1) Build kNN graph (or use given), 2) All‑pairs geodesics, 3) Classical MDS on distances.

## Options
- Landmark Isomap for scalability.
- Handling disconnected components: largest component or infinite‑distance handling.

## Evaluation
- Geodesic distortion, trustworthiness/continuity vs. target dimension.
