def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []
    
    for i, line in enumerate(raw_lines, 1):
        # Split by pipe, handle uneven fields
        parts = line.split('|')
        if len(parts) != 8:
            print(f"⚠️ Skipping line {i}: Wrong fields ({len(parts)})")
            continue
        
        try:
            # Extract fields
            TransactionID, Date, ProductID, ProductName, qty_str, price_str, CustomerID, Region = parts
            
            # Clean ProductName (remove extra commas if needed)
            ProductName = ProductName.replace(',', ' ').strip()
            
            # Clean numbers (remove commas)
            qty_clean = qty_str.strip().replace(',', '')
            price_clean = price_str.strip().replace(',', '')
            
            # Convert to proper types
            Quantity = int(qty_clean)
            UnitPrice = float(price_clean)
            
            transactions.append({
                'TransactionID': TransactionID.strip(),
                'Date': Date.strip(),
                'ProductID': ProductID.strip(),
                'ProductName': ProductName,
                'Quantity': Quantity,
                'UnitPrice': UnitPrice,
                'CustomerID': CustomerID.strip(),
                'Region': Region.strip()
            })
            
        except (ValueError, IndexError) as e:
            print(f"⚠️ Skipping line {i}: Parse error - {e}")
            continue
    
    print(f"✅ Parsed {len(transactions)} transactions")
    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    print("\n🔍 Validation & Filtering Starting...")
    
    # Show available options
    regions = list(set(t['Region'] for t in transactions if t['Region']))
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    print(f"Available Regions: {', '.join(regions)}")
    print(f"Transaction Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")
    
    valid_transactions = []
    invalid_count = 0
    summary = {
        'total_input': len(transactions),
        'invalid': 0,
        'filtered_by_region': 0,
        'filtered_by_amount': 0,
        'final_count': 0
    }
    
    for t in transactions:
        # Validation Rules
        amount = t['Quantity'] * t['UnitPrice']
        is_valid = True
        
        if t['Quantity'] <= 0 or t['UnitPrice'] <= 0:
            is_valid = False
        elif not all([t['TransactionID'].startswith('T'),
                      t['ProductID'].startswith('P'),
                      t['CustomerID'].startswith('C')]):
            is_valid = False
        elif not all([t.get(k) for k in ['TransactionID', 'Date', 'ProductID', 
                                        'ProductName', 'CustomerID', 'Region']]):
            is_valid = False
        
        if not is_valid:
            invalid_count += 1
            continue
        
        # Apply filters
        filtered_out = False
        
        if region and t['Region'] != region:
            filtered_out = True
            summary['filtered_by_region'] += 1
        
        if min_amount and amount < min_amount:
            filtered_out = True
            summary['filtered_by_amount'] += 1
        
        if max_amount and amount > max_amount:
            filtered_out = True
            summary['filtered_by_amount'] += 1
        
        if not filtered_out:
            valid_transactions.append(t)
    
    summary.update({
        'invalid': invalid_count,
        'final_count': len(valid_transactions)
    })
    
    print(f"📊 Filter Summary: {summary}")
    return valid_transactions, invalid_count, summary
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
