from vehicle import Car, Bike, Truck
from pricing_strategy import PeakPricing, OffPeakPricing, WeekendPricing

# HELPER FUNCTION

def create_vehicle():
    v_type = input("Enter vehicle type (car/bike/truck): ").lower().strip()

    if v_type not in ['car', 'bike', 'truck']:
        print("⚠ Invalid vehicle type!")
        return None

    plate = input("Enter plate number: ").strip()
    if not plate:
        print("⚠ Invalid plate number!")
        return None

    if v_type == "car":
        return Car(plate)
    elif v_type == "bike":
        return Bike(plate)
    else:
        return Truck(plate)

def choose_pricing():
    print("Select Pricing Strategy:")
    print("1. Peak")
    print("2. Off-Peak")
    print("3. Weekend")
    choice = input("Choice: ")
    if choice == "1":
        return PeakPricing()
    elif choice == "2":
        return OffPeakPricing()
    elif choice == "3":
        return WeekendPricing()
    else:
        print("Invalid choice! Defaulting to Off-Peak.")
        return OffPeakPricing()
