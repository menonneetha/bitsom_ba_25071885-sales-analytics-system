import os  
import csv
from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter, analyze_sales
from utils.api_handler import ProductAPIHandler


def main():
    print("=== Sales Analytics System ===\n")
    
    # QUESTION 1: Original functionality
    records = read_sales_data('sales_data.txt')
    all_transactions = parse_transactions(records)
    valid_transactions, invalid_count, _ = validate_and_filter(all_transactions)
    
    print(f"Total records parsed: {len(records)}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_transactions)}")
    
    # QUESTION 2: Enhanced analysis
    print("\n" + "="*50)
    print("QUESTION 2 PART 1 - ENHANCED ANALYSIS")
    print("="*50)
    
    # API Integration (Question 1)
    api_handler = ProductAPIHandler()
    enriched_data = api_handler.add_api_info(valid_transactions)
    
    # Analysis
    analyze_sales(enriched_data)
    
    # Save report
    import csv
    os.makedirs('output', exist_ok=True)
    with open('output/cleaned_sales.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
        writer.writeheader()
        writer.writerows(enriched_data)
    print("\n✅ Saved to output/cleaned_sales.csv")

def analyze_sales(sales_data):
    """Simple analysis from Question 1"""
    total_sales = sum(r['Quantity'] * r['UnitPrice'] for r in sales_data)
    regions = {}
    products = {}
    for r in sales_data:
        regions[r['Region']] = regions.get(r['Region'], 0) + (r['Quantity'] * r['UnitPrice'])
        products[r['ProductID']] = products.get(r['ProductID'], 0) + (r['Quantity'] * r['UnitPrice'])
    
    print("\n=== BUSINESS REPORT ===")
    print(f"💰 Total Sales: ₹{total_sales:,.2f}")
    print("📊 Sales by Region:")
    for reg, amt in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print(f"   {reg}: ₹{amt:,.2f}")
    print("🏆 Top 5 Products:")
    for prod, amt in sorted(products.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {prod}: ₹{amt:,.2f}")

if __name__ == "__main__":
    main()
