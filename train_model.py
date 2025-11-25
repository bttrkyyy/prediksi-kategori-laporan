import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from preprocessing import preprocess_text

# ==========================
# LOAD DATASET
# ==========================
df = pd.read_csv("dataset_clean.csv")

X_raw = df["Subjek Laporan"].astype(str)
y = df["Kategori"]

# Preprocess
X_clean = X_raw.apply(preprocess_text)

# Load TF-IDF
with open("tfidf_model.pkl", "rb") as f:
    tfidf = pickle.load(f)

X_tfidf = tfidf.transform(X_clean)

# ==========================
# SPLIT DATA
# ==========================
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# ==========================
# TRAIN MODEL
# ==========================
model = LinearSVC()
model.fit(X_train, y_train)

# ==========================
# SAVE MODEL
# ==========================
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model selesai dilatih!")
print("Akurasi training :", model.score(X_train, y_train))
print("Akurasi testing  :", model.score(X_test, y_test))
