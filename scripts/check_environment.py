"""Print and validate the minimum local environment for stage 0."""

from __future__ import annotations

import platform
import sys

import torch


def choose_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def main() -> None:
    device = choose_device()
    tensor = torch.tensor([1.0, 2.0, 3.0], device=device)
    result = float(tensor.sum().cpu())
    if result != 6.0:
        raise RuntimeError(f"Unexpected tensor result: {result}")

    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    print(f"Selected device: {device}")
    print("Tensor smoke test: PASS")


if __name__ == "__main__":
    main()
