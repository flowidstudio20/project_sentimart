"""
Preprocessing teks untuk SentiMart.

PENTING: IndoBERT adalah model berbasis konteks kalimat, sehingga input yang
dikirim ke tokenizer HARUS teks yang masih utuh strukturnya (bukan hasil
`preprocess_text` versi TF-IDF yang membuang stopword & tanda baca).
Fungsi `light_normalize` di bawah ini identik dengan yang dipakai pada Cell 6
notebook training (fine-tuning IndoBERT), supaya perilaku model di web app
sama persis dengan saat training/testing.
"""
import re

# Slang tambahan yang dirapikan sebelum masuk ke tokenizer IndoBERT
SLANG_EXTRA = {
    "aing": "aku", "gw": "aku", "gue": "aku",
    "lo": "kamu", "elo": "kamu",
}


def light_normalize(text: str) -> str:
    """Normalisasi ringan sebelum tokenisasi IndoBERT (samakan dengan notebook)."""
    text = str(text)
    # Rapikan huruf yang diulang berlebihan: "BANGETTT" -> "BANGET"
    text = re.sub(r"(.)\1{2,}", r"\1", text)
    words = text.split()
    words = [SLANG_EXTRA.get(w.lower(), w) for w in words]
    return " ".join(words)


# --- Dipakai khusus untuk statistik/EDA di halaman Batch & Beranda ---
STOPWORDS_ID = {
    "yang", "dan", "di", "ke", "dari", "ini", "itu", "dengan", "tidak",
    "ada", "untuk", "juga", "saya", "iya", "ya", "nya", "lah", "kah",
    "pun", "akan", "sudah", "belum", "lebih", "bisa", "kami", "kita",
    "dia", "mereka", "anda", "saja", "banget", "buat", "pada", "tapi",
    "atau", "jadi", "karena", "kalau", "beli", "barang", "sama", "sangat",
}


def basic_clean_for_stats(text: str) -> list[str]:
    """Tokenisasi kasar (huruf saja) untuk keperluan word-frequency di dashboard."""
    words = re.sub(r"[^a-zA-Z\s]", " ", str(text).lower()).split()
    return [w for w in words if w not in STOPWORDS_ID and len(w) > 2]
