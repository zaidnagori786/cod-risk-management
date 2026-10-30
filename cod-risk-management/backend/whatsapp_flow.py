from datetime import datetime, timedelta

PREPAID_DISCOUNT = 20
RESPONSE_TIMEOUT_HOURS = 24


def create_whatsapp_message(customer_name, order_id, order_value):
    discounted_price = order_value - PREPAID_DISCOUNT

    message = f"""
Hi {customer_name}! 👋

Thank you for placing your order #{order_id}.

Your order value is ₹{order_value} (Cash on Delivery).

Please confirm your order by replying:

YES - Confirm my order
NO - Cancel my order

Prefer prepaid payment?
Pay ₹{discounted_price} instead of ₹{order_value}
and save ₹{PREPAID_DISCOUNT}!

Please reply within 24 hours.
Thank you!
"""
    return message.strip()


def process_whatsapp_response(response, order_value):
    response = str(response).strip().lower()

    if response in ["yes", "y"]:
        return {
            "status": "CONFIRMED",
            "action": "Ship order",
            "message": "Customer confirmed the COD order."
        }

    elif response in ["no", "n"]:
        return {
            "status": "CANCELLED",
            "action": "Cancel order",
            "message": "Customer requested cancellation."
        }

    elif response in ["prepaid", "pay"]:
        return {
            "status": "PREPAID_OFFER_ACCEPTED",
            "action": "Generate prepaid payment link",
            "discounted_amount": order_value - PREPAID_DISCOUNT,
            "message": "Customer wants to pay online."
        }

    else:
        return {
            "status": "MANUAL_REVIEW",
            "action": "Send to manual review",
            "message": "Customer response was unclear."
        }


def check_no_response(sent_time):
    timeout = timedelta(hours=RESPONSE_TIMEOUT_HOURS)
    current_time = datetime.now()

    if current_time >= sent_time + timeout:
        return {
            "status": "NO_RESPONSE",
            "action": "Hold for manual review",
            "message": "Customer did not respond within 24 hours."
        }

    return {
        "status": "WAITING",
        "action": "Wait for customer response",
        "message": "The 24-hour response window is still open."
    }