from parking_lot import ParkingLot
from helpers import create_vehicle, choose_pricing
from vehicle import Car, Bike, Truck
from pass_system import WeeklyPass, MonthlyPass
from pricing_strategy import OffPeakPricing
from transaction import Transaction
from transaction_manager import TransactionManager
from finance_manager import FinanceManager
from finance import Debtor, Creditor
from reporting import ReportGenerator
from datetime import datetime, timedelta

# MAIN SYSTEM

def purchase_pass_menu(finance_manager, transaction_manager):
    print("\n--- Purchase Pass ---")
    plate = input("Enter plate number: ").strip()

    if not plate:
        print("⚠ Invalid plate number!")
        return

    # Check if already has active pass
    existing = finance_manager.get_creditor_by_plate(plate)
    if existing and existing.is_valid():
        print(f"⚠ This plate already has an active {existing.pass_type}!")
        print(f"   Days remaining: {existing.days_remaining()}")
        return

    v_type = input("Enter vehicle type (car/bike/truck): ").lower().strip()
    if v_type not in ['car', 'bike', 'truck']:
        print("⚠ Invalid vehicle type!")
        return

    print("\nPass Types:")
    print("1. Weekly Pass")
    print("2. Monthly Pass")
    choice = input("Select pass type: ").strip()

    pass_obj = None
    if choice == "1":
        pass_obj = WeeklyPass(plate, v_type)
    elif choice == "2":
        pass_obj = MonthlyPass(plate, v_type)
    else:
        print("⚠ Invalid choice!")
        return

    amount = pass_obj.get_price()
    pass_type = pass_obj.get_pass_type()

    print(f"\nPrice: ${amount}")
    confirm = input("Confirm purchase? (y/n): ").lower().strip()

    if confirm == 'y':
        # Add to creditors
        creditor = Creditor(plate, v_type, pass_type, pass_obj.expiry_date)
        if finance_manager.add_creditor(creditor):
            # Record transaction
            transaction = Transaction(plate, v_type, pass_type, amount)
            transaction_manager.add_transaction(transaction)
            print(f"\n✓ {pass_type} purchased successfully!")
            print(f"  Valid until: {pass_obj.expiry_date.strftime('%Y-%m-%d')}")
        else:
            print("⚠ Error processing purchase!")
    else:
        print("Purchase cancelled.")


def finance_menu(finance_manager, transaction_manager):
    while True:
        print("\n" + "="*50)
        print("      FINANCE & ACCOUNTING MODULE")
        print("="*50)
        print("A. View Financial Summary (Revenue/Expenses/Profit)")
        print("B. Identify Overdue Debtors (30+ Days)")
        print("C. Manage Creditors (Pre-paid Customers)")
        print("D. Manual Entry - Add Debtor")
        print("E. Manual Entry - Add Creditor")
        print("F. View All Debtors")
        print("G. Remove Debtor")
        print("0. Back to Main Menu")
        print("="*50)

        choice = input("Select option: ").strip().upper()

        if choice == "A" or choice == "1":
            # Financial summary
            revenue = finance_manager.calculate_total_revenue(transaction_manager)
            expenses = finance_manager.calculate_total_expenses()
            profit = finance_manager.calculate_profit(transaction_manager)

            print("\n----- Financial Summary -----")
            print(f"Total Revenue:  ${revenue:.2f}")
            print(f"Total Expenses: ${expenses:.2f}")
            print(f"Profit:         ${profit:.2f}")
            print("-----------------------------")

        elif choice == "F" or choice == "6":
            # All debtors
            debtors = finance_manager.get_all_debtors()
            print(f"\n----- All Debtors ({len(debtors)}) -----")
            if debtors:
                for debtor in debtors:
                    print(debtor)
            else:
                print("No debtors found.")
            print("-----------------------------")

        elif choice == "B" or choice == "2":
            # 30-day overdue debtors
            debtors = finance_manager.get_30_day_debtors()
            print(f"\n----- 30+ Day Overdue Debtors ({len(debtors)}) -----")
            if debtors:
                for debtor in debtors:
                    print(debtor)
            else:
                print("No overdue debtors found.")
            print("-----------------------------")

        elif choice == "C" or choice == "3":
            # All creditors
            creditors = finance_manager.get_all_creditors()
            print(f"\n----- Prepaid Subscribers ({len(creditors)}) -----")
            if creditors:
                for creditor in creditors:
                    print(creditor)
            else:
                print("No prepaid subscribers found.")
            print("-----------------------------")

        elif choice == "D" or choice == "4":
            # Manual debtor entry
            print("\n--- Add Debtor ---")
            try:
                plate = input("Plate number: ").strip()
                v_type = input("Vehicle type (car/bike/truck): ").strip()
                amount = float(input("Amount owed: $").strip())
                days_overdue = int(input("Days overdue: ").strip())

                if finance_manager.manual_entry_debtor(plate, v_type, amount, days_overdue):
                    print("✓ Debtor added successfully!")
                else:
                    print("⚠ Error adding debtor!")
            except ValueError:
                print("⚠ Invalid input!")

        elif choice == "E" or choice == "5":
            # Manual creditor entry
            print("\n--- Add Creditor ---")
            try:
                plate = input("Plate number: ").strip()
                v_type = input("Vehicle type (car/bike/truck): ").strip()
                print("Pass type: 1=Weekly, 2=Monthly")
                pass_choice = input("Choice: ").strip()

                if pass_choice == "1":
                    pass_type = "Weekly Pass"
                elif pass_choice == "2":
                    pass_type = "Monthly Pass"
                else:
                    print("⚠ Invalid pass type!")
                    continue

                days = int(input("Days remaining: ").strip())

                if finance_manager.manual_entry_creditor(plate, v_type, pass_type, days):
                    print("✓ Creditor added successfully!")
                else:
                    print("⚠ Error adding creditor!")
            except ValueError:
                print("⚠ Invalid input!")

        elif choice == "G" or choice == "7":
            # Remove debtor
            plate = input("Enter plate number to remove: ").strip()
            if finance_manager.remove_debtor(plate):
                print("✓ Debtor removed successfully!")
            else:
                print("⚠ Error removing debtor!")

        elif choice == "0":
            break
        else:
            print("⚠ Invalid option! Please select A-G or 0.")


def reports_menu(transaction_manager):
    report_gen = ReportGenerator(transaction_manager)

    while True:
        print("\n" + "="*50)
        print("         REPORTING DASHBOARD")
        print("="*50)
        print("A. Generate Monthly Sales Report")
        print("B. Sales Breakdown by Pass Type")
        print("C. Total Cars Processed per Month")
        print("D. List Available Months")
        print("0. Back to Main Menu")
        print("="*50)

        choice = input("Select option: ").strip().upper()

        if choice == "A" or choice == "1":
            # Monthly sales report
            try:
                year = int(input("Enter year (e.g., 2026) or 0 for current: ").strip())
                month = int(input("Enter month (1-12) or 0 for current: ").strip())

                if year == 0 or month == 0:
                    report_gen.generate_monthly_sale_report()
                else:
                    report_gen.generate_monthly_sale_report(year, month)
            except ValueError:
                print("⚠ Invalid input!")

        elif choice == "B" or choice == "2":
            # Pass type report
            report_gen.generate_pass_type_report()

        elif choice == "C" or choice == "3":
            # Vehicle count report
            try:
                year = int(input("Enter year (e.g., 2026) or 0 for current: ").strip())
                month = int(input("Enter month (1-12) or 0 for current: ").strip())

                if year == 0 or month == 0:
                    report_gen.generate_vehicle_count_report()
                else:
                    report_gen.generate_vehicle_count_report(year, month)
            except ValueError:
                print("⚠ Invalid input!")

        elif choice == "D" or choice == "4":
            # List months
            months = report_gen.list_all_months_with_data()
            print("\n----- Available Months -----")
            if months:
                for month_year, count in months:
                    print(f"{month_year}: {count} transactions")
            else:
                print("No data available.")
            print("----------------------------")

        elif choice == "0":
            break
        else:
            print("⚠ Invalid option! Please select A-D or 0.")


def main():
    # Initialize managers
    transaction_manager = TransactionManager()
    finance_manager = FinanceManager()

    # Initialize with default strategy (will be dynamic per entry)
    default_strategy = OffPeakPricing()
    parking_lot = ParkingLot(300, default_strategy, transaction_manager, finance_manager)

    print("\n" + "="*50)
    print("   URBAN CITY PARKING MANAGEMENT SYSTEM")
    print("="*50)

    while True:
        print("\n" + "="*50)
        print("            MAIN MENU")
        print("="*50)
        print("1. Vehicle Entry (Single Entry Parking)")
        print("2. Vehicle Entry (With Weekly/Monthly Pass)")
        print("3. Vehicle Exit & Billing")
        print("4. Purchase Pass (Weekly/Monthly)")
        print("5. Finance & Accounting Module")
        print("6. Reporting Dashboard")
        print("7. View Available Spaces (Capacity: 300)")
        print("8. System Settings")
        print("0. Exit Program")
        print("="*50)

        option = input("Select option: ").strip()

        if option == "1":
            # Park with single entry - ask for pricing strategy dynamically
            vehicle = create_vehicle()
            if vehicle:
                print("\nSelect Pricing Strategy for this entry:")
                strategy = choose_pricing()
                # Temporarily set strategy for this vehicle
                parking_lot.pricing_strategy = strategy
                success = parking_lot.park_vehicle(vehicle)

        elif option == "2":
            # Park with pass
            plate = input("Enter plate number: ").strip()
            if not plate:
                print("⚠ Invalid plate number!")
                continue
            parking_lot.park_with_pass(plate, finance_manager)

        elif option == "3":
            # Exit vehicle
            plate = input("Enter plate number to exit: ").strip()
            if not plate:
                print("⚠ Invalid plate number!")
                continue
            ticket = parking_lot.exit_vehicle(plate)

            # Record transaction if single entry
            if ticket:
                print("\nPayment Options:")
                print("1. Pay Now")
                print("2. Pay Later (30-day credit)")
                pay_choice = input("Select payment option: ").strip()

                if pay_choice == "2":
                    # Create debtor with 30-day due date
                    due_date = datetime.now() + timedelta(days=30)
                    debtor = Debtor(plate, ticket.vehicle_type, ticket.fee, due_date)
                    finance_manager.add_debtor(debtor)
                    print(f"\nPayment deferred. Amount owed: ${ticket.fee:.2f}")
                    print(f"Due date: {due_date.strftime('%Y-%m-%d')}")
                    print("You can view this in Finance > View All Debtors.")
                else:
                    # Pay now - record transaction as revenue
                    transaction = Transaction(
                        plate,
                        ticket.vehicle_type,
                        "Single Entry",
                        ticket.fee,
                        ticket.duration
                    )
                    transaction_manager.add_transaction(transaction)
                    print("Payment received.")

        elif option == "4":
            # Purchase pass
            purchase_pass_menu(finance_manager, transaction_manager)

        elif option == "5":
            # Finance module
            finance_menu(finance_manager, transaction_manager)

        elif option == "6":
            # Reports
            reports_menu(transaction_manager)

        elif option == "7":
            # Show spaces
            print(f"\n{'='*50}")
            print(f"  Parking Capacity Status")
            print(f"{'='*50}")
            print(f"  Total Spaces:     {parking_lot.total_spaces}")
            print(f"  Available Spaces: {parking_lot.available_spaces}")
            print(f"  Occupied Spaces:  {parking_lot.total_spaces - parking_lot.available_spaces}")
            print(f"{'='*50}")

        elif option == "8":
            # System Settings
            print("\n===== System Settings =====")
            print("1. View Current Pricing Rates")
            print("2. Back to Main Menu")

            setting_choice = input("Select option: ").strip()

            if setting_choice == "1":
                print("\n----- Pricing Rates -----")
                print("\nHourly Rates (Single Entry):")
                print("  Car:   $7/hour")
                print("  Bike:  $3/hour")
                print("  Truck: $10/hour")
                print("\nPricing Multipliers:")
                print("  Off-Peak: 1.0x (base rate)")
                print("  Peak:     1.5x")
                print("  Weekend:  1.2x")
                print("\nWeekly Pass Rates:")
                print("  Car:   $40")
                print("  Bike:  $15")
                print("  Truck: $60")
                print("\nMonthly Pass Rates:")
                print("  Car:   $150")
                print("  Bike:  $50")
                print("  Truck: $220")
                print("-------------------------")

        elif option == "0":
            print("\n" + "="*50)
            print("  Thank you for using the Parking System!")
            print("  All data has been saved to CSV files.")
            print("="*50)
            break

        else:
            print("⚠ Invalid option! Please enter a number from the menu.")


if __name__ == "__main__":
    main()
