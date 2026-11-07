
"""
Validasi dan persiapan fitur RFM untuk prediksi pelanggan.
"""

import math
from numbers import Real

import pandas as pd


FEATURES_RFM = [
    "hari_sejak_transaksi_terakhir",
    "jumlah_transaksi_6bln",
    "total_belanja_rp",
]


def prepare_rfm_features(customer, feature_order):
    """
    Menyiapkan data satu pelanggan untuk model K-Means.

    Scaling tidak dilakukan di sini karena StandardScaler
    sudah tersimpan di dalam pipeline model.
    """

    if not isinstance(customer, dict):
        raise ValueError("Input harus berupa dictionary.")

    if list(feature_order) != FEATURES_RFM:
        raise ValueError("Urutan fitur tidak sesuai metadata.")

    cleaned = {}

    for feature in FEATURES_RFM:
        if feature not in customer:
            raise ValueError(f"Fitur {feature} belum diisi.")

        value = customer[feature]

        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"{feature} harus berupa angka.")

        value = float(value)

        if not math.isfinite(value) or value < 0:
            raise ValueError(
                f"{feature} harus berupa angka valid >= 0."
            )

        if feature in FEATURES_RFM[:2]:
            if not value.is_integer():
                raise ValueError(
                    f"{feature} harus berupa bilangan bulat."
                )

        cleaned[feature] = value

    if cleaned["jumlah_transaksi_6bln"] < 1:
        raise ValueError("Jumlah transaksi minimal 1.")

    if cleaned["total_belanja_rp"] <= 0:
        raise ValueError("Total belanja harus lebih dari 0.")

    return pd.DataFrame(
        [cleaned],
        columns=feature_order,
        dtype="float64"
    )
