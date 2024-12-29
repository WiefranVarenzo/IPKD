import streamlit as st
from streamlit_option_menu import option_menu
import welcome
import data_visualisasi
import perhitungan_ipkd
import grafik_ipkd

st.set_page_config(page_title="Aplikasi IPKD", page_icon="📈")
page_bg = """
<style>
    [data-testid="stAppViewContainer"], [data-testid="stToolbar"], [data-testid="stHeader"] {
        background-color: #fefefe;
    }
    [data-testid="stSidebarContent"] {
        background-color: #2e2e2e;
    }
    button p {
        color: black; 
    }
    h1, h2, h3, h4, h5, p, li {
        color: black;
    }
    .menu-title {
        color: black;
    }
    .container-xxl {
        background-color: black; 
    }

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)


with st.sidebar:
    app = option_menu(
        menu_title="Halaman",
        options=['Welcome', 'Visualisasi Data', 'Perhitungan IPKD', 'Grafik IPKD'],
        menu_icon='file-earmark',
        icons=['house', 'bar-chart', 'coin', 'graph-up'],
        styles={
            "container": {"padding": "5!important", "background-color": "#B17457"},
            "icon": {"color": "white", "font-size": "23px"},
            "nav-link": {"color": "white", "font-size": "18px"},
            "nav-link-selected": {"color": "white", "background-color": "#3B3030"},
            "menu-title": {"color": "white", "font-size": "24px"}
        }
    )
if app == 'Welcome':
    welcome.app()
elif app == 'Visualisasi Data':
    data_visualisasi.app()
elif app == 'Perhitungan IPKD':
    perhitungan_ipkd.app()
elif app == 'Grafik IPKD':
    grafik_ipkd.app()
