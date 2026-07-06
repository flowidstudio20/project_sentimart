---
title: SentiMart
emoji: 🛍️
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 7860
pinned: false
short_description: Analisis sentimen ulasan e-commerce Indonesia dengan IndoBERT
---

# SentiMart — Analisis Sentimen Ulasan E-Commerce Indonesia

Aplikasi web (Streamlit) untuk Proyek Akhir Praktikum NLP — Kelompok 5, 3TIB,
Politeknik Caltex Riau. Model: IndoBERT (`indobenchmark/indobert-base-p1`)
fine-tuned pada dataset PRDECT-ID.

## Struktur Project

```
sentimart/
├── app.py                          # Entry point (st.navigation + sidebar)
├── views/
│   ├── home.py                     # Beranda
│   ├── predict.py                  # Prediksi 1 ulasan
│   ├── batch.py                    # Upload CSV, prediksi massal
│   ├── performance.py              # Metrik evaluasi model
│   └── about.py                    # Info dataset & tim
├── utils/
│   ├── preprocessing.py            # light_normalize (sama seperti notebook)
│   ├── model_loader.py             # Load & cache model IndoBERT + diagnostik
│   ├── metrics_data.py             # Load metrics.json / fallback default
│   └── sidebar.py                  # Sidebar terpusat (status model + debug info)
├── model/                          # <-- letakkan model hasil training di sini
│   └── README.md
├── sample_data/contoh_ulasan.csv   # Contoh file untuk Analisis Batch
├── export_metrics_snippet.py       # Tempel di notebook untuk export metrics.json
├── Dockerfile                      # Untuk deploy ke HF Spaces (SDK: Docker)
├── requirements.txt
└── .streamlit/config.toml
```

> Catatan: label & ikon menu sidebar (Beranda, Prediksi, dst.) diatur langsung
> di `app.py` lewat `st.navigation`/`st.Page`, bukan dari nama file — supaya
> tidak rusak/garbled saat di-deploy ke platform lain (masalah umum kalau nama
> file mengandung emoji).

## 1. Setup & Menjalankan Secara Lokal

```bash
cd sentimart
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

Buka `http://localhost:8501` di browser.

> Tanpa model asli, app tetap jalan dalam **mode demo** (lihat bawah).

## 2. Memasang Model Hasil Training (Wajib untuk hasil asli)

1. Di notebook training (`notebook08c6055fdc.ipynb`), setelah Cell 8
   (evaluasi test set) selesai, tempel & jalankan isi `export_metrics_snippet.py`
   sebagai cell baru. Ini membuat:
   - `metrics.json` — semua angka evaluasi & confusion matrix asli kamu
   - `indobert_sentiment_final.zip` — model yang sudah di-zip
2. Download kedua file tersebut (klik kanan di file browser Kaggle/Colab → Download).
3. Extract `indobert_sentiment_final.zip` ke `sentimart/model/indobert_sentiment_final/`
4. Pindahkan `metrics.json` ke `sentimart/model/metrics.json`
5. Restart `streamlit run app.py` — sidebar akan berubah dari "Mode DEMO" jadi
   "Model IndoBERT: siap".

## 3. Mode Demo

Kalau model belum dipasang:
- Halaman **Prediksi** & **Analisis Batch** pakai heuristik kata kunci sederhana
  (bukan model asli) — cukup untuk mengecek alur UI & wireframe.
- Halaman **Performa Model** menampilkan angka dari Progress Proposal
  (Accuracy 98.61%, Precision 98.27%, Recall 98.84%, F1 98.55%) sebagai placeholder,
  dengan label "data demo" yang jelas.
- Sidebar akan menampilkan kotak **"Mode DEMO"** — klik expander
  **"Kenapa model tidak terdeteksi?"** di bawahnya untuk melihat diagnostik:
  path yang dicari, isi folder `model/`, dan apakah file model kamu
  kemungkinan cuma pointer Git LFS (ukurannya kecil, bukan file asli ~400-500MB).

## 4. Opsi Deploy

**A. Hugging Face Spaces — SDK Docker + template Streamlit (rekomendasi)**
> Catatan: HF sudah menghapus opsi SDK "Streamlit" berdiri sendiri. Sekarang
> Streamlit di-deploy lewat SDK **Docker**, memakai `Dockerfile` yang sudah
> disediakan di project ini (`Dockerfile` di root folder).

1. Buat Space baru di [huggingface.co/new-space](https://huggingface.co/new-space)
2. Pilih SDK **Docker** (bukan Gradio), lalu boleh pilih template "Streamlit"
   sebagai starting point — nanti file `Dockerfile` & `README.md` (dengan
   metadata YAML) dari project ini yang dipakai/menimpa.
3. Push semua isi folder ini ke repo Space (via git atau upload manual):
   ```bash
   git clone https://huggingface.co/spaces/USERNAME/sentimart
   cd sentimart
   # copy semua isi folder project sentimart ke sini (termasuk model/)
   git add .
   git commit -m "Initial deploy SentiMart"
   git push
   ```
4. HF otomatis build image Docker dari `Dockerfile`, install `requirements.txt`,
   dan jalankan `streamlit run app.py` di port 7860 (sudah diatur di `Dockerfile`).
5. Model IndoBERT ~500MB — kalau push lewat git, HF otomatis pakai Git LFS
   untuk file besar (biasanya auto-terdeteksi, tidak perlu setup manual).

**B. Streamlit Community Cloud**
1. Push folder ini ke repo GitHub (perlu Git LFS untuk model ~500MB, atau
   host model di Hugging Face Hub dan download otomatis saat startup).
2. Ke [share.streamlit.io](https://share.streamlit.io), connect repo, pilih `app.py`.

**C. VPS sendiri**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
Lalu reverse-proxy dengan Nginx (mirip setup `sibapak.pocari.id` sebelumnya).

## 5. Catatan Preprocessing

Untuk prediksi (Halaman Prediksi & Batch), teks HANYA dilewatkan `light_normalize()`
(rapikan huruf berulang & slang ringan) — **bukan** `preprocess_text()` versi
TF-IDF yang membuang stopword. Ini supaya perilaku model di web app identik
dengan saat training/testing IndoBERT di notebook (Cell 6 & 8).
