import streamlit as st

# Fungsi untuk menambahkan style khusus
def style():
    st.markdown(
        """
        <style>
            img {
                border-radius: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Fungsi utama aplikasi
def app():
    style()

    # Membuat judul untuk halaman utama
    st.title("Selamat Datang di Aplikasi IPKD")

    # Sub-judul halaman
    st.subheader("Panduan Penggunaan Aplikasi")

    # Paragraf pembuka
    st.write("""
        Aplikasi ini dirancang untuk membantu dalam visualisasi data kesehatan, perhitungan Indeks Pembangunan Kesehatan Daerah (IPKD), 
        serta grafik ROV dan confusion matrix untuk analisis lebih lanjut.
        
    """)
    st.write("""
            ### Buku panduan
             Berikut adalah buku panduan, template masukan, serta aturan-aturan penggunaan aplikasi.
    """)
    # Pastikan file "BukuPanduan.pdf" tersedia di direktori proyek
    pdf_file_path = 'source/BukuPanduan.pdf'

    # Fungsi untuk membaca file PDF
    def read_pdf(file_path):
        with open(file_path, "rb") as file:
            pdf_data = file.read()
        return pdf_data

    # Membaca konten file PDF
    pdf_data = read_pdf(pdf_file_path)

    # Menampilkan tombol unduh untuk file PDF
    st.download_button(
        label="Download Buku Panduan",
        data=pdf_data,
        file_name="BukuPanduan.pdf",
        mime="application/pdf"
    )


    # Panduan penggunaan
    st.write("""
        ### 1. Navigasi Halaman
        Di sidebar sebelah kiri, Anda akan melihat menu navigasi yang terdiri dari beberapa halaman:
        - **Welcome**: Halaman ini memberikan gambaran umum dan panduan penggunaan aplikasi.
        - **Data Visualization**: Halaman untuk melihat dan memvisualisasikan data kesehatan yang tersedia.
        - **Perhitungan IPKD**: Halaman untuk melakukan perhitungan IPKD berdasarkan data yang diunggah.
        - **Grafik ROV dan Confusion Matrix**: Halaman untuk menampilkan grafik Range of Values (ROV) dan Confusion Matrix.
    """)

    # Menampilkan gambar info.png
    st.image("src/info.png")

    st.write("""
        ### 2. Menggunakan Data Visualization
        Di halaman ini, Anda bisa melihat visualisasi data kesehatan dalam berbagai bentuk grafik seperti bar chart, line chart, dll.
        Anda juga bisa memfilter data berdasarkan kota atau kabupaten serta tahun.

        ### 3. Menghitung IPKD
        Di halaman ini, Anda bisa melakukan perhitungan IPKD dengan memasukkan data yang relevan.
        Hasil perhitungan akan ditampilkan dalam bentuk tabel dan metrik lainnya.

        ### 4. Grafik IPKD
        Halaman ini digunakan untuk melakukan visualisasi data hasil IPKD yang telah dihitung pada "Perhitungan IPKD".
             
    """)

    # Menambahkan gambar rules2.png
    st.image("src/rules2.png", caption="Panduan Penggunaan Grafik ROV dan Confusion Matrix")

    # Menambahkan informasi tambahan
    st.write("""
        Selain hal diatas, perlu di perhatikan bahwa kolom pada dataset diharuskan sesuai pada panduan, serta pastikan dataset yang akan di visualisasikan sudah clean dan sudah tidak ada data null.
    """)

    st.write("""
        ### 5. Mengunggah Data
        Anda dapat mengunggah file CSV yang berisi data kesehatan untuk dianalisis lebih lanjut. Pastikan format file sesuai dengan template yang diinstruksikan.
    """)

