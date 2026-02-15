# Enhanced Parking Lot Management System

## Project Overview
A comprehensive parking lot management system built with Python, implementing Object-Oriented Programming principles. The system manages vehicle parking, pass subscriptions, financial tracking, and generates detailed reports.

## Features

### 1. Pass System
- **Single Entry Pass**: Hourly-based pricing with time-multipliers (Peak/Off-Peak/Weekend)
- **Weekly Pass**: Flat-fee subscription valid for 7 days
- **Monthly Pass**: Flat-fee subscription valid for 30 days
- Vehicle-specific pricing (Car, Bike, Truck)

### 2. Transaction Management
- CSV-based transaction storage
- Automatic transaction recording for all parking activities
- Transaction filtering by date, pass type, and vehicle type

### 3. Finance Module
- **Revenue & Profit Tracking**: Calculate total revenue, expenses, and profit
- **Debtor Management**: Track unpaid parking fees (pay later), identify 30-day overdue accounts
- **Creditor Management**: Track prepaid subscribers and remaining days
- **Manual Entry**: Add/remove debtors and creditors manually

### 4. Reporting System
- **Monthly Sales Report**: Revenue breakdown by month and pass type
- **Pass Type Report**: Sales analysis for Weekly, Monthly, and Single Entry passes
- **Vehicle Count Report**: Track number of vehicles by type per month

## Installation & Setup

### Prerequisites
- Python 3.7 or higher

### Running the System
```powershell
python main.py
```

### Running Tests
```powershell
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m pytest tests/test_vehicle.py
python -m pytest tests/test_pass_system.py
python -m pytest tests/test_parking.py
python -m pytest tests/test_transaction.py
python -m pytest tests/test_finance.py
python -m pytest tests/test_reporting.py
```

## Usage Guide

### Main Menu Options

1. **Vehicle Entry (Single Entry)**: Park a vehicle with hourly pricing
2. **Vehicle Entry (With Pass)**: Park using a weekly/monthly pass
3. **Vehicle Exit & Billing**: Process vehicle exit with Pay Now / Pay Later options
4. **Purchase Pass**: Buy a weekly or monthly pass
5. **Finance & Accounting Module**: Revenue, expenses, debtors, creditors
6. **Reporting Dashboard**: Generate sales and vehicle reports
7. **View Available Spaces**: View parking capacity status
8. **System Settings**: View current pricing rates
0. **Exit Program**: Close the application

### Pass Pricing

| Vehicle Type | Weekly Pass | Monthly Pass | Hourly Rate |
|-------------|-------------|--------------|-------------|
| Car         | $40         | $150         | $7/hour     |
| Bike        | $15         | $50          | $3/hour     |
| Truck       | $60         | $220         | $10/hour    |

### Pricing Multipliers (Single Entry)
- **Off-Peak**: 1.0x (base rate)
- **Peak**: 1.5x
- **Weekend**: 1.2x

## OOP Concepts Demonstrated

### 1. Inheritance
- `Vehicle` → `Car`, `Bike`, `Truck`
- `Pass` → `SingleEntryPass`, `WeeklyPass`, `MonthlyPass`
- `PricingStrategy` → `PeakPricing`, `OffPeakPricing`, `WeekendPricing`

### 2. Encapsulation
- Private methods (`_initialize_files`, `_detect_vehicle_type`)
- Data hiding in manager classes

### 3. Abstraction
- Abstract base classes (`Vehicle`, `Pass`, `PricingStrategy`)
- Abstract methods (`get_rate()`, `get_price()`, `calculate_fee()`)

### 4. Polymorphism
- Different implementations of `get_rate()` for each vehicle type
- Different `calculate_fee()` implementations for pricing strategies

## Complex Programming Concepts

### Data Structures
- **Dictionaries**: Pass type sales tracking, monthly aggregation, vehicle counts
- **Lists**: Transaction storage, unique plate tracking, debtor/creditor lists

### Control Flow
- **Nested Loops**: Report generation (iterate months, then transactions)
- **Nested If Statements**: Input validation, business logic checks

### Error Handling
- Try-except blocks for file I/O operations
- Input validation with error messages
- CSV parsing error handling

## Testing

The system includes comprehensive unit tests covering:
- Vehicle creation and pricing strategies
- Pass system creation, pricing, and validity
- Parking ticket, lot operations, and per-ticket strategy isolation
- Transaction management and filtering
- Finance operations (debtors, creditors, pay-later flow, CSV round-trips)
- Report generation and data aggregation

**Test Results**: 59 tests, all passing ✓

## Data Persistence

The system uses CSV files for data storage:

### transactions.csv
```
Date,Plate,VehicleType,PassType,Amount,Hours
2026-02-11 10:30:00,ABC123,car,Single Entry,21.0,3
```

### debtors.csv
```
Plate,VehicleType,AmountOwed,DueDate
XYZ789,truck,220.0,2026-01-10
```

### creditors.csv
```
Plate,VehicleType,PassType,ExpiryDate
DEF456,car,Monthly Pass,2026-03-15
```

## Design Guidelines Adherence

✓ Consistent, professional code organization  
✓ Meaningful identifier names (PascalCase for classes, snake_case for functions)  
✓ User-friendly error handling  
✓ Modular design with separate files for each concern  
✓ Reusable components (managers, strategies)  
✓ Extensible architecture (easy to add new vehicle types, pass types)  
✓ Maintainable code with clear separation of concerns  
✓ Adaptable to changing requirements
