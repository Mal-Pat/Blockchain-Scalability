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
        self.changed_blockchain_nodes = []
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

    def nodeActivity(self):
        pass

    # Adds the new block to both global and node's local blockchain and updates both global and node's local levels
    def addNewBlock(self, node):
        # Level to add newly mined block = Level of block that node was mining on + 1
        level = self.global_blockchain[self.ntwk.nodes[node]["mining"]["block_id"]]["level"] + 1
        # or, level = max(list(self.ntwk.nodes[node]["local_levels"])) + 1

        # Defines new_block
        new_block = {"level": level, "prev_block": self.ntwk.nodes[node]["mining"]["block_id"], "miner": node, "time_created": self.time, "n_transactions": self.numTransactions()}

        # Updates global_blockchain
        self.global_blockchain[self.newest_block_id] = new_block
        
        # Updates global_levels
        if not (level in self.global_levels):
            self.global_levels[level] = []
        self.global_levels[level].append(self.newest_block_id)

        # Updates local_blockchain
        self.ntwk.nodes[node]["local_blockchain"][self.newest_block_id] = new_block

        # Updates local_levels (note that the condition must always be true, but I still added the "if" condition just in case)
        if not (level in self.ntwk.nodes[node]["local_levels"]):
            self.ntwk.nodes[node]["local_levels"][level] = []
        self.ntwk.nodes[node]["local_levels"][level].append(self.newest_block_id)

        # Adds node to changed_blockchain_nodes
        self.changed_blockchain_nodes.append(node)

    # BIG ERROR - TWO block_id VARIABLES IN THIS
    def verifyAddingBlockToNode(self, node, level, block_id) -> bool:
        if (level - 1) in self.ntwk.nodes[node]["local_levels"]:
            for block_id in self.ntwk.nodes[node]["local_levels"][level - 1]:
                if block_id == self.global_blockchain[block_id]["prev_block"]:
                    return True
        return False

    # CHANGE LOCAL BLOCKCHAIN TO ONLY HAVE BLOCK ID AND TIME IT RECEIVED IT
    def addBlockToLocalBlockchainFromSignal(self, node, block_id):
        level = self.global_blockchain[block_id]["level"]

        if self.verifyAddingBlockToNode(node, level, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            if not (level in self.ntwk.nodes[node]["local_levels"]):
                self.ntwk.nodes[node]["local_levels"][level] = []
            self.ntwk.nodes[node]["local_levels"][level].append(block_id)
            
            # Adds node to changed_blockchain_nodes
            self.changed_blockchain_nodes.append(node)

        else: # Adds block_id to storage with correct level key
            if not (level in self.ntwk.nodes[node]["storage"]):
                self.ntwk.nodes[node]["storage"][level] = []
            self.ntwk.nodes[node]["storage"][level].append(block_id)

    def tryAddBlockToLocalBlockchainFromStorage(self, node, level, block_id):
        if self.verifyAddingBlockToNode(node, level, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            if not (level in self.ntwk.nodes[node]["local_levels"]):
                self.ntwk.nodes[node]["local_levels"][level] = []
            self.ntwk.nodes[node]["local_levels"][level].append(block_id)
            
            # Adds node to changed_blockchain_nodes
            self.changed_blockchain_nodes.append(node)

            self.ntwk.nodes[node]["storage"][level].remove(block_id)
            
    # Handles mining
    def allMining(self):
        for node in self.ntwk.nodes():
            # Checks mining status of "node" and if it is active
            if self.time == self.ntwk.nodes[node]["mining"]["mine_time"] and self.ntwk.nodes[node]["active"]:
                # Increase newest block id by 1
                self.newest_block_id += 1
                # Add new block to global and local blockchains
                self.addNewBlock(node)
                # Send signal to all neighbors
                self.sendSignal(node, self.newest_block_id)

    def handleSignals(self):
        # If there exist signals supposed to arrive at current time
        if self.time in self.signals:
            # For all nodes supposed to receive those signals
            for node in self.signals[self.time]:
                # Add all blocks that the particular node was supposed to receive to the node local blockchain
                for block_id in self.signals[self.time][node]:
                    self.addBlockToLocalBlockchainFromSignal(node, block_id)
            # Free up memory by deleting the current time signals list
            del self.signals[self.time]

    def checkNodeStorage(self, node):
        for level in self.ntwk.nodes[node]["storage"]:
            for block_id in self.ntwk.nodes[node]["storage"][level]:
                self.tryAddBlockToLocalBlockchainFromStorage(node, level, block_id)

    def getTotalActivePower(self):
        return sum(self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes() if self.ntwk.nodes[node]["active"])

    # CHANGE THE POWER AS NODES CAN BE ACTIVE OR INACTIVE
    def checkNodeRestart(self, node):
        highest_level = max(list(self.ntwk.nodes[node]["local_levels"]))
        longest_chain_block_id = self.ntwk.nodes[node]["local_levels"][highest_level][0]

        # If the block it is mining on isn't longest_chain_block_id, then restart mining on this new block
        if self.ntwk.nodes[node]["mining"]["block_id"] != longest_chain_block_id:
            self.ntwk.nodes[node]["mining"]["block_id"] = longest_chain_block_id
            self.ntwk.nodes[node]["mining"]["mine_time"] = self.time + round(np.random.exponential(self.avg_mine_time * getTotalActivePower()/self.ntwk.nodes[node]["power"]))
    
    # Restarts 
    def restartNode(self, node):
        pass

    def checkNodes(self):
        for _ in range(len(self.changed_blockchain_nodes)):
            node = self.changed_blockchain_nodes.pop(0)
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

    def topActivePowersSquaredSum(self, p):
        power_values = [self.ntwk.nodes[node]["power"] for node in self.ntwk.nodes() if self.ntwk.nodes[node]["active"]]
        power_values.sort(reverse=True)
        return sum(power**2 for power in power_values[:int(len(power_values)*p/100)])

    def measureHHI(self):
        return self.topActivePowersSquaredSum(10)

    def measureNaka(self):
        pass

    def measureEntropy(self):
        pass

    def measureGini(self):
        pass

    def measureDecentralization(self):
        HHI = self.topActivePowersSquaredSum(10)

    def measureTPS(self):
        # Measure TPS
        return sum(self.global_blockchain[block_id]["n_transactions"] for block_id in self.getLongestChain())/self.time

        # The above single line of code is equivalent to the three lines below:
        #   longest_chain = self.getLongestChain()
        #   total_confirmed_transactions = sum(self.global_blockchain[block_id]["n_transactions"] for block_id in longest_chain)
        #   TPS = total_confirmed_transactions/self.time

    # Check the consensus on blockchain - till when do they all agree and by how much?
    def measureConsensus(self):
        pass



class generateNetwork:

    def __init__(self, n):
        self.n = n

    def createGraph(self):
        self.graph = nx.Graph()

    def assignPower(self):
        pass

    def assignCommunication(self):
        pass

    def createNetwork(self):
        pass



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

G.nodes[1]["active"] = False
G.nodes[2]["active"] = True
G.nodes[3]["active"] = True

# print(G.nodes.data())

simulation = PoW(G, 1000, avg_mine_time, max_n_transactions, bandwidth_std)
print(simulation.getTotalPower())

'''
simulation.oneTimeStep()
print(simulation.global_blockchain)
print(simulation.newest_block_id)
print(simulation.time)
'''