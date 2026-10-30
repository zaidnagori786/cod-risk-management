from decision_engine import decide_order
from whatsapp_flow import create_whatsapp_message


def process_order(order, rto_probability):

    decision = decide_order(
        rto_probability=rto_probability,
        customer_prior_orders=order["customer_prior_orders"]
    )

    result = {
        "order_id": order["order_id"],
        "rto_probability": decision["rto_probability"],
        "decision": decision["action"],
        "reason": decision["reason"],
        "whatsapp_message": None
    }

    if decision["action"] == "Ship after confirmation":
        result["whatsapp_message"] = create_whatsapp_message(
            order["customer_name"],
            order["order_id"],
            order["order_value"]
        )

    elif decision["action"] == "Nudge to prepaid":
        result["whatsapp_message"] = create_whatsapp_message(
            order["customer_name"],
            order["order_id"],
            order["order_value"]
        )

    return result