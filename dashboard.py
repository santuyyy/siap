import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Menyiapkan Dataframe
def create_total_rental_monthly_df(df):
    total_rental_monthly_df = df.groupby(by="mnth")['cnt'].sum().sort_values(ascending=False).reset_index()
    return total_rental_monthly_df

def create_total_rental_seasonly_df(df):
    total_rental_seasonly_df = df.groupby(by="season")['cnt'].sum().sort_values(ascending=False).reset_index()
    return total_rental_seasonly_df

hari_df = pd.read_csv("all_data.csv")

# Membuat Komponen Filter
min_date = pd.to_datetime(hari_df["dteday"]).min()
max_date = pd.to_datetime(hari_df["dteday"]).max()
 
with st.sidebar:
    # Menambahkan logo sepeda
    st.image("https://user-images.githubusercontent.com/43513353/193456323-32986aec-d341-485b-9648-dbd4c6749b38.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hari_df[(hari_df["dteday"] >= str(start_date)) & 
                (hari_df["dteday"] <= str(end_date))]

total_rental_monthly_df = create_total_rental_monthly_df(main_df)
total_rental_seasonly_df = create_total_rental_seasonly_df(main_df)

# Melengkapi Dashboard dengan Visualisasi Data
# Membuat Header Dashboard
st.header('Bike Rental Dashboard')

# Membuat Visualisasi Data Jumlah Casual Users dan Registered Users
st.subheader('Perbandingan Jumlah Pengguna Rental')
col1, col2 = st.columns(2)

with col1:
    casual_users = hari_df['casual'].sum()
    st.metric('Casual Users', value= casual_users)

with col2:
    registered_users = hari_df['registered'].sum()
    st.metric('Registered Users', value= registered_users)

# Menampilkan plot
st.subheader('Visualisasi Perbandingan Jumlah Pengguna Rental')
fig, ax = plt.subplots(figsize=(8, 8))
jenis_pengguna = ['Casual Users', 'Registered Users']
jumlah_pengguna = [casual_users, registered_users]
colors = ['#8B4513', '#FFF8DC']
explode = (0.1, 0)

ax.pie(jumlah_pengguna, labels=jenis_pengguna, autopct='%1.1f%%', colors=colors, explode=explode)
st.pyplot(fig)

# Membuat Visualisasi Data Jumlah Rental Sepeda Berdasarkan Bulan dan Musim
st.subheader('Jumlah Rental Sepeda')
# Berdasarkan Bulan
fig, ax = plt.subplots(figsize=(12, 5))

sns.barplot(x='mnth', y='cnt', data=hari_df, hue='yr')

plt.xlabel("Bulan")
plt.ylabel("Jumlah Rental Sepeda")
plt.title("Jumlah Rental Sepeda pada Tahun 2011 dan 2012")

ax.set_title("Berdasarkan Bulan", loc="center", fontsize=30)
ax.set_ylabel('Jumlah Rental Sepeda')
ax.set_xlabel('Bulan')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Berdasarkan Musim
fig, ax = plt.subplots(figsize=(12, 5))

sns.barplot(x='season', y='cnt', data=hari_df, hue='yr')

plt.xlabel("Musim")
plt.ylabel("Jumlah Rental Sepeda")
plt.title("Jumlah Rental Sepeda pada Tahun 2011 dan 2012")

ax.set_title("Berdasarkan Musim", loc="center", fontsize=30)
ax.set_ylabel('Jumlah Rental Sepeda')
ax.set_xlabel('Musim')
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.caption('Copyright (c) Muhamad Alhadid Fadillah 2023')