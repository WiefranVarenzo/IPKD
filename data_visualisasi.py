import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

def app():
    @st.cache_resource
    def load_model():
        try:
            return joblib.load('voting_classifier_model.pkl')
        except Exception as e:
            st.error(f"Error loading the model: {e}")
            return None

    @st.cache_data
    def load_data(file):
        data = pd.read_excel(file)
        data['Tahun'] = data['Tahun'].astype(str)
        data.columns = [col.title() for col in data.columns]
        return data

    st.title("Visualisasi Data")
    
    uploaded_file = st.file_uploader("Silahkan Upload file Excel", type=['xlsx'])
    if uploaded_file is not None:
        data = load_data(uploaded_file)
    else:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "source/kota_kabupaten.xlsx")
        data = load_data(file_path)
        
    st.write("Kolom pada dataset:", data.columns) 
    
    if 'Provinsi' not in data.columns:
        st.error("Column 'Provinsi' not found in the data!")
        return

    regions = data['Provinsi'].unique()
    region = st.selectbox("Pilih Wilayah", regions)
    region_data = data[data['Provinsi'] == region]

    def customize_layout(fig):
        fig.update_layout(
            title=dict(font=dict(color='black', size=20)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            xaxis_title=dict(font=dict(color='black')),
            yaxis_title=dict(font=dict(color='black')),
            xaxis=dict(tickfont=dict(color='black')),
            yaxis=dict(tickfont=dict(color='black')),
            legend=dict(
                title=dict(text='Kota/Kabupaten', font=dict(color='black')),
                font=dict(color='black')
            )
        )
        return fig

    st.markdown("<style>div.row-widget.stSelectbox { color: black; }</style>", unsafe_allow_html=True)

    if 'Jumlah Penduduk L + P' in region_data.columns:
        st.subheader(f"Jumlah Penduduk di {region}")
        fig_population = px.line(region_data, x='Tahun', y='Jumlah Penduduk L + P', color='Kota/Kabupaten',
                                title=f"Total Population in {region} over the years")
        st.plotly_chart(customize_layout(fig_population))

    if 'Jumlah Rumah Tangga' in region_data.columns:
        st.subheader(f"Jumlah Rumah Tangga di {region}")
        fig_households = px.line(region_data, x='Tahun', y='Jumlah Rumah Tangga', color='Kota/Kabupaten',
                                title=f"Number of Households in {region} over the years")
        st.plotly_chart(customize_layout(fig_households))

    if 'Luas Wilayah (Km2)' in region_data.columns and 'Jumlah Penduduk L + P' in region_data.columns:
        st.subheader(f"Persebaran Data di {region}")
        fig_scatter = px.scatter(region_data, x='Luas Wilayah (Km2)', y='Jumlah Penduduk L + P', color='Kota/Kabupaten',
                                size='Jumlah Penduduk L + P', title=f"Persebaran Data di {region} (Luas Wilayah vs Jumlah Penduduk)")
        st.plotly_chart(customize_layout(fig_scatter))

    if 'Jumlah Penduduk L + P' in region_data.columns:
        st.subheader(f"Pertumbuhan Persentase Jumlah Penduduk di {region}")
        region_data['Growth_Population'] = region_data.groupby('Kota/Kabupaten')['Jumlah Penduduk L + P'].pct_change() * 100
        fig_growth = px.line(region_data, x='Tahun', y='Growth_Population', color='Kota/Kabupaten',
                            title=f"Pertumbuhan Persentase Jumlah Penduduk di {region} per Tahun")
        st.plotly_chart(customize_layout(fig_growth))

    if 'Jumlah Penduduk L + P' in region_data.columns and 'Luas Wilayah (Km2)' in region_data.columns:
        st.subheader(f"Kepadatan Penduduk di {region}")
        region_data['Population_Density'] = region_data['Jumlah Penduduk L + P'] / region_data['Luas Wilayah (Km2)']
        fig_density = px.bar(region_data, x='Kota/Kabupaten', y='Population_Density', color='Kota/Kabupaten',
                             title=f"Kepadatan Penduduk di {region} (per km²)")
        st.plotly_chart(customize_layout(fig_density))

    if 'Jumlah Rumah Tangga' in region_data.columns and 'Jumlah Penduduk L + P' in region_data.columns:
        st.subheader(f"Rasio Rumah Tangga terhadap Jumlah Penduduk di {region}")
        region_data['Household_Population_Ratio'] = region_data['Jumlah Rumah Tangga'] / region_data['Jumlah Penduduk L + P']
        fig_household_ratio = px.line(region_data, x='Tahun', y='Household_Population_Ratio', color='Kota/Kabupaten',
                                      title=f"Rasio Rumah Tangga terhadap Jumlah Penduduk di {region}")
        st.plotly_chart(customize_layout(fig_household_ratio))

    st.subheader(f"Distrik di {region}")
    districts = region_data['Kota/Kabupaten'].unique()
    selected_district = st.selectbox("Pilih Distrik untuk melihat detail", districts)

    if selected_district:
        district_data = region_data[region_data['Kota/Kabupaten'] == selected_district].iloc[-1]
        st.markdown(f"<span style='color: black;'>Luas Wilayah {selected_district}: {district_data['Luas Wilayah (Km2)']} km²</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: black;'>Jumlah Desa: {district_data['Desa']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: black;'>Jumlah Kelurahan: {district_data['Kelurahan']}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: black;'>Total Desa dan Kelurahan: {district_data['Desa + Kelurahan']}</span>", unsafe_allow_html=True)

if __name__ == "__main__":
    app()
