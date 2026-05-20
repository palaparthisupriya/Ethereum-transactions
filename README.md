# Ethereum Merkle Tree Implementation

## Project Overview
This project builds a Merkle Tree from scratch in Python to demonstrate how decentralized systems like Ethereum achieve data integrity. It implements a binary Merkle tree, generates and verifies cryptographic inclusion proofs, and pulls real blockchain data from Ethereum's JSON-RPC endpoints to verify transaction roots.

### File Structure
- **`part1_tree.py`**: Pure data structures and algorithms. Implements the `MerkleNode` and `MerkleTree` classes. Contains logic to generate sibling inclusion proofs and mathematically verify those proofs bottom-up.
- **`part2_fetch.py`**: Infrastructure code to interact directly with an Ethereum JSON-RPC endpoint. Iterates fetching blocks and extracting specific block headers like the `transactionsRoot`.
- **`part3_verify.py`**: The orchestration logic. Pulls real blocks using Part 2, hashes the literal transactions in Python using Part 1's structures, and demonstrates a real inclusion proof in action.

## Prerequisites
You will need Python 3 installed. If you are using Windows, ensure Python was added to your PATH during installation. 
Required libraries:
```bash
pip install requests
```

## Running the Code
Run the individual sections in order to view the full pipeline:

**Step 1:** Validate the logic of the tree.
```bash
python part1_tree.py
```

**Step 2:** Ensure RPC fetching logic pulls from the live blockchain.
```bash
python part2_fetch.py
```

**Step 3:** Perform the End-to-End recreation and validation of a live Ethereum block transaction set.
```bash
python part3_verify.py
```


