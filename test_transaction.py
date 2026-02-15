import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transaction import Transaction
from transaction_manager import TransactionManager


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_transactions.csv"

        # Clean up test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_transaction_creation(self):
        trans = Transaction("PLATE001", "car", "Single Entry", 25.5, 3)

        self.assertEqual(trans.plate_number, "PLATE001")
        self.assertEqual(trans.vehicle_type, "car")
        self.assertEqual(trans.pass_type, "Single Entry")
        self.assertEqual(trans.amount, 25.5)
        self.assertEqual(trans.hours, 3)

    def test_transaction_to_csv(self):
        trans = Transaction("TEST001", "bike", "Weekly Pass", 15.0, 0)
        csv_row = trans.to_csv_row()

        # Check that all fields are present
        self.assertIn("TEST001", csv_row)
        self.assertIn("bike", csv_row)
        self.assertIn("Weekly Pass", csv_row)
        self.assertIn("15.0", csv_row)

    def test_transaction_manager_add(self):
        manager = TransactionManager(self.test_file)

        trans = Transaction("ADD001", "car", "Monthly Pass", 150.0)
        result = manager.add_transaction(trans)

        self.assertTrue(result)

        # Verify it was added
        all_trans = manager.get_all_transactions()
        self.assertEqual(len(all_trans), 1)
        self.assertEqual(all_trans[0].plate_number, "ADD001")

    def test_transaction_manager_multiple(self):
        manager = TransactionManager(self.test_file)

        trans1 = Transaction("PLATE1", "car", "Single Entry", 21.0, 3)
        trans2 = Transaction("PLATE2", "bike", "Weekly Pass", 15.0)
        trans3 = Transaction("PLATE3", "truck", "Monthly Pass", 220.0)

        manager.add_transaction(trans1)
        manager.add_transaction(trans2)
        manager.add_transaction(trans3)

        all_trans = manager.get_all_transactions()
        self.assertEqual(len(all_trans), 3)

    def test_transaction_manager_by_pass_type(self):
        manager = TransactionManager(self.test_file)

        manager.add_transaction(Transaction("P1", "car", "Weekly Pass", 40.0))
        manager.add_transaction(Transaction("P2", "bike", "Weekly Pass", 15.0))
        manager.add_transaction(Transaction("P3", "car", "Monthly Pass", 150.0))

        weekly = manager.get_transactions_by_pass_type("Weekly Pass")
        monthly = manager.get_transactions_by_pass_type("Monthly Pass")

        self.assertEqual(len(weekly), 2)
        self.assertEqual(len(monthly), 1)

    def test_transaction_manager_by_vehicle_type(self):
        manager = TransactionManager(self.test_file)

        manager.add_transaction(Transaction("C1", "car", "Single Entry", 21.0))
        manager.add_transaction(Transaction("C2", "car", "Weekly Pass", 40.0))
        manager.add_transaction(Transaction("B1", "bike", "Weekly Pass", 15.0))

        cars = manager.get_transactions_by_vehicle_type("car")
        bikes = manager.get_transactions_by_vehicle_type("bike")

        self.assertEqual(len(cars), 2)
        self.assertEqual(len(bikes), 1)

    def test_transaction_manager_total_revenue(self):
        manager = TransactionManager(self.test_file)

        manager.add_transaction(Transaction("P1", "car", "Weekly Pass", 40.0))
        manager.add_transaction(Transaction("P2", "bike", "Weekly Pass", 15.0))
        manager.add_transaction(Transaction("P3", "truck", "Monthly Pass", 220.0))

        total = manager.calculate_total_revenue()
        self.assertEqual(total, 275.0)


if __name__ == '__main__':
    unittest.main()
