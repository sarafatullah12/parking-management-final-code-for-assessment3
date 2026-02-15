from abc import ABC, abstractmethod

# VEHICLE CLASSES
 
class Vehicle(ABC):
    def __init__(self, plate_number):
        self.plate_number = plate_number
    @abstractmethod
    def get_rate(self):
        pass

class Car(Vehicle):
    def get_rate(self):
        return 7

class Bike(Vehicle):
    def get_rate(self):
        return 3

class Truck(Vehicle):
    def get_rate(self):
        return 10
