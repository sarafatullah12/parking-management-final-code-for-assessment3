from datetime import datetime

# FINANCE CLASSES

class Debtor:
    def __init__(self, plate_number, vehicle_type, amount_owed, due_date):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.amount_owed = amount_owed
        self.due_date = due_date  # datetime object

    def days_overdue(self):
        if isinstance(self.due_date, str):
            self.due_date = datetime.strptime(self.due_date, "%Y-%m-%d")

        delta = datetime.now() - self.due_date
        return max(0, delta.days)

    def is_30_days_overdue(self):
        return self.days_overdue() >= 30

    def to_csv_row(self):
        due_date_str = self.due_date.strftime("%Y-%m-%d") if isinstance(self.due_date, datetime) else self.due_date
        return f"{self.plate_number},{self.vehicle_type},{self.amount_owed},{due_date_str}\n"

    @staticmethod
    def from_csv_row(row):
        try:
            parts = row.strip().split(',')
            if len(parts) != 4:
                return None

            plate, vehicle_type, amount, due_date_str = parts
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
            return Debtor(plate, vehicle_type, float(amount), due_date)
        except Exception:
            return None

    def __str__(self):
        return f"{self.plate_number} | {self.vehicle_type} | Owed: ${self.amount_owed} | Overdue: {self.days_overdue()} days"


class Creditor:
    def __init__(self, plate_number, vehicle_type, pass_type, expiry_date):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.pass_type = pass_type  # 'Weekly Pass' or 'Monthly Pass'
        self.expiry_date = expiry_date  # datetime object

    def days_remaining(self):
        if isinstance(self.expiry_date, str):
            self.expiry_date = datetime.strptime(self.expiry_date, "%Y-%m-%d")

        delta = self.expiry_date - datetime.now()
        return max(0, delta.days)

    def is_valid(self):
        if isinstance(self.expiry_date, str):
            self.expiry_date = datetime.strptime(self.expiry_date, "%Y-%m-%d")
        return datetime.now() < self.expiry_date

    def to_csv_row(self):
        expiry_str = self.expiry_date.strftime("%Y-%m-%d") if isinstance(self.expiry_date, datetime) else self.expiry_date
        return f"{self.plate_number},{self.vehicle_type},{self.pass_type},{expiry_str}\n"

    @staticmethod
    def from_csv_row(row):
        try:
            parts = row.strip().split(',')
            if len(parts) != 4:
                return None

            plate, vehicle_type, pass_type, expiry_str = parts
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
            return Creditor(plate, vehicle_type, pass_type, expiry_date)
        except Exception:
            return None

    def __str__(self):
        return f"{self.plate_number} | {self.vehicle_type} | {self.pass_type} | Days Left: {self.days_remaining()}"
