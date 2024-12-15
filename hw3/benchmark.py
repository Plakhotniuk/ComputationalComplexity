import time

from hw3.utils.data_generation import data_not_partitionable
from hw3.src.partition_approximation import partition_approximation
from hw3.src.partition_exhaustive import partition_exhaustive
from typing import Callable


def benchmark_partition(partition_func: Callable[[list], bool], input_sizes: list):
    """
    Benchmark the partition functions on increasing input sizes.
    The benchmark results demonstrate the difference in time complexity between
    the exhaustive search (O(2^n)) and the dynamic programming approximation (O(n*sum(nums))).

    Observations:
    - As input size increases, the runtime for the exhaustive approach grows exponentially,
      making it infeasible for larger inputs.
    - The DP-based approximation scales more efficiently with both the size of the array and
      the range of subset sums, providing solutions in a fraction of the time required by the
      exhaustive method.
    """
    times_av = []
    samples_num = 10
    for size in input_sizes:
        total_time = 0
        for i in range(samples_num):
            nums = data_not_partitionable(size).tolist()
            start_time_exact = time.perf_counter()
            partition_func(nums)
            elapsed_time_exact = time.perf_counter() - start_time_exact
            total_time += elapsed_time_exact
        times_av.append(total_time / samples_num)

    return times_av


if __name__ == "__main__":

    input_sizes = [4, 6, 8, 10, 12, 14, 16]
    times_exhaustive = benchmark_partition(partition_func=partition_exhaustive, input_sizes=input_sizes)
    times_approx = benchmark_partition(partition_func=partition_approximation, input_sizes=input_sizes)

    print("Average times exhaustive: ", times_exhaustive)
    print("Average times approx: ", times_approx)
