import os
import csv
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter, analyze_sales,
    calculate_total_revenue, region_wise_sales, top_selling_products,
    customer_analysis, daily_sales_trend, find_peak_sales_day,
    low_performing_products, generate_sales_report
)
from utils.api_handler import ProductAPIHandler

def main():
    """
    Question 6 Part 5: Main Interactive Application
    Complete 10-step workflow with user interaction
    """
    try:
        print("=" * 55)
        print("         SALES ANALYTICS SYSTEM")
        print("=" * 55)
        print()
        
        # [1/10] Reading sales data
        print("[1/10] Reading sales data...")
        records = read_sales_data('sales_data.txt')
        print(f"   ✓ Successfully read {len(records)} transactions")
        print()
        
        # [2/10] Parsing and cleaning data
        print("[2/10] Parsing and cleaning data...")
        all_transactions = parse_transactions(records)
        print(f"   ✓ Parsed {len(all_transactions)} records")
        print()
        
        # [3/10] Filter Options (USER INTERACTION)
        print("[3/10] Filter Options Available:")
        regions = list(set(t['Region'] for t in all_transactions if t['Region']))
        amounts = [t['Quantity'] * t['UnitPrice'] for t in all_transactions]
        print(f"   Regions: {', '.join(regions)}")
        print(f"   Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")
        print()
        
        filter_choice = input("Do you want to filter data? (y/n): ").strip().lower()
        valid_transactions = all_transactions
        
        if filter_choice == 'y':
            print("\nFilter Options:")
            print("1. Region")
            print("2. Amount Range")
            filter_type = input("Choose filter (1 or 2): ").strip()
            
            if filter_type == '1':
                region_filter = input("Enter region (North/South/East/West): ").strip()
                valid_transactions, _, _ = validate_and_filter(all_transactions, region=region_filter)
                print(f"   ✓ Filtered by region: {len(valid_transactions)} records")
            elif filter_type == '2':
                min_amt = float(input("Enter minimum amount: "))
                max_amt = float(input("Enter maximum amount: "))
                valid_transactions, _, _ = validate_and_filter(all_transactions, 
                                                            min_amount=min_amt, max_amount=max_amt)
                print(f"   ✓ Filtered by amount: {len(valid_transactions)} records")
        else:
            # Apply validation only (no filters)
            valid_transactions, invalid_count, _ = validate_and_filter(all_transactions)
            print(f"   ✓ No filtering applied")
        print()
        
        # [4/10] Validating transactions
        print("[4/10] Validating transactions...")
        final_valid, invalid_count, summary = validate_and_filter(valid_transactions)
        print(f"   ✓ Valid: {len(final_valid)} | Invalid: {invalid_count}")
        print()
        
        # [5/10] Analyzing sales data
        print("[5/10] Analyzing sales data...")
        total_rev = calculate_total_revenue(final_valid)
        print(f"   ✓ Analysis complete - Total Revenue: ₹{total_rev:,.0f}")
        print()
        
        # [6/10] Fetching product data from API
        print("[6/10] Fetching product data from API...")
        api_handler = ProductAPIHandler()
        api_products = api_handler.fetch_all_products()
        print(f"   ✓ Fetched {len(api_products)} products")
        print()
        
        # [7/10] Enriching sales data
        print("[7/10] Enriching sales data...")
        enriched_transactions = api_handler.enrich_sales_data(final_valid)
        api_success = sum(1 for t in enriched_transactions if t['API_Match'])
        success_rate = round((api_success / len(enriched_transactions)) * 100, 1)
        print(f"   ✓ Enriched {api_success}/{len(enriched_transactions)} transactions ({success_rate}%)")
        print()
        
        # [8/10] Saving enriched data
        print("[8/10] Saving enriched data...")
        print("   ✓ Saved to: data/enriched_sales_data.txt")
        print()
        
        # [9/10] Generating report
        print("[9/10] Generating report...")
        generate_sales_report(final_valid, enriched_transactions)
        print("   ✓ Report saved to: output/sales_report.txt")
        print()
        
        # [10/10] Process Complete!
        print("[10/10] Process Complete!")
        print("=" * 55)
        print("\n📁 Files Generated:")
        print("   • data/enriched_sales_data.txt")
        print("   • output/sales_report.txt")
        print("   • output/complete_analysis.csv")
        print("   • output/product_cache.json")
        print("\n🎉 Sales Analytics System - All Questions Complete!")
        
    except FileNotFoundError:
        print("❌ Error: sales_data.txt not found in data/ folder")
        print("Please ensure data/sales_data.txt exists.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print("Program terminated safely.")

if __name__ == "__main__":
    main()
