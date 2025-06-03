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

def load_map_user(conn, base_path):
    cursor = conn.cursor()
    base_path = os.path.join(base_path, "country", "india", "state")
    for state in os.listdir(base_path):
        for year in os.listdir(os.path.join(base_path, state)):
            year_path = os.path.join(base_path, state, year)
            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue
                with open(os.path.join(year_path, file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                hover_data = data.get("data", {}).get("hoverData", {}) or []
                rows = [
                    ("India", state, district, int(year), stats.get("registeredUsers", 0), stats.get("appOpens", 0))
                    for district, stats in hover_data.items()
                ]
                if rows:
                    try:
                        cursor.executemany("""
                            INSERT INTO map_user (country, state, district, year, registered_users, app_opens)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, rows)
                        conn.commit()
                        print(f"✅ map_user data for {state} {year}")
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Error loading map_user for {state} {year}: {e}")
    cursor.close()

def load_map_transaction(conn, base_path):
    cursor = conn.cursor()
    base_path = os.path.join(base_path, "country", "india", "state")
    for state in os.listdir(base_path):
        for year in os.listdir(os.path.join(base_path, state)):
            year_path = os.path.join(base_path, state, year)
            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue
                with open(os.path.join(year_path, file), "r", encoding="utf-8") as f:
                    data = json.load(f)
                hover_data_list = data.get("data", {}).get("hoverDataList", []) or []
                rows = [
                    ("India", state, item.get("name"), int(year), item.get("metric", [{}])[0].get("count", 0), item.get("metric", [{}])[0].get("amount", 0.0))
                    for item in hover_data_list
                ]
                if rows:
                    try:
                        cursor.executemany("""
                            INSERT INTO map_transaction (country, state, district, year, transaction_count, transaction_amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, rows)
                        conn.commit()
                        print(f"✅ map_transaction data for {state} {year}")
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Error loading map_transaction for {state} {year}: {e}")
    cursor.close()

def load_map_insurance(conn, base_path):
    cursor = conn.cursor()
    base_path = os.path.join(base_path, "country", "india", "state")
    print(f"📂 Scanning path: {base_path}")

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue

                file_path = os.path.join(year_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                hover_list = data.get("data", {}).get("hoverDataList", [])
                rows = []

                for item in hover_list:
                    district = item.get("name")
                    metric = item.get("metric", [{}])[0]
                    count = metric.get("count", 0)
                    amount = metric.get("amount", 0.0)

                    rows.append((
                        "India", state, district, int(year),
                        count, amount
                    ))

                if rows:
                    try:
                        cursor.executemany("""
                            INSERT INTO map_insurance
                            (country, state, district, year, insured_count, insured_amount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, rows)
                        conn.commit()
                        print(f"✅ map_insurance data loaded for {state} {year}")
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Failed map_insurance insert for {state}, year {year}: {e}")

    cursor.close()

def load_top_user(conn, base_path):
    import os, json
    cursor = conn.cursor()
    base_path = os.path.join(base_path, "country", "india", "state")

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue

                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for category in ['states', 'districts', 'pincodes']:
                    records = data.get("data", {}).get(category) or []
                    rows = []

                    for entry in records:
                        name = entry.get("name")
                        count = entry.get("registeredUsers", 0)
                        percentage = entry.get("percentage", 0.0)  # May not be present

                        rows.append((
                            "India", state, int(year), quarter, category[:-1], name, count, percentage
                        ))

                    if rows:
                        try:
                            cursor.executemany("""
                                INSERT INTO top_user (country, state, year, quarter, type, entity_name, count, percentage)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, rows)
                            conn.commit()
                            print(f"✅ top_user data inserted for {state}, {year} Q{quarter}")
                        except Exception as e:
                            conn.rollback()
                            print(f"❌ Error inserting top_user for {state}, {year} Q{quarter}: {e}")

    cursor.close()


def load_top_map(conn, base_path):
    import os, json
    cursor = conn.cursor()
    base_path = os.path.join(base_path, "country", "india", "state")

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue
            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue
                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                rows = []
                for category in ["states", "districts", "pincodes"]:
                    records = data.get("data", {}).get(category, []) or []
                    for record in records:
                        name = record.get("entityName")
                        metric = record.get("metric", {})
                        count = metric.get("count", 0)
                        amount = metric.get("amount", 0.0)
                        rows.append((
                            "India", state, int(year), quarter, category[:-1], name, count, amount
                        ))

                if rows:
                    try:
                        cursor.executemany("""
                            INSERT INTO top_map (country, state, year, quarter, type, entity_name, count, amount)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, rows)
                        conn.commit()
                        print(f"✅ top_map data inserted for {state}, {year} Q{quarter}")
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Failed top_map insert for {state}, {year} Q{quarter}: {e}")
    cursor.close()

def load_top_insurance(conn, base_path):
    import os, json
    cursor = conn.cursor()
    base_path = os.path.join(base_path, "country", "india", "state")

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if not os.path.isdir(year_path):
                continue

            for file in os.listdir(year_path):
                if not file.endswith(".json"):
                    continue

                quarter = int(file.replace(".json", ""))
                file_path = os.path.join(year_path, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                rows = []
                for category in ["states", "districts", "pincodes"]:
                    records = data.get("data", {}).get(category) or []
                    for record in records:
                        name = record.get("entityName")
                        metric = record.get("metric", {})
                        count = metric.get("count", 0)
                        amount = metric.get("amount", 0.0)
                        rows.append((
                            "India", state, int(year), quarter, category[:-1],
                            name, count, amount
                        ))

                if rows:
                    try:
                        cursor.executemany("""
                            INSERT INTO top_insurance (country, state, year, quarter, type, entity_name, count, amount)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, rows)
                        conn.commit()
                        print(f"✅ top_insurance data inserted for {state}, {year} Q{quarter}")
                    except Exception as e:
                        conn.rollback()
                        print(f"❌ Failed top_insurance insert for {state}, {year} Q{quarter}: {e}")
    cursor.close()

