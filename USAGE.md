# Usage

## 1. Start the Dashboard

After installation, launch the application:

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501).

## 2. Navigation

Use the sidebar to switch between pages:

### Overview (`pages/1_Overview.py`)
Displays key performance indicators (total revenue, profit, number of orders) and summary charts.

### Regional (`pages/2_Regional.py`)
Breaks down sales by region (North America, Europe, Asia Pacific, Latin America, Middle East & Africa).

### Product (`pages/3_Product.py`)
Shows performance per product across categories (Software, Cloud Services, Analytics, Security, Integration).

### Data Explorer (`pages/4_Data_Explorer.py`)
An interactive table with filters to explore the raw sales dataset.

## 3. Regenerate Data

To create a fresh dataset, run:

```bash
python generate_data.py
```

This overwrites `data/sales_data.csv`. The dashboard will automatically use the new data on the next page load.