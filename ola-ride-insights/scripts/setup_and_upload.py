import pandas as pd
import os
import psycopg2

DB_NAME = "ola_ride_insights"
USER = "postgres"
PASSWORD = "123"
HOST = "localhost"
PORT = "5432"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
XLSX_PATH = os.path.join(BASE_DIR, 'scripts', 'OLA_DataSet.xlsx')
CSV_PATH = os.path.join(DATA_DIR, 'july_rides.csv')

def extract_july_to_csv():
    df = pd.read_excel(XLSX_PATH, sheet_name='July')
    df.to_csv(CSV_PATH, index=False)
    print(f"Extracted July sheet to {CSV_PATH}")
    return df

def create_table_from_columns(columns):
    # Map pandas dtypes to PostgreSQL types
    dtype_map = {
        'object': 'VARCHAR(255)',
        'int64': 'INT',
        'float64': 'FLOAT',
        'datetime64[ns]': 'DATE'
    }
    col_defs = []
    for col, dtype in columns.items():
        pg_type = dtype_map.get(str(dtype), 'VARCHAR(255)')
        # Use Booking_ID as PRIMARY KEY if present, else first column
        if col == 'Booking_ID':
            col_defs.append(f'"{col}" {pg_type} PRIMARY KEY')
        else:
            col_defs.append(f'"{col}" {pg_type}')
    create_stmt = f'CREATE TABLE IF NOT EXISTS july_rides ({", ".join(col_defs)});'
    return create_stmt

def upload_csv_to_db(df):
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    # Create table
    create_stmt = create_table_from_columns(df.dtypes)
    cur.execute(create_stmt)
    conn.commit()
    # Insert data
    columns = list(df.columns)
    placeholders = ','.join(['%s'] * len(columns))
    column_str = ','.join([f'"{c}"' for c in columns])
    insert_stmt = f'INSERT INTO july_rides ({column_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;'
    for row in df.itertuples(index=False, name=None):
        cur.execute(insert_stmt, row)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Uploaded data to july_rides table.")

if __name__ == "__main__":
    df = extract_july_to_csv()
    upload_csv_to_db(df)