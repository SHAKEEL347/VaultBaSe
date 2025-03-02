import unittest
import time
from vaultbase.blockchain import Blockchain, Block

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain(difficulty=2)
    
    def test_genesis_block(self):
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.prev_hash, "0")
        self.assertEqual(genesis_block.data, "Genesis Block")
        self.assertEqual(genesis_block.hash, genesis_block.calculate_hash())
    
    def test_add_block(self):
        data = "Test Data"
        self.blockchain.add_block(data)
        latest_block = self.blockchain.chain[-1]
        
        self.assertEqual(latest_block.data, data)
        self.assertEqual(latest_block.index, 1)
        self.assertEqual(latest_block.prev_hash, self.blockchain.chain[-2].hash)
        self.assertEqual(latest_block.hash, latest_block.calculate_hash())
    
    def test_blockchain_integrity(self):
        self.blockchain.add_block("Entry 1")
        self.blockchain.add_block("Entry 2")
        self.blockchain.add_block("Entry 3")
        self.assertTrue(self.blockchain.validate_chain())
    
    def test_tamper_detection(self):
        self.blockchain.add_block("Legit Data")
        
        tampered_block = self.blockchain.chain[1]
        tampered_block.data = "Tampered Data"
        
        self.assertFalse(self.blockchain.validate_chain())
    
    def test_tampering_with_prev_hash(self):
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        
        self.blockchain.chain[1].prev_hash = "FakeHash"
        self.assertFalse(self.blockchain.validate_chain())
    
    def test_multiple_blocks_validation(self):
        for i in range(5):
            self.blockchain.add_block(f"Transaction {i}")
        
        self.assertTrue(self.blockchain.validate_chain())
    
    def test_mining_blocks(self):
        block = self.blockchain.add_block("Mining Test", mine=True)
        difficulty = self.blockchain.difficulty
        
        self.assertEqual(block.hash[:difficulty], "0" * difficulty)
    
    def test_multiple_block_tampering(self):
        for i in range(5):
            self.blockchain.add_block(f"Block {i}")
        
        self.blockchain.chain[1].data = "Tampered Block 1"
        self.blockchain.chain[3].data = "Tampered Block 3"
        
        self.assertFalse(self.blockchain.validate_chain())
        
        tampered_indices = self.blockchain.find_tampering()
        self.assertIn(1, tampered_indices)
        self.assertIn(3, tampered_indices)
        self.assertEqual(len(tampered_indices), 2)
    
    def test_chain_repair(self):
        for i in range(3):
            self.blockchain.add_block(f"Block {i}")
        
        self.blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.validate_chain())
        
        result = self.blockchain.repair_chain()
        self.assertTrue(result)
        self.assertTrue(self.blockchain.validate_chain())
    
    def test_validate_single_block(self):
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        
        self.assertTrue(self.blockchain.validate_block(1))
        
        self.blockchain.chain[1].data = "Tampered"
        self.assertFalse(self.blockchain.validate_block(1))
    
    def test_performance_large_blockchain(self):
        start_time = time.time()
        
        block_count = 100
        data_items = [f"Performance Test {i}" for i in range(block_count)]
        self.blockchain.add_blocks(data_items)
        
        validation_start = time.time()
        self.assertTrue(self.blockchain.validate_chain())
        validation_time = time.time() - validation_start
        
        total_time = time.time() - start_time
        print(f"\nPerformance Test: Added {block_count} blocks in {total_time:.4f}s")
        print(f"Validation time for {block_count} blocks: {validation_time:.4f}s")
        
        self.assertLess(validation_time, 1.0)

if __name__ == "__main__":
    unittest.main()