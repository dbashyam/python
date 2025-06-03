from scripts.db import get_postgres_connection, initialize_database
from scripts.load_data import ( 
    load_aggregated_transaction, 
    load_aggregated_user, 
    load_aggregated_insurance,
    load_map_user,
    load_map_transaction,
    load_map_insurance,
    load_top_user,
    load_top_map,
    load_top_insurance
)
from scripts.analysis import analyze_transaction_dynamics


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
    print("Loading map user data...")
    load_map_user(conn, "data/raw_repo/data/map/user/hover")
    print("Loading map_transaction data...")
    load_map_transaction(conn, "data/raw_repo/data/map/transaction/hover")
    print("Loading map_insurance data...")
    load_map_insurance(conn, "data/raw_repo/data/map/insurance/hover")
    print("Loading top_user data...")
    load_top_user(conn, "data/raw_repo/data/top/user")
    print("Loading top_map data...")
    load_top_map(conn, "data/raw_repo/data/top/transaction")
    print("Loading top_insurance data...")
    load_top_insurance(conn, "data/raw_repo/data/top/insurance")

    conn.close()
    print("Data loading complete. Starting analysis...")
    print("\n📊 Running analysis: Transaction Dynamics")
    analyze_transaction_dynamics()

if __name__ == "__main__":
    main()
