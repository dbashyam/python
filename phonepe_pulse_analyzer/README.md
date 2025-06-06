
# 📊 PhonePe Pulse Data Analysis & Visualization Dashboard

## 🔍 Overview
This project aims to analyze and visualize the **PhonePe Pulse** digital transaction data to extract meaningful business insights. By parsing raw JSON files from PhonePe’s open-source GitHub repository, the project transforms scattered data into structured PostgreSQL tables, enabling deep analytical queries and visual dashboards using **Python** and **Streamlit**.

## 🧠 Problem Statement
With the rapid adoption of digital payment platforms like PhonePe, it is essential to understand:
- **User engagement patterns**
- **Transaction trends**
- **Insurance adoption**
- **Geographic distribution of financial activity**

This project provides a scalable data pipeline and dashboard that businesses can use to:
- Enhance decision-making
- Detect anomalies
- Optimize product offerings
- Drive marketing strategies

## 🚀 Key Features
- 📁 **Automated ETL**: Extracts and transforms PhonePe Pulse JSON data into PostgreSQL tables.
- 🧱 **Normalized Database**: Structured tables for aggregated, top, and map data (user, transaction, insurance).
- 📊 **Data Analysis**: SQL & Python-based queries for trend discovery.
- 🌐 **Interactive Dashboard**: Built with Streamlit for real-time filtering and exploration.
- 📌 **Geographic Insights**: Drill down from national to district and pin-code level.
- 📈 **Business Use Cases**: Segmentation, fraud detection, product development, and more.

## 🧰 Tech Stack

| Layer         | Tools/Technologies                     |
|---------------|----------------------------------------|
| Data Source   | [PhonePe Pulse GitHub Repo](https://github.com/PhonePe/pulse) |
| ETL           | Python (os, json, pandas)              |
| Database      | PostgreSQL                             |
| Visualization | Matplotlib, Seaborn, Plotly            |
| Dashboard     | Streamlit                              |
| Deployment    | Localhost (optional: Streamlit Cloud / Heroku) |

## 🧩 Project Structure
```
phonepe_pulse_analyzer/
|   main.py
|   README.md
|   requirements.txt
|   streamlit_app.py
|   
+---data
|   |   phonepe_pulse.db
|   |   
|   \---raw_repo
|       |   .gitignore
|       |   LICENSE
|       |   README.md
|       |   
|       
+---scripts
|   |   analysis.py
|   |   clone_repo.py
|   |   db.py
|   |   init.py
|   |   init_db.py
|   |   load_data.py
|   |   queries.py
|   |   visualize.py
|   |   
|           
\---sqlqueries
        coordinates.sql
        createtable.sql
        issquery.sql
        sql queries - 1.sql```

## 💼 Business Use Cases
- **📍 Transaction Dynamics**
- **👥 Device Engagement**
- **🛡️ Insurance Analysis**: Track growth in digital insurance.
- **📣 Regional Transactions
- **👥 User Registration**


