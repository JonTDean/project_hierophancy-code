# Diffusion Maps & Laplacian Eigenmaps

## Goal
Embed data using graph‑based operators that respect local connectivity and smoothness.

## Adapters
- `DiffusionMaps(EmbeddingPort)`:
  - Build transition matrix `P = D^{-1}A`, eigenpairs of `P` or `L_rw`, diffusion time `t` scheduling.
- `LaplacianEigenmaps(EmbeddingPort)`:
  - Smallest non‑trivial eigenvectors of `L_sym` (drop eigenvalue 0), row‑normalize.

## Practicalities
- Degree‑normalization, α‑decay kernels for densities, anisotropic kernels if needed.
- Eigen solvers: ARPACK/LOBPCG; warm‑starts; deterministic seeds.

## Outputs
- Embedding matrix `Y ∈ R^{n×k}`, with node index mapping and eigenvalue spectrum for diagnostics.
