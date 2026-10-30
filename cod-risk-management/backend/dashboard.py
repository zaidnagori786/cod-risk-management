
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# BUSINESS ASSUMPTIONS
# ==========================================

RTO_COST = 169.40
DELIVERED_GROSS_MARGIN = 402.38
PREPAID_DISCOUNT = 20

COD_RTO_RATE = 0.28
PREPAID_RTO_RATE = 0.04


# ==========================================
# DASHBOARD CALCULATION FUNCTION
# ==========================================

def generate_dashboard(decision_df, conversion_rate=0.50):

    total_orders = len(decision_df)

    counts = decision_df["action"].value_counts()

    ship_count = counts.get("Ship as-is", 0)
    confirmation_count = counts.get("Ship after confirmation", 0)
    prepaid_count = counts.get("Nudge to prepaid", 0)
    hold_count = counts.get("Hold / cancel", 0)

    # Estimate prepaid conversions
    converted_orders = prepaid_count * conversion_rate

    # Estimate RTO savings only for converted orders
    estimated_rto_savings = (
        converted_orders
        * (COD_RTO_RATE - PREPAID_RTO_RATE)
        * RTO_COST
    )

    # Discount applies only to converted prepaid orders
    estimated_discount_cost = (
        converted_orders * PREPAID_DISCOUNT
    )

    # Identify delivered orders in the hold bucket.
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
        "converted_orders": round(converted_orders, 2),
        "estimated_rto_savings": round(estimated_rto_savings, 2),
        "estimated_discount_cost": round(estimated_discount_cost, 2),
        "genuine_orders_at_risk": genuine_orders_at_risk,
        "estimated_lost_margin": round(estimated_lost_margin, 2),
        "estimated_net_financial_impact": round(net_impact, 2)
    }


# ==========================================
# STREAMLIT PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="COD RTO Risk Management",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("📊 COD RTO Risk Management Dashboard")

st.markdown(
    "Machine learning-based order risk analysis, "
    "decision recommendations and estimated financial impact."
)

st.divider()


# ==========================================
# LOAD DATASET
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = PROJECT_ROOT / "data" / "decision_log.csv"

if not CSV_PATH.exists():
    st.error("Decision log file not found.")
    st.write("Expected file location:", str(CSV_PATH))
    st.stop()

try:
    decision_df = pd.read_csv(CSV_PATH)
except Exception as error:
    st.error(f"Unable to load decision log: {error}")
    st.stop()

if decision_df.empty:
    st.warning("The decision log contains no orders.")
    st.stop()

required_columns = {"action"}

if not required_columns.issubset(decision_df.columns):
    st.error("The decision log must contain an 'action' column.")
    st.stop()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Dashboard Settings")

conversion_rate = st.sidebar.slider(
    "Expected prepaid conversion rate",
    min_value=0,
    max_value=100,
    value=50,
    step=5
)

conversion_rate = conversion_rate / 100

st.sidebar.caption(
    "This slider estimates how many customers "
    "accept the prepaid payment offer."
)

st.sidebar.divider()

st.sidebar.subheader("Business Assumptions")

st.sidebar.write(f"RTO cost: ₹{RTO_COST:.2f}")
st.sidebar.write(f"Prepaid discount: ₹{PREPAID_DISCOUNT:.2f}")
st.sidebar.write(f"COD RTO rate: {COD_RTO_RATE:.0%}")
st.sidebar.write(f"Prepaid RTO rate: {PREPAID_RTO_RATE:.0%}")


# ==========================================
# GENERATE DASHBOARD METRICS
# ==========================================

dashboard = generate_dashboard(
    decision_df,
    conversion_rate
)


# ==========================================
# KEY PERFORMANCE INDICATORS
# ==========================================

st.subheader("Order Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    f"{dashboard['total_orders']:,}"
)

col2.metric(
    "Ship After Confirmation",
    f"{dashboard['confirmation']:,}"
)

col3.metric(
    "Nudge to Prepaid",
    f"{dashboard['prepaid_nudge']:,}"
)

col4.metric(
    "Hold / Manual Review",
    f"{dashboard['hold_cancel_manual_review']:,}"
)

st.divider()


# ==========================================
# ORDER DECISION DISTRIBUTION
# ==========================================

st.subheader("Order Decision Distribution")

chart_data = pd.DataFrame({
    "Action": [
        "Ship as-is",
        "Ship after confirmation",
        "Nudge to prepaid",
        "Hold / cancel"
    ],
    "Orders": [
        dashboard["ship_as_is"],
        dashboard["confirmation"],
        dashboard["prepaid_nudge"],
        dashboard["hold_cancel_manual_review"]
    ]
})

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(
        chart_data.set_index("Action"),
        use_container_width=True
    )

with col2:
    st.dataframe(
        chart_data,
        use_container_width=True,
        hide_index=True
    )

st.divider()


# ==========================================
# FINANCIAL IMPACT
# ==========================================

st.subheader("Estimated Financial Impact")

st.caption(
    f"Based on an assumed {conversion_rate:.0%} conversion "
    "of prepaid nudges. These are estimates, not realized savings."
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Estimated RTO Savings",
    f"₹{dashboard['estimated_rto_savings']:,.2f}"
)

col2.metric(
    "Prepaid Discount Cost",
    f"₹{dashboard['estimated_discount_cost']:,.2f}"
)

col3.metric(
    "Estimated Net Impact",
    f"₹{dashboard['estimated_net_financial_impact']:,.2f}"
)

st.divider()


# ==========================================
# CUSTOMER PROTECTION
# ==========================================

st.subheader("Customer Protection")

col1, col2 = st.columns(2)

col1.metric(
    "Genuine Delivered Orders at Risk",
    dashboard["genuine_orders_at_risk"]
)

col2.metric(
    "Potential Lost Gross Margin",
    f"₹{dashboard['estimated_lost_margin']:,.2f}"
)

st.info(
    "Delivered orders appearing in the Hold / cancel category "
    "are treated as potentially genuine orders at risk. "
    "This is a counterfactual estimate, not an actual cancellation."
)


# ==========================================
# ORDER DETAILS
# ==========================================

st.divider()

st.subheader("Order Decision Details")

st.caption(
    "Review individual order risk scores and recommended actions."
)

# Action filter
available_actions = sorted(
    decision_df["action"].dropna().unique().tolist()
)

selected_actions = st.multiselect(
    "Filter by recommended action",
    options=available_actions,
    default=available_actions
)

filtered_df = decision_df[
    decision_df["action"].isin(selected_actions)
]

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.write(
    f"Showing {len(filtered_df)} of {len(decision_df)} orders."
)

# Download decision log
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Decision Log",
    data=csv_data,
    file_name="cod_rto_decision_log.csv",
    mime="text/csv"
)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "COD RTO Risk Management | Machine Learning + Business Rules "
    "| Prepared by Zaid Nagori"
)
