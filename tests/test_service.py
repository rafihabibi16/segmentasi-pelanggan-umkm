
"""
Pengujian otomatis sistem segmentasi pelanggan UMKM.

Menggunakan model final yang telah dilatih.
Tidak melakukan training ulang.
"""

import unittest
from copy import deepcopy

from src.service import segment_customer
from src.recommendations import (
    get_promotion_recommendation
)


class TestSegmentasiUMKM(unittest.TestCase):

    def setUp(self):
        """Contoh pelanggan fiktif untuk pengujian."""
        self.customer = {
            "hari_sejak_transaksi_terakhir": 12,
            "jumlah_transaksi_6bln": 8,
            "total_belanja_rp": 400000
        }

    def test_01_prediksi_valid(self):
        result = segment_customer(self.customer)

        self.assertEqual(result["cluster_id"], 0)
        self.assertEqual(
            result["segment_name"],
            "Aktif Berorientasi Promo"
        )

    def test_02_output_lengkap(self):
        result = segment_customer(self.customer)

        self.assertIn("cluster_id", result)
        self.assertIn("segment_name", result)
        self.assertIn("segment_description", result)
        self.assertIn("promotion", result)

        self.assertEqual(
            set(result["promotion"].keys()),
            {
                "strategy",
                "recommendation",
                "reason",
                "success_metric"
            }
        )

    def test_03_rekomendasi_empat_cluster(self):
        strategies = []

        for cluster in range(4):
            recommendation = (
                get_promotion_recommendation(cluster)
            )

            self.assertTrue(
                recommendation["recommendation"]
            )
            strategies.append(recommendation["strategy"])

        self.assertEqual(len(set(strategies)), 4)

    def test_04_recency_negatif(self):
        customer = deepcopy(self.customer)
        customer["hari_sejak_transaksi_terakhir"] = -5

        with self.assertRaises(ValueError):
            segment_customer(customer)

    def test_05_fitur_hilang(self):
        customer = deepcopy(self.customer)
        del customer["total_belanja_rp"]

        with self.assertRaises(ValueError):
            segment_customer(customer)

    def test_06_frequency_desimal(self):
        customer = deepcopy(self.customer)
        customer["jumlah_transaksi_6bln"] = 2.5

        with self.assertRaises(ValueError):
            segment_customer(customer)

    def test_07_transaksi_nol(self):
        customer = deepcopy(self.customer)
        customer["jumlah_transaksi_6bln"] = 0

        with self.assertRaises(ValueError):
            segment_customer(customer)

    def test_08_belanja_nol(self):
        customer = deepcopy(self.customer)
        customer["total_belanja_rp"] = 0

        with self.assertRaises(ValueError):
            segment_customer(customer)

    def test_09_nilai_nan(self):
        customer = deepcopy(self.customer)
        customer["total_belanja_rp"] = float("nan")

        with self.assertRaises(ValueError):
            segment_customer(customer)

    def test_10_cluster_tidak_dikenal(self):
        with self.assertRaises(ValueError):
            get_promotion_recommendation(99)


if __name__ == "__main__":
    unittest.main()
