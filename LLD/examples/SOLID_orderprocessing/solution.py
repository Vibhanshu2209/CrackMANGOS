from abc import ABC, abstractmethod
import csv
from dataclasses import dataclass
from enum import Enum
import json
import os
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel

class FulfillmentType(Enum):
    DIGITAL_DOWNLOAD = "DIGITAL_DOWNLOAD"
    PHYSICAL_DELIVERY = "PHYSICAL_DELIVERY"
    GIFT_CARD = "GIFT_CARD"


class NotificationType(Enum):
    SMS = "SMS" 
    EMAIL = "EMAIL" 
    PUSH_NOTIFICATION = "PUSH_NOTIFICATION"


class PaymentType(Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PAYPAL = "PAYPAL"
    STORE_CREDIT = "STORE_CREDIT"
    CRYPTO = "CRYPTO"


class UserTierType(Enum):
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"
    EMPLOYEE = "EMPLOYEE"


@dataclass
class Item:
    name: str
    quantity: int
    unit_price: float  # Added to calculate order total dynamically
    fulfillment_type: FulfillmentType = FulfillmentType.PHYSICAL_DELIVERY


@dataclass
class UserInfo:
    user_email: str
    user_tier: UserTierType
    user_id: Optional[str] = None
    phone: Optional[str] = None
    device_token: Optional[str] = None
    store_credit_balance: float = 0.0


@dataclass
class Order:

    AUDIT_FILE_NAME = "order_audit.log"

    id: str
    items: List[Item]
    user_info: UserInfo
    country: str = "US"
    shipping_address: Optional[str] = None

    @property
    def calculate_subtotal(self) -> float:
        return sum(item.unit_price * item.quantity for item in self.items)

@dataclass
class PaymentResult:
    success: bool
    message: str
    transaction_id: Optional[str] = None



class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, order: Order) -> float:
        pass

class FullfillmentStrategy(ABC):
    @abstractmethod
    def fulfill_order_item(self, order: Order, item: Item) -> bool:
        pass

class NoDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, order: Order) -> float:
        return 0.0

class NoFulfillmentStrategy(FullfillmentStrategy):
    def fulfill_order_item(self, order: Order, item: Item) -> bool:
        raise NotImplementedError("Need to have valid and registered delivery type")
    

class DiscountRegistry:

    _handlers = {}

    @classmethod
    def register(self, tier: UserTierType):

        def decorator(stgy_cls):
            if tier in self._handlers:
                raise Exception(f"Duplicate registration for tier: {tier}")
            self._handlers[tier] = stgy_cls()
            return stgy_cls

        return decorator

    @classmethod
    def get_strategy(self, tier: UserTierType) -> DiscountStrategy:
        return self._handlers.get(tier, NoDiscountStrategy())



class FulfillmentRegistry:

    _handlers = {}

    @classmethod
    def register(self, type: FulfillmentType):

        def decorator(stgy_cls):
            if type in self._handlers:
                raise Exception(f"Duplicate registeration for fulfillment type: {type}")
            self._handlers[type] = stgy_cls()
            return stgy_cls

        return decorator

    @classmethod
    def get_strategy(self, type: FulfillmentType) -> FullfillmentStrategy:
        return self._handlers.get(type, NoFulfillmentStrategy())
    

class TaxStrategy(ABC):

    @abstractmethod
    def calculate_tax(self, order: Order, taxable_amount: float) -> float:
        pass
    
    

@DiscountRegistry.register(UserTierType.PREMIUM)
class VIPDiscountStrategy(DiscountStrategy):
    
    def calculate_discount(self, order) -> float:
        return order.calculate_subtotal * 0.10
        

@DiscountRegistry.register(UserTierType.EMPLOYEE)
class EmployeeDiscountStrategy(DiscountStrategy):
    
    def calculate_discount(self, order) -> float:
        return order.calculate_subtotal * 0.20
        

@FulfillmentRegistry.register(FulfillmentType.DIGITAL_DOWNLOAD)
class DigitalDownloadDeliveryStrategy(FullfillmentStrategy):

    def fulfill_order_item(self, order: Order, item: Item):
        if not order.user_info.user_email:
            raise Exception("User must have a valid email address for sending the digital download link")

        print(f"Digital Download Link for Item Name: {item.name} has been successfully sent to user on email: {order.user_info.user_email}")
        return True




class RegionalTaxStrategy(TaxStrategy):

    def __init__(self, tax_rates: Dict[str, float], default_rate: float = 0.0):
        self.tax_rates = tax_rates
        self.default_rate = default_rate

    def calculate_tax(self, order: Order, taxable_amount: float) -> float:
        rate = self.tax_rates.get(order.country, self.default_rate)
        return taxable_amount * rate


class PricingCalculator:

    def __init__(self, discount_strategies: List[DiscountStrategy], tax_strategy: TaxStrategy):

        self.discount_strategies = discount_strategies
        self.tax_strategy = tax_strategy


    def calculate_total(self, order: Order):
        subtotal = order.calculate_subtotal

        total_discount = sum(stgy.calculate_discount(order) for stgy in self.discount_strategies)

        taxable_amount = max(0.0, subtotal - total_discount)

        total_tax = self.tax_strategy.calculate_tax(order, taxable_amount)

        grand_total = taxable_amount + total_tax

        return grand_total
    


class Payment(ABC):

    @abstractmethod
    def process_payment(self, order: Order) -> PaymentResult:
        pass

class Auth(ABC):

    @abstractmethod
    def authenticate(self, user_info: UserInfo) -> bool:
        """Executes verification and returns result in a single atomic action."""
        pass


class SMSAuth(Auth):

    def authenticate(self, user_info: UserInfo) -> bool:
        if not user_info.phone:
            print("Auth Failed: Missing phone number.")
            return False

        generated_code = "191123"
        print(f"SMS code sent to {user_info.phone}")
        user_input = input("Enter your SMS code: ")

        return user_input.isdecimal() and user_input == generated_code


from uuid import UUID, uuid4

class DebitPayment(Payment):
    def __init__(self, auth: Auth):
        self.auth = auth


    def process_payment(self, order, amount: float) -> PaymentResult:
        if not self.auth.authenticate(order.user_info): 
            raise Exception("401, Debit Card Authorisation Failed")


        print(f"Calling the bank API for payment.")
        print(f"Debit Payment Successful for user: {order.user_info.user_email} with Order Id: {order.id} and amount: {amount}")

        return PaymentResult(success=True, message="Payment processed successfully.", transaction_id=str(uuid4()))



class AuditLogger(ABC):

    @abstractmethod
    def log_transaction(self, log_data: Any) -> None:
        """Logs transaction audit details safely."""
        pass


class FileAuditLogger(AuditLogger):

    def __init__(self, log_file_name = "audit.log"):
        self.log_file_name = log_file_name

    def log_transaction(self, log_data: str) -> None:
        print(f"Logging data {log_data} to file: {self.log_file_name}")
        try:
            with open(self.log_file_name, "a") as audit_file:
                audit_file.write(log_data + "\n")
        except Exception as e:
            print(f"Failed to write the log data to the file {self.log_file_name}, with Exception {e}")
        finally:
            audit_file.close()


class CSVAuditLogger(AuditLogger):

    def __init__(self, fieldnames: List[str], log_file_name = "Audit.csv"):
        self.log_file_name = log_file_name
        self.fieldnames = fieldnames

    def log_transaction(self, log_data):
        file_exists = os.path.isfile(self.log_file_name)

        try:
            with open(self.log_file_name, mode="a", newline="", encoding="utf-8") as audit_csv:
                writer = csv.DictWriter(audit_csv, fieldnames=self.fieldnames)

                if not file_exists: writer.writeheader()

                writer.writerow(log_data)
        except Exception as e:
            print(f"Failed to write CSV audit log: {e}")

@dataclass
class OrderProcessorResult:
    status: bool
    message: str
    order_processing_id: UUID


class OrderProcessingException(Exception):
    pass


class OrderProcessor:

    def __init__(
            self,
            pricing_calc: PricingCalculator,
            payment_service: Payment,
            auditing: AuditLogger
            ):
        self.pricing_calc = pricing_calc
        self.payment_service = payment_service
        self.auditing = auditing


    class OrderAuditData(BaseModel):
        order_id: str
        amount_paid: float
        payment_type: str
        payment_transaction_id: Optional[str] = None
        status: str


        def _csv_format(self) -> str:
            return f"{self.order_id},{self.amount_paid},{self.payment_type},{self.payment_transaction_id},{self.status}"

    def process_order(self, order: Order) -> OrderProcessorResult:

        uuid = uuid4()
        if not order.items:
            return OrderProcessorResult(status=False, message="No Items to process", order_processing_id=uuid)
            

        grand_total = self.pricing_calc.calculate_total(order)

        payment_result = self.payment_service.process_payment(order=order, amount=grand_total)
        if not payment_result.success:
            print(f"Payment failed: {payment_result.message}")
            raise Exception("Payment failed, aborting order processing.")

        all_order_items_fulfilled = False

        for item in order.items:
            ffm_stgy = FulfillmentRegistry.get_strategy(item.fulfillment_type)
            all_order_items_fulfilled = ffm_stgy.fulfill_order_item(order=order, item=item)

        if not all_order_items_fulfilled:
            return OrderProcessorResult(status=False, message="Order Fulfillment Failed", order_processing_id=uuid)

        order.status = "Processed"

        order_audit_data = self.OrderAuditData(
            order_id=order.id,
            amount_paid=grand_total,
            payment_type=self.payment_service.__class__.__name__,
            payment_transaction_id=payment_result.transaction_id,
            status=order.status
        )

        self.auditing.log_transaction(log_data=order_audit_data._csv_format())

        return OrderProcessorResult(status=True, message="Order Processed Successfully", order_processing_id=uuid)

        







if __name__ == "__main__":

    tax_table = {"US": 0.07, "EU": 0.20, "CA": 0.13}
    
    # Example usage
    order = Order(
        id="ORD123",
        user_info=UserInfo(
            phone="+1234567890",
            user_email="something@anything.com",
            user_tier=UserTierType.PREMIUM,
        ),
        items=[
            Item(name="Windows 11 Pro", quantity=2, unit_price=25.00, fulfillment_type=FulfillmentType.DIGITAL_DOWNLOAD),
            # Item(name="Laptop", quantity=1, unit_price=1000.00, fulfillment_type=FulfillmentType.PHYSICAL_DELIVERY),
            # Item(name="Mouse", quantity=2, unit_price=25.00, fulfillment_type=FulfillmentType.PHYSICAL_DELIVERY),
        ])

    debit_payment = DebitPayment(auth=SMSAuth())

    discount_stgy = DiscountRegistry.get_strategy(order.user_info.user_tier)
    tax_stgy = RegionalTaxStrategy(tax_rates=tax_table)
    pricing_calc = PricingCalculator([discount_stgy], tax_stgy)


    order_processor = OrderProcessor(
                pricing_calc=pricing_calc, 
                payment_service=debit_payment, 
                auditing=FileAuditLogger(log_file_name=Order.AUDIT_FILE_NAME)
                )

    opr = order_processor.process_order(order=order)
    if not opr.status:
        raise OrderProcessingException(f"Order Processing Failed with message {opr.message} and id {opr.order_processing_id}")

    



    


    
    







    print(f"Order Subtotal: ${order.calculate_subtotal:.2f}")
    





