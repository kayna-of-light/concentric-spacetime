FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    numpy>=1.26 \
    scipy>=1.12 \
    sympy \
    jax[cuda12]>=0.4.35 \
    diffrax>=0.6
