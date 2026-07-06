# ============================================================
# EXPORT UNTUK WEB APP (SentiMart)
# ============================================================
# Tempel & jalankan cell ini di notebook SETELAH Cell 8 (evaluasi test set)
# selesai dijalankan. Ini akan membuat file `metrics.json` yang berisi
# semua angka & confusion matrix asli hasil training kamu.
#
# Setelah file ini terbuat, download `metrics.json` lalu letakkan di:
#   sentimart/model/metrics.json
#
# Untuk model-nya sendiri, folder `./indobert_sentiment_final/` yang sudah
# dibuat otomatis oleh Cell 6 (trainer.save_model(...)) tinggal di-download
# (zip dulu kalau perlu) dan diletakkan di:
#   sentimart/model/indobert_sentiment_final/
# ============================================================

import json

cm = confusion_matrix(y_test_final, y_pred_final)
# cm layout dari sklearn: [[TN, FP], [FN, TP]] karena label 0=Negative, 1=Positive
tn, fp, fn, tp = int(cm[0, 0]), int(cm[0, 1]), int(cm[1, 0]), int(cm[1, 1])

export = {
    "accuracy": float(acc_final),
    "precision": float(prec_final),
    "recall": float(rec_final),
    "f1": float(f1_final),
    "confusion_matrix": {"tn": tn, "fp": fp, "fn": fn, "tp": tp},
    "train_loss": [float(x) for x in train_losses],
    "val_loss": [float(x) for x in val_losses],
    "train_acc": [float(x) for x in train_accs],
    "val_acc": [float(x) for x in val_accs],
    "best_threshold": float(best_threshold),
    "n_test": int(len(y_test_final)),
}

with open("metrics.json", "w", encoding="utf-8") as f:
    json.dump(export, f, indent=2, ensure_ascii=False)

print("metrics.json berhasil dibuat!")
print(json.dumps(export, indent=2))

# Zip folder model biar mudah didownload sekali klik
import shutil
shutil.make_archive("indobert_sentiment_final", "zip", "indobert_sentiment_final")
print("\nindobert_sentiment_final.zip berhasil dibuat, tinggal didownload.")
