# docs/roadmap/04-louvain.md

## Goal

Add classic Louvain modularity optimization using the shared kernel and the modularity objective.

## API

* `src/lib/adapter/algorithms/louvain.py` implements `CommunityDetectionPort`.

## Design

* Phase 1: local moves (kernel).
* Phase 2: aggregate (kernel).
* Repeat until no improvement.

## Reuse

* Uses `ObjectivePort` for ΔQ.
* Same partition lift/aggregate as Leiden.

## Acceptance Criteria

* Matches NetworkX Louvain partition on small weighted graphs (up to permutation of labels).
* Deterministic under fixed seed and node visitation order.
