import matplotlib.pyplot as plt
from benchmark import benchmark_partition
from hw3.src.partition_exhaustive import partition_exhaustive
from hw3.src.partition_approximation import partition_approximation

input_sizes = [4, 6, 8, 10, 12, 14, 16]
times_exhaustive = benchmark_partition(partition_func=partition_exhaustive, input_sizes=input_sizes)
times_approx = benchmark_partition(partition_func=partition_approximation, input_sizes=input_sizes)

fig = plt.figure()
plt.plot(input_sizes, times_exhaustive, label="exhaustive")
plt.plot(input_sizes, times_approx, label="dynamic programming")
plt.grid()
plt.legend()
plt.title('Exhaustive vs DP partition algorithm')
plt.xlabel('array size')
plt.ylabel('time, seconds')
fig.savefig("plot.png")
plt.show()

