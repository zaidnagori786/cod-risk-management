# Decision Log – COD RTO Risk Management

- **Data cleaning:** I removed duplicate orders and excluded records without a final DELIVERED or RTO status. I considered using the raw dataset, but cleaning it first would make the analysis more reliable.

- **Model selection:** I compared Logistic Regression and Random Forest. I chose Random Forest because it performed better in recall, F1 score, and ROC AUC in my initial comparison.

- **Feature selection:** I initially considered customer names and full address text as features. I decided to focus on structured information such as order value, previous orders, previous RTO count, city, state, and marketing source because raw text fields can be noisy and raise privacy concerns.

- **Decision approach:** I chose four actions: Ship as-is, Ship after confirmation, Nudge to prepaid, and Hold / cancel. I considered using only a high-risk cancellation rule, but different risk levels need different actions.

- **First-time customers:** I added a safeguard so high-risk first-time customers are sent for confirmation and manual review instead of automatic cancellation. This helps avoid losing genuine new customers.

- **Risk thresholds:** I kept the thresholds in `backend/config.json` instead of hardcoding them. This makes it easier to change the rules. The current values are initial assumptions and need further testing.

- **WhatsApp workflow:** I built a simulated YES/NO/unclear/no-response flow instead of integrating a live WhatsApp API. This allowed me to demonstrate the process without external API credentials.

- **Prepaid incentive:** I used an assumed ₹20 discount to encourage prepaid payments. I considered offering no discount, but a small incentive could encourage customers to switch from COD while keeping the cost limited.

- **Dashboard:** I used Streamlit to show decision counts and estimated financial impact. I chose it because it was quick to build and allowed interactive testing of prepaid conversion assumptions.

- **Deployment approach:** I recommended a shadow-mode pilot before live deployment instead of immediately automating order decisions. The model needs validation on real order data before it can safely influence fulfilment.