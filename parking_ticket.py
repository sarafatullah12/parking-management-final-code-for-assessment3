from datetime import datetime
import math

# PARKING TICKET

class ParkingTicket:
    def __init__(self, vehicle, pricing_strategy):
        self.vehicle = vehicle
        self.vehicle_type = self._detect_vehicle_type(vehicle)
        self.pricing_strategy = pricing_strategy
        self.entry_time = datetime.now()
        self.exit_time = None
        self.duration = 0
        self.fee = 0

    def _detect_vehicle_type(self, vehicle):
        rate_to_type = {7: "car", 3: "bike", 10: "truck"}
        return rate_to_type.get(vehicle.get_rate(), "car")

    def close_ticket(self):
        self.exit_time = datetime.now()
        time_diff = self.exit_time - self.entry_time
        hours = time_diff.total_seconds() / 3600
        # charge for any started hour (ceil), minimum 1 hour
        self.duration = max(1, int(math.ceil(hours)))
        rate = self.vehicle.get_rate()
        self.fee = self.pricing_strategy.calculate_fee(self.duration, rate)
