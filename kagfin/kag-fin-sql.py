# START GENAI
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import zipfile

# Step 1: Download the dataset from Kaggle

# Ensure you have your Kaggle API credentials set up in ~/.kaggle/kaggle.json
# You can download the dataset using the Kaggle API
os.system('kaggle datasets download -d pacificrm/financial-sheets -p ./data')

# Unzip the downloaded dataset
zip_path = './data/financial-sheets.zip'
extract_path = './data'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Step 2: Load the CSV file

csv_file_path = './data/dataset/dataset/Annual_P_L_1_final.csv'
df = pd.read_csv(csv_file_path)

# Step 3: Connect to PostgreSQL and upload data

# Database credentials
db_user = 'postgres'
db_password = '123'
db_host = 'localhost'
db_port = '5432'
db_name = 'findata'

# Create a connection string
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create a sqlalchemy engine
engine = create_engine(connection_string)

# Table name
table_name = 'annual_pl'

# Try to upload the dataframe to PostgreSQL
try:
    df.to_sql(table_name, engine, if_exists='fail', index=False)
    print("Table created and data uploaded successfully!")
except ValueError as ve:
    # This will catch the error if the table already exists
    print(f"Table {table_name} already exists. Appending data instead.")
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print("Data appended successfully!")
except ProgrammingError as pe:
    # This will catch other SQL-related errors
    print(f"An error occurred: {pe}")

# END GENAI