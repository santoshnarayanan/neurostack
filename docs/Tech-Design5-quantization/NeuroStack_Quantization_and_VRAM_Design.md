# NeuroStack Technical Design

## Quantization and VRAM Interaction Architecture

------------------------------------------------------------------------

## 1. Purpose

This document explains how model quantization interacts with GPU VRAM
limits, and how it affects deployment feasibility, performance, and
hardware utilization.

------------------------------------------------------------------------

## 2. What is Quantization?

Quantization reduces the numerical precision of model weights:

-   FP32 (32-bit floating point)
-   FP16 (16-bit floating point)
-   INT8 (8-bit integer)
-   4-bit quantization (Q4)
-   2-bit experimental compression

Lower precision reduces memory footprint at the cost of some accuracy.

------------------------------------------------------------------------

## 3. VRAM Constraints in GPU Execution

When running LLMs on NVIDIA GPUs:

-   Model weights must fit inside VRAM
-   Activations also consume VRAM
-   CUDA kernels require memory allocation
-   Context window size increases memory consumption

Example (Approximate Memory Needs):

  Model Size   FP16     INT8     Q4
  ------------ -------- -------- ---------
  7B           \~14GB   \~7GB    \~3.5GB
  13B          \~26GB   \~13GB   \~6.5GB

------------------------------------------------------------------------

## 4. Diagram Placeholder -- Quantization vs VRAM Allocation

![Quantization vs VRAM Allocation](/docs/diagrams/phase3/quantization_vram_allocation.png)

Suggested Diagram Concept:

-   GPU VRAM block
-   Model weights portion
-   Activation memory portion
-   CUDA workspace portion
-   Comparison of FP16 vs INT8 vs Q4

------------------------------------------------------------------------

## 5. Execution Flow with Quantization

Client\
→ Control Plane\
→ Ollama Runtime\
→ Quantized Model Loader\
→ VRAM Allocation\
→ CUDA Tensor Execution

Quantization directly affects whether the model can be loaded into GPU
memory.

🔍 VRAM Memory Segmentation During Quantized Execution
![Actual Quantization–VRAM Technica Flow](/docs/diagrams/phase3/actual_quantization_vram_technical.png)

------------------------------------------------------------------------

## 6. Strategic Impact

Higher precision: - Better accuracy - Higher VRAM usage - May not fit
consumer GPUs

Lower precision: - Reduced VRAM usage - Faster memory transfers - Slight
accuracy trade-offs

------------------------------------------------------------------------

## 7. Conclusion

Quantization is a hardware-awareness strategy.

It determines: - Which models can run locally - Whether GPU acceleration
is possible - How efficiently VRAM is utilized

Understanding quantization is critical when designing GPU-backed AI
infrastructure.
