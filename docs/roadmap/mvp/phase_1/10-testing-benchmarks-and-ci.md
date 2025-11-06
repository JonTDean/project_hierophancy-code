
# docs/roadmap/10-testing-benchmarks-and-ci.md

## Goal

Strong test suite, property tests, and performance checks.

## Tests

* Unit: Graph add/weight/degree/cut_weight/volume; Partition move/flatten invariants
* Property: aggregation then flattening equals flattening then union (on partitions)
* Objectives: Δ equals score diff within tolerance
* Algorithms: reference outputs on small fixtures; determinism under seed

## Benchmarks

* Graph sizes: 1e3, 1e4 nodes synthetic SBM; record time/levels/moves
* Memory profiling hooks

## CI Hooks

* Seeded tests; coverage ≥ 90% on domain/services and objectives
* Lint & type check (pyright/mypy), black/ruff config optional

## Acceptance Criteria

* All tests pass locally and in CI.
* Benchmark trends reported as markdown table artifacts.
