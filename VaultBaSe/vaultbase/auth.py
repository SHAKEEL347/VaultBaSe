import hashlib
import os

class Auth:
    def __init__(self):
        self.users = {}

    def hash_password(self, password, salt=None):
        """Hashes the password using SHA-256 with a salt for better security."""
        salt = salt or os.urandom(16).hex()  # Generate a random 16-byte salt
        hashed_pw = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${hashed_pw}"  # Store salt and hash together

    def add_user(self, username, password):
        """Registers a new user with a securely hashed password."""
        if username in self.users:
            raise ValueError("User already exists!")
        self.users[username] = self.hash_password(password)

    def verify_user(self, username, password):
        """Verifies a user by checking the stored hash against the entered password."""
        stored_hash = self.users.get(username)
        if not stored_hash:
            return False

        salt, stored_pw = stored_hash.split("$")
        return stored_pw == hashlib.sha256((salt + password).encode()).hexdigest()
