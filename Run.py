import NetworkCreator
import Simulator
import time
import matplotlib.pyplot as plt

ntwk_params = {
    "n" : 1000,
    "pareto_param" : 1.1,
    "bandwidth_factor" : 10,
    "active_prob" : 1,
}
ntwk_seeds = {
    "scatter" : 1,
    "power" : 2,
    "activity" : 3
}
ntwk = NetworkCreator.UniRnNtwkTriInqGenerator(ntwk_params, ntwk_seeds)
ntwk.createNetwork()

sims = ["sim1", "sim2", "sim3"]
pow_params = {
    "run_time" : [200, 200, 200],
    "avg_mine_time" : [10, 20, 30],
    "max_n_transactions" : [100, 100, 100],
    "avg_signal_noise" : [5, 5, 5],
    "activate" : [0, 0, 0],
    "deactivate" : [0, 0, 0],
    "avg_transaction_rate" : [50, 50, 50]
}
pow_seeds = {
    "poisson_noise" : [10, 11, 12],
    "poisson_new_transactions" : [20, 21, 22],
    "uniform_activity" : [30, 31, 32],
    "exponential_minetime" : [40, 41, 42]
}

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

for k in range(len(sims)):
    sim = Simulator.PoW(
        ntwk.getNetwork().copy(),
        {key : pow_params[key][k] for key in pow_params.keys()},
        {key : pow_seeds[key][k] for key in pow_seeds.keys()}
    )
    print(f"Running {sims[k]}")
    start = time.time()
    sim.runSimulation()
    end = time.time()
    print(f"{sims[k]} ran in {end-start} seconds")
    w = 0
    for i in range(4):
        for j in range(3):
            axs[i][j].plot(list(range(sim.params["run_time"])), sim.measures[measures[w]], label=sims[k])
            axs[i][j].set_title(measures[w])
            axs[i][j].legend()
            w += 1
            if w > 10: break

plt.show()