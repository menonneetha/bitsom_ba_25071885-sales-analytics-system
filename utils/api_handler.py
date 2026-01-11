import requests
import json
import os

class ProductAPIHandler:
    def __init__(self):
        self.cache = {}
        self.api_url = "https://fakestoreapi.com/products"

    def get_product_info(self, product_name):
        try:
            response = requests.get(self.api_url, timeout=5)
            products = response.json()
            for p in products:
                if product_name.lower() in p['title'].lower():
                    return {
                        'name': p['title'],
                        'category': p['category'],
                        'current_price': p['price']
                    }
            return None
        except:
            return None

    def add_api_info(self, sales_data):
        for record in sales_data:
            info = self.get_product_info(record['ProductName'])
            record['api_info'] = info
        print("Added API info to all records")
        return sales_data
