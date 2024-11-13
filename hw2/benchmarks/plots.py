from cProfile import label

import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.bipartite.basic import color

data_fox = np.loadtxt('../data/time_fox.txt')
processes = [1, 4, 9, 16, 25]

mean_times = np.min(data_fox[:, 1].reshape(-1, 5), axis=1)
m_size = int(data_fox[0, 2])
plt.title(f"Matrix multiplication Fox parallel algorithm. \nMatrix size: {m_size}x{m_size}.")
plt.scatter(processes, mean_times[0] / mean_times, color='r', label="Measurements")

plt.plot(processes, processes, label="Theory: y = x")
plt.legend()
plt.xlabel('number of processes')
plt.ylabel('acceleration')
plt.grid()
plt.savefig("FoxAlgorithmAcceleration.png")
plt.show()
