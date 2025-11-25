import pickle
from preprocessing import preprocess_text

# ==============================
# LOAD TF-IDF & MODEL
# ==============================
with open("tfidf_model.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("model.pkl", "rb") as f:   # ← sesuai yang kamu bilang
    model = pickle.load(f)

# ==============================
# MODE INTERAKTIF PREDIKSI
# ==============================
teks = input("Masukkan teks laporan: ")

# Preprocess teks
clean = preprocess_text(teks)

# Vectorize
vec = tfidf.transform([clean])

# Predict
hasil = model.predict(vec)[0]

print("\n=== HASIL KLASIFIKASI ===")
print("Teks :", teks)
print("Kategori Prediksi :", hasil)
