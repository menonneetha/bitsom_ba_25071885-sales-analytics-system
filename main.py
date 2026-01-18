import os
import csv
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter, analyze_sales,
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products
)
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
    
    # QUESTION 2 PART 1: Enhanced analysis (KEEPS original Question 2 output)
    print("\n" + "="*50)
    print("QUESTION 2 PART 1 - ENHANCED ANALYSIS")
    print("="*50)
    
    # API Integration
    api_handler = ProductAPIHandler()
    enriched_data = api_handler.add_api_info(valid_transactions)
    
    # Question 2 BUSINESS REPORT
    analyze_sales(enriched_data)
    
    # NEW Question 3 PART 2: Advanced Data Processing (ADDED)
    print("\n" + "="*60)
    print("QUESTION 3 PART 2 - ADVANCED DATA PROCESSING")
    print("="*60)
    
    # 2.1a Total Revenue
    total_rev = calculate_total_revenue(valid_transactions)
    print(f"💰 2.1a Total Revenue: ₹{total_rev:,.2f}")
    
    # 2.1b Region-wise Sales
    region_sales = region_wise_sales(valid_transactions)
    print("\n📊 2.1b Region-wise Sales (Top 3):")
    for region, stats in list(region_sales.items())[:3]:
        print(f"   {region}: ₹{stats['total_sales']:,.0f} ({stats['percentage']}%, {stats['transaction_count']} txns)")
    
    # 2.1c Top Selling Products
    top_products = top_selling_products(valid_transactions, n=5)
    print("\n🏆 2.1c Top 5 Products (by quantity):")
    for product, qty, revenue in top_products:
        print(f"   {product}: {qty} units (₹{revenue:,.0f})")
    
    # 2.1d Customer Analysis (Top 3)
    customers = customer_analysis(valid_transactions)
    print("\n👥 2.1d Top 3 Customers:")
    for customer, stats in list(customers.items())[:3]:
        print(f"   {customer}: ₹{stats['total_spent']:,.0f} ({stats['purchase_count']} orders, avg ₹{stats['avg_order_value']:,.0f})")
    
    # 2.2b Peak Sales Day
    peak_day = find_peak_sales_day(valid_transactions)
    print(f"\n📅 2.2b Peak Sales Day: {peak_day[0]} (₹{peak_day[1]:,.0f}, {peak_day[2]} transactions)")
    
    # 2.3a Low Performing Products
    low_products = low_performing_products(valid_transactions, threshold=10)
    print(f"\n📉 2.3a Low Performing Products (<10 units): {len(low_products)} products")
    for product, qty, revenue in low_products[:3]:
        print(f"   {product}: {qty} units (₹{revenue:,.0f})")
    
    # Save comprehensive report
    os.makedirs('output', exist_ok=True)
    with open('output/complete_analysis.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=enriched_data[0].keys())
        writer.writeheader()
        writer.writerows(enriched_data)
    print("\n✅ Saved to output/complete_analysis.csv")

if __name__ == "__main__":
    main()
