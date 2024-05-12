import numpy as np
import random
import torch

def set_seed(seed):
    """
    Set the seed for random intialization and set
    CUDANN parameters to ensure determmihstic results across
    multiple runs with the same seed

    :param seed: int
    """
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.enabled = False