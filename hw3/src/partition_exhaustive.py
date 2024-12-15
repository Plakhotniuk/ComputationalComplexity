from itertools import combinations


def partition_exhaustive(nums):
    """
    Determine if the array can be partitioned into two subsets with equal sums using exhaustive search.
    :param nums: List[int] - The input list of integers.
    :return: bool - True if the partition exists, False otherwise.
    """
    total_sum = sum(nums)

    # If the total sum is odd, partitioning into two equal subsets is impossible
    if total_sum % 2 != 0:
        return False

    target_sum = total_sum // 2

    # Check all possible subsets
    for r in range(1, len(nums) + 1):  # Subset sizes from 1 to len(nums)
        for subset in combinations(nums, r):
            if sum(subset) == target_sum:
                return True

    return False


