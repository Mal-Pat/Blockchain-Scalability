import numpy as np
import networkx as nx
import pandas as pd

class PoW:

    def __init__(self, ntwk, total_time):
        self.ntwk = ntwk
        self.global_blockchain = {1: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}
        self.global_levels = {0: [1]}
        self.time = 0
        self.total_time = total_time
        self.signals = pd.DataFrame({"dest": [], "arr_time": [], "block_id": [], "origin": []})
        self.latest_block_id = 0

    # Generates Transactions
    def generateTransactions(self):
        pass

    def sendSignal(self, node):
        for nb in self.ntwk.neighbors(node):
            self.signals.loc[len(self.signals)] = [nb, self.time + self.ntwk[node][nb]["weight"], self.latest_block_id, node]

    def checkMiningStatus(self, node):
        #smth
        return cond

    def addBlock(self, node):
        new_level = max(list(self.ntwk.nodes[node]["local_levels"].keys())) + 1

        # Updating global_blockchain
        self.global_blockchain[self.latest_block_id] = {"level": new_level, "prev_block": self.ntwk.nodes[node]["mining"]["block_id"], "miner": node, "time_created": self.time, "transactions": []}
        
        # Updating global_levels
        if new_level in self.global_levels.keys():
            self.global_levels[level].append(self.latest_block_id) 
        else:
            self.global_levels[level] = []
            self.global_levels[level].append(self.latest_block_id)

        # Updating local_blockchain
        self.ntwk.nodes[node]["local_blockchain"][self.latest_block_id] = {"level": new_level, "prev_block": self.ntwk.nodes[node]["mining"]["block_id"], "miner": node, "time_created": self.time, "transactions": []}

        # Updating local_levels (note that it is impossible for the level to already have been in local_levels)
        self.ntwk.nodes[node]["local_levels"][new_level] = []
        self.ntwk.nodes[node]["local_levels"][new_level].append(self.latest_block_id)

    def verifyAddingBlockToNode(self, node, block_id):
        pass

    def addToLocalBlockchain(self, node, block_id):
        if self.verifyAddingBlockToNode(node, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            level = self.global_blockchain[block_id]["level"]

            if level in self.ntwk.nodes[node]["local_levels"].keys():
                self.ntwk.nodes[node]["local_levels"][new_level].append(block_id)
            else:
                self.ntwk.nodes[node]["local_levels"][new_level] = []
                self.ntwk.nodes[node]["local_levels"][new_level].append(block_id)

    def restartMining(self, node):
        pass

    # Handles mining
    def allMining(self):
        for node in self.ntwk.nodes():
            if self.checkMiningStatus(node):
                self.latest_block_id += 1
                self.addBlock(node)
                self.sendSignal(node)

    def handleSignals(self):
        if self.signals["arr_time"].isin(self.time):
            df = self.signals.loc[self.signals['arr_time'] == self.time]
            for node in df['dest']:
                pass

    def checkNodesForRestart(self):
        for node in self.ntwk.nodes():
            highest_level = max(list(self.ntwk.nodes[node]["local_levels"].keys()))
            longest_chain_block_id = self.ntwk.nodes[node]["local_levels"][highest_level][0]

            # If the block it is mining on isn't longest_chain_block_id, then restart mining on this new block
            if self.ntwk.nodes[node]["mining"]["block_id"] != longest_chain_block_id:
                self.ntwk.nodes[node]["mining"]["block_id"] = longest_chain_block_id
                self.ntwk.nodes[node]["mining"]["start_time"] = self.time

    def oneTimeStep(self):
        while (self.time <= self.total_time):
            self.allMining()
            self.handleSignals()
            self.checkNodesForRestart()
            self.resolveConflicts()
            self.time += 1

    # Check the consensus on blockchain - till when do they all agree and by how much?
    def consensusMeasure(self):
        pass



class Network:

    def __init__(self):
        pass

    def createGraph(self):
        pass

    def assignPower(self):
        pass

    def assignCommunication(self):
        pass



G = nx.Graph()

G.add_edge(1,2)
G[1][2]["weight"] = 5
G.add_edge(2,3)
G[2][3]["weight"] = 4
G.add_edge(1,3)
G[1][3]["weight"] = 8

G.nodes[1]["power"] = 0.3 
G.nodes[2]["power"] = 0.5
G.nodes[3]["power"] = 0.2

G.nodes[1]["mining"] = {"start_time" : 0, "block_id" : 1}
G.nodes[2]["mining"] = {"start_time" : 0, "block_id" : 1}
G.nodes[3]["mining"] = {"start_time" : 0, "block_id" : 1}

G.nodes[1]["local_blockchain"] = {1: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}
G.nodes[2]["local_blockchain"] = {1: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}
G.nodes[3]["local_blockchain"] = {1: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}

G.nodes[1]["local_levels"] = {0: [1]}
G.nodes[2]["local_levels"] = {0: [1]}
G.nodes[3]["Local_levels"] = {0: [1]}

print(G.nodes.data())

for node in G.nodes():
    print(node)
