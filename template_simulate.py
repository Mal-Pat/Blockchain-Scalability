import numpy as np
import networkx as nx
import pandas as pd

class PoW:

    def __init__(self, ntwk, total_time):
        self.ntwk = ntwk
        self.all_blocks = {0: {1: {"prev_block": 0, "miner": 0, "time_created": 0, "transactions": []}}}
        self.time = 0
        self.total_time = total_time
        self.signals = pd.DataFrame({"dest": [], "arr_time": [], "block_id": [], "origin": []})
        self.latest_block_id = 0

    def keepMining(self):
        pass
    
    def simulate(self):
        while (self.time <= self.total_time):
            keepMining()
            handleSignals()
            resolveConflicts()
            checkAllNodes()
            self.time += 1