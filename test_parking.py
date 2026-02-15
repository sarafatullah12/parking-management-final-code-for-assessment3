import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vehicle import Car, Bike, Truck
from parking_lot import ParkingLot
from parking_ticket import ParkingTicket
from pricing_strategy import OffPeakPricing, PeakPricing, WeekendPricing
from transaction_manager import TransactionManager
from finance_manager import FinanceManager
from finance import Creditor


class TestParkingTicket(unittest.TestCase):

    def test_ticket_creation(self):
        car = Car("TEST001")
        strategy = OffPeakPricing()
        ticket = ParkingTicket(car, strategy)

        self.assertEqual(ticket.vehicle, car)
        self.assertEqual(ticket.pricing_strategy, strategy)
        self.assertEqual(ticket.vehicle_type, "car")
        self.assertEqual(ticket.fee, 0)
        self.assertEqual(ticket.duration, 0)
        self.assertIsNotNone(ticket.entry_time)
        self.assertIsNone(ticket.exit_time)

    def test_ticket_vehicle_type_detection(self):
        car_ticket = ParkingTicket(Car("C1"), OffPeakPricing())
        bike_ticket = ParkingTicket(Bike("B1"), OffPeakPricing())
        truck_ticket = ParkingTicket(Truck("T1"), OffPeakPricing())

        self.assertEqual(car_ticket.vehicle_type, "car")
        self.assertEqual(bike_ticket.vehicle_type, "bike")
        self.assertEqual(truck_ticket.vehicle_type, "truck")

    def test_close_ticket_minimum_one_hour(self):
        car = Car("MIN001")
        strategy = OffPeakPricing()
        ticket = ParkingTicket(car, strategy)

        ticket.close_ticket()

        self.assertEqual(ticket.duration, 1)
        self.assertEqual(ticket.fee, 7.0)  # 1 hour * $7/hr * 1.0x
        self.assertIsNotNone(ticket.exit_time)

    def test_close_ticket_uses_stored_strategy(self):
        car = Car("STRAT001")
        peak = PeakPricing()
        ticket = ParkingTicket(car, peak)

        ticket.close_ticket()

        # Should use PeakPricing: 1 hour * $7 * 1.5 = $10.50
        self.assertEqual(ticket.fee, 10.5)

    def test_close_ticket_weekend_pricing(self):
        truck = Truck("WKND001")
        weekend = WeekendPricing()
        ticket = ParkingTicket(truck, weekend)

        ticket.close_ticket()

        # 1 hour * $10 * 1.2 = $12.0
        self.assertEqual(ticket.fee, 12.0)


class TestParkingLot(unittest.TestCase):

    def setUp(self):
        self.test_trans_file = "test_parking_transactions.csv"
        self.test_debtor_file = "test_parking_debtors.csv"
        self.test_creditor_file = "test_parking_creditors.csv"

        # Clean up test files
        for f in [self.test_trans_file, self.test_debtor_file, self.test_creditor_file]:
            if os.path.exists(f):
                os.remove(f)

        self.trans_manager = TransactionManager(self.test_trans_file)
        self.fin_manager = FinanceManager(self.test_debtor_file, self.test_creditor_file)
        self.strategy = OffPeakPricing()
        self.lot = ParkingLot(5, self.strategy, self.trans_manager, self.fin_manager)

    def tearDown(self):
        for f in [self.test_trans_file, self.test_debtor_file, self.test_creditor_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_parking_lot_initialization(self):
        self.assertEqual(self.lot.total_spaces, 5)
        self.assertEqual(self.lot.available_spaces, 5)
        self.assertEqual(len(self.lot.active_tickets), 0)

    def test_park_vehicle_success(self):
        car = Car("PARK001")
        result = self.lot.park_vehicle(car)

        self.assertTrue(result)
        self.assertEqual(self.lot.available_spaces, 4)
        self.assertIn("PARK001", self.lot.active_tickets)

    def test_park_vehicle_full_lot(self):
        # Fill the lot
        for i in range(5):
            self.lot.park_vehicle(Car(f"FILL{i:03d}"))

        # Try to park one more
        result = self.lot.park_vehicle(Car("EXTRA001"))
        self.assertFalse(result)
        self.assertEqual(self.lot.available_spaces, 0)

    def test_park_duplicate_vehicle(self):
        car = Car("DUP001")
        self.lot.park_vehicle(car)

        result = self.lot.park_vehicle(Car("DUP001"))
        self.assertFalse(result)
        self.assertEqual(self.lot.available_spaces, 4)

    def test_exit_vehicle_success(self):
        car = Car("EXIT001")
        self.lot.park_vehicle(car)

        ticket = self.lot.exit_vehicle("EXIT001")

        self.assertIsNotNone(ticket)
        self.assertEqual(self.lot.available_spaces, 5)
        self.assertNotIn("EXIT001", self.lot.active_tickets)

    def test_exit_vehicle_not_found(self):
        result = self.lot.exit_vehicle("GHOST001")
        self.assertIsNone(result)

    def test_park_with_pass_success(self):
        # Add a creditor with valid pass
        expiry = datetime.now() + timedelta(days=10)
        creditor = Creditor("PASS001", "car", "Weekly Pass", expiry)
        self.fin_manager.add_creditor(creditor)

        result = self.lot.park_with_pass("PASS001", self.fin_manager)

        self.assertTrue(result)
        self.assertEqual(self.lot.available_spaces, 4)

    def test_park_with_pass_no_pass(self):
        result = self.lot.park_with_pass("NOPASS001", self.fin_manager)
        self.assertFalse(result)

    def test_park_with_pass_expired(self):
        expiry = datetime.now() - timedelta(days=1)
        creditor = Creditor("EXP001", "car", "Weekly Pass", expiry)
        self.fin_manager.add_creditor(creditor)

        result = self.lot.park_with_pass("EXP001", self.fin_manager)
        self.assertFalse(result)

    def test_exit_pass_vehicle(self):
        expiry = datetime.now() + timedelta(days=10)
        creditor = Creditor("PEXIT001", "car", "Weekly Pass", expiry)
        self.fin_manager.add_creditor(creditor)

        self.lot.park_with_pass("PEXIT001", self.fin_manager)
        result = self.lot.exit_vehicle("PEXIT001")

        # Pass exit returns None (no ticket/charge)
        self.assertIsNone(result)
        self.assertEqual(self.lot.available_spaces, 5)

    def test_multiple_vehicles_different_strategies(self):
        car_a = Car("STRAT_A")
        car_b = Car("STRAT_B")

        # Park car A with Peak pricing
        self.lot.pricing_strategy = PeakPricing()
        self.lot.park_vehicle(car_a)

        # Park car B with Weekend pricing
        self.lot.pricing_strategy = WeekendPricing()
        self.lot.park_vehicle(car_b)

        # Exit car A - should use Peak pricing (1.5x), NOT Weekend
        ticket_a = self.lot.exit_vehicle("STRAT_A")
        self.assertEqual(ticket_a.fee, 10.5)  # 1hr * $7 * 1.5

        # Exit car B - should use Weekend pricing (1.2x)
        ticket_b = self.lot.exit_vehicle("STRAT_B")
        self.assertEqual(ticket_b.fee, 8.4)  # 1hr * $7 * 1.2


class TestParkingLotCapacity(unittest.TestCase):

    def setUp(self):
        self.lot = ParkingLot(3, OffPeakPricing())

    def test_capacity_tracking(self):
        self.lot.park_vehicle(Car("C1"))
        self.assertEqual(self.lot.available_spaces, 2)

        self.lot.park_vehicle(Bike("B1"))
        self.assertEqual(self.lot.available_spaces, 1)

        self.lot.exit_vehicle("C1")
        self.assertEqual(self.lot.available_spaces, 2)

        self.lot.park_vehicle(Truck("T1"))
        self.assertEqual(self.lot.available_spaces, 1)

        self.lot.exit_vehicle("B1")
        self.lot.exit_vehicle("T1")
        self.assertEqual(self.lot.available_spaces, 3)


if __name__ == '__main__':
    unittest.main()
