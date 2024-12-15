from hw3.src.partition_exhaustive import partition_exhaustive
from hw3.src.partition_approximation import partition_approximation
from hw3.utils.data_generation import data_partitionable, data_not_partitionable
from pytest import mark

test_cases = [
    ([1, 5, 11, 5], True),
    ([1, 2, 3, 5], False),
    ([3, 3, 3, 4, 5], True),
    ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10], True),
    ([2, 2, 2, 2, 2, 10], True),
    (data_partitionable(50).tolist(), True),
    (data_not_partitionable(15).tolist(), False),
]

@mark.parametrize('data, expected_result', test_cases)
def test_partition(data: list, expected_result: bool):
    """
    Test the partition functions with a set of predefined and random inputs.
    """

    result_exact = partition_exhaustive(data)
    result_approx = partition_approximation(data)

    assert result_exact == expected_result
    assert result_approx == expected_result