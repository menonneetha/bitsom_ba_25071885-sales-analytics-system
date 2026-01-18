import requests
import os
import json

class ProductAPIHandler:
    def __init__(self):
        self.api_url = "https://dummyjson.com/products"
        self.product_mapping = {}
        self.cache_file = 'output/product_cache.json'

    def fetch_all_products(self):
        """
        Task 3.1a: Fetch All Products from DummyJSON API
        """
        try:
            print("🌐 Fetching products from DummyJSON API...")
            response = requests.get(f"{self.api_url}?limit=100", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            products = data['products']
            
            print(f"✅ Successfully fetched {len(products)} products")
            self.product_mapping = self.create_product_mapping(products)
            self.save_cache()
            return products
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            print("Loading from cache...")
            self.load_cache()
            products = list(self.product_mapping.values())
            return products if products else []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []

    def create_product_mapping(self, api_products):
        """
        Task 3.1b: Create Product Mapping (ID -> Product Info)
        """
        mapping = {}
        for product in api_products:
            # Use product ID as numeric key (1, 2, 3...)
            mapping[product['id']] = {
                'title': product.get('title', 'Unknown'),
                'category': product.get('category', 'Unknown'),
                'brand': product.get('brand', 'Unknown'),
                'price': product.get('price', 0),
                'rating': product.get('rating', 0.0)
            }
        print(f"✅ Created mapping for {len(mapping)} products")
        return mapping

    def get_product_info_by_id(self, product_id_str):
        """
        Extract numeric ID from ProductID (P101 -> 101, P5 -> 5)
        Returns product info or None
        """
        try:
            # Extract numeric part: P101 -> 101, P5 -> 5
            numeric_id = int(''.join(filter(str.isdigit, product_id_str)))
            return self.product_mapping.get(numeric_id)
        except (ValueError, IndexError):
            return None

    def enrich_sales_data(self, transactions, product_mapping=None):
        """
        Task 3.2: Enrich Sales Data with API Product Information
        """
        if product_mapping is None:
            product_mapping = self.product_mapping
        
        enriched_transactions = []
        
        for transaction in transactions:
            enriched = transaction.copy()
            
            # Extract numeric ID and get API product info
            api_product = self.get_product_info_by_id(transaction['ProductID'])
            
            if api_product:
                enriched.update({
                    'API_Category': api_product['category'],
                    'API_Brand': api_product['brand'],
                    'API_Rating': api_product['rating'],
                    'API_Match': True
                })
                print(f"✅ Enriched {transaction['ProductID']} -> {api_product['title']}")
            else:
                enriched.update({
                    'API_Category': None,
                    'API_Brand': None,
                    'API_Rating': None,
                    'API_Match': False
                })
                print(f"⚠️ No API match for {transaction['ProductID']}")
            
            enriched_transactions.append(enriched)
        
        # Save enriched data to file
        self.save_enriched_data(enriched_transactions)
        print(f"✅ Saved {len(enriched_transactions)} enriched records to data/enriched_sales_data.txt")
        return enriched_transactions

    def save_enriched_data(self, enriched_transactions, filename='data/enriched_sales_data.txt'):
        """
        Task 3.2: Save enriched transactions back to pipe-delimited file
        """
        os.makedirs('data', exist_ok=True)
        
        # Define header with new API fields
        header = ['TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 
                 'UnitPrice', 'CustomerID', 'Region', 'API_Category', 'API_Brand', 
                 'API_Rating', 'API_Match']
        
        with open(filename, 'w') as f:
            # Write header
            f.write('|'.join(header) + '\n')
            
            # Write data rows
            for transaction in enriched_transactions:
                row = []
                for field in header:
                    value = transaction.get(field, '')
                    if value is None:
                        row.append('NULL')
                    elif isinstance(value, float):
                        row.append(str(round(value, 2)))
                    else:
                        row.append(str(value))
                f.write('|'.join(row) + '\n')
        
        print(f"✅ Enriched data saved: {filename}")

    def load_cache(self):
        """Load cached products"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                self.product_mapping = cache
                print(f"✅ Loaded {len(self.product_mapping)} products from cache")
        except Exception:
            pass

    def save_cache(self):
        """Save products to cache"""
        try:
            os.makedirs('output', exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.product_mapping, f, indent=2)
        except Exception:
            pass

    # Backward compatibility for Question 1
    def add_api_info(self, sales_data):
        """Old method for Question 1 compatibility"""
        print("⚠️ Using legacy API matching (name-based)")
        self.fetch_all_products()
        return self.enrich_sales_data(sales_data)
