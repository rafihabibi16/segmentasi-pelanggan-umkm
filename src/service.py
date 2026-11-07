
"""
Layanan utama segmentasi pelanggan UMKM.

Menggabungkan prediksi K-Means, interpretasi
segmen, dan rekomendasi promosi.
"""

from src.predict import predict_customer
from src.recommendations import get_promotion_recommendation


# Deskripsi berdasarkan customer profiling training.
# Bukan pernyataan pasti tentang setiap pelanggan.
SEGMENT_PROFILES = {
    0: (
        "Kelompok pelanggan yang relatif aktif dan "
        "cenderung memiliki tingkat penggunaan "
        "promo tinggi."
    ),
    1: (
        "Kelompok pelanggan dengan frekuensi "
        "pembelian rendah dan waktu sejak "
        "transaksi terakhir yang relatif lama."
    ),
    2: (
        "Kelompok pelanggan dengan nominal "
        "pembelian besar per transaksi dan "
        "banyak memiliki kategori favorit "
        "kue ulang tahun atau paket snack."
    ),
    3: (
        "Kelompok pelanggan yang sangat rutin "
        "bertransaksi dengan nilai total "
        "belanja relatif tinggi."
    ),
}


def segment_customer(customer: dict) -> dict:
    """
    Menghasilkan segmentasi dan rekomendasi
    promosi untuk satu pelanggan.
    """

    # 1. Prediksi menggunakan model ML
    prediction = predict_customer(customer)

    cluster_id = prediction["cluster_id"]
    segment_name = prediction["segment_name"]

    # 2. Ambil profil segmen
    if cluster_id not in SEGMENT_PROFILES:
        raise ValueError(
            f"Profil cluster {cluster_id} tidak tersedia."
        )

    description = SEGMENT_PROFILES[cluster_id]

    # 3. Ambil rekomendasi promosi
    promotion = get_promotion_recommendation(
        cluster_id
    )

    # 4. Gabungkan semua informasi
    return {
        "cluster_id": cluster_id,
        "segment_name": segment_name,
        "segment_description": description,
        "promotion": promotion
    }
