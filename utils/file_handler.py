import os

def read_sales_data(file_path):
    """
    Reads the sales data file, handling encoding issues and messy delimiters.
    Returns list of raw records (excluding header).
    """
    data_dir = 'data'
    full_path = os.path.join(data_dir, file_path)
    records = []
    try:
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        if lines:
            header = lines[0].strip()
            print(f"Header detected: {header}")
            records = [line.strip() for line in lines[1:] if line.strip()]
        print(f"Total records parsed: {len(records)}")
        return records
    except FileNotFoundError:
        print(f"File not found: {full_path}")
        return []
