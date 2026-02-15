import os
from transaction import Transaction

# TRANSACTION MANAGER

class TransactionManager:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self._initialize_file()

    def _initialize_file(self):
        try:
            if not os.path.exists(self.filename):
                with open(self.filename, 'w') as file:
                    file.write("Date,Plate,VehicleType,PassType,Amount,Hours\n")
        except Exception as e:
            print(f"⚠ Error initializing transactions file: {e}")

    def add_transaction(self, transaction):
        try:
            with open(self.filename, 'a') as file:
                file.write(transaction.to_csv_row())
            return True
        except Exception as e:
            print(f"⚠ Error adding transaction: {e}")
            return False

    def get_all_transactions(self):
        transactions = []
        try:
            if not os.path.exists(self.filename):
                return transactions

            with open(self.filename, 'r') as file:
                lines = file.readlines()
                # Skip header
                for line in lines[1:]:
                    transaction = Transaction.from_csv_row(line)
                    if transaction:
                        transactions.append(transaction)
        except Exception as e:
            print(f"⚠ Error reading transactions: {e}")

        return transactions

    def get_transactions_by_month(self, year, month):
        month_key = f"{year}-{month:02d}"
        matching_transactions = []

        all_transactions = self.get_all_transactions()
        for transaction in all_transactions:
            if transaction.get_month_year() == month_key:
                matching_transactions.append(transaction)

        return matching_transactions

    def get_transactions_by_pass_type(self, pass_type):
        matching_transactions = []

        all_transactions = self.get_all_transactions()
        for transaction in all_transactions:
            if transaction.pass_type == pass_type:
                matching_transactions.append(transaction)

        return matching_transactions

    def get_transactions_by_vehicle_type(self, vehicle_type):
        matching_transactions = []

        all_transactions = self.get_all_transactions()
        for transaction in all_transactions:
            if transaction.vehicle_type.lower() == vehicle_type.lower():
                matching_transactions.append(transaction)

        return matching_transactions

    def calculate_total_revenue(self):
        total = 0
        all_transactions = self.get_all_transactions()
        for transaction in all_transactions:
            total += transaction.amount
        return total
