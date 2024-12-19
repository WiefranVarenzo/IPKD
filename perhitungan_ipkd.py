import pandas as pd
import streamlit as st
import io
import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import plotly.graph_objects as go
import plotly.express as px

# --- Function to display the weight table ---
def tampilkan_tabel_bobot():
    # Read the weights table from CSV
    df_bobot = pd.read_csv('source/tabelbobot.csv')  # Adjust the file path if necessary

    # Tampilkan tabel di Streamlit
    st.write("### Tabel Bobot untuk Indikator:")
    st.dataframe(df_bobot) # Menambahkan kolom "Bobot" di awal
        # Menambahkan tabel dari file Excel
    tampilkan_tabel_normalisasi()

# --- Function to display the normalization table from the Excel file ---
def tampilkan_tabel_normalisasi():
    # Read the Excel file 'hasil_normalisasi_klusterisasi.xlsx'
    excel_file_path = 'source/hasil_normalisasi_klusterisasi.xlsx'  # Adjust the file path if necessary
    try:
        df_normalisasi = pd.read_excel(excel_file_path)
        st.write("### Tabel Hasil Standarisasi dan Klusterisasi:")
        st.dataframe(df_normalisasi)  # Menampilkan tabel normalisasi
    except FileNotFoundError:
        st.error(f"File '{excel_file_path}' tidak ditemukan. Pastikan file tersebut ada di jalur yang benar.")

# --- Function to split data and calculate IPKD ---
import pandas as pd
import streamlit as st

# --- Function to split data and calculate IPKD --- 
# --- Function to split data and calculate IPKD --- 
def bagi_data_per_kota_kabupaten_dan_tahun(df):
    kota_kabupaten_list = df['KOTA/KABUPATEN'].unique()
    provinsi_list = df['PROVINSI'].unique()

    kota_kabupaten_dfs = {}

    # Calculate minimum and maximum values of numeric columns
    min_values = df.select_dtypes(include='number').min()
    max_values = df.select_dtypes(include='number').max()

    bobot_data = [
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        5, 5, 5, 5, 5, 5, 5, 4, 4, 4,
        4, 4, 4, 4, 4, 4, 4, 3, 3, 3,
        3, 3, 3, 3, 3, 3, 5, 5, 5, 5,
        4, 4, 4, 4, 3, 3, 3, 3, 5, 5,
        5, 4, 4, 3, 3, 3, 3, 4, 4, 4,
        4, 3, 3,
    ]

    kategori = [
        "Kesehatan Balita",
        "Kesehatan Ibu",
        "Pelayanan Kesehatan",
        "Penyakit Tidak Menular",
        "Penyakit Menular",
        "Sanitasi dan Keadaan Lingkungan Hidup"
    ]

    hasil_akhir_df = pd.DataFrame(columns=["Provinsi", "Kota/Kabupaten", "Tahun", "Kesehatan Balita", 
                                           "Kesehatan Ibu", "Pelayanan Kesehatan", 
                                           "Penyakit Tidak Menular", "Penyakit Menular", 
                                           "Sanitasi dan Keadaan Lingkungan Hidup", "Nilai IPKD"])

    for kota_kabupaten in kota_kabupaten_list:
        sub_df = df[df['KOTA/KABUPATEN'] == kota_kabupaten]
        tahun_list = sub_df['TAHUN'].unique()

        for tahun in tahun_list:
            sub_df_tahun = sub_df[sub_df['TAHUN'] == tahun]

            var_name = f"{kota_kabupaten}_{tahun}"
            st.write(f"#### Dataframe untuk {kota_kabupaten} tahun {tahun} (nama variabel: {var_name}):")
            st.dataframe(sub_df_tahun.head())

            numeric_cols = sub_df_tahun.select_dtypes(include='number')

            valid_indices = [i for i, weight in enumerate(bobot_data) if weight > 2]
            filtered_numeric_cols = numeric_cols.iloc[:, valid_indices]

            indikator_df = pd.DataFrame({
                'Nama Indikator': filtered_numeric_cols.columns,
                'Nilai Indikator': filtered_numeric_cols.mean().values,
                'Standard Minimum': min_values[filtered_numeric_cols.columns].values,  # Add standard min
                'Standard Maximum': max_values[filtered_numeric_cols.columns].values,  # Add standard max
            })

            indikator_df['Bobot'] = [bobot_data[i] for i in valid_indices]

            # Calculate Indeks Indikator
            # Adjust the Standard Minimum to 0 if Nilai Indikator is equal to Standard Minimum
            adjusted_min = np.where(
                indikator_df['Nilai Indikator'] == indikator_df['Standard Minimum'], 
                0, 
                indikator_df['Standard Minimum']
            )
            
            # Calculate Indeks Indikator using the adjusted minimum
            indikator_df['Indeks Indikator'] = (indikator_df['Nilai Indikator'] - adjusted_min) / (indikator_df['Standard Maximum'] - adjusted_min)

            
            kategori_labels = []
            for index in range(len(indikator_df)):
                if index <= 35:
                    kategori_labels.append(kategori[0])
                elif index <= 47:
                    kategori_labels.append(kategori[1])
                elif index <= 55:
                    kategori_labels.append(kategori[2])
                elif index <= 59:
                    kategori_labels.append(kategori[3])
                elif index <= 60:
                    kategori_labels.append(kategori[4])
                else:
                    kategori_labels.append(kategori[5])

            indikator_df['Kategori'] = kategori_labels

            # Initialize indeks kelompok per kategori
            indeks_kelompok = {kat: 0 for kat in kategori}
            kategori_total_bobot = indikator_df.groupby('Kategori')['Bobot'].transform('sum')
            indikator_df['Proporsi Bobot'] = indikator_df['Bobot'] / kategori_total_bobot

            # Calculate Indeks Kelompok Indikator
            for kat in kategori:
                if kat in indikator_df['Kategori'].values:
                    indeks_kelompok[kat] = (indikator_df.loc[indikator_df['Kategori'] == kat, 'Indeks Indikator'] * indikator_df.loc[indikator_df['Kategori'] == kat, 'Proporsi Bobot']).sum()

            indikator_df['Indeks Kelompok Indikator'] = indikator_df['Kategori'].map(indeks_kelompok)
            ipkd = sum(indeks_kelompok.values()) / len(kategori)

            st.write(f"##### Tabel Hasil Indikator untuk {kota_kabupaten} tahun {tahun}:")
            st.dataframe(indikator_df)

            st.write(f"**Nilai IPKD untuk {kota_kabupaten} tahun {tahun}: {ipkd:.3f}**")

            indikator_df['Nilai IPKD'] = ipkd
            kota_kabupaten_dfs[var_name] = indikator_df

            provinsi = df.loc[df['KOTA/KABUPATEN'] == kota_kabupaten, 'PROVINSI'].values[0]

            nilai_kategori = [indeks_kelompok[kat] if kat in indeks_kelompok else 0 for kat in kategori]

            baris_baru = pd.DataFrame({
                "Provinsi": [provinsi],
                "Kota/Kabupaten": [kota_kabupaten],
                "Tahun": [tahun],
                **{kategori[i]: [nilai_kategori[i]] for i in range(len(nilai_kategori))},
                "Nilai IPKD": [ipkd],
            })

            hasil_akhir_df = pd.concat([hasil_akhir_df, baris_baru], ignore_index=True)

    st.write("### Tabel Hasil Akhir Semua Kota/Kabupaten dan Tahun:")
    st.dataframe(hasil_akhir_df)

    return kota_kabupaten_dfs, hasil_akhir_df



# --- Function to download data as Excel ---
# --- Function to download data as Excel ---
# --- Function to download data as Excel ---
def download_excel(kota_kabupaten_dfs, hasil_akhir_df):
    output = io.BytesIO()  # Create a buffer for the Excel file

    # Create a new workbook
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for kota_kabupaten, df in kota_kabupaten_dfs.items():
            # Replace '/' in the city/district name with '_' to make it a valid sheet name
            safe_sheet_name = kota_kabupaten.replace('/', '_')[:31]
            df.to_excel(writer, sheet_name=safe_sheet_name, index=False)  # Save each DataFrame to Excel

        # Write the final results to a separate sheet
        hasil_akhir_df.to_excel(writer, sheet_name="Hasil_Akhir", index=False)

    # Get the content from the output buffer
    output.seek(0)

    # Display the download button in Streamlit
    st.download_button(
        label="Download IPKD Results as Excel",
        data=output,
        file_name="ipkd_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



# --- Function to visualize ROV and Confusion Matrix ---
def visualize_results(kota_kabupaten_dfs):
    if "Hasil_Akhir" not in kota_kabupaten_dfs:
        st.warning("Harap melakukan perhitungan IPKD terlebih dahulu!")
        return

    hasil_akhir_df = kota_kabupaten_dfs["Hasil_Akhir"]

    st.write("### Visualisasi Hasil IPKD")

    # Loop melalui setiap baris di hasil_akhir_df
    for index, row in hasil_akhir_df.iterrows():
        kota = row["Kota/Kabupaten"]
        tahun = row["Tahun"]
        ipkd = row["Nilai IPKD"]

        st.write(f"#### {kota} - {tahun}")
        st.write(f"**Nilai IPKD: {ipkd:.3f}**")

        # ROV Visualization
        # Asumsikan ROV adalah Indeks Indikator * Bobot (atau sesuai definisi Anda)
        # Anda bisa menyesuaikan visualisasi sesuai kebutuhan
        st.write("##### Visualisasi Indeks Indikator per Kategori")
        kategori_cols = ["Kesehatan Balita", "Kesehatan Ibu", "Pelayanan Kesehatan", 
                         "Penyakit Tidak Menular", "Penyakit Menular", "Sanitasi dan Keadaan Lingkungan Hidup"]
        nilai_kategori = row[kategori_cols].values

        fig, ax = plt.subplots()
        ax.bar(kategori_cols, nilai_kategori, color='skyblue')
        ax.set_ylim(0, 1)
        ax.set_ylabel('Indeks Kelompok Indikator')
        ax.set_title('Indeks Kelompok Indikator per Kategori')
        st.pyplot(fig)

        # Confusion Matrix Visualization
        st.write("##### Confusion Matrix (Simulasi)")
        # Simulasi true labels
        true_labels = np.random.choice([0, 1], size=len(kategori_cols))
        predicted_labels = (nilai_kategori > 0.5).astype(int)  # Misalnya threshold 0.5

        cm = confusion_matrix(true_labels, predicted_labels)
        cm_display = ConfusionMatrixDisplay(cm, display_labels=["Negatif", "Positif"])
        fig_cm, ax_cm = plt.subplots()
        cm_display.plot(ax=ax_cm, cmap=plt.cm.Blues)
        st.pyplot(fig_cm)

# --- Function to calculate Permutation Importance ---
def calculate_permutation_importance():
    st.write("### Permutation Importance Analysis")
    if 'model' not in st.session_state:
        st.warning("Model belum dimuat. Silakan muat model terlebih dahulu.")
        return

    model = st.session_state['model']
    X = st.session_state['X']
    y = st.session_state['y']

    from sklearn.inspection import permutation_importance

    st.write("Menghitung Permutation Importance...")
    result = permutation_importance(model, X, y, n_repeats=10, random_state=42, n_jobs=-1)

    # Simpan hasil ke session state
    st.session_state['permutation_importance'] = result

    # Tampilkan hasil
    st.write("#### Permutation Importance:")
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': result.importances_mean,
        'Std': result.importances_std
    }).sort_values(by='Importance', ascending=False)

    st.dataframe(importance_df)

    # Visualisasi
    st.write("##### Visualisasi Permutation Importance:")
    fig_pi, ax_pi = plt.subplots(figsize=(10, 8))
    ax_pi.barh(importance_df['Feature'], importance_df['Importance'], xerr=importance_df['Std'])
    ax_pi.set_xlabel('Permutation Importance')
    ax_pi.set_title('Feature Importance')
    plt.gca().invert_yaxis()
    st.pyplot(fig_pi)

# --- Function to load and preprocess data ---
def load_data():
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.upper() for col in df.columns]
        st.session_state['df'] = df
        st.success("Data berhasil diunggah!")
        st.write("### Pratinjau Data:")
        st.dataframe(df.head())
    else:
        st.info("Silakan unggah file CSV Anda.")
def plot_ipkd_results(hasil_akhir_df):
    # Extract unique provinces from the in-memory dataframe
    unique_provinces = hasil_akhir_df['Provinsi'].str.upper().unique()
    
    # Selection box for province
    provinsi = st.selectbox('Pilih Provinsi', unique_provinces, key='provinsi_selectbox')
    
    # Filter cities based on the selected province
    filtered_cities = hasil_akhir_df[hasil_akhir_df['Provinsi'].str.upper() == provinsi]['Kota/Kabupaten'].str.upper().unique()

    # Filter years based on the selected province
    available_years = hasil_akhir_df[hasil_akhir_df['Provinsi'].str.upper() == provinsi]['Tahun'].unique()

    # Selection box for year with available years
    year = st.selectbox('Pilih Tahun', available_years, key='year_selectbox')

    # Selection box for column (health categories + IPKD)
    kolom_list = ['Kesehatan Balita', 'Kesehatan Ibu', 'Pelayanan Kesehatan', 
                  'Penyakit Tidak Menular', 'Penyakit Menular', 'Sanitasi dan Keadaan Lingkungan Hidup', 'Nilai IPKD']
    field = st.selectbox('Pilih Kolom', kolom_list, key='field_selectbox')

    st.subheader(f'Grafik {field} Provinsi {provinsi} Tahun {year}')

    # Filter data for the selected province and year
    data = hasil_akhir_df[(hasil_akhir_df['Kota/Kabupaten'].str.upper().isin(filtered_cities)) & 
                           (hasil_akhir_df['Tahun'] == year)]

    # Get the city names and their corresponding values
    city_names = data['Kota/Kabupaten'].str.upper().tolist()
    values = data[field].tolist()

    colors = [f'rgba({np.random.randint(0, 255)}, {np.random.randint(0, 255)}, {np.random.randint(0, 255)}, 0.8)' for _ in range(len(city_names))]

    # Create the plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=city_names, y=values, name=field, marker=dict(color='blue')))

    # Update layout
    fig.update_layout(
        title=dict(text=f"Perbandingan {field} di Provinsi {provinsi} Tahun {year}", font=dict(color='black', size=20)),
        xaxis_title=dict(text='Kota/Kabupaten', font=dict(color='black', size=14, family="Arial", weight="bold")),
        yaxis_title=dict(text='Nilai', font=dict(color='black', size=14, family="Arial", weight="bold")),
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        font=dict(color='black', weight="bold"),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


# Modify the main app function
def app():
    st.title("Perhitungan IPKD")

    # Load data
    load_data()

    # If data is loaded, display options for calculation and analysis
    if 'df' in st.session_state:
        df = st.session_state['df']

        # Choose action
        task = st.selectbox("Pilih Tindakan:", ["Tampilkan Tabel Bobot", "Hitung IPKD"])

        if task == "Tampilkan Tabel Bobot":
            tampilkan_tabel_bobot()

        elif task == "Hitung IPKD":
            st.write("## Perhitungan IPKD")
            
            # Step 1: Perform the IPKD calculation
            kota_kabupaten_dfs, hasil_akhir_df = bagi_data_per_kota_kabupaten_dan_tahun(df)
            
            # Store the final results in session state
            st.session_state['hasil_akhir_df'] = hasil_akhir_df
            
            # Provide option to download the results as an Excel file
            download_excel(kota_kabupaten_dfs, hasil_akhir_df)

            # Step 3: Plot the line graph for selected province and city
            st.write("## Visualisasi Hasil IPKD")
            plot_ipkd_results(hasil_akhir_df)  # Display the plot directly after the table


# Run the app
if __name__ == '__main__':
    app()
