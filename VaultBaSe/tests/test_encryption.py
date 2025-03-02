import unittest
from vaultbase.encryption import Encryption

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.enc = Encryption()

    def test_fernet_encryption(self):
        """Tests Fernet symmetric encryption."""
        original = "Sensitive Data"
        encrypted = self.enc.encrypt(original)
        decrypted = self.enc.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_rsa_encryption(self):
        """Tests RSA asymmetric encryption and decryption."""
        private_key, public_key = Encryption.generate_rsa_keys()
        original = "Confidential Message"
        encrypted = Encryption.rsa_encrypt(original, public_key)
        decrypted = Encryption.rsa_decrypt(encrypted, private_key)
        self.assertEqual(original, decrypted)

    def test_hashing(self):
        """Tests SHA-256 hashing function."""
        data = "Secure Password"
        hashed1 = Encryption.hash_data(data)
        hashed2 = Encryption.hash_data(data)
        self.assertEqual(hashed1, hashed2)  # Hash should always be the same

if __name__ == "__main__":
    unittest.main()

