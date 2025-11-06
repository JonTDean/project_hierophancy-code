# docs/roadmap/09-graph-io-and-builders.md

## Goal

Standardize ingestion/serialization and additional builders.

## Builders

* `from_adj_list`, `from_coo`, `from_numpy_dense`, `from_pandas_edgelist`, `from_networkx`

## Serialization

* `to_json()` / `from_json()` (adjacency with weights and optional node metadata)
* Partition I/O: `Partition.to_json()`, `Partition.from_json()`

## Validation

* Check symmetry, non‑negative weights, isolated nodes allowed, self‑loop policy.

## Acceptance Criteria

* Round‑trip JSON preserves weights and supernodes.
* CSV edgelist load with dtype inference and weight defaulting works on examples.
