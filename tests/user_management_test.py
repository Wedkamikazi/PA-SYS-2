import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import time
from auth.user_management import UserManager, UserRole, User

class UserManagementTest(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.test_username = "testuser"
        self.test_password = "Test@123"
        
    def test_authentication(self):
        """4.1 Authentication"""
        print("\nTest Case 1: Basic Authentication")
        
        # Test user creation
        self.assertTrue(self.user_manager.create_user(
            self.test_username, 
            self.test_password,
            UserRole.USER
        ))
        
        # Test successful login
        user = self.user_manager.authenticate(self.test_username, self.test_password)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.test_username)
        
        # Test failed login
        user = self.user_manager.authenticate(self.test_username, "wrong_password")
        self.assertIsNone(user)
        
        # Test logout
        self.assertTrue(self.user_manager.logout(self.test_username))
        
    def test_password_validation(self):
        """4.1 Password Validation"""
        print("\nTest Case 2: Password Validation")
        
        # Test password strength
        self.assertFalse(self.user_manager.create_user("user1", "weak", UserRole.USER))
        self.assertFalse(self.user_manager.create_user("user1", "123456", UserRole.USER))
        self.assertTrue(self.user_manager.create_user("user1", "Strong@123", UserRole.USER))
        
        # Test password change
        self.assertTrue(self.user_manager.change_password("user1", "NewStrong@123"))
        user = self.user_manager.authenticate("user1", "NewStrong@123")
        self.assertIsNotNone(user)
        
    def test_session_management(self):
        """4.1 Session Management"""
        print("\nTest Case 3: Session Management")
        
        # Test session creation
        user = self.user_manager.authenticate(
            self.test_username, 
            self.test_password, 
            remember=True
        )
        self.assertIsNotNone(user.session_token)
        
        # Test session validation
        self.assertTrue(self.user_manager.validate_session(
            self.test_username,
            user.session_token
        ))
        
        # Test session expiration
        time.sleep(1)  # Simulate time passing
        self.user_manager.session_timeout = 0  # Force timeout
        self.assertFalse(self.user_manager.validate_session(
            self.test_username,
            user.session_token
        ))
        
    def test_remember_me(self):
        """4.1 Remember Me Functionality"""
        print("\nTest Case 4: Remember Me")
        
        # Test remember me token creation
        user = self.user_manager.authenticate(
            self.test_username, 
            self.test_password,
            remember=True
        )
        self.assertIsNotNone(user.remember_token)
        
        # Test remember me token validation
        self.assertTrue(self.user_manager.validate_remember_token(
            self.test_username,
            user.remember_token
        ))
        
    def test_authorization(self):
        """4.2 Authorization"""
        print("\nTest Case 5: Authorization")
        
        # Create users with different roles
        self.user_manager.create_user("admin_user", "Admin@123", UserRole.ADMIN)
        self.user_manager.create_user("normal_user", "User@123", UserRole.USER)
        
        # Test admin privileges
        admin = self.user_manager.authenticate("admin_user", "Admin@123")
        self.assertTrue(self.user_manager.has_permission(admin, "edit_users"))
        self.assertTrue(self.user_manager.has_permission(admin, "view_reports"))
        
        # Test user privileges
        user = self.user_manager.authenticate("normal_user", "User@123")
        self.assertFalse(self.user_manager.has_permission(user, "edit_users"))
        self.assertTrue(self.user_manager.has_permission(user, "view_reports"))
        
    def test_resource_access(self):
        """4.2 Resource Access Control"""
        print("\nTest Case 6: Resource Access Control")
        
        # Test file access permissions
        admin = self.user_manager.authenticate("admin_user", "Admin@123")
        user = self.user_manager.authenticate("normal_user", "User@123")
        
        # Admin should have full access
        self.assertTrue(self.user_manager.can_access_resource(admin, "sensitive_file.txt"))
        self.assertTrue(self.user_manager.can_access_resource(admin, "user_data.txt"))
        
        # User should have limited access
        self.assertFalse(self.user_manager.can_access_resource(user, "sensitive_file.txt"))
        self.assertTrue(self.user_manager.can_access_resource(user, "public_file.txt"))
        
    def test_session_timeout(self):
        """4.2 Session Timeout"""
        print("\nTest Case 7: Session Timeout")
        
        # Test session timeout
        self.user_manager.session_timeout = 1  # Set timeout to 1 second
        user = self.user_manager.authenticate(self.test_username, self.test_password)
        
        # Session should be valid initially
        self.assertTrue(self.user_manager.validate_session(
            self.test_username,
            user.session_token
        ))
        
        # Wait for timeout
        time.sleep(2)
        
        # Session should be invalid after timeout
        self.assertFalse(self.user_manager.validate_session(
            self.test_username,
            user.session_token
        ))

if __name__ == '__main__':
    unittest.main(verbosity=2)
