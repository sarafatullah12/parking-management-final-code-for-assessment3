from abc import ABC, abstractmethod

#  PRICING STRATEGY

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, hours, rate):
        pass

class PeakPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate * 1.5

class OffPeakPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate

class WeekendPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate * 1.2
