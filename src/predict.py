
"""
Modul inferensi segmentasi pelanggan UMKM.

Menggunakan model K-Means dan metadata yang
telah disimpan dari eksperimen Google Colab.
"""

import json
from functools import lru_cache
from pathlib import Path

import joblib

from src.features import prepare_rfm_features


# Lokasi proyek, relatif terhadap file predict.py
PROJECT_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_DIR / "artifacts" / "kmeans_rfm_v1.joblib"
)

METADATA_PATH = (
    PROJECT_DIR / "artifacts" / "cluster_metadata.json"
)


@lru_cache(maxsize=1)
def load_model():
    """Memuat model dan metadata satu kali."""

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model tidak ditemukan: {MODEL_PATH}"
        )

    if not METADATA_PATH.is_file():
        raise FileNotFoundError(
            f"Metadata tidak ditemukan: {METADATA_PATH}"
        )

    # Hanya gunakan file joblib dari sumber tepercaya
    model = joblib.load(MODEL_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    # Validasi kesesuaian metadata dengan model
    if metadata["n_clusters"] != model.named_steps[
        "kmeans"
    ].n_clusters:
        raise ValueError(
            "Jumlah cluster model dan metadata tidak cocok."
        )

    if list(metadata["feature_order"]) != list(
        model.feature_names_in_
    ):
        raise ValueError(
            "Urutan fitur model dan metadata tidak cocok."
        )

    return model, metadata


def predict_customer(customer: dict) -> dict:
    """
    Memprediksi segmen seorang pelanggan.

    Parameters
    ----------
    customer : dict
        Data Recency, Frequency, dan Monetary.

    Returns
    -------
    dict
        Nomor cluster dan nama segmen.
    """

    model, metadata = load_model()

    # Validasi dan persiapan input
    features = prepare_rfm_features(
        customer,
        metadata["feature_order"]
    )

    # StandardScaler berjalan otomatis dalam pipeline
    cluster_id = int(model.predict(features)[0])

    # Ambil nama segmen dari metadata
    segment_name = metadata["cluster_names"][
        str(cluster_id)
    ]

    return {
        "cluster_id": cluster_id,
        "segment_name": segment_name
    }
