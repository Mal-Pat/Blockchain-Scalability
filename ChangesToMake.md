# Changes To Make

## Code Efficiency

### Time Steps

- Only jump to time steps where actions are to be taken

## Security

### Double Spend Simulation

1. Create a cooperating group of malicious nodes
2. Choose a base transaction block to start from
3. Attempt to create a longer malicious chain in secret
4. Wait till base transaction block has enough blocks build on it to be "confirmed"
4. When malicious chain exceeds length of main chain, broadcast the blocks of malicious chain

## Scalability

### Transactions

1. Track number of transactions in transaction pool
2. Increase them using Poisson Distribution whose average may drift according to some probabilistic function
3. When a node restarts mining, assign it some number of transactions from transaction pool to add to their block to mine on
4. Decrease them when a block is created by number of transactions in that block
5. But it gets more complicated as some transactions (those not in main chain) in orphaned blocks must be added back into pool

### Hash Rate Control

1. In real world, hash rate control is done once every two weeks (by checking last 2016 blocks)
2. Simulate the same in the code