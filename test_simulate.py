import numpy as np
import networkx as nx
import pandas as pd

class PoW:

    def __init__(self, ntwk, total_time):
        self.ntwk = ntwk
        self.global_blockchain = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}
        self.global_levels = {0: [0]}
        self.time = 0
        self.total_time = total_time
        self.newest_block_id = 0
        self.signals = {}
        self.changed_node_blockchains = []

    # Generates Transactions
    def generateTransactions(self):
        pass

    def sendSignal(self, node, block_id = self.newest_block_id):
        # Send signal to all neighbors of node
        for nb in self.ntwk.neighbors(node):
            # Calculate arrival time of signal for neighbor "nb"
            arrival_time = self.time + self.ntwk[node][nb]["weight"]

            # Handle missing arrival_time and nb cases
            if not (arrival_time in self.signals.keys()):
                self.signals[arrival_time] = {}
            if not (nb in self.signals[arrival_time].keys()):
                self.signals[arrival_time][nb] = []

            # Add block_id in "arrival_time" at correct neighbor "nb"
            self.signals[arrival_time][nb].append(block_id)

    def checkMiningStatus(self, node):
        #smth
        return cond

    # Adds the new block to both global and node's local blockchain and updates both global and node's local levels
    def addNewBlock(self, node):
        level = max(list(self.ntwk.nodes[node]["local_levels"].keys())) + 1

        # Updating global_blockchain
        self.global_blockchain[self.newest_block_id] = {"level": level, "prev_block": self.ntwk.nodes[node]["mining"]["block_id"], "miner": node, "time_created": self.time, "transactions": []}
        
        # Updating global_levels
        if not (level in self.global_levels.keys()):
            self.global_levels[level] = []
        self.global_levels[level].append(self.newest_block_id)

        # Updating local_blockchain
        self.ntwk.nodes[node]["local_blockchain"][self.newest_block_id] = {"level": level, "prev_block": self.ntwk.nodes[node]["mining"]["block_id"], "miner": node, "time_created": self.time, "transactions": []}

        # Updating local_levels (note that the condition must always be true, but I still added the "if" condition just in case)
        if not (level in self.ntwk.nodes[node]["local_levels"].keys()):
            self.ntwk.nodes[node]["local_levels"][level] = []
        self.ntwk.nodes[node]["local_levels"][level].append(self.newest_block_id)

        # Adding node to changed_node_blockchains
        self.changed_node_blockchains.append(node)

    def verifyAddingBlockToNode(self, node, block_id) -> bool:
        pass

    def addBlockToLocalBlockchainFromSignal(self, node, block_id):
        level = self.global_blockchain[block_id]["level"]

        if self.verifyAddingBlockToNode(node, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            if not (level in self.ntwk.nodes[node]["local_levels"].keys()):
                self.ntwk.nodes[node]["local_levels"][level] = []
            self.ntwk.nodes[node]["local_levels"][level].append(block_id)
            
            self.changed_node_blockchains.append(node)

        else: # Add block_id to storage with correct level key
            if not (level in self.ntwk.nodes[node]["storage"].keys()):
                self.ntwk.nodes[node]["storage"][level] = []
            self.ntwk.nodes[node]["storage"][level].append(block_id)

    def tryAddBlockToLocalBlockchainFromStorage(self, node, level, block_id):
        if self.verifyAddingBlockToNode(node, block_id):
            self.ntwk.nodes[node]["local_blockchain"][block_id] = self.global_blockchain[block_id]

            if not (level in self.ntwk.nodes[node]["local_levels"].keys()):
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
                self.sendSignal(node) # By default sends the newest_block_id to all neighbors of node

    def handleSignals(self):
        if self.time in self.signals.keys():
            for node in self.signals[self.time].keys():
                for block_id in self.signals[self.time][node]:
                    self.addBlockToLocalBlockchainFromSignal(node, block_id)

    def checkNodeStorage(self, node):
        for level in self.ntwk.nodes[node]["storage"]:
            for block_id in self.ntwk.nodes[node]["storage"][level]:
                self.tryAddBlockToLocalBlockchainFromStorage(node, level, block_id)
    
    def checkNodeRestart(self, node):
        highest_level = max(list(self.ntwk.nodes[node]["local_levels"].keys()))
        longest_chain_block_id = self.ntwk.nodes[node]["local_levels"][highest_level][0]

        # If the block it is mining on isn't longest_chain_block_id, then restart mining on this new block
        if self.ntwk.nodes[node]["mining"]["block_id"] != longest_chain_block_id:
            self.ntwk.nodes[node]["mining"]["block_id"] = longest_chain_block_id
            self.ntwk.nodes[node]["mining"]["start_time"] = self.time

    def checkNodesForRestart(self):
        for _ in range(len(self.changed_node_blockchains)):
            node = self.changed_node_blockchains.pop(0)
            self.checkNodeStorage(node)
            self.checkNodeRestart(node)

    def resolveStorageConflicts():
        for node in self.changed_node_storage:
            pass

        self.changed_node_storage.clear()

    def oneTimeStep(self):
        while (self.time <= self.total_time):
            self.allMining()
            self.handleSignals()
            self.checkNodesForRestart()
            self.resolveStorageConflicts()
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

G.nodes[1]["mining"] = {"start_time" : 0, "block_id" : 0}
G.nodes[2]["mining"] = {"start_time" : 0, "block_id" : 0}
G.nodes[3]["mining"] = {"start_time" : 0, "block_id" : 0}

G.nodes[1]["local_blockchain"] = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}
G.nodes[2]["local_blockchain"] = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}
G.nodes[3]["local_blockchain"] = {0: {"level": 0, "prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}

G.nodes[1]["local_levels"] = {0: [0]}
G.nodes[2]["local_levels"] = {0: [0]}
G.nodes[3]["Local_levels"] = {0: [0]}

G.nodes[1]["arriving_signals"] = {}
G.nodes[2]["arriving_signals"] = {}
G.nodes[3]["arriving_signals"] = {}

G.nodes[1]["storage"] = {}
G.nodes[2]["storage"] = {}
G.nodes[3]["storage"] = {}

print(G.nodes.data())

for node in G.nodes():
    print(node)
