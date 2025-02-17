import numpy as np
import networkx as nx
import pandas as pd

class PoW:

    def __init__(self, ntwk, total_time, avg_mine_time, max_n_transactions, bandwidth_std):
        self.ntwk = ntwk
        self.global_blockchain = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "n_transactions": 1}}
        self.global_levels = {0: [0]}
        self.time = 0
        self.total_time = total_time
        self.newest_block_id = 0
        self.signals = {}
        self.changed_node_blockchains = []
        self.avg_mine_time = avg_mine_time
        self.max_n_transactions = max_n_transactions
        self.bandwidth_std = bandwidth_std

    def randomSignalNoise(self):
        return round(np.random.normal(0, self.bandwidth_std))

    def numTransactions(self):
        return round(self.max_n_transactions*np.random.beta(10,2.5))

    def sendSignal(self, node, block_id):
        # Send signal to all neighbors of node
        for nb in self.ntwk.neighbors(node):
            # Calculate arrival time of signal for neighbor "nb"
            arrival_time = self.time + self.ntwk[node][nb]["distance"] + round(self.global_blockchain[block_id]["n_transactions"]/self.ntwk[node][nb]["bandwidth"]) + self.randomSignalNoise()

            # Handle missing arrival_time and nb cases
            if not (arrival_time in self.signals):
                self.signals[arrival_time] = {}
            if not (nb in self.signals[arrival_time]):
                self.signals[arrival_time][nb] = []

            # Add block_id in "arrival_time" at correct neighbor "nb"
            self.signals[arrival_time][nb].append(block_id)

    def checkMiningStatus(self, node):
        if self.time == self.ntwk.nodes[node]["mining"]["mine_time"] and self.ntwk.nodes[node]["active"] == True:
            return True
        else:
            return False

    # Adds the new block to both global and node's local blockchain and updates both global and node's local levels
    def addNewBlock(self, node):
        level = self.global_blockchain[self.ntwk.nodes[node]["mining"]["block_id"]]["level"] + 1
        # or, level = max(list(self.ntwk.nodes[node]["local_levels"])) + 1

        # Number of transactions in this block
        n_transactions = self.numTransactions()

        # Define new_block
        new_block = {"level": level, "prev_block": self.ntwk.nodes[node]["mining"]["block_id"], "miner": node, "time_created": self.time, "n_transactions": n_transactions}

        # Updating global_blockchain
        self.global_blockchain[self.newest_block_id] = new_block
        
        # Updating global_levels
        if not (level in self.global_levels):
            self.global_levels[level] = []
        self.global_levels[level].append(self.newest_block_id)

        # Updating local_blockchain
        self.ntwk.nodes[node]["local_blockchain"][self.newest_block_id] = new_block

        # Updating local_levels (note that the condition must always be true, but I still added the "if" condition just in case)
        if not (level in self.ntwk.nodes[node]["local_levels"]):
            self.ntwk.nodes[node]["local_levels"][level] = []
        self.ntwk.nodes[node]["local_levels"][level].append(self.newest_block_id)

        # Adding node to changed_node_blockchains
        self.changed_node_blockchains.append(node)

    def verifyAddingBlockToNode(self, node, level, block_id) -> bool:
        prev_block_id = self.global_blockchain[block_id]["prev_block"]
        if (level - 1) in self.ntwk.nodes[node]["local_levels"]: 
            for block_id in self.ntwk.nodes[node]["local_levels"][level - 1]:
                if block_id == prev_block_id:
                    return True
        return False

    def addBlockToLocalBlockchainFromSignal(self, node, block_id):
        level = self.global_blockchain[block_id]["level"]

        if self.verifyAddingBlockToNode(node, level, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            if not (level in self.ntwk.nodes[node]["local_levels"]):
                self.ntwk.nodes[node]["local_levels"][level] = []
            self.ntwk.nodes[node]["local_levels"][level].append(block_id)
            
            self.changed_node_blockchains.append(node)

        else: # Add block_id to storage with correct level key
            if not (level in self.ntwk.nodes[node]["storage"]):
                self.ntwk.nodes[node]["storage"][level] = []
            self.ntwk.nodes[node]["storage"][level].append(block_id)

    def tryAddBlockToLocalBlockchainFromStorage(self, node, level, block_id):
        if self.verifyAddingBlockToNode(node, level, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            if not (level in self.ntwk.nodes[node]["local_levels"]):
                self.ntwk.nodes[node]["local_levels"][level] = []
            self.ntwk.nodes[node]["local_levels"][level].append(block_id)
            
            self.changed_node_blockchains.append(node)

            self.ntwk.nodes[node]["storage"][level].remove(block_id)
            
    # Handles mining
    def allMining(self):
        for node in self.ntwk.nodes():
            if self.checkMiningStatus(node):
                self.newest_block_id += 1
                self.addNewBlock(node)
                self.sendSignal(node, self.newest_block_id) # By default sends the newest_block_id to all neighbors of node

    def handleSignals(self):
        if self.time in self.signals:
            for node in self.signals[self.time]:
                for block_id in self.signals[self.time][node]:
                    self.addBlockToLocalBlockchainFromSignal(node, block_id)

    def checkNodeStorage(self, node):
        for level in self.ntwk.nodes[node]["storage"]:
            for block_id in self.ntwk.nodes[node]["storage"][level]:
                self.tryAddBlockToLocalBlockchainFromStorage(node, level, block_id)

    def checkNodeRestart(self, node):
        highest_level = max(list(self.ntwk.nodes[node]["local_levels"]))
        longest_chain_block_id = self.ntwk.nodes[node]["local_levels"][highest_level][0]

        # If the block it is mining on isn't longest_chain_block_id, then restart mining on this new block
        if self.ntwk.nodes[node]["mining"]["block_id"] != longest_chain_block_id:
            self.ntwk.nodes[node]["mining"]["block_id"] = longest_chain_block_id
            self.ntwk.nodes[node]["mining"]["mine_time"] = self.time + round(np.random.exponential(self.avg_mine_time/self.ntwk.nodes[node]["power"]))

    def checkNodes(self):
        for _ in range(len(self.changed_node_blockchains)):
            node = self.changed_node_blockchains.pop(0)
            self.checkNodeStorage(node)
            self.checkNodeRestart(node)

    def oneTimeStep(self):
        while (self.time < self.total_time):
            self.time += 1
            self.allMining()
            self.handleSignals()
            self.checkNodes()

    def getLongestChain(self):
        longest_chain = []

        # Get longest chain block id
        block_id = self.ntwk.nodes[node]["local_levels"][max(list(self.global_levels))][0]

        while block_id != 0:
            longest_chain.append(block_id)
            block_id = self.global_blockchain[block_id]["prev_block"]
        
        return longest_chain

    def topPowersSquaredSum(self, p):
        power_values = [self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes()]
        power_values.sort(reverse=True)
        return sum(power**2 for power in power_values[:int(len(power_values)*p/100)])
    
    # Check the consensus on blockchain - till when do they all agree and by how much?
    def measureConsensus(self):
        pass

    def measureDecentralization(self):
        pass

    def measureScalability(self):
        # Measure TPS
        TPS = sum(self.global_blockchain[block_id]["n_transactions"] for block_id in self.getLongestChain())/self.time

        # Simply put:
        #   longest_chain = self.getLongestChain()
        #   total_confirmed_transactions = sum(self.global_blockchain[block_id]["n_transactions"] for block_id in longest_chain)
        #   TPS = total_confirmed_transactions/self.time



class Network:

    def __init__(self, n):
        self.n = n

    def createGraph(self):
        pass

    def assignPower(self):
        pass

    def assignCommunication(self):
        pass

    def createNetwork(self):
        pass



class Measure:

    def __init__(self, ntwk, total_time, global_blockchain, global_levels, max_n_transactions):
        self.ntwk = ntwk
        self.total_time = total_time
        self.global_blockchain = global_blockchain
        self.global_levels = global_levels
        self.max_n_transactions = max_n_transactions

    def topPowersSquaredSum(self, p):
        power_values = [self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes()]
        power_values.sort(reverse=True)
        return sum(power**2 for power in power_values[:int(len(power_values)*p/100)])

    def measureDecentralization(self):
        HHI = self.topPowersSquaredSum(10)
        pass

    def measureSecurity(self):
        pass

    def measureScalability(self):
        # INCORRECT
        TPS = len(self.global_levels)*self.max_n_transactions/self.total_time



avg_mine_time = 100
max_n_transactions = 5000
bandwidth_std = 10

G = nx.Graph()

G.add_edge(1,2)
G[1][2]["bandwidth"] = 500
G[1][2]["distance"] = 10
G.add_edge(2,3)
G[2][3]["bandwidth"] = 750
G[2][3]["distance"] = 20
G.add_edge(1,3)
G[1][3]["bandwidth"] = 100
G[1][3]["distance"] = 30

G.nodes[1]["power"] = 0.3
G.nodes[2]["power"] = 0.5
G.nodes[3]["power"] = 0.2

G.nodes[1]["mining"] = {"mine_time" : round(np.random.exponential(avg_mine_time/0.3)), "block_id" : 0}
G.nodes[2]["mining"] = {"mine_time" : round(np.random.exponential(avg_mine_time/0.5)), "block_id" : 0}
G.nodes[3]["mining"] = {"mine_time" : round(np.random.exponential(avg_mine_time/0.2)), "block_id" : 0}

G.nodes[1]["local_blockchain"] = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "n_transactions": 1}}
G.nodes[2]["local_blockchain"] = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "n_transactions": 1}}
G.nodes[3]["local_blockchain"] = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "n_transactions": 1}}

G.nodes[1]["local_levels"] = {0: [0]}
G.nodes[2]["local_levels"] = {0: [0]}
G.nodes[3]["local_levels"] = {0: [0]}

G.nodes[1]["storage"] = {}
G.nodes[2]["storage"] = {}
G.nodes[3]["storage"] = {}

G.nodes[1]["active"] = True
G.nodes[2]["active"] = True
G.nodes[3]["active"] = True

print(G.nodes.data())

simulation = PoW(G, 1000, avg_mine_time, max_n_transactions, bandwidth_std)
simulation.oneTimeStep()
print(simulation.global_blockchain)
print(simulation.newest_block_id)
print(simulation.time)