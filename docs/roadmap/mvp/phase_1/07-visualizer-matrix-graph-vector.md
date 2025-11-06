# docs/roadmap/07-visualizer-matrix-graph-vector.md

## Goal

Broaden the visualizer to cover three coordinated views: Graph (nodes/edges + hulls), Matrix (adjacency heatmap), and Vector (layouts, eigenvectors, membership vectors).

## Ports

* Extend `VisualizerPort` or add specialized ports:

  * `src/lib/port/visualizer_matrix.py` → `render_adjacency(G, order: list[NodeLike])`
  * `src/lib/port/visualizer_vector.py` → `render_vectors(vectors: dict[str, dict[NodeLike, float]])`

## Adapters

* `MatplotlibAdjacencyVisualizer` — heatmap, optional bandwidth reordering (seriation)
* `MatplotlibVectorVisualizer` — bar/line plots per vector, small multiples
* `PlotlyInteractiveVisualizer` (optional dependency) — hover, pan, save HTML

## Features

* Edge thickness by weight, loop rendering, cut edges highlighting
* Label overlays by community, centroid labels for supernodes
* Export: PNG, SVG, and JSON (positions + styles)

## Acceptance Criteria

* Given a partition, matrix view shows block structure after node ordering by community.
* Vector view plots eigenvector 1..k or membership score per node.
