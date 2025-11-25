import streamlit as st
import pandas as pd
from helper import prediksi_kategori   # ← GANTI DI SINI
import numpy as np
from pathlib import Path
import re
import json

try:
    from streamlit_lottie import st_lottie
    _HAS_LOTTIE = True
except:
    _HAS_LOTTIE = False

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Aplikasi Klasifikasi Kategori Laporan",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# WARNA
# =========================
BG1 = "#FCE7E9"
BG2 = "#E46470"
PRIMARY = "#E46470"
CARD_BG = "#FFFFFF"
TEXT = "#5A1A1F"

# =========================
# CSS GLOBAL
# =========================
st.markdown(f"""
<style>
html, body, .stApp {{
    padding: 0;
    margin: 0;
}}
header {{
    visibility: hidden;
    height: 0px;
}}
.stApp {{
    background: linear-gradient(135deg, {BG1}, {BG2});
}}
[data-testid="stSidebar"] > div:first-child {{
    background-color: {PRIMARY};
    color: white;
}}
[data-testid="stSidebar"] * {{
    color: white !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}}
.card {{
    background: {CARD_BG};
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}}
h1 {{
    color: {PRIMARY} !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    margin-bottom: 4px !important;
}}
h2 {{
    color: {PRIMARY} !important;
    font-size: 24px !important;
}}
.subtitle {{
    color: {TEXT};
    margin-top: -6px;
    font-size: 15px;
}}
.stDownloadButton button {{
    background: {PRIMARY};
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 6px 14px;
}}
.stDownloadButton button:hover {{
    background: #c8505a;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# LOTTIE HERO
# =========================
def load_lottie():
    path = Path("animation.json")
    if _HAS_LOTTIE and path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

lottie_data = load_lottie()

# =========================
# SIDEBAR NAV
# =========================
st.sidebar.markdown("## Menu")
choice = st.sidebar.radio("", ["Home", "Input Data", "Proses", "Hasil"])

# =========================
# HALAMAN HOME
# =========================
if choice == "Home":
    col1, col2 = st.columns([2,1], gap="large")
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown('<h1>🌳 Aplikasi Klasifikasi Kategori Laporan</h1>', unsafe_allow_html=True)
        st.subheader("Prototipe menggunakan KNN + TF-IDF untuk mengklasifikasikan kategori laporan masyarakat.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Selamat Datang 👋")
        st.write("""
        Aplikasi ini digunakan untuk melakukan preprocessing teks
        dan mengklasifikasikan kategori laporan secara otomatis
        menggunakan model Machine Learning (TF-IDF + KNN).
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
        if lottie_data:
            st_lottie(lottie_data, height=200, key="hero")
        else:
            st.markdown(f"<h2 style='color:{PRIMARY};'>Ready ✔</h2>", unsafe_allow_html=True)
            st.markdown("<div style='color:#8a4a52;'>Animasi tidak ditemukan.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# INPUT DATA
# =========================
elif choice == "Input Data":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("📥 Input Data Laporan")
    st.write("Unggah file CSV atau masukkan teks manual.")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        try:
            try:
                df = pd.read_csv(uploaded, on_bad_lines='skip')
            except Exception:
                uploaded.seek(0)
                df = pd.read_csv(uploaded, sep=';', on_bad_lines='skip')
            st.session_state["input_df"] = df
            st.success("File berhasil diunggah!")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error membaca file: {e}")

    st.markdown("---")
    manual = st.text_area("Input manual (satu baris = satu laporan)", height=150)
    if st.button("Simpan Manual"):
        if manual.strip() == "":
            st.warning("Masukkan minimal satu baris teks.")
        else:
            lines = [l for l in manual.splitlines() if l.strip()]
            dfm = pd.DataFrame({"Subjek Laporan": lines})
            st.session_state["input_df"] = dfm
            st.success("Data manual berhasil disimpan!")
            st.dataframe(dfm)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PROSES
# =========================
elif choice == "Proses":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("⚙️ Proses Data Laporan")
    st.subheader("Mulai Proses Klasifikasi")

    if st.button("🚀 Proses Data"):
        if "input_df" not in st.session_state:
            st.warning("⚠ Belum ada data. Silakan upload data di menu Input Data.")
        else:
            try:
                df_proc = st.session_state["input_df"].copy()

                if "Subjek Laporan" not in df_proc.columns:
                    first_col = df_proc.columns[0]
                    df_proc = df_proc.rename(columns={first_col: "Subjek Laporan"})

                df_proc["Subjek Laporan"] = df_proc["Subjek Laporan"].astype(str)

                # 🔥 GANTI: sekarang prediksi kategori
                df_proc["Prediksi Kategori"] = df_proc["Subjek Laporan"].apply(prediksi_kategori)

                st.session_state["prediksi_df"] = df_proc
                st.success("✔ Data berhasil diproses dan diklasifikasikan!")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {e}")

    if "input_df" in st.session_state:
        st.markdown("---")
        st.subheader("Preview Data Input")
        st.dataframe(st.session_state["input_df"], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# HASIL
# =========================
elif choice == "Hasil":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("📊 Hasil Prediksi Kategori")
    st.markdown("<div class='subtitle'>Berikut adalah hasil klasifikasi kategori laporan.</div>", unsafe_allow_html=True)

    if "prediksi_df" not in st.session_state:
        st.warning("⚠ Belum ada hasil. Silakan lakukan *Proses* terlebih dahulu.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        df = st.session_state["prediksi_df"]
        st.success("✔ Prediksi Berhasil Diproses")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Hasil Prediksi",
            data=csv,
            file_name="hasil_prediksi_kategori.csv",
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)
