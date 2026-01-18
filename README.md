# Sales Analytics System - Complete Assignment Solution

**Python Data Analytics System** implementing file processing, API integration, advanced analytics, and automated reporting (Questions 1-6).

## 📋 Features Implemented

✅ **Question 1**: File I/O with encoding handling, data cleaning  
✅ **Question 2**: Interactive validation & filtering  
✅ **Question 3**: Advanced analytics (region/product/customer analysis)  
✅ **Question 4**: DummyJSON API integration & data enrichment  
✅ **Question 5**: Comprehensive formatted report generation  
✅ **Question 6**: Interactive 10-step main application workflow  

## 📁 Repository Structure
sales-analytics-system/ 
├── README.md # Documentation 
├── main.py # Interactive main application 
├── requirements.txt # Dependencies 
├── data/ 
│ └── sales_data.txt # Input dataset (~80 records) 
├── utils/ # Modular utilities 
│ ├── file_handler.py # File reading & encoding 
│ ├── data_processor.py # All analysis functions 
│ └── api_handler.py # DummyJSON API integration 
├── output/ # Generated reports (gitignored) 
└── .gitignore # Excludes generated files 


## 🚀 Quick Start (Mac/Linux)

1. **Clone/Download** repository
2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
3. Run interactive application:
python3 main.py

🖥️ Expected Interactive Output

=================================================  
         SALES ANALYTICS SYSTEM. 
=================================================  

- [1/10] Reading sales data... ✓ 80 transactions
- [2/10] Parsing and cleaning data... ✓ 80 records
- [3/10] Filter Options: Regions: North,South,East,West  
Do you want to filter data? (y/n): n
- [4/10] Validating transactions... ✓ Valid: 70 | Invalid: 10  
...  
- [10/10] Process Complete!

📊 Generated Files (Auto-created by program)

output/sales_report.txt           # Question 5: 8-section report  
data/enriched_sales_data.txt      # Question 4: API-enriched data   
output/complete_analysis.csv      # All transaction data  
output/product_cache.json         # API cache  

🔍 Key Features Demonstrated

Question 1: Data Processing  
- Handles non-UTF8 encoding issues
- Pipe-delimited parsing with error handling
- Removes 10 invalid records → 70 valid

Question 2: Interactive Filtering  
Filter Options Available:  
- Regions: North, South, East, West    
- Amount Range: ₹-8,982 - ₹818,960  
- Do you want to filter data? (y/n):  

Question 3: Advanced Analytics (9 Functions)  
- calculate_total_revenue() → ₹3,527,808
- region_wise_sales() → North: 37.45%
- top_selling_products() → Laptop: 45 units
- customer_analysis() → C001: ₹95,000
- daily_sales_trend(), find_peak_sales_day()
- low_performing_products()

Question 4: DummyJSON API Integration  
https://dummyjson.com/products?limit=100  
✅ Fetched 100 products  
✅ Enriched P101 → iPhone 9 (45/70 matches)  

Question 5: Report Generation  

output/sales_report.txt (30+ lines):  
- SALES ANALYTICS REPORT  
- Total Revenue: ₹3,527,808.00  
- Region-wise tables, Top 5 products/customers  
- Peak sales day, API enrichment summary  

Question 6: Main Application  

- 10-step interactive workflow
- User-driven filtering
- Complete error handling
- Professional progress indicators

📈 Sample Results  

Metric			Value  
Total Records		80  
Valid Records		70  
Invalid Records		10  
Total Revenue		₹3,527,808  
Top Region		North (37.45%)  
Top Product		Laptop (45 units)  
API Matches		45/70 (64%)  

🛠️ Technologies
- Python 3.8+
- requests 2.31.0 - HTTP API calls
- Modular architecture - 3 utility modules
- Interactive CLI - User input handling

🎯 Assignment Requirements Met
- Q1: File handling, encoding, cleaning (15 pts)
- Q2: Validation/filtering, user display (15 pts)
- Q3: 9 analytics functions (25 pts)
- Q4: DummyJSON API + enrichment (13 pts)
- Q5: 8-section formatted report (15 pts)
- Q6: Interactive 10-step workflow (10 pts)

📝 Usage Examples
No filtering:
python3 main.py
### Answer 'n' to filter prompt

Region filter:
python3 main.py  
### Answer 'y' → '1' → 'North'

