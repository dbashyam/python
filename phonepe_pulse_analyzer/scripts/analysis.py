# scripts/analysis.py

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from scripts.queries import QUERY_TOP_STATES_TRANSACTIONS_2023

def analyze_transaction_dynamics():
        engine = create_engine("postgresql+psycopg2://postgres:123@localhost:5432/phonepe")
        df = pd.read_sql_query(QUERY_TOP_STATES_TRANSACTIONS_2023, engine)
        # conn.close()  # Removed because 'conn' is not defined; SQLAlchemy handles connections.

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
        fig.suptitle('Top 10 States - Transaction Dynamics (2023)', fontsize=16)

        # Plot 1: Transaction count
        sns.barplot(data=df, x='state', y='total_transactions', hue='state', palette='Blues_d', legend=False, ax=ax1)
        ax1.set_title('Total Transactions')
        ax1.set_xlabel('State')
        ax1.set_ylabel('Transaction Count')
        ax1.tick_params(axis='x', rotation=45)

        # Plot 2: Transaction amount
        sns.barplot(data=df, x='state', y='total_amount', hue='state', palette='Greens_d', legend=False, ax=ax2)
        ax2.set_title('Total Transaction Amount')
        ax2.set_xlabel('State')
        ax2.set_ylabel('Transaction Value (₹)')
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

        # # Plot total transactions
        # plt.figure(figsize=(12, 6))
        # sns.barplot(data=df, x='state', y='total_transactions', hue='state', palette='Blues_d', legend=False)
        # plt.title('Top 10 States by Transaction Count (2023)')
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.show()
    
        # # Plot total amount
        # plt.figure(figsize=(12, 6))
        # sns.barplot(data=df, x='state', y='total_amount', hue='state', palette='Greens_d', legend=False)
        # plt.title('Top 10 States by Transaction Amount (2023)')
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.show()
