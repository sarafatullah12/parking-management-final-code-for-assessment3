from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# PASS SYSTEM

class Pass(ABC):
    def __init__(self, plate_number, vehicle_type):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type  # 'car', 'bike', 'truck'
        self.purchase_date = datetime.now()

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_pass_type(self):
        pass


class SingleEntryPass(Pass):
    def __init__(self, plate_number, vehicle_type, pricing_strategy):
        super().__init__(plate_number, vehicle_type)
        self.pricing_strategy = pricing_strategy
        self.hours = 0
        self.fee = 0

    def get_price(self):
        return self.fee

    def get_pass_type(self):
        return "Single Entry"

    def calculate_fee(self, hours, base_rate):
        self.hours = hours
        self.fee = self.pricing_strategy.calculate_fee(hours, base_rate)
        return self.fee


class WeeklyPass(Pass):
    # Flat fee prices for weekly passes
    WEEKLY_PRICES = {
        'car': 40,
        'bike': 15,
        'truck': 60
    }

    def __init__(self, plate_number, vehicle_type):
        super().__init__(plate_number, vehicle_type)
        self.expiry_date = self.purchase_date + timedelta(days=7)

    def get_price(self):
        return self.WEEKLY_PRICES.get(self.vehicle_type.lower(), 40)

    def get_pass_type(self):
        return "Weekly Pass"

    def is_valid(self):
        return datetime.now() < self.expiry_date

    def days_remaining(self):
        if self.is_valid():
            delta = self.expiry_date - datetime.now()
            return max(1, delta.days)
        return 0


class MonthlyPass(Pass):
    # Flat fee prices for monthly passes
    MONTHLY_PRICES = {
        'car': 150,
        'bike': 50,
        'truck': 220
    }

    def __init__(self, plate_number, vehicle_type):
        super().__init__(plate_number, vehicle_type)
        self.expiry_date = self.purchase_date + timedelta(days=30)

    def get_price(self):
        return self.MONTHLY_PRICES.get(self.vehicle_type.lower(), 150)

    def get_pass_type(self):
        return "Monthly Pass"

    def is_valid(self):
        return datetime.now() < self.expiry_date

    def days_remaining(self):
        if self.is_valid():
            delta = self.expiry_date - datetime.now()
            return max(1, delta.days)
        return 0
