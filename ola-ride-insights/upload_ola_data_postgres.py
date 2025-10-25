import psycopg2
import pandas as pd
import os

DB_NAME = "ola_ride_insights"
USER = "postgres"
PASSWORD = "123"
HOST = "localhost"
PORT = "5432"
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def create_database():
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='123', host='localhost', port='5432')
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created.")
    else:
        print(f"Database '{DB_NAME}' already exists.")
    cur.close()
    conn.close()

def create_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rides (
        ride_id SERIAL PRIMARY KEY,
        user_id INT,
        driver_id INT,
        ride_date DATE,
        pickup_location VARCHAR(255),
        drop_location VARCHAR(255),
        distance_km FLOAT,
        fare_amount FLOAT,
        payment_method VARCHAR(50),
        ride_status VARCHAR(50)
    );
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY,
        registration_date DATE,
        gender VARCHAR(10),
        age INT,
        city VARCHAR(100)
    );
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id INT PRIMARY KEY,
        registration_date DATE,
        rating FLOAT,
        city VARCHAR(100)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created (if not exist).")

def upload_csv(table, csv_file, columns):
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    file_path = os.path.join(DATA_DIR, csv_file)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    df = pd.read_csv(file_path)
    df = df[columns]
    for _, row in df.iterrows():
        values = tuple(row)
        placeholders = ','.join(['%s'] * len(values))
        cur.execute(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;", values)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Uploaded data to {table} from {csv_file}")

if __name__ == "__main__":
    create_database()
    create_tables()
    upload_csv('users', 'users.csv', ['user_id', 'registration_date', 'gender', 'age', 'city'])
    upload_csv('drivers', 'drivers.csv', ['driver_id', 'registration_date', 'rating', 'city'])
    upload_csv('rides', 'rides.csv', ['user_id', 'driver_id', 'ride_date', 'pickup_location', 'drop_location', 'distance_km', 'fare_amount', 'payment_method', 'ride_status'])