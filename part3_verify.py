from part1_tree import MerkleTree, verify_proof
from part2_fetch import fetch_block, inspect_block

import hashlib

def hash_transaction(tx: dict) -> bytes:
    tx_hash_hex = tx["hash"].replace("0x", "")
    return hashlib.sha256(tx_hash_hex.encode("utf-8")).digest()

def reconstruct_transactions_root(transactions: list[dict]) -> bytes:
    if not transactions:
        return b""
        
    leaves = [hash_transaction(tx) for tx in transactions]
    tree = MerkleTree(leaves)
    return tree.root

def verify_transactions_root(block: dict) -> bool:
    transactions = block.get("transactions", [])
    if not transactions:
        print("No transactions in block.")
        return False
        
    reconstructed_root = reconstruct_transactions_root(transactions)
    reconstructed_root_hex = "0x" + reconstructed_root.hex()
    actual_root = block["transactionsRoot"]
    
    print(f"Expected root (from block) : {actual_root}")
    print(f"Reconstructed root (Option A): {reconstructed_root_hex}")
    
    match = (reconstructed_root_hex == actual_root)
    if not match:
        print("Note: With simplified Option A hashing, these roots are not expected to match.")
    return match

def prove_transaction_inclusion(block: dict, tx_index: int) -> None:
    transactions = block.get("transactions", [])
    if not transactions:
        print("No transactions to prove.")
        return
        
    tx = transactions[tx_index]
    leaf_data = hash_transaction(tx)
    
    leaves = [hash_transaction(t) for t in transactions]
    tree = MerkleTree(leaves)
    
    proof = tree.get_proof(tx_index)
    
    print(f"--- Proof for Tx Index {tx_index} ---")
    print(f"Tx Hash: {tx['hash']}")
    print(f"Proof length: {len(proof)} hashes")
    for i, p in enumerate(proof):
        print(f"  Level {i}: {p['position']} -> {p['hash'].hex()}")
        
    is_valid = verify_proof(leaf_data, proof, tree.root)
    print(f"Proof verification: {'SUCCESS' if is_valid else 'FAILED'}")
    
    tampered_proof = [dict(p) for p in proof]
    if tampered_proof:
        tampered_proof[0]["hash"] = b"\x00" * 32
        is_tampered_valid = verify_proof(leaf_data, tampered_proof, tree.root)
        print(f"Tampered proof verification: {'SUCCESS' if is_tampered_valid else 'FAILED'}")

if __name__ == '__main__':
    RPC_URL = "https://ethereum-rpc.publicnode.com"
    print("Fetching latest block...")
    block = fetch_block(RPC_URL, "latest")
    
    tx_count = len(block.get("transactions", []))
    if tx_count == 0:
        print("Latest block empty, falling back to a past block...")
        block = fetch_block(RPC_URL, 18000000)
        
    inspect_block(block)
    verify_transactions_root(block)
    
    print("\n--- Inclusion Proof Demonstration ---")
    if block.get("transactions"):
        prove_transaction_inclusion(block, 0)
