import multiprocessing
import os
import random
from typing import List, Optional

import numpy as np
import torch

_SEED: Optional[int] = None


def get_balanced_devices(
    count: Optional[int] = None,
    use_cuda: bool = True,
    cuda_ids: Optional[List[int]] = None,
) -> List[str]:
    count = count if count is not None else multiprocessing.cpu_count()
    if use_cuda and torch.cuda.is_available():
        if cuda_ids is not None:
            devices = [f"cuda:{id_}" for id_ in cuda_ids]
        else:
            devices = [f"cuda:{id_}" for id_ in range(torch.cuda.device_count())]
    else:
        devices = ["cpu"]
    factor = int(count / len(devices))
    remainder = count % len(devices)
    devices = devices * factor + devices[:remainder]
    return devices


def set_seed_number(seed: int):
    global _SEED
    _SEED = seed


def set_seeds():
    torch.manual_seed(_SEED)
    random.seed(_SEED)
    np.random.seed(_SEED)
    torch.cuda.manual_seed(_SEED)
    torch.cuda.manual_seed_all(_SEED)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    os.environ["PYTHONHASHSEED"] = str(_SEED)


def set_device(device: str):
    global _DEVICE
    _DEVICE = torch.device(device)


def get_device() -> torch.device:
    return _DEVICE
