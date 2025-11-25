# preprocessing.py
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

STOPWORDS = set([
    "dan","di","ke","dari","yang","pada","untuk","dengan","oleh","atau","sebagai",
    "adalah","ini","itu","saat","telah","sudah","juga","yg","kpd","dlm","rt","rw"
])

def preprocess_text(text: str) -> str:
    """
    Membersihkan teks:
    - lowercase
    - hapus URL/email/angka/tanda baca
    - stemming (Sastrawi)
    - hapus stopwords sederhana
    """
    if text is None:
        return ""

    t = str(text).lower()

    # hapus URL & email
    t = re.sub(r'http\S+|www\.\S+',' ', t)
    t = re.sub(r'\S+@\S+',' ', t)

    # hapus karakter non alphabet
    t = re.sub(r'[^a-z\s]', ' ', t)

    # collapse spasi
    t = re.sub(r'\s+', ' ', t).strip()

    # stemming
    try:
        t = stemmer.stem(t)
    except:
        pass

    # hapus stopwords
    words = [w for w in t.split() if w not in STOPWORDS and len(w) > 1]

    return " ".join(words)
