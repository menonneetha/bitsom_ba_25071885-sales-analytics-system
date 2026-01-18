import os

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    """
    data_path = os.path.join('data', filename)
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(data_path, 'r', encoding=encoding, errors='ignore') as f:
                lines = f.readlines()
            
            # Skip header, remove empty lines
            raw_lines = [line.strip() for line in lines[1:] if line.strip()]
            print(f"✅ Successfully read {len(raw_lines)} records with {encoding}")
            return raw_lines
            
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"❌ File not found: {data_path}")
            print("Please ensure sales_data.txt is in data/ folder")
            return []
    
    print("❌ Could not read file with any encoding")
    return []
