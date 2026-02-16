# 🧠 AI Data Plane Technical Design

## NeuroStack -- Phase 2 (LLM Runtime Deployment)

------------------------------------------------------------------------

# 1️⃣ Purpose

This document defines the **AI Data Plane architecture and
implementation details** for NeuroStack.

It focuses exclusively on:

-   LLM runtime deployment
-   GPU-backed inference execution
-   CUDA offloading lifecycle
-   Model quantization strategy
-   VRAM utilization
-   Performance validation
-   Runtime observability at inference level

This document complements:

-   `README.md` (Project Overview)
-   `technical_design.md` (Control Plane & System Architecture)
-   `infrastructure_design.md` (Host & GPU Enablement)

------------------------------------------------------------------------

# 2️⃣ Data Plane Philosophy

The AI Data Plane is responsible for:

> Deterministic, measurable, GPU-accelerated token generation.

Design Goals:

-   Local-first execution
-   Hardware-aware model sizing
-   Predictable VRAM allocation
-   Quantized model optimization
-   Clean separation from Control Plane logic
-   Measurable inference throughput

The Data Plane executes --- it does not orchestrate.

------------------------------------------------------------------------

# 3️⃣ Runtime Environment

## 🖥 Host Layer

-   Windows 11
-   NVIDIA Studio Driver 591.74
-   CUDA 13.x

## 🐧 Linux Execution Layer

-   WSL2 Ubuntu 24.04
-   Shared Windows NVIDIA driver bridge

## 🤖 LLM Runtime

-   Ollama v0.16.1
-   HTTP endpoint: http://127.0.0.1:11434
-   Model storage: \~/.ollama

------------------------------------------------------------------------

# 4️⃣ Model Configuration

## Primary Model

Model: `phi3:mini`\
Architecture: Phi-3\
Parameters: 3.8B\
Quantization: Q4_0\
Context Length: 131072

## Quantization Strategy

-   4-bit weight quantization
-   Reduces VRAM footprint
-   Enables 3B model to fit within 4GB VRAM
-   Minimal quality degradation

------------------------------------------------------------------------

# 5️⃣ GPU Offloading Architecture

Execution Flow:

User Prompt\
→ Ollama Service\
→ Model Loaded into VRAM\
→ CUDA Kernel Execution\
→ Token Generation\
→ Response Streaming

Under the hood:

Ollama\
↓\
CUDA Runtime (WSL2)\
↓\
Windows NVIDIA Driver\
↓\
RTX 3050 Ti (4GB VRAM)

------------------------------------------------------------------------

# 6️⃣ GPU Memory Management

Total GPU VRAM: 4GB\
Model Allocation: \~3.3GB\
Remaining Headroom: \~700MB

VRAM remains allocated while model is loaded in memory.

------------------------------------------------------------------------

# 7️⃣ Performance Characteristics

Observed GPU Metrics:

-   \~25--35 tokens/sec
-   \~3.3GB VRAM usage
-   GPU utilization: 30--50% during generation
-   GPU utilization: 0% when idle

CPU Fallback (Pre-driver update):

-   \~14 tokens/sec
-   \~200MB VRAM baseline only

------------------------------------------------------------------------

# 8️⃣ Inference Lifecycle States

1.  Model Load\
2.  Active Generation\
3.  Idle Warm State\
4.  Shutdown & VRAM Release

------------------------------------------------------------------------

# 9️⃣ Validation Commands

``` bash
nvidia-smi
ollama run phi3:mini --verbose
watch -n 0.5 nvidia-smi
```

------------------------------------------------------------------------

# 🔟 Failure Modes & Resolutions

GPU Not Used:

-   Update Windows NVIDIA Driver (591+)
-   Restart WSL (`wsl --shutdown`)
-   Restart Ollama service

------------------------------------------------------------------------

# 1️⃣1️⃣ Data Plane Boundaries

The AI Data Plane strictly performs:

-   Model loading
-   CUDA execution
-   Token generation
-   Runtime metrics exposure

Routing and orchestration belong to the Control Plane.

------------------------------------------------------------------------

# 🏁 Conclusion

The AI Data Plane provides:

-   Stable GPU-backed local inference
-   Deterministic execution path
-   Quantized model optimization
-   Measurable performance metrics
-   Clean separation from orchestration logic

------------------------------------------------------------------------

End of AI Data Plane Technical Design
