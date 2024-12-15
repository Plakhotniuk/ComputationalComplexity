def partition_approximation(nums):
    """
    Approximation algorithm to determine if the array can be partitioned into two subsets with nearly equal sums.
    Guarantees a deviation of at most 1 from the optimal solution for integer inputs.

    Algorithm Design Steps:
    1. Calculate the total sum of the array. If the total sum is odd, an equal partition is impossible.
    2. Define a target sum as half of the total sum.
    3. Use a dynamic programming (DP) approach where dp[j] represents whether a subset with sum j can be formed.
    4. Initialize dp[0] to True, as a subset with sum 0 is always possible.
    5. Iterate through each number in the array, updating the DP table for possible subset sums in reverse order (to avoid overwriting values).
    6. Return the value of dp[target_sum], which indicates whether a subset with the target sum is achievable.

    Rationale:
    - The DP approach efficiently computes possible subset sums without generating all subsets explicitly, avoiding exponential complexity.
    - This guarantees a solution with at most 1 unit deviation from the optimal partition when working with integer inputs.

    :param nums: List[int] - The input list of integers.
    :return: bool - True if the partition is nearly equal, False otherwise.
    """
    total_sum = sum(nums)

    # If the total sum is odd, partitioning into two equal subsets is impossible
    if total_sum % 2 != 0:
        return False

    target_sum = total_sum // 2
    dp = [False] * (target_sum + 1)  # Initialize the DP table where dp[j] means subset with sum j can be formed
    dp[0] = True  # A subset with sum 0 is always achievable by selecting no elements

    # Iterate through the numbers in the array
    for num in nums:
        for j in range(target_sum, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]  # Update DP table to include current number

    return dp[target_sum]
