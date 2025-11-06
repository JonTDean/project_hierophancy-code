# Production APIs & Model Registry

## APIs
- Inference endpoints for partitioning, embeddings, and link prediction.
- Batch and streaming modes; schema for inputs/outputs (Graph JSON, edge lists).
- Versioned artifacts with metadata: seed, objective, backend, metrics.

## Ops
- Export TorchScript/ONNX where applicable; checksum-based caching; reproducibility manifests.
