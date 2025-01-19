import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import threading
import time
from pathlib import Path
from core.file_manager import FileManager
from datetime import datetime

class FileOperationsTest(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)
        
    def test_file_management(self):
        """2.1 File Management"""
        print("\nTest Case 1: Basic File Operations")
        
        # Test file creation
        test_file = self.test_dir / "test.txt"
        self.assertTrue(self.file_manager.create_file(test_file))
        self.assertTrue(test_file.exists())
        
        # Test file writing
        content = "Test content"
        self.assertTrue(self.file_manager.write_file(test_file, content))
        
        # Test file reading
        read_content = self.file_manager.read_file(test_file)
        self.assertEqual(read_content, content)
        
        # Test file deletion
        self.assertTrue(self.file_manager.delete_file(test_file))
        self.assertFalse(test_file.exists())
        
    def test_concurrent_access(self):
        """2.1 Concurrent Access Handling"""
        print("\nTest Case 2: Concurrent Access")
        
        test_file = self.test_dir / "concurrent.txt"
        
        def write_operation(content):
            self.file_manager.write_file(test_file, content)
            
        # Create multiple threads trying to write simultaneously
        threads = []
        for i in range(5):
            t = threading.Thread(target=write_operation, args=(f"Content {i}",))
            threads.append(t)
            
        # Start all threads
        for t in threads:
            t.start()
            
        # Wait for all threads to complete
        for t in threads:
            t.join()
            
        # Verify file integrity
        content = self.file_manager.read_file(test_file)
        self.assertIsNotNone(content)
        
    def test_payment_record_verification(self):
        """2.2 Payment Record Verification"""
        print("\nTest Case 3: Payment Record Verification")
        
        # Test bank statement verification
        statement_file = self.test_dir / "bank_statement.txt"
        self.file_manager.write_file(statement_file, "Valid statement content")
        self.assertTrue(self.file_manager.verify_bank_statement(statement_file))
        
        # Test CNP file verification
        cnp_file = self.test_dir / "cnp_file.txt"
        self.file_manager.write_file(cnp_file, "Valid CNP content")
        self.assertTrue(self.file_manager.verify_cnp_file(cnp_file))
        
        # Test treasury record verification
        treasury_file = self.test_dir / "treasury.txt"
        self.file_manager.write_file(treasury_file, "Valid treasury content")
        self.assertTrue(self.file_manager.verify_treasury_record(treasury_file))
        
    def test_error_handling(self):
        """2.3 Error Handling"""
        print("\nTest Case 4: Error Handling")
        
        # Test missing file
        missing_file = self.test_dir / "missing.txt"
        with self.assertRaises(FileNotFoundError):
            self.file_manager.read_file(missing_file)
            
        # Test corrupted file
        corrupted_file = self.test_dir / "corrupted.txt"
        with open(corrupted_file, 'wb') as f:
            f.write(b'\x00\xFF\xFF\xFF')  # Invalid UTF-8
        with self.assertRaises(UnicodeError):
            self.file_manager.read_file(corrupted_file)
            
        # Test permission issues
        if os.name != 'nt':  # Skip on Windows
            restricted_file = self.test_dir / "restricted.txt"
            restricted_file.touch()
            os.chmod(restricted_file, 0o000)
            with self.assertRaises(PermissionError):
                self.file_manager.write_file(restricted_file, "test")

if __name__ == '__main__':
    unittest.main(verbosity=2)
