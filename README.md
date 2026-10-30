# COD Risk Management & RTO Reduction System

## Project Overview

COD Risk Management is a machine learning-based project designed to help a Direct-to-Consumer (D2C) business reduce Return to Origin (RTO) losses from Cash on Delivery orders.

The system predicts the probability of an order becoming RTO and recommends an appropriate action based on the predicted risk.

Instead of automatically rejecting risky orders, the system uses four decision categories:

- Ship as-is
- Ship after WhatsApp confirmation
- Nudge to prepaid
- Hold / cancel for manual review

It also includes a simulated WhatsApp confirmation workflow and an interactive Streamlit dashboard to monitor decisions and estimate financial impact.

## Key Features

- Data cleaning and exploratory data analysis using Pandas.
- RTO prediction using a Random Forest classification model.
- Configurable risk thresholds through a JSON configuration file.
- Customer protection rules for high-risk first-time buyers.
- Simulated WhatsApp confirmation and prepaid discount workflow.
- 24-hour customer response timeout handling.
- Integrated order decision workflow.
- Interactive Streamlit dashboard.
- Estimated RTO savings, prepaid discount costs and potential lost margin analysis.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Pandas, NumPy | Data processing |
| Scikit-learn | Machine learning |
| Random Forest | RTO risk prediction |
| Matplotlib, Seaborn | Data visualization |
| Streamlit | Interactive dashboard |
| JSON | Configurable decision thresholds |
| Jupyter Notebook | Data analysis and model development |

## Project Structure

```text
cod-risk-management/
│
├── backend/
│   ├── config.json
│   ├── decision_engine.py
│   ├── whatsapp_flow.py
│   ├── order_workflow.py
│   └── dashboard.py
│
├── data/
│   ├── orders_sample.csv
│   └── decision_log.csv
│
├── notebooks/
│   └── cod_rto_analysis.ipynb
│
├── dashboard_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: Adjust the notebook filename and folder structure above to match the actual files in your repository.*

## How the System Works

### 1. Data Preparation

The order dataset is cleaned and prepared using Pandas.

- Remove duplicate order IDs.
- Standardise order status values.
- Filter delivered and RTO orders.
- Create a binary target variable for RTO prediction.

### 2. Machine Learning Model

A Random Forest classifier is used to predict the probability of an order becoming RTO.

The model uses customer history, order value and selected order and location attributes.

Model performance is evaluated using accuracy, precision, recall, F1-score and ROC-AUC.

### 3. Decision Engine

The predicted RTO probability is passed to a configurable decision engine.

Based on risk thresholds, the system recommends one of four actions:

1. Ship as-is.
2. Ship after WhatsApp confirmation.
3. Nudge to prepaid.
4. Hold / cancel for manual review.

High-risk first-time customers are routed to confirmation rather than automatic cancellation to avoid losing genuine customers.

### 4. WhatsApp Mock Workflow

The WhatsApp module simulates:

- Order confirmation messages.
- YES and NO customer responses.
- Prepaid payment discount offers.
- Unclear response handling.
- 24-hour response timeout.

This is a mock workflow and does not send actual WhatsApp messages or payment links.

### 5. Founder Dashboard

An interactive Streamlit dashboard displays:

- Total orders analysed.
- Orders in each decision category.
- Estimated RTO savings.
- Estimated prepaid discount cost.
- Potential lost margin from genuine orders in the hold category.
- Estimated net financial impact.

A prepaid conversion rate control allows different business scenarios to be evaluated.

## Business Assumptions

| Parameter | Value |
|---|---:|
| COD RTO rate | 28% |
| Prepaid RTO rate | 4% |
| Forward shipping | ₹65 |
| Return shipping | ₹65 |
| Packaging and handling | ₹25 |
| Expected damage loss | ₹14.40 |
| Total RTO cost | ₹169.40 |
| Prepaid discount | ₹20 |
| Average order value | ₹649 |
| Delivered gross margin | 62% |

Expected RTO cost avoided per successful prepaid conversion:

`(28% - 4%) × ₹169.40 = ₹40.66`

Estimated net benefit after a ₹20 discount:

`₹40.66 - ₹20 = ₹20.66`

These are estimates based on the business assumptions provided in the assignment.

## Model Evaluation

Initial model comparison:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 71.1% | 49.1% | 47.8% | 48.4% | 68.8% |
| Random Forest | 70.4% | 48.1% | 55.8% | 51.6% | 69.6% |

Random Forest was selected because it achieved better recall, F1-score and ROC-AUC in the initial comparison.

These are initial held-out test results, not production performance guarantees.

## Latest Decision Results

The refreshed decision engine was tested on 398 orders.

| Recommended Action | Orders |
|---|---:|
| Ship as-is | 0 |
| Ship after confirmation | 132 |
| Nudge to prepaid | 240 |
| Hold / cancel | 26 |
| Total | 398 |

The first-time customer protection rule resulted in zero first-time customers being assigned to Hold / cancel.

## Installation and Setup

### Prerequisites

- Python 3.10 or later.
- Git.
- Jupyter Notebook.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd cod-risk-management
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Jupyter Notebook

```bash
jupyter notebook
```

Open the project notebook and execute the cells in order to perform data preparation, model training, evaluation and decision generation.

### 5. Run the Streamlit Dashboard

After generating the decision log CSV file, run:

```bash
python -m streamlit run dashboard_app.py
```

Open the local URL displayed in your terminal, usually:

`http://localhost:8501`

## Limitations and Future Improvements

- Improve model performance through further feature engineering and validation.
- Calibrate predicted probabilities before relying on risk thresholds.
- Validate decision thresholds using actual business outcomes.
- Integrate the WhatsApp Business API.
- Integrate real payment links and payment confirmation.
- Monitor actual RTO rates and prepaid conversion rates.
- Improve the decision engine using customer feedback and delivery history.

## Conclusion

This project demonstrates how machine learning, rule-based decision-making and business analytics can work together to reduce COD-related RTO losses while protecting genuine customers.

The system is designed as a prototype for controlled testing before production deployment.

## Author
Zaid Nagori
