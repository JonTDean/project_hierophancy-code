# TorchKernel & JAX Backends

## Goal
Run kernels and objectives on GPU with vectorized ops and autodiff.

## Features
- Torch-backed Laplacians, eigen-solvers (ARPACK wrappers or LOBPCG), and batched operations.
- RNG and seeding for determinism across CPU/GPU.
- Optional JAX backend for XLA compilation; common Port to swap backends.
