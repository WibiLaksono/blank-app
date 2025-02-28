import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fungsi untuk koneksi ke database MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",   # Ganti dengan host MySQL kamu
        user="root",        # Ganti dengan user MySQL kamu
        password="",        # Ganti dengan password MySQL kamu
        database="wrpl"  # Ganti dengan nama database kamu
    )

# Fungsi untuk mengambil data dari database
def fetch_data(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Streamlit UI
st.title("Data dari MySQL dalam Tabel dan Chart")
st.write("Menampilkan data dari database MySQL dalam bentuk tabel dan chart")

# Mengambil data dari tabel transaction
transaction_query = "SELECT * FROM transaction"
transaction_df = fetch_data(transaction_query)

# Mengambil data dari tabel listing
listing_query = "SELECT * FROM listing"
listing_df = fetch_data(listing_query)

# Mengambil data dari tabel user
user_query = "SELECT * FROM user"
user_df = fetch_data(user_query)

# Menampilkan tabel transaction
st.subheader("Tabel Transaction")
st.dataframe(transaction_df)

# Menampilkan tabel listing
st.subheader("Tabel Listing")
st.dataframe(listing_df)

# Menampilkan tabel user
st.subheader("Tabel User")
st.dataframe(user_df)

# Mengolah data dan menampilkan chart untuk tabel transaction
st.subheader("Chart untuk Tabel Transaction")
if not transaction_df.empty:
    # Contoh pengolahan data: menghitung jumlah transaksi per bulan
    transaction_df['transaction_date'] = pd.to_datetime(transaction_df['transaction_date'])
    transaction_df['month'] = transaction_df['transaction_date'].dt.to_period('M').astype(str)
    monthly_transactions = transaction_df.groupby('month').size().reset_index(name='count')
    monthly_transactions['month'] = monthly_transactions['month'].astype(str)

    # Menampilkan chart interaktif dengan plotly
    fig = px.bar(monthly_transactions, x='month', y='count', title='Monthly Transactions', labels={'month': 'Month', 'count': 'Number of Transactions'})
    fig.update_layout(xaxis_title='Month', yaxis_title='Number of Transactions')
    st.plotly_chart(fig)
else:
    st.write("Tidak ada data di tabel transaction.")

# Mengolah data dan menampilkan chart garis naik turun penjualan listing berdasarkan condition
st.subheader("Chart Garis Naik Turun Penjualan Listing Berdasarkan Condition")
if not transaction_df.empty and not listing_df.empty:
    # Menggabungkan data transaction dan listing berdasarkan listing_id
    merged_df = pd.merge(transaction_df, listing_df, left_on='listing_id', right_on='id')

    # Menghitung jumlah transaksi per bulan berdasarkan condition
    merged_df['transaction_date'] = pd.to_datetime(merged_df['transaction_date'])
    condition_sales = merged_df.groupby([merged_df['transaction_date'].dt.to_period('M').astype(str), 'condition']).size().unstack(fill_value=0).reset_index()
    condition_sales.rename(columns={'transaction_date': 'month'}, inplace=True)
    condition_sales = merged_df.groupby(['month', 'condition']).size().unstack(fill_value=0).reset_index()

    # Menampilkan chart garis interaktif dengan plotly
    fig = go.Figure()
    for condition in condition_sales.columns[1:]:
        fig.add_trace(go.Scatter(x=condition_sales['month'], y=condition_sales[condition], mode='lines+markers', name=condition))
    fig.update_layout(title='Monthly Sales by Condition', xaxis_title='Month', yaxis_title='Number of Sales')
    st.plotly_chart(fig)
else:
    st.write("Tidak ada data yang cukup untuk menampilkan chart.")
