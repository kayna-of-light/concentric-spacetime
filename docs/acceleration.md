# Computation Acceleration Infrastructure

## Overview

The solenoid cascade ODE integration (210 branches × thousands of evaluation points) is the primary computational bottleneck. Three acceleration backends are available, each with different tradeoffs.

## Backend Comparison

| Backend | Module | Speedup vs scipy | Best For |
|---------|--------|-------------------|----------|
| **scipy** | `solenoid_system.py` | 1× (baseline) | Debugging, small T, compatibility |
| **numba** | `solenoid_numba.py` | ~5–15× | Multi-core CPU, no extra deps |
| **jax** | `solenoid_jax.py` | ~200× (CPU) | Production runs, large T |

### When to Use Each

- **scipy** (`backend='scipy'`): Default. Use for small explorations (T < 50), debugging ODE formulations, or when JAX is not installed. Safe, well-understood, no JIT overhead.

- **numba** (`backend='numba'`): Use when JAX is unavailable but you need better performance than scipy. Compiles the ODE RHS to native code via LLVM and uses `ProcessPoolExecutor` to bypass the GIL. First call triggers ~2–5s JIT compilation (cached to disk). On Windows, process spawning adds ~5–10s startup.

- **jax** (`backend='jax'`): **Recommended for all production work.** Uses `jax.vmap` to vectorize across all 210 branches in a single JIT-compiled function, then solves with Diffrax's Dopri8 (8th-order Runge-Kutta). First call includes ~10–30s JIT compilation; subsequent calls with same shapes are near-instant. The 200× speedup comes from JIT + vmap vectorization, not GPU parallelism.

### GPU vs CPU for This Workload

The cascade ODE is a **sequential time-stepping** problem — each step depends on the previous. GPU parallelism helps with `vmap` across branches, but device transfer overhead and the sequential nature of the solver negate the benefit for typical problem sizes:

| Platform | Backend | T=500, 210 branches | Notes |
|----------|---------|---------------------|-------|
| Local Intel CPU | scipy | 502.80s | Baseline |
| Local Intel CPU | JAX JIT+vmap | 2.34s | **215× speedup** |
| Azure ML E16s_v3 CPU | JAX JIT+vmap | 2.86s | Comparable to local |
| Azure ML V100 GPU | JAX JIT+vmap | 7.83s | Slower than CPU JAX |

**Bottom line:** JAX on CPU is optimal for this workload. GPU only makes sense if the problem scales to much larger branch counts or evaluation grids where the vmap dimension saturates GPU cores.

## Usage

### In Notebooks

```python
from solenoid_system import SolenoidSystem

sys0 = SolenoidSystem()
branches = sys0.all_branches()

# JAX backend (recommended)
results = sys0.integrate_all_branches(
    branches, t_eval, T_max, backend='jax'
)

# Scipy baseline (debugging)
results = sys0.integrate_all_branches(
    branches, t_eval, T_max, backend='scipy'
)
```

### Direct JAX Import

```python
from solenoid_jax import integrate_all_branches_jax, warmup, detect_device

print(detect_device())  # "CPU (N device(s))" or "GPU (Tesla V100-...)"
warmup()                # Pre-compile JIT (optional, avoids timing JIT in benchmarks)
results = integrate_all_branches_jax(branches, t_eval, T_max)
```

### Numerical Agreement

All three backends produce identical results within numerical tolerance:
- JAX vs scipy: max |diff| = 5.18e-09 (at T=500, 3819 crossings)
- Tolerances: rtol=1e-12, atol=1e-14

## Azure ML Remote Execution

For very large T or batch parameter sweeps, jobs can be submitted to Azure ML compute clusters.

### Prerequisites

1. **Azure credentials**: `az login` (uses DefaultAzureCredential)
2. **Configuration**: Create `secrets/azure_ml.env` (gitignored):
   ```env
   AZURE_ML_SUBSCRIPTION_ID=<subscription-id>
   AZURE_ML_RESOURCE_GROUP=<resource-group>
   AZURE_ML_WORKSPACE=<workspace-name>
   AZURE_ML_GPU_COMPUTE=<gpu-compute-target>
   AZURE_ML_CPU_COMPUTE=<cpu-compute-target>
   AZURE_ML_EXPERIMENT=ds-numerical-experiments
   ```
3. **SDK**: `pip install azure-ai-ml azure-identity`

### Submitting Jobs

```bash
# Benchmark on GPU (default)
python scripts/azure_ml_submit.py --benchmark --T 5000

# Benchmark on CPU compute
python scripts/azure_ml_submit.py --benchmark --T 5000 --cpu

# Custom script
python scripts/azure_ml_submit.py --script my_analysis.py

# Dry run (preview without submitting)
python scripts/azure_ml_submit.py --benchmark --T 5000 --dry-run
```

### Privacy & Discretion

The submit script includes several measures to prevent project information from appearing in shared Azure ML workspaces:

- **Git metadata suppression**: Changes cwd to a temp directory before SDK calls to prevent mlflow from discovering the git repo
- **Generic naming**: Experiment name, display names, and descriptions use neutral labels (configurable via `AZURE_ML_EXPERIMENT` in the .env file)
- **MLflow tracking disabled**: `MLFLOW_TRACKING_URI` set to empty, `MLFLOW_DISABLE_SOURCE_CODE_LOGGING` enabled
- **Auto-cleanup**: Delete jobs after downloading results to minimize visibility

### Architecture

The submit script uses a **curated AzureML environment** (`sklearn-1.5`) as the base, with JAX and Diffrax installed at runtime via pip. This avoids unreliable custom Docker image builds.

```
Local: python azure_ml_submit.py --benchmark --T 5000
  → Uploads scripts/ as code snapshot
  → Creates command job with pip install + benchmark_gpu.py
  → Cluster scales up, installs deps, runs benchmark
  → Results saved to outputs/results.npz
  → Download with: ml_client.jobs.download(job_name, ...)
```

## File Reference

| File | Purpose |
|------|---------|
| `scripts/solenoid_jax.py` | JAX/Diffrax vmap'd integration (Tier 2) |
| `scripts/solenoid_numba.py` | Numba JIT + ProcessPoolExecutor (Tier 1) |
| `scripts/solenoid_system.py` | Backend dispatch via `backend=` param |
| `scripts/benchmark_gpu.py` | Standalone benchmark for local/remote |
| `scripts/azure_ml_submit.py` | Azure ML job submission |
| `secrets/azure_ml.env` | Azure ML workspace config (gitignored) |
| `scripts/docker_env/Dockerfile` | Docker build context (legacy, superseded by curated env) |
| `scripts/azure_ml_env.yml` | Conda env spec (legacy) |

## Dependencies

**JAX backend** (recommended):
```bash
pip install jax diffrax          # CPU only
pip install jax[cuda12] diffrax  # GPU (CUDA 12)
```

**Numba backend**:
```bash
pip install numba  # Already in concentric env
```

**Azure ML** (remote execution only):
```bash
pip install azure-ai-ml azure-identity
```
