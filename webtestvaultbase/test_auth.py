from vaultbase import VaultBaSe

auth = VaultAuth()
hashed_password = auth.hash_password("testpassword123")
print("Hashed Password:", hashed_password)

is_valid = auth.verify_password("testpassword123", hashed_password)
print("Password Valid:", is_valid)
