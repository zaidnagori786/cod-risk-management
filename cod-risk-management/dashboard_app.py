
import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="COD Risk Management Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("COD Risk Management Dashboard")
st.caption("Founder overview | COD order risk and financial impact")

# -----------------------------
# LOAD DATA
# -----------------------------

DATA_PATH = Path(__file__).parent / "data" / "decision_log.csv"

if not DATA_PATH.exists():
    st.error("decision_log.csv not found. Export it from your notebook first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

required_columns = ["action", "actual_status"]

if not all(col in df.columns for col in required_columns):
    st.error("Decision log is missing required columns.")
    st.stop()

# -----------------------------
# BUSINESS ASSUMPTIONS
# -----------------------------

RTO_COST = 169.40
COD_RTO_RATE = 0.28
PREPAID_RTO_RATE = 0.04
PREPAID_DISCOUNT = 20
GROSS_MARGIN = 402.38

# -----------------------------
# ORDER COUNTS
# -----------------------------

counts = df["action"].value_counts()

ship_count = counts.get("Ship as-is", 0)
confirmation_count = counts.get("Ship after confirmation", 0)
prepaid_count = counts.get("Nudge to prepaid", 0)
hold_count = counts.get("Hold / cancel", 0)

total_orders = len(df)

# -----------------------------
# PREPAID CONVERSION ASSUMPTION
# -----------------------------

st.subheader("Business assumptions")

conversion_rate = st.slider(
    "Expected prepaid conversion rate",
    min_value=0,
    max_value=100,
    value=50,
    step=5
) / 100

converted_orders = prepaid_count * conversion_rate

estimated_savings = (
    converted_orders
    * (COD_RTO_RATE - PREPAID_RTO_RATE)
    * RTO_COST
)

discount_cost = converted_orders * PREPAID_DISCOUNT

net_prepaid_benefit = estimated_savings - discount_cost

# -----------------------------
# GENUINE ORDER RISK
# -----------------------------

genuine_orders_at_risk = len(
    df[
        (df["action"] == "Hold / cancel")
        & (df["actual_status"] == "DELIVERED")
    ]
)

potential_lost_margin = genuine_orders_at_risk * GROSS_MARGIN

# -----------------------------
# KPI CARDS
# -----------------------------

st.subheader("Order overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total COD orders", f"{total_orders:,}")
col2.metric("Ship as-is", f"{ship_count:,}")
col3.metric("Confirmation", f"{confirmation_count:,}")
col4.metric("Prepaid nudges", f"{prepaid_count:,}")

col1, col2, col3 = st.columns(3)

col1.metric("Hold / manual review", f"{hold_count:,}")
col2.metric("Estimated RTO savings", f"₹{estimated_savings:,.2f}")
col3.metric("Prepaid discount cost", f"₹{discount_cost:,.2f}")

# -----------------------------
# FINANCIAL IMPACT
# -----------------------------

st.divider()
st.subheader("Financial impact")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Net prepaid benefit",
    f"₹{net_prepaid_benefit:,.2f}"
)

col2.metric(
    "Genuine orders at risk",
    f"{genuine_orders_at_risk:,}"
)

col3.metric(
    "Potential lost gross margin",
    f"₹{potential_lost_margin:,.2f}"
)

st.info(
    "Genuine orders at risk are historical delivered orders "
    "that received a hold recommendation. They are not confirmed "
    "cancellations. Potential lost margin is a counterfactual estimate."
)

# -----------------------------
# DECISION DISTRIBUTION
# -----------------------------

st.divider()
st.subheader("Decision distribution")

decision_chart = pd.DataFrame({
    "Action": [
        "Ship as-is",
        "Ship after confirmation",
        "Nudge to prepaid",
        "Hold / cancel"
    ],
    "Orders": [
        ship_count,
        confirmation_count,
        prepaid_count,
        hold_count
    ]
})

st.bar_chart(
    decision_chart.set_index("Action")
)

# -----------------------------
# RISK DISTRIBUTION
# -----------------------------

if "rto_probability" in df.columns:

    st.subheader("Predicted RTO risk distribution")

    st.bar_chart(
        df["rto_probability"],
        horizontal=False
    )

# -----------------------------
# ORDER DECISION LOG
# -----------------------------

st.divider()
st.subheader("Order decision log")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Financial estimates use assignment-provided assumptions. "
    "Actual savings depend on prepaid conversion, delivery outcomes "
    "and operational execution."
)
