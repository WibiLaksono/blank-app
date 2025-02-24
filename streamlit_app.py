import streamlit as st
import mysql.connector
import pandas as pd

# Fungsi untuk koneksi ke database MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",   # Ganti dengan host MySQL kamu
        user="root",        # Ganti dengan user MySQL kamu
        password="",        # Ganti dengan password MySQL kamu
        database="wrpl"  # Ganti dengan nama database kamu
    )

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Ganti dengan query yang sesuai dengan tabelmu
    cursor.execute("SELECT id, first_name, last_name, email FROM user")  
    data = cursor.fetchall()

    # Ambil nama kolom dari deskripsi cursor
    columns = [col[0] for col in cursor.description]

    cursor.close()
    conn.close()

    # Mengubah hasil query menjadi DataFrame pandas
    return pd.DataFrame(data, columns=columns)

# Streamlit UI
st.title("Data dari MySQL dalam Tabel")
st.write("Menampilkan data dari database MySQL dalam bentuk tabel")

# Mengambil data
df = fetch_data()

# Menampilkan tabel
st.dataframe(df)  # Tabel dengan fitur scroll dan sort

# Jika ingin tabel lebih statis tanpa fitur sort, gunakan:
# st.table(df)
