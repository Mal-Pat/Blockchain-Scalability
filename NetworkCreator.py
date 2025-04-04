import numpy as np
import networkx as nx

class UniRnNtwkTriInqGenerator:

    def __init__(self, params, seeds):
        self.params = params
        self.ntwk = nx.complete_graph(self.params["n"])
        self.seeds = seeds

    def generateScatter(self):
        rng_uniform_scatter = np.random.default_rng(self.seeds["scatter"])
        self.X = rng_uniform_scatter.uniform(size=(self.params["n"], 2))

    def assignPower(self):
        rng_pareto_power = np.random.default_rng(self.seeds["power"])
        for i in range(self.params["n"]):
            self.ntwk.nodes[i]["power"] = rng_pareto_power.pareto(self.params["pareto_param"]) + 1

    def assignBandwidth(self):
        for i in range(self.params["n"] - 1):
            for j in range(i + 1, self.params["n"]):
                self.ntwk[i][j]["bandwidth"] = int(self.params["bandwidth_factor"]/np.linalg.norm(self.X[i] - self.X[j]))

    def assignActivity(self):
        rng_uniform_activity = np.random.default_rng(self.seeds["activity"])
        for i in range(self.params["n"]):
            self.ntwk.nodes[i]["active"] = (rng_uniform_activity.uniform() < self.params["active_prob"])

    def plotAll(self):
        plt.scatter(self.X[:,0], self.X[:,1], c=[self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes])
        plt.title("All Nodes")
        plt.colorbar()
        plt.show()

    def getStats(self):
        total_power = sum(self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes())
        print(f"Total Power : {total_power}")
        print(f"Max power : {max([self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes()])}")
        print(f"Max power share : {max([self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes()])/total_power}")
        print(f"Min power : {min([self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes()])}")
        print(f"Min power share : {min([self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes()])/total_power}")
        print(f"Max bandwidth : {max([self.ntwk.edges[edge]["bandwidth"] for edge in self.ntwk.edges()])}")
        print(f"Min bandwidth : {min([self.ntwk.edges[edge]["bandwidth"] for edge in self.ntwk.edges()])}")

    def createNetwork(self):
        self.generateScatter()
        self.assignPower()
        self.assignBandwidth()
        # self.assignActivity()

    def getNetwork(self):
        return self.ntwk