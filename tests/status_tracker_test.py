import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime
from core.status_tracker import StatusTracker
from pathlib import Path

class StatusTrackerTest(unittest.TestCase):
    def setUp(self):
        self.status_tracker = StatusTracker()
        self.test_payment_id = "PAY123456"
        
    def test_status_transitions(self):
        """3.1 Payment Status Transitions"""
        print("\nTest Case 1: Status Transitions")
        
        # Test initial status
        status = self.status_tracker.get_status(self.test_payment_id)
        self.assertEqual(status, "INITIATED")
        
        # Test valid transition
        self.assertTrue(self.status_tracker.update_status(self.test_payment_id, "PENDING"))
        status = self.status_tracker.get_status(self.test_payment_id)
        self.assertEqual(status, "PENDING")
        
        # Test invalid transition (can't go from PENDING to INITIATED)
        self.assertFalse(self.status_tracker.update_status(self.test_payment_id, "INITIATED"))
        
        # Test complete flow
        valid_flow = ["APPROVED", "PROCESSING", "COMPLETED"]
        for new_status in valid_flow:
            self.assertTrue(self.status_tracker.update_status(self.test_payment_id, new_status))
            status = self.status_tracker.get_status(self.test_payment_id)
            self.assertEqual(status, new_status)
            
    def test_status_history(self):
        """3.1 Status History"""
        print("\nTest Case 2: Status History")
        
        # Create a sequence of status updates
        statuses = ["INITIATED", "PENDING", "APPROVED", "PROCESSING", "COMPLETED"]
        for status in statuses:
            self.status_tracker.update_status(self.test_payment_id, status)
            
        # Get history
        history = self.status_tracker.get_status_history(self.test_payment_id)
        
        # Verify history
        self.assertEqual(len(history), len(statuses))
        for i, entry in enumerate(history):
            self.assertEqual(entry['status'], statuses[i])
            self.assertIsInstance(entry['timestamp'], datetime)
            
    def test_status_queries(self):
        """3.1 Status Queries"""
        print("\nTest Case 3: Status Queries")
        
        # Create multiple payments with different statuses
        payments = {
            "PAY1": "PENDING",
            "PAY2": "APPROVED",
            "PAY3": "COMPLETED",
            "PAY4": "PENDING"
        }
        
        for payment_id, status in payments.items():
            self.status_tracker.update_status(payment_id, status)
            
        # Test filtering by status
        pending_payments = self.status_tracker.get_payments_by_status("PENDING")
        self.assertEqual(len(pending_payments), 2)
        
        # Test getting all active payments
        active_payments = self.status_tracker.get_active_payments()
        self.assertEqual(len(active_payments), 3)  # Excluding COMPLETED
        
    def test_directory_management(self):
        """3.2 Directory Management"""
        print("\nTest Case 4: Directory Management")
        
        test_dir = Path("test_status_dir")
        
        # Test directory creation
        self.assertTrue(self.status_tracker.create_status_directory(test_dir))
        self.assertTrue(test_dir.exists())
        
        # Test subdirectory creation for each status
        status_dirs = ["pending", "approved", "completed"]
        for status_dir in status_dirs:
            self.assertTrue((test_dir / status_dir).exists())
            
        # Test path validation
        self.assertTrue(self.status_tracker.validate_status_path(test_dir))
        self.assertFalse(self.status_tracker.validate_status_path(test_dir / "nonexistent"))
        
        # Test permission checks
        if os.name != 'nt':  # Skip on Windows
            test_restricted = test_dir / "restricted"
            test_restricted.mkdir(exist_ok=True)
            os.chmod(test_restricted, 0o000)
            self.assertFalse(self.status_tracker.validate_status_path(test_restricted))
            
        # Clean up
        import shutil
        shutil.rmtree(test_dir)
        
    def test_status_updates(self):
        """3.1 Status Updates with Validation"""
        print("\nTest Case 5: Status Updates with Validation")
        
        # Test invalid status
        self.assertFalse(self.status_tracker.update_status(self.test_payment_id, "INVALID_STATUS"))
        
        # Test status update with notes
        self.assertTrue(self.status_tracker.update_status(
            self.test_payment_id, 
            "PENDING", 
            notes="Awaiting approval"
        ))
        
        # Test status update with invalid payment ID
        self.assertFalse(self.status_tracker.update_status("INVALID_ID", "PENDING"))

if __name__ == '__main__':
    unittest.main(verbosity=2)
