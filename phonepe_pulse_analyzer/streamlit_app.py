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

    query = """
        SELECT state, SUM(count) AS total_transactions
        FROM aggregated_transaction
        WHERE year = %s
        GROUP BY state
        ORDER BY total_transactions DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn, params=(selected_year,))

    st.subheader("Top 10 States by Transaction Count")
    fig = px.bar(df, x='state', y='total_transactions', color='total_transactions', title='State-wise Transactions')
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name="transaction_dynamics.csv")

# ---------------------- TAB 2: Device Engagement ----------------------
with tab2:
    st.header("Device Dominance and User Engagement")

    query = """
        SELECT brand, SUM(count) AS total_users
        FROM aggregated_user
        WHERE year = %s
        GROUP BY brand
        ORDER BY total_users DESC;
    """
    df = pd.read_sql_query(query, conn, params=(selected_year,))

    st.subheader("Users by Device Brand")
    fig = px.bar(df, x='brand', y='total_users', color='total_users', title='Device Brand Usage')
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name="device_engagement.csv")

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

    st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name="insurance_insights.csv")

# ---------------------- TAB 4: Regional Transactions ----------------------
with tab4:
    st.header("Regional Transaction Analysis")

    query = """
        SELECT state, district, SUM(transaction_count) AS total_txn, SUM(transaction_amount) AS total_amt
        FROM map_transaction
        WHERE year = %s
        GROUP BY state, district
        ORDER BY total_txn DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn, params=(selected_year,))

    st.subheader("Top Districts by Transaction Count")
    fig = px.bar(df, x='district', y='total_txn', color='state', title='District-wise Transactions')
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name="regional_transactions.csv")

# ---------------------- TAB 5: User Registration ----------------------
with tab5:
    st.header("User Registration Trends")

    query = """
        SELECT state, district, SUM(registered_users) AS total_users
        FROM map_user
        WHERE year = %s
        GROUP BY state, district
        ORDER BY total_users DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn, params=(selected_year,))

    st.subheader("Top Districts by Registered Users")
    fig = px.bar(df, x='district', y='total_users', color='state', title='District-wise User Registrations')
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name="user_registration.csv")

# --- Close DB connection
conn.close()
