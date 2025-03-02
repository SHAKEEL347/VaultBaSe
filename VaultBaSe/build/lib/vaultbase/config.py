from cryptography.fernet import Fernet

# Generate a key only once and store it securely (e.g., in a .env file)
ENCRYPTION_KEY = Fernet.generate_key().decode()
