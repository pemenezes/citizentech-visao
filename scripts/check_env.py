"""Mostra GPU, VRAM e versões do ambiente de visão. Não baixa modelos."""

from __future__ import annotations

import importlib
import os
import platform
import sys


MODULES = (
    "torch",
    "torchvision",
    "cv2",
    "ultralytics",
    "supervision",
    "pandas",
    "matplotlib",
    "yaml",
    "dotenv",
)


def version_of(name: str) -> str:
    try:
        module = importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001 — diagnóstico de ambiente
        return f"ausente ({exc.__class__.__name__}: {exc})"
    return str(getattr(module, "__version__", "importado"))


def main() -> int:
    print(f"python {sys.version.replace(chr(10), ' ')}")
    print(f"executable {sys.executable}")
    print(f"platform {platform.platform()}")
    for name in MODULES:
        print(f"{name}: {version_of(name)}")

    for key in (
        "HF_HOME",
        "TORCH_HOME",
        "PIP_CACHE_DIR",
        "YOLO_CONFIG_DIR",
        "CV_DATA_DIR",
        "TMP",
        "TEMP",
    ):
        print(f"{key}={os.environ.get(key, '')}")

    try:
        import torch
    except Exception as exc:  # noqa: BLE001
        print(f"torch_check_failed {exc}")
        return 1

    print(f"cuda_build {torch.version.cuda}")
    print(f"cuda_available {torch.cuda.is_available()}")
    if not torch.cuda.is_available():
        print("gpu ausente para o PyTorch")
        return 1

    print(f"gpu {torch.cuda.get_device_name(0)}")
    print(f"capability {torch.cuda.get_device_capability(0)}")
    free, total = torch.cuda.mem_get_info()
    print(f"vram_free_mib {free / 1024 ** 2:.0f}")
    print(f"vram_total_mib {total / 1024 ** 2:.0f}")
    props = torch.cuda.get_device_properties(0)
    print(f"vram_device_mib {props.total_memory / 1024 ** 2:.0f}")

    # Confere que um kernel CUDA realmente executa nesta GPU (sm_75).
    tensor = torch.zeros(1, device="cuda")
    torch.cuda.synchronize()
    print(f"kernel_ok {tensor.device}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
