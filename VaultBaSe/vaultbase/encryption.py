from cryptography.fernet import Fernet
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import hashlib
import base64

class Encryption:
    def __init__(self, key=None):
        """Initializes symmetric encryption using Fernet (AES-based)."""
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Encrypts data using AES-based Fernet encryption."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypts AES-based Fernet encrypted data."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    @staticmethod
    def generate_rsa_keys():
        """Generates RSA public-private key pair for asymmetric encryption."""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key.decode(), public_key.decode()

    @staticmethod
    def rsa_encrypt(data: str, public_key: str) -> str:
        """Encrypts data using RSA public key encryption."""
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    @staticmethod
    def rsa_decrypt(encrypted_data: str, private_key: str) -> str:
        """Decrypts RSA-encrypted data using a private key."""
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted = cipher.decrypt(base64.b64decode(encrypted_data))
        return decrypted.decode()

    @staticmethod
    def hash_data(data: str) -> str:
        """Hashes data securely using SHA-256."""
        return hashlib.sha256(data.encode()).hexdigest()
