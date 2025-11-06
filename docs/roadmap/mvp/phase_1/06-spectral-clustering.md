# docs/roadmap/06-spectral-clustering.md

## Goal

Add spectral clustering using the normalized Laplacian and k‑means on first k eigenvectors.

## Design

* Build L = D^{-1/2}(D−A)D^{-1/2} from `Graph` (treat supernodes as expanded weight sums).
* Compute top‑k smallest eigenvectors (scipy optional dependency; or power method fallback).
* k selection: eigengap heuristic.

## API

* `src/lib/adapter/algorithms/spectral.py` implements `CommunityDetectionPort`
* `src/lib/domain/services/matrix.py` — helpers to construct dense/CSR matrices from `Graph`

## Acceptance Criteria

* Recovers known blocks on SBM fixtures.
* Unit tests check Laplacian PSD and symmetry.