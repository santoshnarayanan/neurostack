# 🏗 NVIDIA AI Control Plane (NACP)

## Infrastructure & Runtime Technical Design

------------------------------------------------------------------------

# 1️⃣ Purpose

This document describes the **Infrastructure Foundation** of the NVIDIA
AI Control Plane (NACP).

It covers:

-   Host operating environment
-   GPU enablement architecture
-   WSL2 Linux bridge design
-   Docker runtime configuration
-   NVIDIA Container Toolkit integration
-   Execution flow for GPU inference
-   Rebuild & disaster recovery strategy

This document complements `technical_design.md`, which focuses on
Control Plane and orchestration logic.

------------------------------------------------------------------------

# 2️⃣ Infrastructure Philosophy

NACP follows a **Local-First, GPU-Native Architecture**.

Design goals:

-   Deterministic runtime behavior
-   Reproducible container execution
-   Hardware-aware optimization
-   Clear separation between host, kernel bridge, and container runtime
-   Minimal virtualization overhead

------------------------------------------------------------------------

# 3️⃣ Host Environment

## 🖥 Operating System

-   Windows 11 (Primary Host)

## 🎮 GPU Hardware

-   NVIDIA RTX 3050 Ti (4GB VRAM)
-   CUDA-enabled
-   Tensor Cores active

## 🧩 NVIDIA Driver

-   Windows NVIDIA Driver (v512.78)
-   CUDA 11.6 host compatibility

The Windows driver remains the authoritative GPU driver.

------------------------------------------------------------------------

# 4️⃣ WSL2 Linux Bridge Architecture

## 🐧 WSL2 (Ubuntu 24.04)

WSL2 provides:

-   A lightweight Linux kernel
-   Direct GPU passthrough
-   CUDA compatibility layer
-   Shared driver integration with Windows host

WSL2 acts as a **Linux kernel bridge**, enabling Docker to run
Linux-native GPU workloads on Windows.

### Execution Flow

    Container (Ollama / PyTorch)
        ↓
    Docker Engine
        ↓
    NVIDIA Container Runtime
        ↓
    WSL2 Linux Kernel
        ↓
    Windows NVIDIA Driver
        ↓
    RTX 3050 Ti GPU

WSL2 is not a virtual machine in the traditional sense.\
It provides near-native performance with minimal overhead.

------------------------------------------------------------------------

# 5️⃣ Docker Runtime Configuration

## 🐳 Docker Desktop (WSL Backend)

-   Uses WSL2 backend
-   GPU-enabled via NVIDIA Container Toolkit
-   Runtime registered: `nvidia`

Validation command:

    docker info | findstr -i nvidia

Expected output:

    Runtimes: io.containerd.runc.v2 nvidia runc

------------------------------------------------------------------------

# 6️⃣ NVIDIA Container Toolkit

Installed inside WSL2 Ubuntu.

Responsibilities:

-   Registers NVIDIA runtime
-   Enables `--gpus all` flag
-   Bridges Docker containers to host GPU

Verification:

    docker run --rm --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi

------------------------------------------------------------------------

# 7️⃣ GPU Inference Lifecycle

When an LLM inference request is executed:

    User Request
        ↓
    FastAPI (Control Plane)
        ↓
    Ollama Container
        ↓
    Docker NVIDIA Runtime
        ↓
    WSL2 Kernel
        ↓
    Windows NVIDIA Driver
        ↓
    RTX 3050 Ti executes CUDA kernels
        ↓
    Inference output returned to container
        ↓
    Response returned to API

GPU is engaged only during model inference.

Database operations remain CPU-bound.

![GPU reference cycle](/docs/diagrams/phase3/gpu_inference_cycle.png)

------------------------------------------------------------------------

# 8️⃣ Containerization Strategy

All AI runtime components are containerized:

-   LLM runtime (Ollama)
-   Embedding service (future phase)
-   Graph reasoning adapters (future phase)

Container flags include:

-   `--gpus all`
-   `--restart unless-stopped`
-   Persistent volume mounting for model storage

Example deployment:

    docker run -d \
      --gpus all \
      -p 11434:11434 \
      --name ollama \
      --restart unless-stopped \
      -v ollama_data:/root/.ollama \
      ollama/ollama

------------------------------------------------------------------------

# 9️⃣ Parallel Execution Considerations

Infrastructure supports:

-   Concurrent CPU-based retrieval tasks
-   GPU-based inference tasks
-   Asynchronous orchestration from Control Plane

Resource contention is monitored via:

-   GPU utilization
-   VRAM usage
-   Token throughput

------------------------------------------------------------------------

# 🔟 Observability at Infrastructure Layer

Metrics available:

-   `nvidia-smi` GPU metrics
-   Docker container stats
-   Token/sec from LLM runtime
-   Latency per execution stage

Future integration planned:

-   Prometheus exporters
-   Structured metrics aggregation

------------------------------------------------------------------------

# 1️⃣1️⃣ Rebuild & Disaster Recovery Strategy

Infrastructure can be rebuilt via scripted steps:

## Windows Layer

-   Install NVIDIA Driver
-   Enable WSL2

## WSL2 Layer

-   Install Ubuntu
-   Install NVIDIA Container Toolkit
-   Configure Docker runtime

## Container Layer

-   Redeploy containers via Docker Compose
-   Restore volumes

This enables deterministic infrastructure recovery.

------------------------------------------------------------------------

# 1️⃣2️⃣ Current Infrastructure Status

  Layer                       Status
  --------------------------- ----------------
  Windows Host                ✅ Stable
  NVIDIA Driver               ✅ Active
  WSL2 GPU Bridge             ✅ Operational
  Docker NVIDIA Runtime       ✅ Registered
  CUDA Container Validation   ✅ Passed
  PyTorch GPU Validation      ✅ Passed

------------------------------------------------------------------------

# 🏁 Conclusion

The NACP infrastructure foundation provides:

-   Stable GPU-backed local inference
-   Minimal-overhead Linux bridge via WSL2
-   Containerized reproducibility
-   Deterministic execution path
-   Enterprise-ready separation between host, runtime, and orchestration
    layers

This infrastructure layer forms the compute backbone for:

-   Control Plane orchestration
-   Hybrid reasoning workflows
-   Retrieval-Augmented Generation
-   Graph reasoning extensions

------------------------------------------------------------------------

End of Infrastructure Technical Design Document
