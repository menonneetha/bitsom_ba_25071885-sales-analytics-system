def parse_and_clean(records):
    """
    Parses pipe-delimited records, cleans data, validates, and returns valid transactions.
    Prints validation statistics.
    """
    valid_records = []
    invalid_count = 0
    reasons = []

    for record in records:
        parts = record.split('|')
        if len(parts) != 8:
            invalid_count += 1
            reasons.append(f"Wrong field count: {len(parts)}")
            continue

        trans_id, date, prod_id, prod_name, qty_str, price_str, cust_id, region = parts

        # Validation
        if not trans_id.startswith('T'):
            invalid_count += 1
            reasons.append(f"Invalid TransactionID: {trans_id}")
            continue
        if not cust_id or cust_id.strip() == '':
            invalid_count += 1
            reasons.append(f"Missing CustomerID: {cust_id}")
            continue
        if not region or region.strip() == '':
            invalid_count += 1
            reasons.append(f"Missing Region: {region}")
            continue

        try:
            qty = int(qty_str.strip())
            price_clean = price_str.strip().replace(',', '')
            price = float(price_clean)
        except ValueError:
            invalid_count += 1
            reasons.append(f"Invalid qty/price: {qty_str}/{price_str}")
            continue

        if qty <= 0 or price <= 0:
            invalid_count += 1
            reasons.append(f"Non-positive qty/price: {qty}/{price}")
            continue

        # Valid record
        valid_records.append({
            'TransactionID': trans_id,
            'Date': date,
            'ProductID': prod_id,
            'ProductName': prod_name,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': cust_id,
            'Region': region,
            'TotalSales': qty * price
        })

    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")
    if reasons:
        print("Sample invalid reasons:", reasons[:3])
    return valid_records

def analyze_sales(sales_data):
    """Simple analysis"""
    total_sales = sum(r['TotalSales'] for r in sales_data)
    regions = {}
    products = {}
    for r in sales_data:
        regions[r['Region']] = regions.get(r['Region'], 0) + r['TotalSales']
        products[r['ProductID']] = products.get(r['ProductID'], 0) + r['TotalSales']
    
    print("\n=== ANALYSIS REPORT ===")
    print(f"Total Sales: ₹{total_sales:,.2f}")
    print("Sales by Region:")
    for reg, amt in sorted(regions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {reg}: ₹{amt:,.2f}")
    print("Top Products:")
    for prod, amt in sorted(products.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {prod}: ₹{amt:,.2f}")
