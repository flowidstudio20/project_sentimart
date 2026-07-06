"""
Loader model IndoBERT untuk SentiMart.

Model hasil fine-tuning (dari notebook, cell 6: `trainer.save_model(...)`)
diharapkan berada di folder `model/indobert_sentiment_final/` pada root
project ini. Struktur folder tersebut biasanya berisi:
    config.json, model.safetensors (atau pytorch_model.bin),
    tokenizer_config.json, vocab.txt, special_tokens_map.json

Cara mengisi folder ini:
    1. Di notebook (Kaggle/Colab), setelah training selesai, download folder
       './indobert_sentiment_final/' (klik kanan -> Download, atau zip dulu).
    2. Extract ke: sentimart/model/indobert_sentiment_final/

Jika model belum ada, app tetap bisa dijalankan dalam MODE DEMO (prediksi
dummy berbasis kata kunci) supaya wireframe & alur UI tetap bisa dicek.
"""
import os
import numpy as np
import streamlit as st

# Opsi 1: Muat model lokal dari folder proyek Anda (default)
# MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "indobert_sentiment_final")

# Opsi 2: Hubungkan langsung ke repositori model Hugging Face Anda
MODEL_DIR = "flowidstudio/sentimart"

MAX_LENGTH = 128
LABEL_MAP = {0: "Negative", 1: "Positive"}


def model_is_available() -> bool:
    # Jika MODEL_DIR adalah path lokal, cek keberadaannya
    if os.path.exists(MODEL_DIR) and os.path.isdir(MODEL_DIR):
        return any(f.startswith("config.json") for f in os.listdir(MODEL_DIR))
    # Jika MODEL_DIR merujuk ke model hub Hugging Face (mengandung / dan bukan folder lokal)
    if isinstance(MODEL_DIR, str) and "/" in MODEL_DIR:
        return True
    return False


def get_model_debug_info() -> dict:
    """Info diagnostik untuk membantu cari tahu kenapa model tidak terdeteksi di deployment."""
    if isinstance(MODEL_DIR, str) and "/" in MODEL_DIR and not os.path.isdir(MODEL_DIR):
        return {
            "expected_model_dir": MODEL_DIR,
            "model_root_exists": False,
            "model_dir_exists": False,
            "files_in_model_root": [],
            "files_in_model_dir": [],
            "suspicious_small_files": [],
            "note": "Menggunakan model dari Hugging Face Hub."
        }
    model_root = os.path.dirname(MODEL_DIR)
    info = {
        "expected_model_dir": MODEL_DIR,
        "model_root_exists": os.path.isdir(model_root),
        "model_dir_exists": os.path.isdir(MODEL_DIR),
        "files_in_model_root": [],
        "files_in_model_dir": [],
        "suspicious_small_files": [],
    }
    if os.path.isdir(model_root):
        info["files_in_model_root"] = os.listdir(model_root)
    if os.path.isdir(MODEL_DIR):
        entries = os.listdir(MODEL_DIR)
        info["files_in_model_dir"] = entries
        for fname in entries:
            fpath = os.path.join(MODEL_DIR, fname)
            if os.path.isfile(fpath):
                size = os.path.getsize(fpath)
                # File model (.bin/.safetensors) yang cuma beberapa ratus byte biasanya
                # adalah pointer Git LFS yang belum ter-resolve, bukan file asli.
                if fname.endswith((".bin", ".safetensors")) and size < 10_000:
                    info["suspicious_small_files"].append((fname, size))
    return info


@st.cache_resource(show_spinner=False)
def load_model():
    """Load tokenizer + model sekali saja, disimpan di cache Streamlit."""
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return tokenizer, model, device


def _demo_predict(text: str):
    """Fallback berbasis kata kunci sederhana, dipakai kalau model belum di-copy."""
    positive_words = ["bagus", "cepat", "puas", "recommended", "ramah", "sesuai", "mantap", "keren"]
    negative_words = ["jelek", "rusak", "lambat", "kecewa", "buruk", "tidak sesuai", "lama", "cacat"]
    t = text.lower()
    pos_hits = sum(w in t for w in positive_words)
    neg_hits = sum(w in t for w in negative_words)
    if pos_hits == neg_hits:
        label, conf = ("Positive", 0.55) if len(t) % 2 == 0 else ("Negative", 0.55)
    elif pos_hits > neg_hits:
        label, conf = "Positive", min(0.6 + 0.1 * pos_hits, 0.97)
    else:
        label, conf = "Negative", min(0.6 + 0.1 * neg_hits, 0.97)
    probs = {label: conf, ("Negative" if label == "Positive" else "Positive"): 1 - conf}
    return label, conf, probs


def predict_sentiment(text: str):
    """Prediksi satu review. Return: (label, confidence, {'Positive': p, 'Negative': p})"""
    from .preprocessing import light_normalize

    if not model_is_available():
        return _demo_predict(text)

    import torch

    tokenizer, model, device = load_model()
    clean_text = light_normalize(text)
    inputs = tokenizer(
        clean_text, truncation=True, padding="max_length",
        max_length=MAX_LENGTH, return_tensors="pt",
    ).to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1).cpu().numpy()[0]

    pred_idx = int(np.argmax(probs))
    label = LABEL_MAP[pred_idx]
    confidence = float(probs[pred_idx])
    prob_dict = {"Negative": float(probs[0]), "Positive": float(probs[1])}
    return label, confidence, prob_dict


def predict_batch(texts: list[str], progress_callback=None):
    """Prediksi banyak review sekaligus. Return list of (label, confidence, prob_dict)."""
    results = []
    total = len(texts)
    for i, t in enumerate(texts):
        results.append(predict_sentiment(t))
        if progress_callback is not None:
            progress_callback((i + 1) / total)
    return results
