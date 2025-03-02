import unittest
from vaultbase.auth import Auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        """Set up authentication instance and add a test user."""
        self.auth = Auth()
        self.auth.add_user("user1", "securepassword123")

    def test_add_user(self):
        """Test user registration with unique usernames."""
        self.auth.add_user("user2", "anotherpassword")
        self.assertTrue("user2" in self.auth.users)

    def test_duplicate_user(self):
        """Test adding a duplicate username raises an error."""
        with self.assertRaises(ValueError):
            self.auth.add_user("user1", "newpassword")

    def test_verify_correct_password(self):
        """Test successful login with correct credentials."""
        self.assertTrue(self.auth.verify_user("user1", "securepassword123"))

    def test_verify_wrong_password(self):
        """Test login failure with incorrect password."""
        self.assertFalse(self.auth.verify_user("user1", "wrongpassword"))

    def test_verify_non_existent_user(self):
        """Test login failure for a user that does not exist."""
        self.assertFalse(self.auth.verify_user("unknown", "password"))

if __name__ == "__main__":
    unittest.main()
