import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from core.validation_system import ValidationSystem

class ValidationSystemTest(unittest.TestCase):
    def setUp(self):
        self.validation_system = ValidationSystem()
        
    def test_company_validation(self):
        """1.1 Company Name Validation"""
        print("\nTest Case 1.1: Company Name Validation")
        
        # Test valid company
        valid, error = self.validation_system.validate_company("SALAM")
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test invalid company
        valid, error = self.validation_system.validate_company("INVALID")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test empty company
        valid, error = self.validation_system.validate_company("")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test None
        valid, error = self.validation_system.validate_company(None)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_beneficiary_validation(self):
        """1.1 Beneficiary Details Validation"""
        print("\nTest Case 1.2: Beneficiary Validation")
        
        # Test valid beneficiary
        valid_beneficiary = {
            'name': 'John Doe',
            'account': 'SA4420152043595120123456',
            'bank': 'Saudi National Bank'
        }
        valid, error = self.validation_system.validate_beneficiary(valid_beneficiary)
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test invalid beneficiary
        invalid_beneficiary = {
            'name': '',  # Empty name
            'account': 'INVALID',  # Invalid IBAN
            'bank': None  # Invalid bank
        }
        valid, error = self.validation_system.validate_beneficiary(invalid_beneficiary)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_reference_validation(self):
        """1.1 Reference Number Validation"""
        print("\nTest Case 1.3: Reference Number Validation")
        
        current_year = str(datetime.now().year)
        
        # Test valid reference
        valid, error = self.validation_system.validate_reference(f"TST-{current_year}-0001")
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test invalid format
        valid, error = self.validation_system.validate_reference("INVALID")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test empty reference
        valid, error = self.validation_system.validate_reference("")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_amount_validation(self):
        """1.1 Amount Validation"""
        print("\nTest Case 1.4: Amount Validation")
        
        # Test valid amount
        valid, error = self.validation_system.validate_amount(Decimal("1000.00"))
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test zero amount
        valid, error = self.validation_system.validate_amount(0)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test negative amount
        valid, error = self.validation_system.validate_amount(-100)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test invalid format
        valid, error = self.validation_system.validate_amount("invalid")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_date_validation(self):
        """1.1 Date Validation"""
        print("\nTest Case 1.5: Date Validation")
        
        today = datetime.now()
        
        # Test valid date (today)
        valid, error = self.validation_system.validate_date(today)
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test future date
        valid, error = self.validation_system.validate_date(today + timedelta(days=1))
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test old date (more than 1 year)
        valid, error = self.validation_system.validate_date(today - timedelta(days=366))
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_special_chars(self):
        """1.1 Special Characters Handling"""
        print("\nTest Case 1.6: Special Characters Handling")
        
        # Test special characters in reference
        valid, error = self.validation_system.validate_reference("REF#123")
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test special characters in beneficiary
        invalid_beneficiary = {
            'name': 'John<>Doe',
            'account': 'SA4420152043595120123456',
            'bank': 'Saudi National Bank'
        }
        valid, error = self.validation_system.validate_beneficiary(invalid_beneficiary)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_format_validation(self):
        """1.2 Format Validation"""
        print("\nTest Case 2.1: Format Validation")
        
        current_year = str(datetime.now().year)
        
        # Test valid data
        valid_data = {
            'company': 'SALAM',
            'beneficiary': {
                'name': 'John Doe',
                'account': 'SA4420152043595120123456',
                'bank': 'Saudi National Bank'
            },
            'reference': f'TST-{current_year}-0001',
            'amount': Decimal('1000.00'),
            'date': datetime.now()
        }
        valid, error = self.validation_system.validate_payment_data(valid_data)
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test invalid data
        invalid_data = {
            'company': 'INVALID',
            'beneficiary': {
                'name': '',
                'account': 'INVALID',
                'bank': None
            },
            'reference': 'INVALID',
            'amount': '-100',
            'date': datetime.now() + timedelta(days=1)
        }
        valid, error = self.validation_system.validate_payment_data(invalid_data)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
    def test_business_rules(self):
        """1.3 Business Rules Validation"""
        print("\nTest Case 3.1: Business Rules")
        
        current_year = str(datetime.now().year)
        
        # Test valid payment data
        valid_data = {
            'company': 'SALAM',
            'beneficiary': {
                'name': 'John Doe',
                'account': 'SA4420152043595120123456',
                'bank': 'Saudi National Bank'
            },
            'reference': f'TST-{current_year}-0001',
            'amount': Decimal('1000.00'),
            'date': datetime.now()
        }
        valid, error = self.validation_system.validate_payment_data(valid_data)
        self.assertTrue(valid)
        self.assertIsNone(error)
        
        # Test amount exceeding limit
        invalid_data = valid_data.copy()
        invalid_data['amount'] = Decimal('1000001.00')  # Exceeds 1M limit
        valid, error = self.validation_system.validate_payment_data(invalid_data)
        self.assertFalse(valid)
        self.assertIsNotNone(error)
        
        # Test invalid year in reference
        invalid_data = valid_data.copy()
        invalid_data['reference'] = 'TST-2020-0001'  # Old year
        valid, error = self.validation_system.validate_payment_data(invalid_data)
        self.assertFalse(valid)
        self.assertIsNotNone(error)

if __name__ == '__main__':
    unittest.main(verbosity=2)
