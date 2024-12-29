import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def app():
    st.title('Aplikasi Visualisasi Data IPKD dan Prevalensi')
    st.header("Bagian 1: Grafik IPKD (Garis dan Batang)")
    st.subheader('Upload File untuk Grafik IPKD')
    
    uploaded_ipkd_file = st.file_uploader("Upload File IPKD (Excel)", type=["xlsx"])
    if uploaded_ipkd_file is not None:
        df_ipkd = pd.read_excel(uploaded_ipkd_file, sheet_name='Hasil_Akhir')
    else:
        df_ipkd = pd.read_excel('source/ipkd_results.xlsx') 
        
    df_ipkd.columns = df_ipkd.columns.str.upper()
    df_ipkd = df_ipkd.applymap(lambda s: s.upper() if type(s) == str else s)
    unique_provinces = df_ipkd['PROVINSI'].unique()

    st.subheader("Grafik Garis: Peningkatan Nilai IPKD Tiap Tahun")
    provinsi = st.selectbox('Pilih Provinsi', unique_provinces, key='provinsi_selectbox')

    filtered_cities = df_ipkd[df_ipkd['PROVINSI'] == provinsi]['KOTA/KABUPATEN'].unique()
    kota = st.selectbox('Pilih Kota/Kabupaten', filtered_cities, key='kota_selectbox')

    kolom_list = ['KESEHATAN BALITA', 'KESEHATAN REPRODUKSI', 'PELAYANAN KESEHATAN', 
                  'PENYAKIT TIDAK MENULAR', 'PENYAKIT MENULAR', 'SANITASI DAN KEADAAN LINGKUNGAN HIDUP']

    field = st.selectbox('Pilih Kolom', kolom_list, key='field_selectbox')
    data = df_ipkd[df_ipkd['KOTA/KABUPATEN'] == kota]
    tahun = data['TAHUN'].astype(str).str[:4].tolist()
    value = data[field].tolist()

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=tahun, y=value, mode='lines+markers', name=field, line=dict(color='red', width=2)))

    fig_line.update_layout(
        title=dict(text=f"Grafik {field} di {kota} ({provinsi})", font=dict(color='black', size=20)),
        xaxis_title=dict(text='Tahun', font=dict(color='black', size=14, family="Arial", weight="bold")),
        yaxis_title=dict(text='Nilai', font=dict(color='black', size=14, family="Arial", weight="bold")),
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        font=dict(color='black', weight="bold"),
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(tickfont=dict(color='black'))
    )

    st.plotly_chart(fig_line)
    st.subheader("Grafik Batang: Perbandingan Nilai IPKD Antar Daerah")

    tahun_select = st.selectbox("Pilih Tahun", sorted(df_ipkd['TAHUN'].unique()), key='tahun_selectbox')
    provinsi_select = st.selectbox("Pilih Provinsi untuk Grafik Batang", unique_provinces, key='provinsi_bar_selectbox')
    data_provinsi_tahun = df_ipkd[(df_ipkd['PROVINSI'] == provinsi_select) & (df_ipkd['TAHUN'] == tahun_select)]

    if not data_provinsi_tahun.empty:
        fig_bar = px.bar(
            data_provinsi_tahun, 
            x='KOTA/KABUPATEN', 
            y='NILAI IPKD', 
            color='NILAI IPKD', 
            title=f"Perbandingan Nilai IPKD di Provinsi {provinsi_select} pada Tahun {tahun_select}",
            labels={'NILAI IPKD': 'Nilai IPKD', 'KOTA/KABUPATEN': 'Kota/Kabupaten'},
            color_continuous_scale='Bluered'
        )

        fig_bar.update_layout(
            title=dict(font=dict(color='black', size=20)),
            coloraxis_colorbar=dict(
                title="Nilai IPKD",
                titlefont=dict(color='black'),
                tickfont=dict(color='black')
            ),
            xaxis_title=dict(text='Kota/Kabupaten', font=dict(color='black', size=14, family="Arial", weight="bold")),
            yaxis_title=dict(text='Nilai IPKD', font=dict(color='black', size=14, family="Arial", weight="bold")),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            font=dict(color='black', weight="bold"),
            xaxis=dict(tickfont=dict(color='black')),
            yaxis=dict(tickfont=dict(color='black'))
        )
        
        st.plotly_chart(fig_bar)
    else:
        st.write("Data tidak ditemukan untuk pilihan tahun dan provinsi tersebut.")
    st.header("Bagian 2: Grafik Persentase atau Prevalensi")
    st.subheader('Upload File untuk Grafik Persentase')
    
    uploaded_percentage_file = st.file_uploader("Upload File Persentase (CSV)", type=["csv"])
    if uploaded_percentage_file is not None:
        df_percentage = pd.read_csv(uploaded_percentage_file)
    else:
        df_percentage = pd.read_csv('source/datasetreal.csv') 
    df_percentage.columns = df_percentage.columns.str.upper()
    df_percentage = df_percentage.applymap(lambda s: s.upper() if type(s) == str else s)

    unique_provinces_percentage = df_percentage['PROVINSI'].unique()
    provinsi_percentage = st.selectbox("Pilih Provinsi untuk Persentase", unique_provinces_percentage)

    filtered_kabupaten = df_percentage[df_percentage['PROVINSI'] == provinsi_percentage]['KOTA/KABUPATEN'].unique()
    kabupaten = st.selectbox("Pilih Kabupaten/Kota", filtered_kabupaten)
    options_for_graph = df_percentage.columns.tolist()
    options_for_graph.remove('PROVINSI')
    options_for_graph.remove('KOTA/KABUPATEN')
    options_for_graph.remove('TAHUN')
    pilihan_grafik = st.selectbox("Pilih Data untuk Ditampilkan", options_for_graph)

    df_filtered = df_percentage[(df_percentage['PROVINSI'] == provinsi_percentage) & (df_percentage['KOTA/KABUPATEN'] == kabupaten)]

    if not df_filtered.empty:
        st.write(f"Menampilkan grafik {pilihan_grafik} untuk {kabupaten}, {provinsi_percentage}")
        fig_prevalensi = px.line(df_filtered, x='TAHUN', y=pilihan_grafik, markers=True)
        fig_prevalensi.update_traces(line=dict(color='red', width=2))
        fig_prevalensi.update_layout(
            title=dict(text=f"Grafik {pilihan_grafik} di {kabupaten} ({provinsi_percentage})", font=dict(color='black', size=20)),
            xaxis_title=dict(text='Tahun', font=dict(color='black', size=14, family="Arial", weight="bold")),
            yaxis_title=dict(text='Nilai (%)', font=dict(color='black', size=14, family="Arial", weight="bold")),
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white',
            font=dict(color='black', weight="bold"),
            xaxis=dict(tickfont=dict(color='black')),
            yaxis=dict(tickfont=dict(color='black'))
        )
        st.plotly_chart(fig_prevalensi)
    else:
        st.write("Data tidak ditemukan untuk pilihan yang dipilih.")

if __name__ == "__main__":
    app()
