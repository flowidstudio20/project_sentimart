"""
Loader untuk metrik evaluasi model (halaman Performa Model).

Cara mengisi data asli:
    Setelah training & testing selesai di notebook, jalankan cell export
    (lihat `export_metrics_snippet.py` di root project ini) untuk membuat
    file `metrics.json`, lalu letakkan di: sentimart/model/metrics.json

Kalau file itu belum ada, halaman Performa Model akan menampilkan nilai
default di bawah ini -- yaitu hasil aktual yang sudah dilaporkan di
Progress Proposal (Accuracy 98.61%, dst. -- lihat bagian 7.8 proposal),
supaya dashboard tetap informatif sebelum model asli di-plug in.
"""
import json
import os

METRICS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "metrics.json")

DEFAULT_METRICS = {
    "accuracy": 0.9861,
    "precision": 0.9827,
    "recall": 0.9884,
    "f1": 0.9855,
    "confusion_matrix": {  # sesuai proposal 7.9: 555 negatif & 510 positif benar, 15 salah
        "tn": 555, "fp": 9,
        "fn": 6, "tp": 510,
    },
    "train_loss": [0.6821, 0.3245, 0.1876, 0.1102, 0.0731],
    "val_loss": [0.2954, 0.1873, 0.1241, 0.0983, 0.0874],
    "train_acc": [0.8924, 0.9412, 0.9651, 0.9784, 0.9861],
    "val_acc": [0.9341, 0.9587, 0.9712, 0.9798, 0.9861],
    "best_threshold": 0.5,
    "is_demo": True,
    "n_test": 1080,
}


def load_metrics() -> dict:
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["is_demo"] = False
            return data
        except Exception:
            pass
    return DEFAULT_METRICS
