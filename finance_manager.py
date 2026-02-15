import os
from datetime import datetime, timedelta
from finance import Debtor, Creditor

# FINANCE MANAGER

class FinanceManager:
    def __init__(self, debtor_file="debtors.csv", creditor_file="creditors.csv"):
        self.debtor_file = debtor_file
        self.creditor_file = creditor_file
        self._initialize_files()

    def _initialize_files(self):
        try:
            if not os.path.exists(self.debtor_file):
                with open(self.debtor_file, 'w') as file:
                    file.write("Plate,VehicleType,AmountOwed,DueDate\n")

            if not os.path.exists(self.creditor_file):
                with open(self.creditor_file, 'w') as file:
                    file.write("Plate,VehicleType,PassType,ExpiryDate\n")
        except Exception as e:
            print(f"⚠ Error initializing finance files: {e}")

    # DEBTOR OPERATIONS

    def add_debtor(self, debtor):
        try:
            with open(self.debtor_file, 'a') as file:
                file.write(debtor.to_csv_row())
            return True
        except Exception as e:
            print(f"⚠ Error adding debtor: {e}")
            return False

    def get_all_debtors(self):
        debtors = []
        try:
            if not os.path.exists(self.debtor_file):
                return debtors

            with open(self.debtor_file, 'r') as file:
                lines = file.readlines()
                # Skip header
                for line in lines[1:]:
                    debtor = Debtor.from_csv_row(line)
                    if debtor:
                        debtors.append(debtor)
        except Exception as e:
            print(f"⚠ Error reading debtors: {e}")

        return debtors

    def get_30_day_debtors(self):
        overdue_debtors = []
        all_debtors = self.get_all_debtors()

        # Nested loop for checking each debtor
        for debtor in all_debtors:
            if debtor.is_30_days_overdue():
                overdue_debtors.append(debtor)

        return overdue_debtors

    def remove_debtor(self, plate_number):
        try:
            debtors = self.get_all_debtors()

            # Rewrite file without the specified debtor
            with open(self.debtor_file, 'w') as file:
                file.write("Plate,VehicleType,AmountOwed,DueDate\n")
                for debtor in debtors:
                    if debtor.plate_number != plate_number:
                        file.write(debtor.to_csv_row())
            return True
        except Exception as e:
            print(f"⚠ Error removing debtor: {e}")
            return False

    # CREDITOR OPERATIONS

    def add_creditor(self, creditor):
        try:
            # Check if plate already exists and update
            creditors = self.get_all_creditors()
            found = False

            for i in range(len(creditors)):
                if creditors[i].plate_number == creditor.plate_number:
                    creditors[i] = creditor
                    found = True
                    break

            if not found:
                creditors.append(creditor)

            # Rewrite file
            with open(self.creditor_file, 'w') as file:
                file.write("Plate,VehicleType,PassType,ExpiryDate\n")
                for cred in creditors:
                    file.write(cred.to_csv_row())
            return True
        except Exception as e:
            print(f"⚠ Error adding creditor: {e}")
            return False

    def get_all_creditors(self):
        creditors = []
        try:
            if not os.path.exists(self.creditor_file):
                return creditors

            with open(self.creditor_file, 'r') as file:
                lines = file.readlines()
                # Skip header
                for line in lines[1:]:
                    creditor = Creditor.from_csv_row(line)
                    if creditor:
                        creditors.append(creditor)
        except Exception as e:
            print(f"⚠ Error reading creditors: {e}")

        return creditors

    def get_creditor_by_plate(self, plate_number):
        creditors = self.get_all_creditors()
        for creditor in creditors:
            if creditor.plate_number == plate_number:
                return creditor
        return None

    def remove_creditor(self, plate_number):
        try:
            creditors = self.get_all_creditors()

            # Rewrite file without the specified creditor
            with open(self.creditor_file, 'w') as file:
                file.write("Plate,VehicleType,PassType,ExpiryDate\n")
                for creditor in creditors:
                    if creditor.plate_number != plate_number:
                        file.write(creditor.to_csv_row())
            return True
        except Exception as e:
            print(f"⚠ Error removing creditor: {e}")
            return False

    # FINANCIAL CALCULATIONS

    def calculate_total_expenses(self):
        # Basic operational expenses: maintenance, utilities, staff
        monthly_expenses = 5000  # Base monthly operational cost
        return monthly_expenses

    def calculate_total_revenue(self, transaction_manager):
        return transaction_manager.calculate_total_revenue()

    def calculate_profit(self, transaction_manager):
        revenue = self.calculate_total_revenue(transaction_manager)
        expenses = self.calculate_total_expenses()
        return revenue - expenses

    def manual_entry_debtor(self, plate_number, vehicle_type, amount_owed, days_until_due=0):
        try:
            due_date = datetime.now() - timedelta(days=abs(days_until_due))
            debtor = Debtor(plate_number, vehicle_type, amount_owed, due_date)
            return self.add_debtor(debtor)
        except Exception as e:
            print(f"⚠ Error in manual debtor entry: {e}")
            return False

    def manual_entry_creditor(self, plate_number, vehicle_type, pass_type, days_remaining):
        try:
            expiry_date = datetime.now() + timedelta(days=days_remaining)
            creditor = Creditor(plate_number, vehicle_type, pass_type, expiry_date)
            return self.add_creditor(creditor)
        except Exception as e:
            print(f"⚠ Error in manual creditor entry: {e}")
            return False
