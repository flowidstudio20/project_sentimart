# Folder ini untuk model hasil training

Letakkan di sini:

1. **`indobert_sentiment_final/`** — folder hasil `trainer.save_model(...)` dari
   notebook (Cell 6). Isinya kira-kira: `config.json`, `model.safetensors`
   (atau `pytorch_model.bin`), `tokenizer_config.json`, `vocab.txt`, dll.

2. **`metrics.json`** — file hasil menjalankan `export_metrics_snippet.py`
   di notebook (setelah Cell 8). Berisi accuracy, precision, recall, f1,
   confusion matrix, dan training/validation loss per epoch.

Selama dua item di atas belum ada, aplikasi tetap bisa dijalankan dalam
**mode demo**:
- Halaman Prediksi & Analisis Batch akan memakai heuristik kata kunci
  sederhana (bukan model asli).
- Halaman Performa Model akan menampilkan angka dari Progress Proposal
  (Accuracy 98.61%, dst.) sebagai placeholder.
