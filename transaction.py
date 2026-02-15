from datetime import datetime

# TRANSACTION

class Transaction:
    def __init__(self, plate_number, vehicle_type, pass_type, amount, hours=0):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type  # 'car', 'bike', 'truck'
        self.pass_type = pass_type  # 'Single Entry', 'Weekly Pass', 'Monthly Pass'
        self.amount = amount
        self.hours = hours  # Only for single entry
        self.date = datetime.now()

    def to_csv_row(self):
        date_str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        return f"{date_str},{self.plate_number},{self.vehicle_type},{self.pass_type},{self.amount},{self.hours}\n"

    @staticmethod
    def from_csv_row(row):
        try:
            parts = row.strip().split(',')
            if len(parts) != 6:
                return None

            date_str, plate, vehicle_type, pass_type, amount, hours = parts
            transaction = Transaction(plate, vehicle_type, pass_type, float(amount), int(hours))
            transaction.date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return transaction
        except Exception:
            return None

    def get_month_year(self):
        return self.date.strftime("%Y-%m")

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} | {self.plate_number} | {self.pass_type} | ${self.amount}"
