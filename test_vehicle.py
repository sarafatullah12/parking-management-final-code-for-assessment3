import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vehicle import Car, Bike, Truck
from pricing_strategy import OffPeakPricing, PeakPricing, WeekendPricing


class TestVehicle(unittest.TestCase):

    def test_car_creation(self):
        car = Car("CAR123")
        self.assertEqual(car.plate_number, "CAR123")
        self.assertEqual(car.get_rate(), 7)

    def test_bike_creation(self):
        bike = Bike("BIKE456")
        self.assertEqual(bike.plate_number, "BIKE456")
        self.assertEqual(bike.get_rate(), 3)

    def test_truck_creation(self):
        truck = Truck("TRUCK789")
        self.assertEqual(truck.plate_number, "TRUCK789")
        self.assertEqual(truck.get_rate(), 10)


class TestPricingStrategy(unittest.TestCase):

    def test_off_peak_pricing(self):
        pricing = OffPeakPricing()
        fee = pricing.calculate_fee(3, 7)
        self.assertEqual(fee, 21.0)  # 3 * 7 * 1.0

    def test_peak_pricing(self):
        pricing = PeakPricing()
        fee = pricing.calculate_fee(3, 7)
        self.assertEqual(fee, 31.5)  # 3 * 7 * 1.5

    def test_weekend_pricing(self):
        pricing = WeekendPricing()
        fee = pricing.calculate_fee(3, 7)
        self.assertEqual(fee, 25.2)  # 3 * 7 * 1.2


if __name__ == '__main__':
    unittest.main()
