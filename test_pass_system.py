import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pass_system import Pass, SingleEntryPass, WeeklyPass, MonthlyPass
from pricing_strategy import OffPeakPricing, PeakPricing


class TestPassSystem(unittest.TestCase):

    def test_weekly_pass_creation(self):
        pass_obj = WeeklyPass("ABC123", "car")
        self.assertEqual(pass_obj.plate_number, "ABC123")
        self.assertEqual(pass_obj.vehicle_type, "car")
        self.assertEqual(pass_obj.get_pass_type(), "Weekly Pass")

    def test_weekly_pass_prices(self):
        car_pass = WeeklyPass("CAR001", "car")
        bike_pass = WeeklyPass("BIKE001", "bike")
        truck_pass = WeeklyPass("TRUCK001", "truck")

        self.assertEqual(car_pass.get_price(), 40)
        self.assertEqual(bike_pass.get_price(), 15)
        self.assertEqual(truck_pass.get_price(), 60)

    def test_monthly_pass_creation(self):
        pass_obj = MonthlyPass("XYZ789", "truck")
        self.assertEqual(pass_obj.plate_number, "XYZ789")
        self.assertEqual(pass_obj.vehicle_type, "truck")
        self.assertEqual(pass_obj.get_pass_type(), "Monthly Pass")

    def test_monthly_pass_prices(self):
        car_pass = MonthlyPass("CAR002", "car")
        bike_pass = MonthlyPass("BIKE002", "bike")
        truck_pass = MonthlyPass("TRUCK002", "truck")

        self.assertEqual(car_pass.get_price(), 150)
        self.assertEqual(bike_pass.get_price(), 50)
        self.assertEqual(truck_pass.get_price(), 220)

    def test_weekly_pass_validity(self):
        pass_obj = WeeklyPass("TEST001", "car")
        self.assertTrue(pass_obj.is_valid())
        self.assertGreater(pass_obj.days_remaining(), 0)

    def test_monthly_pass_validity(self):
        pass_obj = MonthlyPass("TEST002", "bike")
        self.assertTrue(pass_obj.is_valid())
        self.assertGreater(pass_obj.days_remaining(), 0)

    def test_single_entry_pass(self):
        pricing = OffPeakPricing()
        pass_obj = SingleEntryPass("SINGLE001", "car", pricing)

        self.assertEqual(pass_obj.get_pass_type(), "Single Entry")

        # Calculate fee for 3 hours at rate 7
        fee = pass_obj.calculate_fee(3, 7)
        self.assertEqual(fee, 21.0)  # 3 * 7 * 1.0


if __name__ == '__main__':
    unittest.main()
