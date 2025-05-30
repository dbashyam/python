import os
import json

def load_aggregated_transaction(conn, data_path_trans):
    cursor = conn.cursor()
    base_path = os.path.join(data_path_trans, "country")

    total_rows_inserted = 0

    for country in os.listdir(base_path):
        country_path = os.path.join(base_path, country)
        if not os.path.isdir(country_path):
            continue

        state_folder_path = os.path.join(country_path, "state")
        if os.path.exists(state_folder_path) and os.path.isdir(state_folder_path):
            for state in os.listdir(state_folder_path):
                state_path = os.path.join(state_folder_path, state)
                if not os.path.isdir(state_path):
                    continue

                for year in os.listdir(state_path):
                    year_path = os.path.join(state_path, year)
                    if not os.path.isdir(year_path):
                        continue

                    rows_to_insert = []

                    for file_name in os.listdir(year_path):
                        if not file_name.endswith(".json"):
                            continue

                        file_path = os.path.join(year_path, file_name)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        transactions = data.get("data", {}).get("transactionData", [])
                        for record in transactions:
                            name = record.get("name")
                            for instrument in record.get("paymentInstruments", []):
                                if instrument.get("type") == "TOTAL":
                                    count = instrument.get("count", 0)
                                    amount = instrument.get("amount", 0.0)

                                    rows_to_insert.append((
                                        country,
                                        state,
                                        int(year),
                                        name,
                                        count,
                                        amount
                                    ))

                    if rows_to_insert:
                        try:
                            insert_query = """
                                INSERT INTO aggregated_transaction
                                (country, state, year, name, count, amount)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """
                            cursor.executemany(insert_query, rows_to_insert)
                            conn.commit()
                            print(f"✅ Committed data for state {state}, year {year}")
                            total_rows_inserted += len(rows_to_insert)
                        except Exception as e:
                            conn.rollback()
                            print(f"❌ Failed to commit data for state {state}, year {year}: {e}")
        else:
            for year in os.listdir(country_path):
                year_path = os.path.join(country_path, year)
                if not os.path.isdir(year_path) or year == "state":
                    continue

                rows_to_insert = []

                for file_name in os.listdir(year_path):
                    if not file_name.endswith(".json"):
                        continue

                    file_path = os.path.join(year_path, file_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    transactions = data.get("data", {}).get("transactionData", [])
                    for record in transactions:
                        name = record.get("name")
                        for instrument in record.get("paymentInstruments", []):
                            if instrument.get("type") == "TOTAL":
                                count = instrument.get("count", 0)
                                amount = instrument.get("amount", 0.0)

                                rows_to_insert.append((
                                    country,
                                    None,
                                    int(year),
                                    name,
                                    count,
                                    amount
                                ))

                if rows_to_insert:
                    try:
                        insert_query = """
                            INSERT INTO aggregated_transaction
                            (country, state, year, name, count, amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.executemany(insert_query, rows_to_insert)
                        conn.commit()
                        print(f"✅ Committed data for country {country}, year {year}")
                        total_rows_inserted += len(rows_to_insert)
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Failed to commit data for country {country}, year {year}: {e}")

    cursor.close()
    print(f"Rows in table now: {total_rows_inserted}")
    print("✅ Aggregated transaction data loaded into PostgreSQL. Total rows inserted:", total_rows_inserted)


def load_aggregated_user(conn, data_path_user):
    cursor = conn.cursor()
    base_path = os.path.join(data_path_user, "country")
    total_rows = 0

    for country in os.listdir(base_path):
        country_path = os.path.join(base_path, country)
        if not os.path.isdir(country_path):
            continue

        state_folder_path = os.path.join(country_path, "state")
        if os.path.exists(state_folder_path):
            for state in os.listdir(state_folder_path):
                state_path = os.path.join(state_folder_path, state)
                if not os.path.isdir(state_path):
                    continue
                for year in os.listdir(state_path):
                    year_path = os.path.join(state_path, year)
                    if not os.path.isdir(year_path):
                        continue

                    rows_to_insert = []

                    for file_name in os.listdir(year_path):
                        if not file_name.endswith(".json"):
                            continue

                        file_path = os.path.join(year_path, file_name)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        users = data.get("data", {}).get("usersByDevice", []) or []
                        for record in users:
                            brand = record.get("brand")
                            count = record.get("count", 0)
                            rows_to_insert.append((country, state, int(year), brand, count))

                    if rows_to_insert:
                        try:
                            cursor.executemany(
                                "INSERT INTO aggregated_user (country, state, year, brand, count) VALUES (%s,%s,%s,%s,%s)",
                                rows_to_insert,
                            )
                            conn.commit()
                            print(f"✅ Inserted aggregated_user data for {state}, year {year}")
                            total_rows += len(rows_to_insert)
                        except Exception as e:
                            conn.rollback()
                            print(f"❌ Error inserting aggregated_user for {state}, year {year}: {e}")
        else:
            for year in os.listdir(country_path):
                year_path = os.path.join(country_path, year)
                if not os.path.isdir(year_path) or year == "state":
                    continue

                rows_to_insert = []

                for file_name in os.listdir(year_path):
                    if not file_name.endswith(".json"):
                        continue

                    file_path = os.path.join(year_path, file_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    users = data.get("data", {}).get("usersByDevice", []) or []
                    for record in users:
                        brand = record.get("brand")
                        count = record.get("count", 0)
                        rows_to_insert.append((country, None, int(year), brand, count))

                if rows_to_insert:
                    try:
                        cursor.executemany(
                            "INSERT INTO aggregated_user (country, state, year, brand, count) VALUES (%s,%s,%s,%s,%s)",
                            rows_to_insert,
                        )
                        conn.commit()
                        print(f"✅ Inserted aggregated_user data for country {country}, year {year}")
                        total_rows += len(rows_to_insert)
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Error inserting aggregated_user for country {country}, year {year}: {e}")

    cursor.close()
    print(f"Total aggregated_user rows inserted: {total_rows}")


def load_aggregated_insurance(conn, data_path_insurance):
    cursor = conn.cursor()
    base_path = os.path.join(data_path_insurance, "country")
    total_rows = 0

    for country in os.listdir(base_path):
        country_path = os.path.join(base_path, country)
        if not os.path.isdir(country_path):
            continue

        state_folder_path = os.path.join(country_path, "state")
        if os.path.exists(state_folder_path):
            for state in os.listdir(state_folder_path):
                state_path = os.path.join(state_folder_path, state)
                if not os.path.isdir(state_path):
                    continue
                for year in os.listdir(state_path):
                    year_path = os.path.join(state_path, year)
                    if not os.path.isdir(year_path):
                        continue

                    rows_to_insert = []

                    for file_name in os.listdir(year_path):
                        if not file_name.endswith(".json"):
                            continue

                        file_path = os.path.join(year_path, file_name)
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        insurance_records = data.get("data", {}).get("transactionData", []) or []
                        for record in insurance_records:
                            name = record.get("name")
                            payment_instruments = record.get("paymentInstruments", []) or []
                            for instrument in payment_instruments:
                                if instrument.get("type") == "TOTAL":
                                    count = instrument.get("count", 0)
                                    amount = instrument.get("amount", 0.0)
                                    rows_to_insert.append((country, state, int(year), name, count, amount))

                    if rows_to_insert:
                        try:
                            cursor.executemany(
                                """INSERT INTO aggregated_insurance
                                (country, state, year, name, count, amount)
                                VALUES (%s,%s,%s,%s,%s,%s)""",
                                rows_to_insert,
                            )
                            conn.commit()
                            print(f"✅ Inserted aggregated_insurance for {state}, year {year}")
                            total_rows += len(rows_to_insert)
                        except Exception as e:
                            conn.rollback()
                            print(f"❌ Error inserting aggregated_insurance for {state}, year {year}: {e}")
        else:
            for year in os.listdir(country_path):
                year_path = os.path.join(country_path, year)
                if not os.path.isdir(year_path) or year == "state":
                    continue

                rows_to_insert = []

                for file_name in os.listdir(year_path):
                    if not file_name.endswith(".json"):
                        continue

                    file_path = os.path.join(year_path, file_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    insurance_records = data.get("data", {}).get("transactionData", []) or []
                    for record in insurance_records:
                        name = record.get("name")
                        payment_instruments = record.get("paymentInstruments", []) or []
                        for instrument in payment_instruments:
                            if instrument.get("type") == "TOTAL":
                                count = instrument.get("count", 0)
                                amount = instrument.get("amount", 0.0)
                                rows_to_insert.append((country, None, int(year), name, count, amount))

                if rows_to_insert:
                    try:
                        cursor.executemany(
                            """INSERT INTO aggregated_insurance
                            (country, state, year, name, count, amount)
                            VALUES (%s,%s,%s,%s,%s,%s)""",
                            rows_to_insert,
                        )
                        conn.commit()
                        print(f"✅ Inserted aggregated_insurance for country {country}, year {year}")
                        total_rows += len(rows_to_insert)
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Error inserting aggregated_insurance for country {country}, year {year}: {e}")

    cursor.close()
    print(f"Total aggregated_insurance rows inserted: {total_rows}")
