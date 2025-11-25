import pandas as pd

# 1. Load dataset
df = pd.read_excel("Data Klasifikasi.xlsx")

# 2. Normalisasi teks ke lowercase
df['Subjek Laporan'] = df['Subjek Laporan'].astype(str).str.lower()

# 3. Fungsi aturan kategori
def tentukan_kategori(text):
    if "tambang" in text or "mining" in text or "peti" in text:
        return "Illegal Mining"
    elif "batas" in text or "tenurial" in text:
        return "Konflik Tenurial"
    elif "perambah" in text or "lahan" in text or "hutan" in text:
        return "Perambahan"
    else:
        return "Lainnya"

# 4. Terapkan aturan ke seluruh dataset
df['Kategori'] = df['Subjek Laporan'].apply(tentukan_kategori)

# 5. Simpan hasil relabel
df.to_excel("Data_Klasifikasi_Baru.xlsx", index=False)

print("Relabeling selesai! File disimpan sebagai Data_Klasifikasi_Baru.xlsx")
