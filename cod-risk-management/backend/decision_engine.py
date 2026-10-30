
import json
from pathlib import Path

# Load configuration
config_path = Path(__file__).with_name("config.json")

with open(config_path, "r") as file:
    config = json.load(file)


def decide_order(rto_probability, customer_prior_orders=0):

    thresholds = config["thresholds"]
    risk = float(rto_probability)

    if risk < thresholds["ship_as_is"]:
        action = "Ship as-is"
        reason = "Order has a low predicted RTO risk."

    elif risk < thresholds["confirmation"]:
        action = "Ship after confirmation"
        reason = "Customer confirmation is recommended before shipping."

    elif risk < thresholds["prepaid"]:
        action = "Nudge to prepaid"
        reason = "Offer a small discount to encourage online payment."

    else:
        # High-risk orders
        if customer_prior_orders == 0:
            action = "Ship after confirmation"
            reason = (
                "High predicted RTO risk for a first-time customer. "
                "Require confirmation and manual review."
            )
        else:
            action = "Hold / cancel"
            reason = (
                "High predicted RTO risk. "
                "Hold for manual review before cancellation."
            )

    return {
        "rto_probability": round(risk * 100, 2),
        "action": action,
        "reason": reason
    }
