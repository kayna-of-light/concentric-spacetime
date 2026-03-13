"""Submit GPU-accelerated ODE batch to Azure ML."""

import argparse
import os
import sys
from pathlib import Path

# Suppress git metadata detection BEFORE importing azure.ai.ml
os.environ["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "0"
os.environ["GIT_DIR"] = ""
os.environ["MLFLOW_DISABLE_SOURCE_CODE_LOGGING"] = "true"

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parent
ENV_FILE = ROOT / "secrets" / "azure_ml.env"


def _load_env():
    """Load workspace config from secrets/azure_ml.env."""
    if not ENV_FILE.exists():
        print(f"ERROR: {ENV_FILE} not found.")
        print("Create it with AZURE_ML_SUBSCRIPTION_ID, AZURE_ML_RESOURCE_GROUP, etc.")
        sys.exit(1)
    cfg = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                cfg[k.strip()] = v.strip()
    return cfg


_CFG = _load_env()
SUBSCRIPTION_ID = _CFG["AZURE_ML_SUBSCRIPTION_ID"]
RESOURCE_GROUP = _CFG["AZURE_ML_RESOURCE_GROUP"]
WORKSPACE_NAME = _CFG["AZURE_ML_WORKSPACE"]
COMPUTE_TARGET = _CFG["AZURE_ML_GPU_COMPUTE"]
CPU_COMPUTE = _CFG["AZURE_ML_CPU_COMPUTE"]
EXPERIMENT_NAME = _CFG.get("AZURE_ML_EXPERIMENT", "ds-numerical-experiments")


def get_ml_client():
    """Connect to Azure ML workspace."""
    try:
        from azure.ai.ml import MLClient
        from azure.identity import DefaultAzureCredential
    except ImportError:
        print("ERROR: Azure ML SDK not installed.")
        print("  pip install azure-ai-ml azure-identity")
        sys.exit(1)

    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential,
        subscription_id=SUBSCRIPTION_ID,
        resource_group_name=RESOURCE_GROUP,
        workspace_name=WORKSPACE_NAME,
    )
    print(f"Connected to workspace: {ml_client.workspace_name}")
    return ml_client


def create_environment(ml_client, gpu: bool = True):
    """Use a curated AzureML environment."""
    # Use curated environment — avoid custom image builds
    return "azureml://registries/azureml/environments/sklearn-1.5/labels/latest"


def submit_benchmark(ml_client, T_max: int, gpu: bool = True, dry_run: bool = False):
    """Submit benchmark job."""
    from azure.ai.ml import command
    import tempfile

    compute = COMPUTE_TARGET if gpu else CPU_COMPUTE

    env_vars = {
        "MLFLOW_TRACKING_URI": "",
        "MLFLOW_DISABLE_SOURCE_CODE_LOGGING": "true",
    }

    jax_pkg = "jax[cuda12]" if gpu else "jax"
    install_cmd = f"pip install --quiet {jax_pkg} diffrax sympy && "

    # Change cwd to temp to prevent SDK git discovery
    orig_cwd = os.getcwd()
    os.chdir(tempfile.gettempdir())
    try:
        job = command(
            code=str(SCRIPTS_DIR),
            command=f"{install_cmd}python benchmark_gpu.py --T {T_max}",
            environment=create_environment(ml_client, gpu=gpu),
            compute=compute,
            experiment_name=EXPERIMENT_NAME,
            display_name=f"ode-batch-{T_max}",
            description=f"Numerical ODE batch integration, N={T_max}",
            environment_variables=env_vars,
        )

        if dry_run:
            print("\n--- DRY RUN ---")
            print(f"Compute: {compute}")
            print(f"GPU: {gpu}")
            print("(job not submitted)")
            return None

        submitted = ml_client.jobs.create_or_update(job)
    finally:
        os.chdir(orig_cwd)

    print(f"\nJob submitted: {submitted.name}")
    print(f"  Status: {submitted.status}")
    print(f"  Studio URL: {submitted.studio_url}")
    return submitted


def submit_custom_script(ml_client, script_path: str, gpu: bool = True, dry_run: bool = False):
    """Submit a custom script."""
    from azure.ai.ml import command
    import tempfile

    compute = COMPUTE_TARGET if gpu else CPU_COMPUTE

    env_vars = {
        "MLFLOW_TRACKING_URI": "",
        "MLFLOW_DISABLE_SOURCE_CODE_LOGGING": "true",
    }

    jax_pkg = "jax[cuda12]" if gpu else "jax"
    install_cmd = f"pip install --quiet {jax_pkg} diffrax sympy && "

    orig_cwd = os.getcwd()
    os.chdir(tempfile.gettempdir())
    try:
        job = command(
            code=str(SCRIPTS_DIR),
            command=f"{install_cmd}python {script_path}",
            environment=create_environment(ml_client, gpu=gpu),
            compute=compute,
            experiment_name=EXPERIMENT_NAME,
            display_name="ode-custom",
            description="Custom numerical computation",
            environment_variables=env_vars,
        )

        if dry_run:
            print(f"\n--- DRY RUN ---")
            print(f"Script: {script_path}")
            return None

        submitted = ml_client.jobs.create_or_update(job)
    finally:
        os.chdir(orig_cwd)

    print(f"\nJob submitted: {submitted.name}")
    print(f"  Studio URL: {submitted.studio_url}")
    return submitted


def main():
    parser = argparse.ArgumentParser(
        description="Submit ODE batch to Azure ML"
    )
    parser.add_argument("--benchmark", action="store_true",
                        help="Run the benchmark")
    parser.add_argument("--script", type=str, default=None,
                        help="Custom script to run")
    parser.add_argument("--T", type=int, default=5000,
                        help="T_max for benchmark (default: 5000)")
    parser.add_argument("--cpu", action="store_true",
                        help="Run on CPU compute instead of GPU")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show job config without submitting")
    args = parser.parse_args()

    ml_client = get_ml_client()
    gpu = not args.cpu

    if args.benchmark:
        submit_benchmark(ml_client, args.T, gpu=gpu, dry_run=args.dry_run)
    elif args.script:
        submit_custom_script(ml_client, args.script, gpu=gpu, dry_run=args.dry_run)
    else:
        print("Specify --benchmark or --script <path>")
        parser.print_help()


if __name__ == "__main__":
    main()
