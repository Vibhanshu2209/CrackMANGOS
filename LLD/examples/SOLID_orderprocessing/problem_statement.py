import json


class OrderProcessor:

    def process_order(
        self,
        order_data: dict,
        payment_type: str,
        notification_type: str,
        fulfillment_type: str,
    ) -> bool:
        # ----------------------------------------------------
        # 1. Validation & Inventory Check
        # ----------------------------------------------------
        if not order_data.get("items") or order_data.get("total", 0) <= 0:
            print("Error: Invalid order payload.")
            return False

        for item in order_data["items"]:
            # Hardcoded stock check
            if item.get("stock_qty", 0) < item.get("quantity", 1):
                print(f"Error: Item {item.get('name')} is out of stock.")
                return False

        print(f"Processing order #{order_data['id']} for {order_data['user_email']}")

        # ----------------------------------------------------
        # 2. Dynamic Pricing & Tax Strategy
        # ----------------------------------------------------
        total_amount = float(order_data["total"])
        user_tier = order_data.get("user_tier", "standard")

        if user_tier == "vip":
            total_amount *= 0.90  # 10% VIP Discount
        elif user_tier == "employee":
            total_amount *= 0.80  # 20% Employee Discount

        # Country Taxing
        country = order_data.get("country", "US")
        if country == "US":
            total_amount *= 1.07
        elif country == "EU":
            total_amount *= 1.20

        # ----------------------------------------------------
        # 3. Payment Processing
        # ----------------------------------------------------
        if payment_type == "credit_card":
            print(f"Charging ${total_amount:.2f} via Credit Card API...")
            payment_success = True
        elif payment_type == "paypal":
            print(f"Charging ${total_amount:.2f} via PayPal REST API...")
            payment_success = True
        elif payment_type == "crypto":
            # Crypto charges a flat gas fee
            gas_fee = 15.00
            crypto_total = total_amount + gas_fee
            print(f"Charging ${crypto_total:.2f} via Web3 Wallet (Gas Included)...")
            payment_success = True
        elif payment_type == "store_credit":
            # Store credit balance check simulated inline
            user_credit = order_data.get("store_credit_balance", 0.0)
            if user_credit < total_amount:
                print("Error: Insufficient store credit.")
                return False
            print(f"Deducting ${total_amount:.2f} from Store Credit...")
            payment_success = True
        else:
            raise ValueError(f"Unsupported payment gateway: {payment_type}")

        if not payment_success:
            return False

        # ----------------------------------------------------
        # 4. Fulfillment & Logistics
        # ----------------------------------------------------
        if fulfillment_type == "physical_shipment":
            if "shipping_address" not in order_data:
                print("Fulfillment Failed: Missing shipping address!")
                return False
            print(
                f"Generating Shipping Label for {order_data['shipping_address']}..."
            )
        elif fulfillment_type == "digital_download":
            # Digital fulfillment generates a license key
            print(f"Generating License Keys for digital items...")
            order_data["download_link"] = (
                f"https://store.com/download/{order_data['id']}"
            )
        elif fulfillment_type == "gift_card":
            print("Generating digital gift card codes...")
        else:
            raise ValueError(f"Unknown fulfillment type: {fulfillment_type}")

        # ----------------------------------------------------
        # 5. Multi-Channel Customer Notification
        # ----------------------------------------------------
        if notification_type == "email":
            print(
                f"Sending Email to {order_data['user_email']}: Order #{order_data['id']} Confirmed!"
            )
        elif notification_type == "sms":
            if "phone" not in order_data:
                print("Notification Failed: SMS requires target phone number!")
                return False
            print(
                f"Sending SMS to {order_data['phone']}: Order #{order_data['id']} Confirmed!"
            )
        elif notification_type == "push":
            if "device_token" not in order_data:
                print("Notification Failed: Missing push device token!")
                return False
            print(
                f"Sending Push to device {order_data['device_token']}: Order Confirmed!"
            )

        # ----------------------------------------------------
        # 6. Database / File Audit Logging
        # ----------------------------------------------------
        # Direct file I/O dependency tightly coupled to the processor
        try:
            with open("audit_orders.json", "a") as f:
                log_entry = {
                    "order_id": order_data["id"],
                    "amount_paid": total_amount,
                    "payment_type": payment_type,
                    "fulfillment_type": fulfillment_type,
                    "status": "COMPLETED",
                }
                f.write(json.dumps(log_entry) + "\n")
        except IOError as e:
            print(f"Failed to write audit logs: {e}")
            return False

        return True