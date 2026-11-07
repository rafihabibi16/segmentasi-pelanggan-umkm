
"""
Pengujian awal inferensi model K-Means UMKM.
"""

from src.predict import predict_customer


# Kasus 1: Input pelanggan valid
customer = {
    "hari_sejak_transaksi_terakhir": 12,
    "jumlah_transaksi_6bln": 8,
    "total_belanja_rp": 400000
}

result = predict_customer(customer)

print("=== HASIL PREDIKSI PELANGGAN ===")
print("Cluster :", result["cluster_id"])
print("Segmen  :", result["segment_name"])

# Dibandingkan dengan hasil aktual Google Colab
assert result["cluster_id"] == 0
assert (
    result["segment_name"]
    == "Aktif Berorientasi Promo"
)

print("\nPengujian prediksi valid berhasil!")


# Kasus 2: Input tidak valid harus ditolak
invalid_customer = {
    "hari_sejak_transaksi_terakhir": -10,
    "jumlah_transaksi_6bln": 8,
    "total_belanja_rp": 400000
}

try:
    predict_customer(invalid_customer)

except ValueError as error:
    print("\n=== PENGUJIAN INPUT TIDAK VALID ===")
    print("Input berhasil ditolak:", error)

else:
    raise AssertionError(
        "Input negatif seharusnya ditolak."
    )

print("\nSemua pengujian berhasil!")
