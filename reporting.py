from datetime import datetime

# REPORTING SYSTEM

class ReportGenerator:
    def __init__(self, transaction_manager):
        self.transaction_manager = transaction_manager

    def generate_monthly_sale_report(self, year=None, month=None):
        # Use current month if not specified
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month

        print("\n" + "="*50)
        print(f"MONTHLY SALES REPORT - {year}-{month:02d}")
        print("="*50)

        transactions = self.transaction_manager.get_transactions_by_month(year, month)

        if not transactions:
            print("No transactions found for this month.")
            print("="*50)
            return

        # Use dictionary to group by pass type
        pass_type_sales = {}
        total_revenue = 0

        # Nested loop: iterate through transactions and group by pass type
        for transaction in transactions:
            pass_type = transaction.pass_type

            # Initialize if not exists
            if pass_type not in pass_type_sales:
                pass_type_sales[pass_type] = {
                    'count': 0,
                    'revenue': 0
                }

            pass_type_sales[pass_type]['count'] += 1
            pass_type_sales[pass_type]['revenue'] += transaction.amount
            total_revenue += transaction.amount

        # Display results
        print(f"\nTotal Transactions: {len(transactions)}")
        print(f"Total Revenue: ${total_revenue:.2f}\n")

        print("Breakdown by Pass Type:")
        print("-" * 50)
        for pass_type, data in pass_type_sales.items():
            print(f"{pass_type:20s} | Count: {data['count']:3d} | Revenue: ${data['revenue']:8.2f}")

        print("="*50)

    def generate_pass_type_report(self):
        print("\n" + "="*50)
        print("PASS TYPE SALES REPORT")
        print("="*50)

        all_transactions = self.transaction_manager.get_all_transactions()

        if not all_transactions:
            print("No transactions found.")
            print("="*50)
            return

        # Dictionary to store pass type data
        pass_data = {
            'Weekly Pass': {'count': 0, 'revenue': 0},
            'Monthly Pass': {'count': 0, 'revenue': 0},
            'Single Entry': {'count': 0, 'revenue': 0}
        }

        # Nested structure: loop through transactions and categorize
        for transaction in all_transactions:
            pass_type = transaction.pass_type
            if pass_type in pass_data:
                pass_data[pass_type]['count'] += 1
                pass_data[pass_type]['revenue'] += transaction.amount

        # Display results
        print("\nPass Type          | Sold | Total Revenue")
        print("-" * 50)
        for pass_type, data in pass_data.items():
            print(f"{pass_type:18s} | {data['count']:4d} | ${data['revenue']:10.2f}")

        total_count = sum(data['count'] for data in pass_data.values())
        total_revenue = sum(data['revenue'] for data in pass_data.values())

        print("-" * 50)
        print(f"{'TOTAL':18s} | {total_count:4d} | ${total_revenue:10.2f}")
        print("="*50)

    def generate_vehicle_count_report(self, year=None, month=None):
        # Use current month if not specified
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month

        print("\n" + "="*50)
        print(f"VEHICLE COUNT REPORT - {year}-{month:02d}")
        print("="*50)

        transactions = self.transaction_manager.get_transactions_by_month(year, month)

        if not transactions:
            print("No transactions found for this month.")
            print("="*50)
            return

        # Dictionary to count vehicles by type
        vehicle_counts = {
            'car': 0,
            'bike': 0,
            'truck': 0
        }

        # Use list to track unique plates
        unique_plates = []

        # Nested loop: count vehicles by type
        for transaction in transactions:
            vehicle_type = transaction.vehicle_type.lower()

            # Count all transactions by vehicle type
            if vehicle_type in vehicle_counts:
                vehicle_counts[vehicle_type] += 1

            # Track unique plates
            if transaction.plate_number not in unique_plates:
                unique_plates.append(transaction.plate_number)

        # Display results
        print(f"\nTotal Transactions: {len(transactions)}")
        print(f"Unique Vehicles: {len(unique_plates)}\n")

        print("Breakdown by Vehicle Type:")
        print("-" * 50)
        print(f"Cars:   {vehicle_counts['car']:4d} transactions")
        print(f"Bikes:  {vehicle_counts['bike']:4d} transactions")
        print(f"Trucks: {vehicle_counts['truck']:4d} transactions")
        print("="*50)

    def list_all_months_with_data(self):
        all_transactions = self.transaction_manager.get_all_transactions()

        # Use dictionary to track unique months
        months_dict = {}

        for transaction in all_transactions:
            month_year = transaction.get_month_year()
            if month_year not in months_dict:
                months_dict[month_year] = 0
            months_dict[month_year] += 1

        # Convert to sorted list
        months_list = []
        for month_year, count in months_dict.items():
            months_list.append((month_year, count))

        months_list.sort()

        return months_list
