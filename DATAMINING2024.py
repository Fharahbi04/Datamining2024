import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
bola = pd.read_excel('OSN Dataset Datmin.xlsx')
data = pd.read_csv('data.csv')

# Title and description
st.title("Dashboard Analisis Data Clustering Menggunakan Metode K-means")
st.write("""
Analisis ini bertujuan untuk mengelompokkan dan mengetahui provinsi dan pulau mana yang sering mendapatkan prestasi terbanyak yaitu berupa medali
""")

# Display the initial dataset
st.header("Dataset OSN")
st.write(bola[['Nama Peserta', 'Provinsi', 'Medali', 'Tahun']])  # Display specific columns

# Sidebar Filters
st.sidebar.header("Filter Data")

# Cluster Selection Filter
cluster_filter = st.sidebar.multiselect(
    "Pilih Cluster",
    options=data["Cluster"].unique(),
    default=data["Cluster"].unique()
)

# Filter data based on cluster selection
filtered_data = data[data["Cluster"].isin(cluster_filter)]

# Display filtered dataset
st.header("Data Hasil Filter Cluster")
st.dataframe(filtered_data[['Nama Peserta', 'Provinsi', 'Medali', 'Cluster']])

# Visualization Options
st.sidebar.header("Visualisasi")
visualization_type = st.sidebar.selectbox(
    "Pilih Tipe Visualisasi",
    ["Scatter Plot", "Bar Chart", "Detail Cluster","Kesimpulan"]
)

# Scatter Plot
if visualization_type == "Scatter Plot":
    st.header("Visualisasi Cluster")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=filtered_data,
        x="Provinsi",
        y="Medali",
        hue="Cluster",
        palette="viridis",
        ax=ax
    )
    plt.title("Scatter Plot Provinsi vs. Medali")
    st.pyplot(fig)

# Bar Chart
elif visualization_type == "Bar Chart":
    st.header("Bar Chart Provinsi dan Medali")
    bar_data = filtered_data.groupby("Cluster")[["Provinsi", "Medali"]].sum().reset_index()

    fig, ax = plt.subplots()
    bar_data.plot(kind="bar", x="Cluster", stacked=True, ax=ax)
    plt.title("Jumlah Provinsi dan Medali per Cluster")
    plt.ylabel("Jumlah")
    plt.xlabel("Cluster")
    st.pyplot(fig)

# Detail Cluster View
elif visualization_type == "Detail Cluster":
    st.sidebar.header("Pilih Detail Cluster")
    cluster_options = data["Cluster"].unique()
    selected_cluster = st.sidebar.selectbox(
        "Pilih Cluster:",
        options=cluster_options,
        index=0
    )

    # Filter data for the selected cluster
    detailed_cluster = data[data["Cluster"] == selected_cluster]

    # Display detailed participants
    st.header(f"Peserta dalam Cluster {selected_cluster}")
    st.write(detailed_cluster[['Nama Peserta', 'Provinsi', 'Medali']])

    # Additional information
    st.write(f"Jumlah peserta dalam Cluster {selected_cluster}: {len(detailed_cluster)}")

#Kesimpulan
elif visualization_type == "Kesimpulan":
    st.title("Kesimpulan")
    st.write("""
             Berdasarkan data yang telah di clusterkan Hasil Terbanyak di Peroleh Oleh cluster 1 yaitu 5-11: 
             DIY,DKI,Gorontalo,Jateng,Jatim,Kalbar dan Lampung. Kemudian Cluster Ini Didapatkan
             Partisipan Terbanyak dan Perolehan Medali Terbanyak dengan 2 Emas,3Perak,dan 4 Perunggu
             """)
