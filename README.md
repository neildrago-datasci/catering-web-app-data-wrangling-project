# Caterlytics — Catering Orders Data Wrangling

## Project overview
Caterlytics is a Data Wrangling mini-project built from the uploaded `catering_orders_demo.csv`.
The project follows the same academic workflow used in the previous Translytics-style project:

**Home → Load & Understand Data → Clean Data → Balance Data → Visualize & Analyze**

## Dataset
- Raw records: 150
- Raw columns: 5
- Clients: 19
- Fulfillment statuses: Cancelled, Delayed, Delivered, Pending
- Date range: 2020-01-07 to 2024-12-22
- Raw missing cells: 0
- Raw exact duplicates: 0

## Cleaning
The dataset was standardized and validated:
1. Column names were normalized.
2. IDs and numeric fields were converted to appropriate types.
3. Order dates were parsed as dates.
4. Text values were stripped and standardized.
5. Exact duplicates were removed if present.
6. Fulfillment statuses were checked against the expected categories.
7. Positive numeric cost values and non-missing identifiers/dates were required.
8. Date-derived features were added: year, month, month name, day name and quarter.

No records required deletion in this dataset because the supplied data contains no missing cells, no exact duplicate rows, and no invalid cost/status/date records.

## Balancing
`fulfillment_status` is imbalanced in the original data:
fulfillment_status
Delivered    72
Cancelled    32
Pending      28
Delayed      18

Random oversampling with `random_state=42` was used to create a separate balanced dataset containing 288 records, with 72 records per status.

**Important:** The cleaned dataset retains the real distribution. The balanced dataset is a derived dataset for fair class-based analysis/modeling.

## Main findings
- Delivered orders are the largest group (72 / 150 = 48.0%).
- Cancelled orders account for 21.3%.
- Delayed orders have the highest average order cost (₹5,097.83).
- Client C07 has the highest number of orders (16).
- Total recorded catering cost is ₹580,051.38.
- Average order cost is ₹3,867.01; median is ₹3,717.51.
- The dataset covers 2020–2024.

## Run the app
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — Streamlit application
- `data/catering_orders_raw.csv` — original data copy
- `data/catering_orders_cleaned.csv` — cleaned + engineered data
- `data/catering_orders_balanced.csv` — balanced data
- `docs/` — report, presentation and speaking/viva material
