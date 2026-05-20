import requests

def fetch_block(rpc_url: str, block_number: int | str = "latest") -> dict:
    if isinstance(block_number, int):
        block_param = hex(block_number)
    else:
        block_param = block_number
        
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [block_param, True],
        "id": 1
    }
    
    response = requests.post(rpc_url, json=payload)
    response.raise_for_status()
    data = response.json()
    
    if "error" in data:
        raise Exception(f"RPC Error: {data['error']}")
        
    return data["result"]

def fetch_transaction_proof(rpc_url: str, tx_hash: str) -> dict:
    """
    Fetch a transaction inclusion proof using eth_getProof or equivalent.
    Returns the proof path for the transaction in the block's transaction trie.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getProof",
        "params": [tx_hash, [], "latest"],
        "id": 1
    }
    response = requests.post(rpc_url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("result", {})

def inspect_block(block: dict) -> None:
    number = int(block["number"], 16)
    timestamp = int(block["timestamp"], 16)
    transactions = block.get("transactions", [])
    tx_root = block.get("transactionsRoot")
    
    print("--- Block Inspection ---")
    print(f"Block Number: {number}")
    print(f"Timestamp: {timestamp}")
    print(f"Transaction Count: {len(transactions)}")
    print(f"Transactions Root: {tx_root}")
    print("------------------------")

if __name__ == '__main__':
    RPC_URL = "https://ethereum-rpc.publicnode.com"
    block = fetch_block(RPC_URL, "latest")
    inspect_block(block)
