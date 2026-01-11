from utils.file_handler import read_sales_data
from utils.data_processor import parse_and_clean, analyze_sales
from utils.api_handler import ProductAPIHandler

def main():
    print("=== Sales Analytics System ===\n")
    
    # Step 1: Read file
    records = read_sales_data('sales_data.txt')
    
    # Step 2: Clean data
    sales_data = parse_and_clean(records)
    
    # Step 3: API integration
    api_handler = ProductAPIHandler()
    enriched_data = api_handler.add_api_info(sales_data)
    
    # Step 4: Analysis
    analyze_sales(enriched_data)
    
    # Save report
    import csv
    with open('output/cleaned_sales.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=sales_data[0].keys())
        writer.writeheader()
        writer.writerows(enriched_data)
    print("\nSaved cleaned data to output/cleaned_sales.csv")

if __name__ == "__main__":
    main()
