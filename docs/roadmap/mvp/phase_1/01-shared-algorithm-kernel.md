# docs/roadmap/01-shared-algorithm-kernel.md

## Goal

Factor reusable building blocks (move/aggregate/refine/scan) so multiple algorithms (Leiden, Louvain, Label Propagation, Spectral) share one execution kernel.

## Why

Removes duplication, centralizes invariants (symmetry, supernodes), and gives consistent logging, determinism, and performance knobs.

## Public API (new/extended)

* `src/lib/port/algorithms/Kernel.py`

  ```python
  from typing import Protocol, Iterable, Optional
  from src.lib.domain.types.delta import DeltaFn
  from src.lib.domain.models.graph import Graph
  from src.lib.domain.models.partition import Partition

  class KernelPort(Protocol):
      def local_move(self, g: Graph, p: Partition, delta_fn: DeltaFn) -> Partition: ...
      def refine(self, g: Graph, p: Partition, *, delta_fn: DeltaFn, gamma: float, theta: float) -> Partition: ...
      def aggregate(self, g: Graph, p_refined: Partition) -> Graph: ...
      def multi_level(self, g: Graph, p0: Partition, *, delta_fn: DeltaFn, gamma: float, theta: float, max_levels: int) -> Partition: ...
  ```
* Backed by existing domain services: `move_nodes_fast`, `merge_nodes_subset`, `aggregate_graph`.

## Directory & Files

* `src/lib/adapter/algorithms/kernel.py` — concrete kernel using current services
* `src/lib/domain/services/kernel_invariants.py` — guards for symmetry, degree totals, partition soundness

## Invariants 

* Graph is undirected weighted. `adj[u][v] == adj[v][u]`.
* Supernodes are `frozenset[NodeLike]`; functions must accept/return them.
* Determinism controlled only by seed; all randomness comes from a kernel RNG.

## Instrumentation

* `KernelEvents` dataclass for counts: moves tried/applied, levels, deltas > 0, time per phase.
* Optional callbacks for progress.

## Acceptance Criteria

* Leiden re-implemented using `KernelPort.multi_level` with identical outputs (seeded).
* Louvain and Label Propagation can be implemented without touching services.
* Property tests: partition flattening and aggregation commute with kernel steps (see Testing doc).

## Open Questions

* Do we expose asynchronous local-move schedules, or keep queue semantics fixed?
* Per-node delta caches at kernel level or objective level?