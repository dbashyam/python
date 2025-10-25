import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(layout="wide", page_title="Ola July Rides Insights")
st.title("Ola July Rides Insights Dashboard")

# Database connection
@st.cache_resource
def get_conn():
    return psycopg2.connect(
        dbname="ola_ride_insights",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

conn = get_conn()

# Helper to run SQL and return DataFrame
def run_query(query):
    return pd.read_sql_query(query, conn)

# --- Filters ---
df = run_query('SELECT * FROM july_rides')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Date range filter
min_date, max_date = df['Date'].min(), df['Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
if isinstance(date_range, list) and len(date_range) == 2:
    df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]

# Vehicle type filter
vehicle_types = df['Vehicle_Type'].dropna().unique().tolist()
vehicle_type = st.sidebar.multiselect("Vehicle Type", vehicle_types, default=vehicle_types)
df = df[df['Vehicle_Type'].isin(vehicle_type)]

# Booking status filter
statuses = df['Booking_Status'].dropna().unique().tolist()
status = st.sidebar.multiselect("Booking Status", statuses, default=statuses)
df = df[df['Booking_Status'].isin(status)]

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Rides", len(df))
with col2:
    st.metric("Total Revenue", f"₹{df['Booking_Value'].sum():,.2f}")
with col3:
    st.metric("Avg. Driver Rating", f"{df['Driver_Ratings'].mean():.2f}")
with col4:
    st.metric("Avg. Customer Rating", f"{df['Customer_Rating'].mean():.2f}")

# --- Business Insight: Top 5 Pickup Locations ---
st.subheader("Top 5 Pickup Locations")
pickup_df = df.groupby("Pickup_Location").size().reset_index(name="Rides").sort_values("Rides", ascending=False).head(5)
st.bar_chart(pickup_df.set_index("Pickup_Location"))

# --- Business Insight: Booking Status Breakdown ---
st.subheader("Booking Status Breakdown")
status_df = df["Booking_Status"].value_counts().reset_index()
status_df.columns = ["Booking_Status", "Count"]
st.bar_chart(status_df.set_index("Booking_Status"))

# --- Business Insight: Revenue by Payment Method ---
st.subheader("Revenue by Payment Method")
pay_df = df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
st.bar_chart(pay_df.set_index("Payment_Method"))

# --- Business Insight: Canceled Rides Reasons ---
st.subheader("Canceled Rides Reasons")
if "Incomplete_Rides_Reason" in df.columns:
    reason_df = df["Incomplete_Rides_Reason"].value_counts().reset_index()
    reason_df.columns = ["Reason", "Count"]
    st.bar_chart(reason_df.set_index("Reason"))

# --- Show filtered data ---
with st.expander("Show Filtered Data"):
    st.dataframe(df)
# with st.expander("Show Filtered Data"):
#     for idx, row in df.iterrows():
#         st.write(f"**Booking ID:** {row['Booking_ID']}")
#         if 'vehicle images' in df.columns and pd.notna(row['vehicle images']):
#             st.image(row['vehicle images'], width=200)
#         st.write(row)
#         st.markdown("---")

#conn.close()