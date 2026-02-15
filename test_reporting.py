import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transaction import Transaction
from transaction_manager import TransactionManager
from reporting import ReportGenerator


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_report_transactions.csv"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        self.manager = TransactionManager(self.test_file)
        self.report_gen = ReportGenerator(self.manager)

        # Add sample transactions for current month
        now = datetime.now()
        transactions = [
            Transaction("CAR001", "car", "Single Entry", 21.0, 3),
            Transaction("CAR002", "car", "Weekly Pass", 40.0),
            Transaction("BIKE001", "bike", "Single Entry", 9.0, 3),
            Transaction("BIKE002", "bike", "Monthly Pass", 50.0),
            Transaction("TRUCK001", "truck", "Weekly Pass", 60.0),
            Transaction("CAR003", "car", "Monthly Pass", 150.0),
        ]
        for t in transactions:
            t.date = now
            self.manager.add_transaction(t)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_monthly_sale_report_runs(self):
        now = datetime.now()
        # Should not raise any exceptions
        self.report_gen.generate_monthly_sale_report(now.year, now.month)

    def test_pass_type_report_runs(self):
        self.report_gen.generate_pass_type_report()

    def test_vehicle_count_report_runs(self):
        now = datetime.now()
        self.report_gen.generate_vehicle_count_report(now.year, now.month)

    def test_list_months_with_data(self):
        months = self.report_gen.list_all_months_with_data()
        self.assertEqual(len(months), 1)
        self.assertEqual(months[0][1], 6)  # 6 transactions

    def test_empty_report(self):
        # Use a month with no data
        self.report_gen.generate_monthly_sale_report(2020, 1)

    def test_transactions_by_pass_type(self):
        weekly = self.manager.get_transactions_by_pass_type("Weekly Pass")
        monthly = self.manager.get_transactions_by_pass_type("Monthly Pass")
        single = self.manager.get_transactions_by_pass_type("Single Entry")

        self.assertEqual(len(weekly), 2)
        self.assertEqual(len(monthly), 2)
        self.assertEqual(len(single), 2)

    def test_transactions_by_vehicle_type(self):
        cars = self.manager.get_transactions_by_vehicle_type("car")
        bikes = self.manager.get_transactions_by_vehicle_type("bike")
        trucks = self.manager.get_transactions_by_vehicle_type("truck")

        self.assertEqual(len(cars), 3)
        self.assertEqual(len(bikes), 2)
        self.assertEqual(len(trucks), 1)

    def test_total_revenue_calculation(self):
        total = self.manager.calculate_total_revenue()
        expected = 21.0 + 40.0 + 9.0 + 50.0 + 60.0 + 150.0
        self.assertEqual(total, expected)


if __name__ == '__main__':
    unittest.main()
