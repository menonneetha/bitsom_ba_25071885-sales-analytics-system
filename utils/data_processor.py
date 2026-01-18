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

def calculate_total_revenue(transactions):
    """Task 2.1a: Calculate Total Revenue"""
    total = sum(t['Quantity'] * t['UnitPrice'] for t in transactions)
    return round(total, 2)

def region_wise_sales(transactions):
    """Task 2.1b: Region-wise Sales Analysis"""
    total_revenue = calculate_total_revenue(transactions)
    region_stats = {}
    
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
    
    # Add percentages and sort
    for region in region_stats:
        region_stats[region]['percentage'] = round(
            (region_stats[region]['total_sales'] / total_revenue) * 100, 2
        )
    
    return dict(sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True))

def top_selling_products(transactions, n=5):
    """Task 2.1c: Top Selling Products by Quantity"""
    product_stats = {}
    
    for t in transactions:
        product = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        
        if product not in product_stats:
            product_stats[product] = {'total_qty': 0, 'total_revenue': 0.0}
        product_stats[product]['total_qty'] += qty
        product_stats[product]['total_revenue'] += revenue
    
    # Convert to list of tuples and sort by quantity
    top_products = []
    for product, stats in product_stats.items():
        top_products.append((
            product,
            stats['total_qty'],
            round(stats['total_revenue'], 2)
        ))
    
    return sorted(top_products, key=lambda x: x[1], reverse=True)[:n]

def customer_analysis(transactions):
    """Task 2.1d: Customer Purchase Analysis"""
    customer_stats = {}
    
    for t in transactions:
        customer = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']
        
        if customer not in customer_stats:
            customer_stats[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
        
        customer_stats[customer]['total_spent'] += amount
        customer_stats[customer]['purchase_count'] += 1
        customer_stats[customer]['products_bought'].add(product)
    
    # Convert sets to lists and calculate avg
    for customer in customer_stats:
        stats = customer_stats[customer]
        stats['avg_order_value'] = round(stats['total_spent'] / stats['purchase_count'], 2)
        stats['products_bought'] = list(stats['products_bought'])
    
    # Sort by total_spent
    return dict(sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True))

def daily_sales_trend(transactions):
    """Task 2.2a: Daily Sales Trend"""
    daily_stats = {}
    
    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']
        
        if date not in daily_stats:
            daily_stats[date] = {'revenue': 0.0, 'transaction_count': 0, 'unique_customers': set()}
        
        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['unique_customers'].add(customer)
    
    # Convert sets to counts and round revenue
    for date in daily_stats:
        daily_stats[date]['unique_customers'] = len(daily_stats[date]['unique_customers'])
        daily_stats[date]['revenue'] = round(daily_stats[date]['revenue'], 2)
    
    return dict(sorted(daily_stats.items()))

def find_peak_sales_day(transactions):
    """Task 2.2b: Find Peak Sales Day"""
    daily_stats = daily_sales_trend(transactions)
    peak_date = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
    date, stats = peak_date
    return (date, stats['revenue'], stats['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """Task 2.3a: Low Performing Products"""
    product_stats = {}
    
    for t in transactions:
        product = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']
        
        if product not in product_stats:
            product_stats[product] = {'total_qty': 0, 'total_revenue': 0.0}
        product_stats[product]['total_qty'] += qty
        product_stats[product]['total_revenue'] += revenue
    
    # Find low performers
    low_performers = []
    for product, stats in product_stats.items():
        if stats['total_qty'] < threshold:
            low_performers.append((
                product,
                stats['total_qty'],
                round(stats['total_revenue'], 2)
            ))
    
    return sorted(low_performers, key=lambda x: x[1])  # Sort by quantity ascending
