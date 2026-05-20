import hashlib
from dataclasses import dataclass

def sha256_pair(left: bytes, right: bytes) -> bytes:
    """Hash two child digests together to produce a parent node hash."""
    return hashlib.sha256(left + right).digest()

@dataclass
class MerkleNode:
    hash: bytes
    left: "MerkleNode | None" = None
    right: "MerkleNode | None" = None

class MerkleTree:
    def __init__(self, leaves: list[bytes]):
        self.leaves_data = leaves
        if not leaves:
            raise ValueError("Cannot build a Merkle tree with no leaves")
            
        leaf_nodes = [MerkleNode(hashlib.sha256(leaf).digest()) for leaf in leaves]
        self._root_node = self._build(leaf_nodes)

    def _build(self, nodes: list[MerkleNode]) -> MerkleNode:
        if len(nodes) == 1:
            return nodes[0]
            
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
            
        parent_nodes = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1]
            parent_hash = sha256_pair(left.hash, right.hash)
            parent_nodes.append(MerkleNode(hash=parent_hash, left=left, right=right))
            
        return self._build(parent_nodes)

    @property
    def root(self) -> bytes:
        return self._root_node.hash
        
    def get_proof(self, index: int) -> list[dict]:
        if index < 0 or index >= len(self.leaves_data):
            raise IndexError("Index out of bounds")
            
        proof = []
        nodes = [MerkleNode(hashlib.sha256(leaf).digest()) for leaf in self.leaves_data]
        curr_index = index
        
        while len(nodes) > 1:
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1])
                
            parent_nodes = []
            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1]
                parent_hash = sha256_pair(left.hash, right.hash)
                parent_nodes.append(MerkleNode(hash=parent_hash, left=left, right=right))
                
                if i == curr_index or i + 1 == curr_index:
                    is_left = (curr_index % 2 == 0)
                    if is_left:
                        sibling_index = i + 1
                        position = "right"
                    else:
                        sibling_index = i
                        position = "left"
                        
                    proof.append({
                        "hash": nodes[sibling_index].hash,
                        "position": position
                    })
            
            curr_index = curr_index // 2
            nodes = parent_nodes
            
        return proof

def verify_proof(leaf_data: bytes, proof: list[dict], expected_root: bytes) -> bool:
    current_hash = hashlib.sha256(leaf_data).digest()
    for item in proof:
        sibling_hash = item["hash"]
        position = item["position"]
        if position == "left":
            current_hash = sha256_pair(sibling_hash, current_hash)
        else:
            current_hash = sha256_pair(current_hash, sibling_hash)
            
    return current_hash == expected_root

if __name__ == '__main__':
    items = [b"alice", b"bob", b"carol", b"dave"]
    tree = MerkleTree(items)

    proof = tree.get_proof(2)
    assert verify_proof(b"carol", proof, tree.root), "Valid proof should verify"

    assert not verify_proof(b"mallory", proof, tree.root), "Invalid data should fail"

    tampered_proof = [dict(p) for p in proof]
    tampered_proof[0]["hash"] = b"\x00" * 32
    assert not verify_proof(b"carol", tampered_proof, tree.root), "Tampered proof should fail"
    
    print("Part 1: All tests passed!")
