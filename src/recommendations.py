
"""
Strategi promosi berbasis profil cluster pelanggan UMKM.

Rekomendasi bersifat rule-based berdasarkan hasil
customer profiling, bukan prediksi respons promosi.
"""

from copy import deepcopy


PROMOTION_RULES = {
    0: {
        "strategy": "Bundling dan Promo Pembelian Berulang",
        "recommendation": (
            "Tawarkan paket bundling kopi dan roti "
            "dengan minimum nilai pembelian."
        ),
        "reason": (
            "Segmen ini relatif aktif dan memiliki "
            "rata-rata penggunaan promo tinggi."
        ),
        "success_metric": (
            "Tingkat penggunaan penawaran, nilai "
            "transaksi, dan margin promosi."
        ),
    },

    1: {
        "strategy": "Reaktivasi Pelanggan",
        "recommendation": (
            "Berikan voucher reaktivasi satu kali "
            "dengan masa berlaku terbatas."
        ),
        "reason": (
            "Segmen ini memiliki recency tinggi "
            "dan frekuensi transaksi rendah."
        ),
        "success_metric": (
            "Persentase pelanggan yang kembali "
            "bertransaksi setelah penawaran."
        ),
    },

    2: {
        "strategy": "Penawaran Produk Acara",
        "recommendation": (
            "Tawarkan katalog pre-order kue ulang "
            "tahun dan paket snack, termasuk opsi "
            "pesanan dalam jumlah besar."
        ),
        "reason": (
            "Segmen ini memiliki nominal transaksi "
            "tinggi dan didominasi pelanggan dengan "
            "kategori favorit produk acara."
        ),
        "success_metric": (
            "Konversi pre-order dan nilai "
            "pesanan produk acara."
        ),
    },

    3: {
        "strategy": "Loyalty dan Retensi Pelanggan",
        "recommendation": (
            "Berikan reward loyalitas, poin "
            "pembelian, atau benefit khusus "
            "tanpa harus memberikan diskon besar."
        ),
        "reason": (
            "Segmen ini memiliki frekuensi "
            "transaksi dan total belanja tinggi "
            "dengan recency rendah."
        ),
        "success_metric": (
            "Retensi pelanggan, frekuensi pembelian "
            "ulang, dan biaya reward."
        ),
    },
}


def get_promotion_recommendation(cluster_id: int) -> dict:
    """
    Mengambil strategi promosi berdasarkan ID cluster.

    Parameter
    ---------
    cluster_id : int
        Nomor cluster hasil prediksi model.

    Returns
    -------
    dict
        Strategi, rekomendasi, alasan, dan metrik.
    """

    if type(cluster_id) is not int:
        raise ValueError("Cluster ID harus integer.")

    if cluster_id not in PROMOTION_RULES:
        raise ValueError(
            f"Rekomendasi untuk cluster {cluster_id} "
            "tidak tersedia."
        )

    return deepcopy(PROMOTION_RULES[cluster_id])
