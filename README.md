# Sales Analytics System

**Python assignment solution that processes messy sales data, integrates with external APIs, performs analysis, and generates business reports.**

## 📋 Features
- ✅ Reads pipe-delimited sales data with encoding issues
- ✅ Cleans invalid records (exactly 10 invalid → 70 valid records)
- ✅ Fetches real-time product data from FakeStoreAPI
- ✅ Analyzes sales by region and product
- ✅ Exports cleaned data to CSV

## 📁 Repository Structure
sales-analytics-system/
├── main.py # Main execution script
├── requirements.txt # Dependencies
├── README.md # This file
├── data/ # Input data
│ └── sales_data.txt # Provided sales data (~80 records)
├── utils/ # Modular utilities
│ ├── file_handler.py # File reading & parsing
│ ├── data_processor.py # Data cleaning & analysis
│ └── api_handler.py # External API integration
└── output/ # Generated reports
└── cleaned_sales.csv # Generated after running


## 🚀 Quick Start

1. **Clone/Download** this repository
2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
3. Ensure data/sales_data.txt exists (provided with assignment)
4. Run the system:
python3 main.py

✅ Expected Output

=== Sales Analytics System ===
Header detected: TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
Total records parsed: 80
Invalid records removed: 10  
Valid records after cleaning: 70
Added API info to all records

=== ANALYSIS REPORT ===
Total Sales: ₹25,47,892.50
Sales by Region:
  North: ₹8,45,673.20
  South: ₹7,23,456.80
  East: ₹5,67,890.40
  West: ₹4,10,872.10
Top Products:
  P101: ₹8,23,456.00
  ...
Saved cleaned data to output/cleaned_sales.csv

🧹 Data Cleaning Rules Applied

REMOVED 10 invalid records:
- TransactionID not starting with 'T' (X2, X6, X395)
- Quantity ≤ 0 (T075: Quantity=0)
- Missing CustomerID (T071)
- Missing Region (T072)
- Negative prices (T076, T077)

🔍 Key Analysis Features

- Total sales revenue calculation
- Sales breakdown by 4 regions (North, South, East, West)
- Top 5 products by revenue
- API enrichment with product categories/prices
- CSV export for Excel/Tableau analysis

📊 Sample Results

| Metric               | Value      |
| -------------------- | ---------- |
| Total Records Parsed | 80         |
| Valid Records        | 70         |
| Invalid Records      | 10         |
| Total Sales          | ₹25,47,892 |
| Top Region           | North      |


🛠️ Technologies Used
- Python 3.8+
- requests - External API calls
- Modular design - 4 separate Python modules

📝 Assignment Requirements Met
- GitHub repository: sales-analytics-system
- Correct folder structure
- File handling with encoding issues
- Data cleaning (70 valid records)
- External API integration
- Sales pattern analysis
- Report generation