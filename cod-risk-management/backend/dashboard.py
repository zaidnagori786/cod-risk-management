
RTO_COST = 169.40
DELIVERED_GROSS_MARGIN = 402.38
PREPAID_DISCOUNT = 20

COD_RTO_RATE = 0.28
PREPAID_RTO_RATE = 0.04


def generate_dashboard(decision_df):

    total_orders = len(decision_df)

    counts = decision_df["action"].value_counts()

    ship_count = counts.get("Ship as-is", 0)
    confirmation_count = counts.get("Ship after confirmation", 0)
    prepaid_count = counts.get("Nudge to prepaid", 0)
    hold_count = counts.get("Hold / cancel", 0)

    # Estimate RTO savings if every prepaid nudge converts
    estimated_rto_savings = (
        prepaid_count
        * (COD_RTO_RATE - PREPAID_RTO_RATE)
        * RTO_COST
    )

    # Estimate prepaid discount cost
    estimated_discount_cost = prepaid_count * PREPAID_DISCOUNT

    # Identify genuine delivered orders in the hold bucket.
    # This is a counterfactual estimate, not an actual cancellation.
    genuine_orders_at_risk = 0

    if "actual_status" in decision_df.columns:
        genuine_orders_at_risk = len(
            decision_df[
                (decision_df["action"] == "Hold / cancel")
                & (decision_df["actual_status"] == "DELIVERED")
            ]
        )

    estimated_lost_margin = (
        genuine_orders_at_risk * DELIVERED_GROSS_MARGIN
    )

    net_impact = (
        estimated_rto_savings
        - estimated_discount_cost
        - estimated_lost_margin
    )

    return {
        "total_orders": total_orders,
        "ship_as_is": ship_count,
        "confirmation": confirmation_count,
        "prepaid_nudge": prepaid_count,
        "hold_cancel_manual_review": hold_count,
        "estimated_rto_savings": round(estimated_rto_savings, 2),
        "estimated_discount_cost": round(estimated_discount_cost, 2),
        "genuine_orders_at_risk": genuine_orders_at_risk,
        "estimated_lost_margin": round(estimated_lost_margin, 2),
        "estimated_net_financial_impact": round(net_impact, 2)
    }
