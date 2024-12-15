import numpy as np


def data_partitionable(seq_size: int) -> np.ndarray:
    """
    Generate np array for partition algorithm.
    Expected result of partition: True
    :param seq_size:
    :return:
    """
    result = np.ones(seq_size - 1, dtype=int)
    result = np.insert(result, np.random.choice(len(result), size=1), result.sum())
    return result


def data_not_partitionable(seq_size: int) -> np.ndarray:
    """
    Generate np array for partition algorithm.
    Expected result of partition: False
    :param seq_size:
    :return:
    """
    result = np.ones(seq_size - 1, dtype=int)
    result = np.insert(result, np.random.choice(len(result), size=1), result.sum() + 2)
    return result