import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from finance import Debtor, Creditor
from finance_manager import FinanceManager


class TestFinance(unittest.TestCase):

    def setUp(self):
        self.test_debtor_file = "test_debtors.csv"
        self.test_creditor_file = "test_creditors.csv"

        # Clean up test files if they exist
        if os.path.exists(self.test_debtor_file):
            os.remove(self.test_debtor_file)
        if os.path.exists(self.test_creditor_file):
            os.remove(self.test_creditor_file)

    def tearDown(self):
        if os.path.exists(self.test_debtor_file):
            os.remove(self.test_debtor_file)
        if os.path.exists(self.test_creditor_file):
            os.remove(self.test_creditor_file)

    def test_debtor_creation(self):
        due_date = datetime.now() - timedelta(days=35)
        debtor = Debtor("DEBT001", "car", 150.0, due_date)

        self.assertEqual(debtor.plate_number, "DEBT001")
        self.assertEqual(debtor.vehicle_type, "car")
        self.assertEqual(debtor.amount_owed, 150.0)
        self.assertTrue(debtor.is_30_days_overdue())

    def test_debtor_days_overdue(self):
        due_date = datetime.now() - timedelta(days=45)
        debtor = Debtor("DEBT002", "truck", 200.0, due_date)

        self.assertGreaterEqual(debtor.days_overdue(), 45)

    def test_creditor_creation(self):
        expiry = datetime.now() + timedelta(days=10)
        creditor = Creditor("CRED001", "bike", "Weekly Pass", expiry)

        self.assertEqual(creditor.plate_number, "CRED001")
        self.assertEqual(creditor.vehicle_type, "bike")
        self.assertEqual(creditor.pass_type, "Weekly Pass")
        self.assertTrue(creditor.is_valid())

    def test_creditor_days_remaining(self):
        expiry = datetime.now() + timedelta(days=20)
        creditor = Creditor("CRED002", "car", "Monthly Pass", expiry)

        self.assertGreaterEqual(creditor.days_remaining(), 19)
        self.assertLessEqual(creditor.days_remaining(), 20)

    def test_finance_manager_add_debtor(self):
        manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)

        due_date = datetime.now() - timedelta(days=40)
        debtor = Debtor("TEST001", "car", 100.0, due_date)

        result = manager.add_debtor(debtor)
        self.assertTrue(result)

        # Verify it was added
        all_debtors = manager.get_all_debtors()
        self.assertEqual(len(all_debtors), 1)
        self.assertEqual(all_debtors[0].plate_number, "TEST001")

    def test_finance_manager_30_day_debtors(self):
        manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)

        # Add overdue debtor
        due_date1 = datetime.now() - timedelta(days=35)
        debtor1 = Debtor("OVER001", "car", 150.0, due_date1)
        manager.add_debtor(debtor1)

        # Add non-overdue debtor
        due_date2 = datetime.now() - timedelta(days=20)
        debtor2 = Debtor("OK001", "bike", 50.0, due_date2)
        manager.add_debtor(debtor2)

        # Get 30-day overdue
        overdue = manager.get_30_day_debtors()

        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].plate_number, "OVER001")

    def test_finance_manager_add_creditor(self):
        manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)

        expiry = datetime.now() + timedelta(days=15)
        creditor = Creditor("CTEST001", "truck", "Monthly Pass", expiry)

        result = manager.add_creditor(creditor)
        self.assertTrue(result)

        # Verify it was added
        all_creditors = manager.get_all_creditors()
        self.assertEqual(len(all_creditors), 1)
        self.assertEqual(all_creditors[0].plate_number, "CTEST001")

    def test_pay_later_debtor_future_due_date(self):
        due_date = datetime.now() + timedelta(days=30)
        debtor = Debtor("LATER001", "car", 7.0, due_date)

        self.assertEqual(debtor.plate_number, "LATER001")
        self.assertEqual(debtor.amount_owed, 7.0)
        self.assertEqual(debtor.days_overdue(), 0)
        self.assertFalse(debtor.is_30_days_overdue())

    def test_pay_later_debtor_persists_in_manager(self):
        manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)

        due_date = datetime.now() + timedelta(days=30)
        debtor = Debtor("LATER002", "bike", 3.0, due_date)
        manager.add_debtor(debtor)

        all_debtors = manager.get_all_debtors()
        self.assertEqual(len(all_debtors), 1)
        self.assertEqual(all_debtors[0].plate_number, "LATER002")
        self.assertEqual(all_debtors[0].amount_owed, 3.0)
        self.assertFalse(all_debtors[0].is_30_days_overdue())

    def test_pay_later_debtor_not_in_overdue_list(self):
        manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)

        # Fresh debtor (due in 30 days)
        due_future = datetime.now() + timedelta(days=30)
        debtor_new = Debtor("FRESH001", "car", 10.5, due_future)
        manager.add_debtor(debtor_new)

        # Old debtor (due 40 days ago)
        due_past = datetime.now() - timedelta(days=40)
        debtor_old = Debtor("OLD001", "truck", 15.0, due_past)
        manager.add_debtor(debtor_old)

        overdue = manager.get_30_day_debtors()
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].plate_number, "OLD001")

    def test_remove_debtor(self):
        manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)

        due_date = datetime.now() + timedelta(days=30)
        debtor = Debtor("REM001", "car", 7.0, due_date)
        manager.add_debtor(debtor)

        self.assertEqual(len(manager.get_all_debtors()), 1)

        result = manager.remove_debtor("REM001")
        self.assertTrue(result)
        self.assertEqual(len(manager.get_all_debtors()), 0)

    def test_creditor_expired(self):
        expiry = datetime.now() - timedelta(days=1)
        creditor = Creditor("EXP001", "car", "Weekly Pass", expiry)

        self.assertFalse(creditor.is_valid())
        self.assertEqual(creditor.days_remaining(), 0)

    def test_debtor_csv_round_trip(self):
        due_date = datetime.now() + timedelta(days=30)
        debtor = Debtor("CSV001", "truck", 15.0, due_date)

        csv_row = debtor.to_csv_row()
        restored = Debtor.from_csv_row(csv_row)

        self.assertIsNotNone(restored)
        self.assertEqual(restored.plate_number, "CSV001")
        self.assertEqual(restored.vehicle_type, "truck")
        self.assertEqual(restored.amount_owed, 15.0)

    def test_creditor_csv_round_trip(self):
        expiry = datetime.now() + timedelta(days=7)
        creditor = Creditor("CSV002", "bike", "Weekly Pass", expiry)

        csv_row = creditor.to_csv_row()
        restored = Creditor.from_csv_row(csv_row)

        self.assertIsNotNone(restored)
        self.assertEqual(restored.plate_number, "CSV002")
        self.assertEqual(restored.pass_type, "Weekly Pass")
        self.assertTrue(restored.is_valid())


if __name__ == '__main__':
    unittest.main()
