import hashlib
import time
import json
from typing import List, Dict, Any, Optional
import threading

class Block:
    def __init__(self, index: int, prev_hash: str, data: Any, timestamp: Optional[float] = None, 
                 difficulty: int = 4, nonce: int = 0):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp or time.time()
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        block_data = json.dumps({
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "difficulty": self.difficulty,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self._lock = threading.Lock()
        self._hash_cache = {}
    
    def create_genesis_block(self) -> Block:
        genesis = Block(0, "0", "Genesis Block")
        return genesis
    
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_block(self, data: Any, mine: bool = False) -> Block:
        with self._lock:
            last_block = self.get_latest_block()
            new_block = Block(
                index=len(self.chain),
                prev_hash=last_block.hash,
                data=data,
                difficulty=self.difficulty
            )
            
            if mine:
                new_block.mine_block(self.difficulty)
                
            self.chain.append(new_block)
            self._hash_cache[new_block.index] = new_block.hash
            return new_block
    
    def add_blocks(self, data_items: List[Any], mine: bool = False) -> List[Block]:
        blocks = []
        with self._lock:
            for data in data_items:
                blocks.append(self.add_block(data, mine))
        return blocks
    
    def validate_chain(self, start_index: int = 1) -> bool:
        for i in range(start_index, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]
            
            if curr_block.prev_hash != prev_block.hash:
                print(f"Tampering detected: Block {curr_block.index} has incorrect prev_hash")
                return False
            
            recalculated_hash = curr_block.calculate_hash()
            if curr_block.hash != recalculated_hash:
                print(f"Tampering detected: Block {curr_block.index} data has been altered")
                return False
            
            self._hash_cache[curr_block.index] = curr_block.hash
            
        return True
    
    def validate_block(self, block_index: int) -> bool:
        if block_index <= 0 or block_index >= len(self.chain):
            return False
            
        curr_block = self.chain[block_index]
        prev_block = self.chain[block_index - 1]
        
        if curr_block.prev_hash != prev_block.hash:
            return False
            
        if curr_block.hash != curr_block.calculate_hash():
            return False
            
        return True
    
    def find_tampering(self) -> List[int]:
        tampered_indices = []
        
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]
            
            if curr_block.prev_hash != prev_block.hash:
                tampered_indices.append(i)
                continue
                
            if curr_block.hash != curr_block.calculate_hash():
                tampered_indices.append(i)
                
        return tampered_indices
    
    def get_chain(self) -> List[Dict[str, Any]]:
        return [block.to_dict() for block in self.chain]
    
    def get_chain_length(self) -> int:
        return len(self.chain)
    
    def repair_chain(self) -> bool:
        with self._lock:
            for i in range(1, len(self.chain)):
                prev_block = self.chain[i - 1]
                curr_block = self.chain[i]
                
                curr_block.prev_hash = prev_block.hash
                curr_block.hash = curr_block.calculate_hash()
                self._hash_cache[curr_block.index] = curr_block.hash
                
            return self.validate_chain()


if __name__ == "__main__":
    blockchain = Blockchain(difficulty=2)
    start_time = time.time()
    
    blockchain.add_block("Transaction 1")
    blockchain.add_block("Transaction 2")
    blockchain.add_blocks(["Transaction 3", "Transaction 4", "Transaction 5"])
    
    print(f"\nBlockchain created with {len(blockchain.chain)} blocks in {time.time() - start_time:.4f} seconds")
    print("Initial Blockchain Validation:", blockchain.validate_chain())
    
    print("\n🚨 Tampering with multiple blocks...")
    blockchain.chain[1].data = "Tampered Data 1"
    blockchain.chain[3].data = "Tampered Data 3"
    
    print("Blockchain Validation After Tampering:", blockchain.validate_chain())
    tampered_blocks = blockchain.find_tampering()
    print(f"Tampered blocks found at indices: {tampered_blocks}")
    
    print("\n🔧 Repairing blockchain...")
    blockchain.repair_chain()
    print("Blockchain Validation After Repair:", blockchain.validate_chain())