# docs/roadmap/02-objectives-and-delta-library.md

## Goal

Unify quality objectives and their exact/heuristic delta computations behind a Port. Keep current `DeltaFn` but add first‑class `ObjectivePort` that can compute both global score and per-move deltas.

## Public API (new)

* `src/lib/port/objective.py`

  ```python
  from typing import Protocol
  from src.lib.domain.models.graph import Graph
  from src.lib.domain.models.partition import Partition
  from src.lib.domain.types.delta import DeltaFn

  class ObjectivePort(Protocol):
      def delta_fn(self, g: Graph, p: Partition) -> DeltaFn: ...
      def score(self, g: Graph, p: Partition) -> float: ...
  ```

## Implementations (adapters)

* `src/lib/adapter/objectives/modularity.py` — Newman–Girvan modularity (weighted, undirected, self-loops ok)
* `src/lib/adapter/objectives/cpm.py` — Constant Potts Model with resolution γ
* `src/lib/adapter/objectives/conductance.py` — average/normalized cut
* `src/lib/adapter/objectives/heuristics.py` — current neighbor-weight delta as `ObjectivePort`

## Notes

* Exact ΔQ for modularity with supernodes requires tracking community degree sums; caching recommended.
* `score()` enables sanity checks and regression tests across algorithms.

## Acceptance Criteria

* Plug objective into Leiden/Louvain via `delta_fn(...)`; outputs stable across seeds.
* Unit tests verify Δ equals `score(after) - score(before)` within 1e-9 on random small graphs.