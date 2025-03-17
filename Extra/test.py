import numpy as np
import matplotlib.pyplot as plt
import random as rd

'''
measures = [
    "HHI",
    "gini",
    "entropy",
    "naka",
    "TPS",
    "storage_ratio",
    "fork_rate",
    "fork_ratio",
    "orphaned_ratio",
    "consensus",
    "percent_mining_longest_chain"
]

fig, axs = plt.subplots(4,3)
w = 0
for i in range(4):
    for j in range(3):
        axs[i][j].plot([1,2,3],[1,2,3])
        axs[i][j].plot([1,2,3],[1,1.5,2])
        axs[i][j].set_title(measures[w])
        w += 1
        if w > 10: break

axs[3][2].plot([],[], label="y")
axs[3][2].plot([],[], label="n")
axs[3][2].set_xticks([])
axs[3][2].set_yticks([])
axs[3][2].spines['top'].set_visible(False)
axs[3][2].spines['right'].set_visible(False)
axs[3][2].spines['bottom'].set_visible(False)
axs[3][2].spines['left'].set_visible(False)
axs[3][2].legend(loc='center')
plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()
'''

l1 = [1,2,3]
l2 = [4,5,6]

d = {l1[i] : l2[i] for i in range(3)}

print(d)