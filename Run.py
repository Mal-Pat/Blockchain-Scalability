import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

import NetworkCreator
import Simulator

ntwk_params = {
    "n" : 4000,
    "pareto_param" : 1.1,
    "bandwidth_factor" : 10,
    "active_prob" : None
}

ntwk_seeds = {
    "scatter" : 1,
    "power" : 2,
    "activity" : None
}

print("Creating Network...")
start = time.time()

ntwk = NetworkCreator.UniRnNtwkTriInqGenerator(ntwk_params, ntwk_seeds)
ntwk.createNetwork()

end = time.time()
print(f"Network created in {end - start} sec!")

print("Network Stats ----->")
ntwk.getStats()
print("<----- Network Stats")

sims = ["sim1", "sim2", "sim3"]

pow_params = {
    "run_time" : [10000, 10000, 10000],
    "avg_mine_time" : [100, 200, 300],
    "max_n_transactions" : [1000, 1000, 1000],
    "avg_signal_noise" : [5, 5, 5],
    "avg_transaction_rate" : [50, 50, 50]
}

pow_seeds = {
    "poisson_noise" : [10, 11, 12],
    "poisson_new_transactions" : [20, 21, 22],
    "exponential_minetime" : [40, 41, 42]
}

measures = [
    "TPS",
    "storage_ratio",
    "fork_rate",
    "fork_ratio",
    "orphaned_ratio",
    "consensus",
    "percent_mining_longest_chain"
]

X, Y = 3,3
fig, axs = plt.subplots(X,Y)

for k in range(len(sims)):
    sim = Simulator.PoW(
        ntwk.getNetwork().copy(),
        {key : pow_params[key][k] for key in pow_params.keys()},
        {key : pow_seeds[key][k] for key in pow_seeds.keys()}
    )
    print(f"Running {sims[k]}...")
    start = time.time()

    sim.runSimulation()

    end = time.time()
    print(f"{sims[k]} ran in {end-start} sec!")

    w = 0
    for i in range(X):
        for j in range(Y):
            axs[i][j].plot(list(range(sim.params["run_time"])), sim.measures[measures[w]], label=sims[k])
            axs[i][j].set_title(measures[w])
            axs[i][j].legend()
            w += 1
            if w >= len(measures): break

plt.show()