from scripts.db import get_postgres_connection, initialize_database
from scripts.load_data import load_aggregated_transaction, load_aggregated_user, load_aggregated_insurance

def main():
    print("Checking repository...")
    # clone repo code here...

    print("Initializing database...")
    initialize_database()

    conn = get_postgres_connection()
    data_path_trans = "data/raw_repo/data/aggregated/transaction"
    data_path_insurance = "data/raw_repo/data/aggregated/insurance"
    data_path_user = "data/raw_repo/data/aggregated/user"

    print("Loading aggregated transaction data...")
    load_aggregated_transaction(conn, data_path_trans)
    print("Loading user data...")
    load_aggregated_user(conn, data_path_user)
    print("Loading insurance data...")
    load_aggregated_insurance(conn, data_path_insurance)

    conn.close()

if __name__ == "__main__":
    main()
