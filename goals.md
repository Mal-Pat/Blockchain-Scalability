# Simulate Blockchain Network

## Proof of Work

### Initialization
- Build a graph network
- Assign compute power to each node
- Assign communication time to each edge
- Create a transaction pool

### At each time step
- Generate transactions to be added to the pool
- There is a probability that one (or more) nodes will mine their block(s).
- All `new_block_added` signals will move forward one step.
- The global blockchain (only accessible by us) is updated.

#### If a block is mined
- The node that mined it will send out a `new_block_added` with the information of updated blockchain.

#### If a node receives `new_block_added` signal
- The node will delete its chosen block and update its blockchain.
- The node will pick up `block_size` number transactions and start mining again.
- If it receives more than one such signal, only one will be chosen.
