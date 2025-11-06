# docs/roadmap/05-label-propagation-suite.md

## Goal

Implement Label Propagation (LPA) variants with weighted voting and semi‑supervised seeding.

## Variants

* Asynchronous LPA (queue like kernel’s local_move order)
* Semi-synchronous (grouped by random buckets)
* Weighted tie-break by total edge weight; optional random tiebreak with seed
* Seeded labels: keep seed nodes fixed

## API

* `src/lib/adapter/algorithms/label_propagation.py` implements `CommunityDetectionPort`
* Optional config dataclass `LPAConfig(max_iter: int, seeded: dict[BaseNode, int] | None, tie: str)`

## Acceptance Criteria

* Converges within `max_iter` on test graphs.
* With seeded labels, seeds never change; purity improves on SBM fixtures.
