from abc import ABC, abstractmethod


class DiscountStrategy(ABC):

    @abstractmethod
    def get_discount_percentage(self) -> float:
        ...

class DiwaliDiscountStrategy(DiscountStrategy):
    def get_discount_percentage(self):
        return 0.2


class StudentDiscountStrategy(DiscountStrategy):
    def get_discount_percentage(self):
        return 0.15

class InvoiceCalculationService:

    def __init__(self, discount_strategy: DiscountStrategy):
        self._disc_stgy = discount_strategy
        pass


    def calculate_total(self, amount: float):
        discount_rate = self._disc_stgy.get_discount_percentage()
        discount = amount * discount_rate
        return amount - discount
    


ics = InvoiceCalculationService(DiwaliDiscountStrategy())

print(ics.calculate_total(3000))