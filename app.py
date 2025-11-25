# app.py
import streamlit as st
import pandas as pd
from helper import prediksi_kategori
import matplotlib.pyplot as plt

# =========================
# Setup halaman & icon
# =========================
st.set_page_config(
    page_title="Prediksi Kategori Laporan Kehutanan",
    page_icon="🌲",
    layout="wide"
)

# =========================
# Custom CSS untuk cream/coklat aesthetic
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fdf6e3, #f5e0c3);
}
.card {
    background-color: #fff8f0;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}
.stButton>button {
    background-color: #a67853;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 8px;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #8b5e3c;
}
.dataframe tbody tr:hover {
    background-color: #f0e6da;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div style="text-align: center; padding: 25px;">
<h1 style="color: #8b5e3c;">🌲 Prediksi Kategori Laporan Kehutanan</h1>
<p style="color: #5c4033; font-size: 16px;">Masukkan subjek laporan atau upload file untuk mendapatkan kategori otomatis</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Fungsi baca file aman
# =========================
def read_file(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file)
            except:
                try:
                    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8', engine='python')
                except:
                    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8-sig', engine='python')
        else:
            try:
                df = pd.read_excel(uploaded_file, sheet_name=0)
            except:
                st.error("Gagal membaca Excel. Pastikan file tidak corrupt dan sheet ada isinya.")
                return None

        if df.empty or len(df.columns) == 0:
            st.error("File kosong atau tidak memiliki kolom. Pastikan file benar.")
            return None

        cols_lower = [c.lower().strip() for c in df.columns]
        if 'subjek laporan' in cols_lower:
            col_index = cols_lower.index('subjek laporan')
            df = df.iloc[:, [col_index]]
            df.columns = ['Subjek Laporan']
        else:
            st.error("File harus memiliki kolom 'Subjek Laporan'.")
            return None

        df.dropna(subset=['Subjek Laporan'], inplace=True)
        df['Subjek Laporan'] = df['Subjek Laporan'].astype(str)
        if df.empty:
            st.error("Tidak ada data valid untuk diprediksi.")
            return None

        return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        return None

# =========================
# Layout dua kolom
# =========================
col1, col2 = st.columns([1, 1])

# ======= Kolom 1: Prediksi Satu Laporan =======
with col1:
    st.subheader("Prediksi Satu Laporan")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    teks_input = st.text_area("Masukkan Subjek Laporan:", height=180)
    if st.button("Prediksi Kategori Laporan", key="btn_satu"):
        if teks_input.strip() == "":
            st.warning("Tolong masukkan teks laporan terlebih dahulu!")
        else:
            kategori = prediksi_kategori(teks_input)
            st.success(f"🌲 Kategori yang diprediksi: **{kategori}**")
    st.markdown('</div>', unsafe_allow_html=True)

# ======= Kolom 2: Prediksi Banyak Laporan (Interaktif) =======
with col2:
    st.subheader("Prediksi Banyak Laporan (Excel / CSV)")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload file Excel/CSV", type=["xlsx", "csv"], key="uploader")

    if uploaded_file is not None:
        df = read_file(uploaded_file)
        if df is not None:
            st.success(f"File berhasil dibersihkan! Jumlah baris valid: {len(df)}")
            
            # Prediksi kategori
            df['Kategori Prediksi'] = df['Subjek Laporan'].apply(prediksi_kategori)

            # Pilihan filter kategori dengan tooltip penjelas
            kategori_unique = df['Kategori Prediksi'].unique().tolist()
            selected_kategori = st.multiselect(
                "Filter kategori untuk ditampilkan:",
                options=kategori_unique,
                default=kategori_unique
            )
            st.caption("💡 Tips: Pilih kategori untuk menampilkan hanya kategori tersebut. Jika tidak memilih apapun, semua kategori akan ditampilkan.")

            df_filtered = df[df['Kategori Prediksi'].isin(selected_kategori)]

            # Highlight kategori
            color_map = {
                "Illegal Mining": "#f8d7da",
                "Perambahan Lahan": "#fff3cd",
                "Konflik Tenurial": "#d1ecf1",
                "Perambahan Hutan": "#f5e0c3"
            }
            def highlight_category(row):
                return [f"background-color: {color_map.get(row['Kategori Prediksi'], '')}"]*len(row)

            st.markdown("### Tabel Hasil Prediksi")
            st.dataframe(df_filtered.style.apply(highlight_category, axis=1), use_container_width=True)

            # ====== Visualisasi summary ======
            st.markdown("### Ringkasan Kategori Laporan")
            kategori_count = df_filtered['Kategori Prediksi'].value_counts()
            
            # Bar chart
            st.bar_chart(kategori_count)

            # Pie chart
            fig, ax = plt.subplots()
            ax.pie(kategori_count, labels=kategori_count.index, autopct='%1.1f%%', startangle=90,
                   colors=[color_map.get(k,'#ccc') for k in kategori_count.index])
            ax.axis('equal')
            st.pyplot(fig)

            # Tombol download CSV
            csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Unduh Hasil Prediksi Filtered CSV",
                data=csv,
                file_name='hasil_prediksi_filtered.csv',
                mime='text/csv'
            )
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("<hr><p style='text-align: center; color: #5c4033;'>© 2025 Prediksi Kategori Laporan Kehutanan</p>", unsafe_allow_html=True)
