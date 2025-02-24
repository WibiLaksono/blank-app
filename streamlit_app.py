import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

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
    transaction_df['month'] = transaction_df['transaction_date'].dt.to_period('M')
    monthly_transactions = transaction_df.groupby('month').size()

    # Menampilkan chart
    fig, ax = plt.subplots()
    monthly_transactions.plot(kind='bar', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Transactions")
    ax.set_title("Monthly Transactions")
    st.pyplot(fig)
else:
    st.write("Tidak ada data di tabel transaction.")
