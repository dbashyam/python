import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# --- Page config
st.set_page_config(layout="wide", page_title="📊 PhonePe Pulse | Business Insights Dashboard")
st.title("📊 PhonePe Pulse: Business Case Study Dashboard")

# --- Sidebar Filters
years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
selected_year = st.sidebar.selectbox("Select Year", years, index=5)

# --- Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="phonepe",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

# --- Tabs for 5 Business Use Cases
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Transaction Dynamics", 
    "📱 Device Engagement", 
    "🛡️ Insurance Insights",
    "🌍 Regional Transactions", 
    "👥 User Registration"
])

# ---------------------- TAB 1: Transaction Dynamics ----------------------
with tab1:
    st.header("Decoding Transaction Dynamics")

    # 1️⃣ Top 10 States by Transaction Count
    query = """
        SELECT state, SUM(count) AS total_transactions
        FROM aggregated_transaction
        WHERE year = %s
        GROUP BY state
        ORDER BY total_transactions DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn, params=(selected_year,))
    st.subheader("1️⃣ Top 10 States by Transaction Count")
    fig = px.bar(df, x='state', y='total_transactions', color='total_transactions')
    st.plotly_chart(fig, use_container_width=True)

    # 2️⃣ Best Performing Payment Categories
    query1 = """
        SELECT name AS transaction_type, SUM(count) AS total_count, SUM(amount) AS total_amount
        FROM aggregated_transaction
        GROUP BY name;
    """
    df1 = pd.read_sql_query(query1, conn)
    st.subheader("2️⃣ Best Performing Payment Categories")
    metric_choice = st.radio("Sort by:", ["Amount", "Count"], horizontal=True)
    if metric_choice == "Amount":
        sorted_df1 = df1.sort_values(by='total_amount', ascending=False)
        fig1 = px.bar(sorted_df1, x='transaction_type', y='total_amount', color='total_amount')
    else:
        sorted_df1 = df1.sort_values(by='total_count', ascending=False)
        fig1 = px.bar(sorted_df1, x='transaction_type', y='total_count', color='total_count')
    st.plotly_chart(fig1, use_container_width=True)

 # 3️⃣ Year-wise Transaction Amount Growth
    query2 = """
        SELECT year, SUM(amount) AS total_amount
        FROM aggregated_transaction
        GROUP BY year
        ORDER BY year;
    """
    df2 = pd.read_sql_query(query2, conn)

    # Ensure year is treated as string for the pie chart
    df2['year'] = df2['year'].astype(str)

    st.subheader("3️⃣ Year-wise Transaction Growth")
    fig2b = px.pie(
        df2,
        values='total_amount',
        names='year',
        title='Transaction Amount Distribution by Year'
    )
    st.plotly_chart(fig2b, use_container_width=True)

    # 4️⃣ Top Transaction Types by Year
    query3 = """
        SELECT year, name AS transaction_type, SUM(amount) AS total_amount
        FROM aggregated_transaction
        GROUP BY year, name
        ORDER BY year, total_amount DESC;
    """
    df3 = pd.read_sql_query(query3, conn)
    st.subheader("4️⃣ Top Transaction Types by Year")

    fig3 = px.bar(
        df3,
        x="year",
        y="total_amount",
        color="transaction_type",
        title="Top Transaction Types Across Years",
        barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 5️⃣ Least Performing States
    query4 = """
        SELECT state, SUM(count) AS total_transactions
        FROM aggregated_transaction
        GROUP BY state
        ORDER BY total_transactions ASC
        LIMIT 10;
    """
    df4 = pd.read_sql_query(query4, conn)
    st.subheader("5️⃣ Least Performing States")
    fig4 = px.bar(df4, x='state', y='total_transactions', color='total_transactions')
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------- TAB 2: Device Engagement ----------------------
with tab2:
    st.header("📱 Device Dominance and User Engagement")

    # 1️⃣ Users by Device Brand (existing)
    query1 = """
        SELECT brand, SUM(count) AS total_users
        FROM aggregated_user
        WHERE year = %s
        GROUP BY brand
        ORDER BY total_users DESC;
    """
    df1 = pd.read_sql_query(query1, conn, params=(selected_year,))
    st.subheader("1️⃣ Users by Device Brand")
    fig1 = px.bar(df1, x='brand', y='total_users', color='total_users', title='Device Brand Usage')
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Brand Market Share for Selected Year
    st.subheader("2️⃣ Brand Market Share (Pie Chart)")
    fig2 = px.pie(df1, values='total_users', names='brand', title=f'Device Brand Market Share - {selected_year}')
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Brand-wise User Growth Over Years
    query3 = """
        SELECT year, brand, SUM(count) AS total_users
        FROM aggregated_user
        GROUP BY year, brand
        ORDER BY year, total_users DESC;
    """
    df3 = pd.read_sql_query(query3, conn)
    st.subheader("3️⃣ Brand-wise User Growth Over Years")
    fig3 = px.line(df3, x="year", y="total_users", color="brand", markers=True,
                   title="Brand-wise User Growth Over the Years")
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Top States Using a Selected Brand
    st.subheader("4️⃣ Top States Using a Selected Brand")
    brand_list = pd.read_sql("SELECT DISTINCT brand FROM aggregated_user ORDER BY brand;", conn)
    selected_brand = st.selectbox("Select Device Brand", brand_list['brand'])
    query4 = """
        SELECT state, SUM(count) AS total_users
        FROM aggregated_user
        WHERE brand = %s AND year = %s
        GROUP BY state
        ORDER BY total_users DESC
        LIMIT 10;
    """
    df4 = pd.read_sql_query(query4, conn, params=(selected_brand, selected_year))
    fig4 = px.bar(df4, x="state", y="total_users", color="total_users",
                  title=f"Top 10 States Using {selected_brand} in {selected_year}")
    st.plotly_chart(fig4, use_container_width=True)

    # Optional download for all aggregated_user data of selected year
    st.download_button("Download Device Engagement Data (CSV)", df1.to_csv(index=False), file_name="device_engagement.csv")

# ---------------------- TAB 3: Insurance Insights ----------------------
with tab3:
    st.header("Insurance Penetration and Growth Potential")

    query = """
        SELECT state, SUM(insured_count) AS total_users, SUM(insured_amount) AS total_amount
        FROM map_insurance
        WHERE year = %s
        GROUP BY state
        ORDER BY total_users DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn, params=(selected_year,))

    st.subheader("Top 10 States by Insurance Users")
    fig = px.bar(df, x='state', y='total_users', color='total_users', title='Insurance User Count by State')
    st.plotly_chart(fig, use_container_width=True)

 # 2️⃣ Top 10 Districts by Insured Amount
    query2 = """
        SELECT district, state, SUM(insured_amount) AS total_amount
        FROM map_insurance
        WHERE year = %s
        GROUP BY state, district
        ORDER BY total_amount DESC
        LIMIT 10;
    """
    df2 = pd.read_sql_query(query2, conn, params=(selected_year,))
    st.subheader("2️⃣ Top 10 Districts by Insured Amount")
    fig2 = px.bar(df2, x='district', y='total_amount', color='state', title='Districts by Insurance Amount')
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Insurance Penetration by State (Pie Chart)
    query3 = """
        SELECT state, SUM(insured_count) AS total_users
        FROM map_insurance
        WHERE year = %s
        GROUP BY state
        ORDER BY total_users DESC;
    """
    df3 = pd.read_sql_query(query3, conn, params=(selected_year,))
    st.subheader("3️⃣ Insurance Market Share by State")
    fig3 = px.pie(df3, values='total_users', names='state', title='State-wise Insurance Market Share')
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Year-over-Year Growth in Insured Amount
    query4 = """
        SELECT year, SUM(insured_amount) AS total_amount
        FROM map_insurance
        GROUP BY year
        ORDER BY year;
    """
    df4 = pd.read_sql_query(query4, conn)
    st.subheader("4️⃣ Insurance Growth Over Years")
    fig4 = px.line(df4, x='year', y='total_amount', markers=True, title='Yearly Insurance Amount Growth')
    st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ States with Highest Average Insurance per User
    query5 = """
        SELECT state,
               SUM(insured_amount) / NULLIF(SUM(insured_count), 0) AS avg_amount_per_user
        FROM map_insurance
        WHERE year = %s
        GROUP BY state
        HAVING SUM(insured_count) > 0
        ORDER BY avg_amount_per_user DESC
        LIMIT 10;
    """
    df5 = pd.read_sql_query(query5, conn, params=(selected_year,))
    st.subheader("5️⃣ Top States by Avg Insurance Amount per User")
    fig5 = px.bar(df5, x='state', y='avg_amount_per_user', color='avg_amount_per_user',
                  title='Average Insurance Amount per User by State')
    st.plotly_chart(fig5, use_container_width=True)

    # 6️⃣ Top Districts for a Selected State
    st.subheader("6️⃣ District-wise Insurance in Selected State")
    state_list = pd.read_sql("SELECT DISTINCT state FROM map_insurance ORDER BY state;", conn)
    selected_state = st.selectbox("Select State", state_list['state'])
    query6 = """
        SELECT district, SUM(insured_amount) AS total_amount, SUM(insured_count) AS total_users
        FROM map_insurance
        WHERE state = %s AND year = %s
        GROUP BY district
        ORDER BY total_amount DESC
        LIMIT 10;
    """
    df6 = pd.read_sql_query(query6, conn, params=(selected_state, selected_year))
    fig6 = px.bar(df6, x='district', y='total_amount', color='total_users',
                  title=f"Top Districts in {selected_state} by Insurance Amount")
    st.plotly_chart(fig6, use_container_width=True)

    st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name="insurance_insights.csv")

    # ---------------------- TAB 4: Regional Transactions ----------------------
    with tab4:
        st.header("Regional Transaction Analysis")

        # 1️⃣ Top Districts by Transaction Count
        query1 = """
            SELECT state, district, SUM(transaction_count) AS total_txn
            FROM map_transaction
            WHERE year = %s
            GROUP BY state, district
            ORDER BY total_txn DESC
            LIMIT 10;
        """
        df1 = pd.read_sql_query(query1, conn, params=(selected_year,))
        st.subheader("1️⃣ Top Districts by Transaction Count")
        fig1 = px.bar(df1, x='district', y='total_txn', color='state', title='Top Districts by Transaction Count')
        st.plotly_chart(fig1, use_container_width=True)

        # 2️⃣ Top Districts by Transaction Amount
        query2 = """
            SELECT state, district, SUM(transaction_amount) AS total_amt
            FROM map_transaction
            WHERE year = %s
            GROUP BY state, district
            ORDER BY total_amt DESC
            LIMIT 10;
        """
        df2 = pd.read_sql_query(query2, conn, params=(selected_year,))
        st.subheader("2️⃣ Top Districts by Transaction Amount")
        fig2 = px.bar(df2, x='district', y='total_amt', color='state', title='Top Districts by Transaction Amount')
        st.plotly_chart(fig2, use_container_width=True)

        # 3️⃣ State-wise Average Transaction Value
        query3 = """
            SELECT state, 
                SUM(transaction_amount) / NULLIF(SUM(transaction_count), 0) AS avg_transaction_value
            FROM map_transaction
            WHERE year = %s
            GROUP BY state
            ORDER BY avg_transaction_value DESC
            LIMIT 10;
        """
        df3 = pd.read_sql_query(query3, conn, params=(selected_year,))
        st.subheader("3️⃣ State-wise Average Transaction Value")
        fig3 = px.bar(df3, x='state', y='avg_transaction_value', color='avg_transaction_value',
                    title='Top States by Avg Transaction Value')
        st.plotly_chart(fig3, use_container_width=True)

        # 4️⃣ Most Active States by Total Transactions
        query4 = """
            SELECT state, SUM(transaction_count) AS total_txn
            FROM map_transaction
            WHERE year = %s
            GROUP BY state
            ORDER BY total_txn DESC
            LIMIT 10;
        """
        df4 = pd.read_sql_query(query4, conn, params=(selected_year,))
        st.subheader("4️⃣ Most Active States by Total Transactions")
        fig4 = px.bar(df4, x='state', y='total_txn', color='total_txn', title='States with Highest Transaction Volume')
        st.plotly_chart(fig4, use_container_width=True)

        # 5️⃣ District Contribution to State Transaction (Pie Chart Example)
        query5 = """
            SELECT district, SUM(transaction_amount) AS total_amt
            FROM map_transaction
            WHERE year = %s AND state = %s
            GROUP BY district
            ORDER BY total_amt DESC
            LIMIT 10;
        """
        state_for_pie = st.selectbox("Select a State to View District-Wise Contribution", df4['state'].unique())
        df5 = pd.read_sql_query(query5, conn, params=(selected_year, state_for_pie))
        st.subheader(f"5️⃣ District-wise Transaction Distribution in {state_for_pie}")
        fig5 = px.pie(df5, values='total_amt', names='district', title=f'District Contribution in {state_for_pie}')
        st.plotly_chart(fig5, use_container_width=True)

        # Download all data
        all_data = pd.concat([df1, df2, df3, df4], axis=1)
        st.download_button("Download All Regional Data (CSV)", all_data.to_csv(index=False), file_name="regional_insights.csv")

# ---------------------- TAB 5: User Registration ----------------------
with tab5:
    st.header("User Registration Trends")

    # 1️⃣ Top Districts by Registered Users
    query1 = """
        SELECT state, district, SUM(registered_users) AS total_users
        FROM map_user
        WHERE year = %s
        GROUP BY state, district
        ORDER BY total_users DESC
        LIMIT 10;
    """
    df1 = pd.read_sql_query(query1, conn, params=(selected_year,))
    st.subheader("1️⃣ Top Districts by Registered Users")
    fig1 = px.bar(df1, x='district', y='total_users', color='state', title='District-wise User Registrations')
    st.plotly_chart(fig1, use_container_width=True)

    # 2️⃣ Top States by Registered Users
    query2 = """
        SELECT state, SUM(registered_users) AS total_users
        FROM map_user
        WHERE year = %s
        GROUP BY state
        ORDER BY total_users DESC
        LIMIT 10;
    """
    df2 = pd.read_sql_query(query2, conn, params=(selected_year,))
    st.subheader("2️⃣ Top States by Registered Users")
    fig2 = px.bar(df2, x='state', y='total_users', color='total_users', title='Top States by Registrations')
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Top Districts by App Opens
    query3 = """
        SELECT state, district, SUM(app_opens) AS total_opens
        FROM map_user
        WHERE year = %s
        GROUP BY state, district
        ORDER BY total_opens DESC
        LIMIT 10;
    """
    df3 = pd.read_sql_query(query3, conn, params=(selected_year,))
    st.subheader("3️⃣ Top Districts by App Opens")
    fig3 = px.bar(df3, x='district', y='total_opens', color='state', title='District-wise App Opens')
    st.plotly_chart(fig3, use_container_width=True)

    # 4️⃣ Top States by App Opens
    query4 = """
        SELECT state, SUM(app_opens) AS total_opens
        FROM map_user
        WHERE year = %s
        GROUP BY state
        ORDER BY total_opens DESC
        LIMIT 10;
    """
    df4 = pd.read_sql_query(query4, conn, params=(selected_year,))
    st.subheader("4️⃣ Top States by App Opens")
    fig4 = px.bar(df4, x='state', y='total_opens', color='total_opens', title='Top States by App Usage')
    st.plotly_chart(fig4, use_container_width=True)

    # 5️⃣ App Engagement Rate (App Opens per User) by State
    query5 = """
        SELECT state, 
               SUM(registered_users) AS total_users,
               SUM(app_opens) AS total_opens,
               ROUND(SUM(app_opens)::decimal / NULLIF(SUM(registered_users), 0), 2) AS opens_per_user
        FROM map_user
        WHERE year = %s
        GROUP BY state
        HAVING SUM(registered_users) > 0
        ORDER BY opens_per_user DESC
        LIMIT 10;
    """
    df5 = pd.read_sql_query(query5, conn, params=(selected_year,))
    st.subheader("5️⃣ Most Engaged States (App Opens per User)")
    fig5 = px.bar(df5, x='state', y='opens_per_user', color='opens_per_user', title='Engagement Rate by State')
    st.plotly_chart(fig5, use_container_width=True)

    # Download button for the main registration dataset
    st.download_button("Download User Registration Data (CSV)", df1.to_csv(index=False), file_name="user_registration.csv")

# --- Close DB connection
conn.close()
