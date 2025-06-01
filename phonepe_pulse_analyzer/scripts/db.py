import psycopg2

def get_postgres_connection():
    return psycopg2.connect(
        dbname="phonepe",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

def initialize_database():
    conn = get_postgres_connection()
    cursor = conn.cursor()
    print("Creating table if not exists...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
        id SERIAL PRIMARY KEY,
        country TEXT,
        state TEXT,
        year INTEGER,
        name TEXT,
        count BIGINT,
        amount DOUBLE PRECISION
    );
    """
    # Aggregated User Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_user (
        id SERIAL PRIMARY KEY,
        country TEXT,
        state TEXT,
        year INTEGER,
        brand TEXT,
        count BIGINT
    );
    """)

    # Aggregated Insurance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_insurance (
        id SERIAL PRIMARY KEY,
        country TEXT,
        state TEXT,
        year INTEGER,
        name TEXT,
        count BIGINT,
        amount DOUBLE PRECISION
    );
    """)


    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database and table initialized.")
