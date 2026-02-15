from parking_ticket import ParkingTicket

# PARKING LOT

class ParkingLot:
    def __init__(self, total_spaces, pricing_strategy, transaction_manager=None, finance_manager=None):
        self.total_spaces = total_spaces
        self.available_spaces = total_spaces
        self.active_tickets = {}
        self.pricing_strategy = pricing_strategy
        self.transaction_manager = transaction_manager
        self.finance_manager = finance_manager

    def park_vehicle(self, vehicle):
        if self.available_spaces <= 0:
            print("Parking Full!")
            return False
        if vehicle.plate_number in self.active_tickets:
            print("⚠ Vehicle already inside!")
            return False
        ticket = ParkingTicket(vehicle, self.pricing_strategy)
        self.active_tickets[vehicle.plate_number] = ticket
        self.available_spaces -= 1
        print(f"Vehicle {vehicle.plate_number} parked. Spaces left: {self.available_spaces}")
        return True

    def park_with_pass(self, plate_number, finance_manager):
        if self.available_spaces <= 0:
            print("Parking Full!")
            return False

        # Check if vehicle has valid pass
        creditor = finance_manager.get_creditor_by_plate(plate_number)

        if creditor is None:
            print("⚠ No active pass found for this plate.")
            print("  Please purchase a pass first (Main Menu > Option 4).")
            return False

        if not creditor.is_valid():
            print("⚠ Pass has expired!")
            print("  Please renew your pass (Main Menu > Option 4).")
            return False

        if plate_number in self.active_tickets:
            print("⚠ Vehicle already inside!")
            return False

        print(f"Vehicle {plate_number} ({creditor.pass_type}) parked.")
        print(f"   Pass valid for {creditor.days_remaining()} more days.")
        print(f"   Spaces left: {self.available_spaces - 1}")

        # Create simple ticket for tracking (no fee)
        self.active_tickets[plate_number] = {
            'type': 'pass',
            'pass_type': creditor.pass_type
        }
        self.available_spaces -= 1
        return True

    def exit_vehicle(self, plate_number):
        if plate_number not in self.active_tickets:
            print("Vehicle not found!")
            return None

        ticket = self.active_tickets.pop(plate_number)
        self.available_spaces += 1

        # Check if it's a pass-based entry
        if isinstance(ticket, dict) and ticket.get('type') == 'pass':
            print(f"\nVehicle {plate_number} exited (pass holder).")
            print(f"   Spaces left: {self.available_spaces}")
            return None

        # Process single entry ticket
        ticket.close_ticket()

        print("\n----- Parking Bill -----")
        print(f"Plate: {plate_number}")
        print(f"Vehicle Type: {ticket.vehicle_type}")
        print(f"Hours: {ticket.duration}")
        print(f"Total Fee: ${ticket.fee:.2f}")
        print(f"Spaces left: {self.available_spaces}")
        print("------------------------")

        return ticket
