# docs/roadmap/03-leiden-plus.md

## Goal

Strengthen Leiden with resolution scanning, consensus clustering, and richer refine conditions while retaining current API.

## Enhancements

* **Resolution scan**: sweep γ ∈ [0.1, 3.0] with step or log grid; return Pareto frontier of (γ, #comms, score).
* **Consensus**: run K seeds, build co-association matrix, recluster with Leiden on that matrix.
* **Refine hooks**: configurable `theta` schedule; early stop on score plateau.

## API Additions

* `LeidenAdapter.detect_many(g, p0, objectives: list[ObjectivePort], gammas: list[float], seeds: int)`

## Acceptance Criteria

* Produces monotone trend (# communities vs γ) on standard graphs.
* Consensus stabilizes ARI across seeds on stochastic block model fixtures.
