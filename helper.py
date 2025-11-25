import pickle
from preprocessing import preprocess_text

# Load TF-IDF
with open("tfidf_model.pkl", "rb") as f:
    tfidf = pickle.load(f)

# Load Model KNN
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def prediksi_kategori(teks: str):
    """
    Fungsi untuk memprediksi kategori laporan berdasarkan teks input.
    """
    # Preprocess
    clean = preprocess_text(teks)

    # Vectorize
    vec = tfidf.transform([clean])

    # Predict
    hasil = model.predict(vec)[0]

    return hasil
