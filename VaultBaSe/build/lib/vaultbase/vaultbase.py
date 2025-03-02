import hashlib
import time
import json
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Auth:
    users = {"admin": "securepassword"}  # Example user database (replace with secure storage)

    @staticmethod
    def authenticate(username, password):
        return Auth.users.get(username) == password

class Encryption:
    SECRET_KEY = b"16ByteSecretKey1"  # Ensure this key is securely stored

    @staticmethod
    def encrypt(data):
        cipher = AES.new(Encryption.SECRET_KEY, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + encrypted_data).decode()

    @staticmethod
    def decrypt(enc_data):
        enc_data = base64.b64decode(enc_data)
        iv = enc_data[:AES.block_size]
        cipher = AES.new(Encryption.SECRET_KEY, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(enc_data[AES.block_size:]), AES.block_size)
        return decrypted_data.decode()

class Block:
    def __init__(self, index, prev_hash, encrypted_data, timestamp=None):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = timestamp or time.time()
        self.encrypted_data = encrypted_data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "encrypted_data": self.encrypted_data
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", Encryption.encrypt("Genesis Block"))

    def add_block(self, data):
        encrypted_data = Encryption.encrypt(data)
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, encrypted_data)
        self.chain.append(new_block)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]

            if curr_block.prev_hash != prev_block.hash:
                print(f"Tampering detected: Block {curr_block.index} has incorrect prev_hash")
                return False

            recalculated_hash = curr_block.calculate_hash()
            if curr_block.hash != recalculated_hash:
                print(f"Tampering detected: Block {curr_block.index} data has been altered")
                return False

        return True

    def get_chain(self):
        return [block.__dict__ for block in self.chain]

    def retrieve_data(self, index):
        if index < 0 or index >= len(self.chain):
            return "Invalid block index"
        return Encryption.decrypt(self.chain[index].encrypted_data)

# Main execution
if __name__ == "__main__":
    blockchain = Blockchain()
    
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not Auth.authenticate(username, password):
        print("Authentication failed.")
        exit()

    while True:
        print("\n1. Store Data")
        print("2. Retrieve Data")
        print("3. Validate Blockchain")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            data = input("Enter data to store securely: ")
            blockchain.add_block(data)
            print("Data stored securely in blockchain.")

        elif choice == "2":
            index = int(input("Enter block index to retrieve: "))
            print("Retrieved Data:", blockchain.retrieve_data(index))

        elif choice == "3":
            print("Blockchain Validity:", blockchain.validate_chain())

        elif choice == "4":
            break

        else:
            print("Invalid choice. Try again.")
