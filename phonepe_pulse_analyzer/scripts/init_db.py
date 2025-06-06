from scripts.db import get_postgres_connection

def initialize_database():
    conn = get_postgres_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Aggregated_transaction (
            state VARCHAR(100),
            year VARCHAR(10),
            name VARCHAR(100),
            type VARCHAR(50),
            count BIGINT,
            amount DOUBLE PRECISION
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("Database and table initialized.")
