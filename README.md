# Segmentasi Pelanggan UMKM Menggunakan K-Means RFM · Tim Rafi–Rafli

**Kasus:** 05 — Segmentasi Pelanggan UMKM  
**Aplikasi:** https://segmentasi-pelanggan-umkm-rafi.streamlit.app/  
**Video:** [Tambahkan tautan video demonstrasi setelah tersedia]  
**Repositori:** https://github.com/rafihabibi16/segmentasi-pelanggan-umkm

| **Anggota** | **NIM** | **Bagian yang dikerjakan** |
| --- | --- | --- |
| Rafi Ahmad Habibi | 2409956 | Data understanding, EDA, data cleaning, feature engineering RFM, dan dokumentasi eksperimen. |
| Rafli Putra Permana | 2408471 | Pemodelan dan evaluasi K-Means, pengembangan aplikasi Streamlit, pengujian, dan deployment. |

> **Catatan kontribusi:** Pembagian di atas merupakan pembagian tugas yang direncanakan. Sebelum pengumpulan, pastikan sesuai kontribusi aktual dan setiap anggota memiliki commit yang dapat ditelusuri.

## Masalah dan pengguna

Pengguna sistem adalah pemilik atau pengelola UMKM bakery dan coffee shop yang ingin memahami perbedaan perilaku pembelian pelanggan. Promosi yang sama untuk seluruh pelanggan belum tentu relevan karena pelanggan memiliki frekuensi transaksi, nilai belanja, dan tingkat keaktifan yang berbeda. Sistem membantu mengidentifikasi segmen pelanggan serta memberikan **usulan strategi promosi** berdasarkan karakteristik masing-masing segmen, bukan menjamin peningkatan penjualan.

Aplikasi menyediakan dashboard profil segmen, prediksi cluster untuk satu pelanggan berdasarkan data RFM, rekomendasi promosi berbasis aturan bisnis, dan unduhan hasil prediksi dalam format CSV.

## Data dan pembersihan

**Sumber dataset:** [Repository studi kasus resmi, Kasus 05](https://github.com/nurhikam/mkb-ml-project/tree/main/kasus/05-segmentasi-umkm) · [raw.csv](https://raw.githubusercontent.com/nurhikam/mkb-ml-project/main/kasus/05-segmentasi-umkm/data/raw.csv).

Dataset bersifat **sintetis** dan merupakan ringkasan perilaku pelanggan selama enam bulan hingga Juni 2026. Data awal terdiri atas **10.150 baris dan 12 kolom**; data akhir setelah pembersihan memuat **10.000 pelanggan unik**. Selisih keseluruhan adalah **150 baris**; angka ini **bukan** jumlah masing-masing jenis kesalahan. Data akhir dibagi menjadi 7.000 baris training (70%), 1.500 validation (15%), dan 1.500 holdout test (15%).


| Masalah yang ditemukan | Jumlah baris | Cara menangani |
|---|---:|---|
| Duplikat baris identik | 90 | Menghapus baris yang benar-benar identik. |
| Pengulangan ID pelanggan lainnya | 60 | Memeriksa dan mengonsolidasikan catatan berdasarkan ID agar setiap pelanggan memiliki satu baris. |
| Nilai umur kosong | 208 | Memeriksa missing value; umur tidak digunakan sebagai fitur clustering final. |
| Nilai rating rata-rata kosong | 812 | Memeriksa missing value; rating tidak digunakan sebagai fitur clustering final. |
| Variasi penulisan kecamatan | 254 | Menyeragamkan kapitalisasi, spasi, dan variasi nama kecamatan. |


### Ringkasan Hasil Pembersihan

Dataset awal berisi 10.150 baris dengan 12 atribut dan 10.000 ID pelanggan unik. Audit menemukan 90 duplikat baris identik dan 60 pengulangan ID lainnya, sehingga total terdapat 150 baris tambahan berdasarkan ID pelanggan.

Selain itu, ditemukan 208 nilai umur kosong, 812 nilai rating rata-rata kosong, dan 254 baris dengan variasi penulisan kecamatan.

Setelah proses pembersihan dan deduplikasi, dataset akhir terdiri atas 10.000 pelanggan unik. Dataset dibagi menjadi 7.000 data training, 1.500 validation, dan 1.500 holdout test.

Fitur model final hanya menggunakan Recency, Frequency, dan Monetary (RFM). Rincian keputusan preprocessing dan implementasinya tersedia pada notebook eksperimen.



**Catatan:** Jumlah kasus per kategori dapat saling tumpang tindih; totalnya tidak harus sama dengan 150. Angka pada tanda kurung siku wajib dilengkapi dari sel audit notebook sebelum pengumpulan, bukan diperkirakan.

### Fitur model

Model final menggunakan tiga fitur **RFM (Recency, Frequency, Monetary)** berikut:

| Fitur | Makna |
| --- | --- |
| `hari_sejak_transaksi_terakhir` | Jarak hari sejak transaksi terakhir (*recency*). |
| `jumlah_transaksi_6bln` | Jumlah transaksi dalam enam bulan (*frequency*). |
| `total_belanja_rp` | Total nilai belanja enam bulan dalam rupiah (*monetary*). |

Ketiga fitur distandardisasi menggunakan `StandardScaler` sebelum K-Means agar skala nominal rupiah tidak mendominasi jarak Euclidean. Informasi penggunaan promo dan kategori produk favorit dimanfaatkan untuk **interpretasi profil** segmen; keduanya **bukan input** model final.

Seluruh langkah data understanding, audit kualitas, EDA, preprocessing, pemilihan fitur, eksperimen, dan evaluasi ada pada [`notebooks/TugasPraktisi_Clustering.ipynb`](notebooks/TugasPraktisi_Clustering.ipynb).

## Hasil

### Pemodelan dan perbandingan eksperimen

**Baseline wajib:** `StandardScaler` + `KMeans` dengan fitur RFM, `n_clusters=4`, `random_state=42`, dan `n_init=10`. Pemilihan `k` ditinjau melalui percobaan beberapa jumlah cluster, kualitas pengelompokan (*silhouette score*), stabilitas, serta kemudahan interpretasi bisnis.

| **Model** | **Silhouette validation** | **Silhouette test** |
| --- | ---: | ---: |
| **Baseline:** StandardScaler + K-Means RFM, k=4 | **0,5619** | — |
| Eksperimen: transformasi Log1p RFM, k=4 | 0,5296 | — |
| Eksperimen: transformasi Log1p RFM, k=5 | 0,5303 | — |
| Eksperimen: RFM + fitur promo, k=4 | 0,5625 | — |
| **Model final:** StandardScaler + K-Means RFM, k=4 | **0,5619** | **0,5497** |

Tanda **—** berarti model tersebut tidak dilaporkan pada holdout test; alternatif dibandingkan dalam tahap pengembangan menggunakan validation set. Model final mempertahankan baseline RFM karena sederhana, stabil, konsisten dengan masukan aplikasi, dan mudah dijelaskan kepada pemilik UMKM. Model RFM + promo memberikan silhouette validation sedikit lebih tinggi, tetapi memakai ruang fitur berbeda sehingga nilainya **tidak menjadi satu-satunya dasar** pemilihan model.

**Evaluasi model final:**

- Silhouette training (sampel 1.500): **0,5525**.
- Silhouette validation (1.500): **0,5619**.
- Silhouette holdout test (1.500): **0,5497**.
- Stabilitas resampling, rata-rata Adjusted Rand Index (ARI): **0,9951**.
- Seluruh eksperimen berhasil dijalankan ulang dari awal di Google Colab dengan hasil evaluasi yang sama.

Holdout test digunakan setelah keputusan model final. Eksekusi ulang notebook dilakukan untuk memeriksa reproduksibilitas, **bukan untuk memilih ulang model berdasarkan test**.

### Profil empat segmen pelanggan

Statistik berikut dihitung dari **7.000 data training**, bukan seluruh 10.000 data:

| **Cluster** | **Nama segmen** | **Pelanggan (training)** | **Recency rata-rata (hari)** | **Transaksi rata-rata/6 bulan** | **Belanja rata-rata/6 bulan** |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | Aktif Berorientasi Promo | 2.688 (38,40%) | 14,77 | 10,28 | Rp420.490 |
| 1 | Pelanggan Kurang Aktif | 1.912 (27,31%) | 114,12 | 2,57 | Rp106.784 |
| 2 | Pembeli Produk Acara Bernilai Tinggi | 655 (9,36%) | 30,40 | 4,66 | Rp1.408.475 |
| 3 | Pelanggan Rutin Bernilai Tinggi | 1.745 (24,93%) | 5,20 | 30,43 | Rp1.480.720 |

### Rekomendasi promosi

| **Segmen** | **Usulan promosi** | **Tujuan bisnis** |
| --- | --- | --- |
| Aktif Berorientasi Promo | Bundling kopi dan roti serta penawaran yang relevan. | Menjaga frekuensi transaksi dan nilai keranjang belanja. |
| Pelanggan Kurang Aktif | Voucher reaktivasi dengan masa berlaku terbatas. | Mendorong pelanggan kembali bertransaksi. |
| Pembeli Produk Acara Bernilai Tinggi | Penawaran pre-order, paket ulang tahun, atau produk acara. | Memfasilitasi kebutuhan pesanan bernilai besar. |
| Pelanggan Rutin Bernilai Tinggi | Program loyalitas, reward, dan akses penawaran khusus. | Mempertahankan hubungan dengan pelanggan rutin. |

**Threshold yang dipakai:** **Tidak berlaku (N/A)**. K-Means adalah metode *unsupervised clustering* yang tidak menggunakan threshold probabilitas untuk menghasilkan label. Parameter jumlah kelompok yang digunakan ialah **`k=4`**, bukan threshold klasifikasi. Rekomendasi promosi bersifat *rule-based* berdasarkan label cluster dan belum divalidasi melalui A/B testing atau pengukuran peningkatan penjualan nyata.

## Cara menjalankan

### Mengakses aplikasi online

Buka **https://segmentasi-pelanggan-umkm-rafi.streamlit.app/**. Aplikasi menerima input satu pelanggan dan menampilkan label cluster, karakteristik segmen, rekomendasi promosi, serta opsi ekspor CSV.

### Menjalankan secara lokal

Persyaratan: Python **3.13** (versi yang digunakan saat pengembangan), Git, dan koneksi internet untuk memasang dependensi.

```bash
git clone https://github.com/rafihabibi16/segmentasi-pelanggan-umkm.git
cd segmentasi-pelanggan-umkm
python -m venv .venv
```

Aktivasi virtual environment **Windows CMD**:

```cmd
.venv\Scripts\activate
```

Untuk Linux/macOS, gunakan `source .venv/bin/activate`.

Pasang dependensi dan jalankan aplikasi:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Proyek ini menggunakan **Streamlit tanpa FastAPI**, sehingga tidak memerlukan `uvicorn` dan tidak mempunyai entry point `app/api/main.py`.

### Menjalankan pengujian

```bash
python -m unittest discover -s tests -v
```

Pengujian unit mencakup validasi input, inferensi cluster, serta respons layanan. Selain itu, enam fungsi utama aplikasi publik telah diuji secara manual: akses halaman, Overview, eksplorasi segmen, prediksi, rekomendasi promo, dan ekspor CSV.

### Menjalankan ulang notebook

1. Buka [`notebooks/TugasPraktisi_Clustering.ipynb`](notebooks/TugasPraktisi_Clustering.ipynb) di Google Colab.
2. Pilih **Runtime → Restart session**, kemudian **Runtime → Run all**.
3. Notebook membaca data mentah dari URL GitHub sumber.
4. Hasil reproduksi disimpan di `repro_outputs/data/cleaned_customers.csv`, `repro_outputs/artifacts/kmeans_rfm_v1.joblib`, dan `repro_outputs/artifacts/cluster_metadata.json` relatif terhadap direktori kerja notebook.

Model hasil reproduksi tidak perlu menggantikan `artifacts/kmeans_rfm_v1.joblib` yang dipakai aplikasi. Notebook telah diuji ulang dan menghasilkan metrik evaluasi yang konsisten.

## Struktur repositori

```text
segmentasi-pelanggan-umkm/
├── .streamlit/
│   └── config.toml                 # Tema aplikasi
├── artifacts/
│   ├── cluster_metadata.json       # Versi model, fitur, dan metrik
│   ├── cluster_profiles.json       # Profil statistik empat segmen
│   └── kmeans_rfm_v1.joblib        # Pipeline StandardScaler + K-Means
├── notebooks/
│   └── TugasPraktisi_Clustering.ipynb  # EDA hingga evaluasi dan ekspor model
├── src/
│   ├── __init__.py
│   ├── dashboard.py                # Visualisasi dashboard
│   ├── features.py                 # Validasi dan pembuatan fitur RFM saat inferensi
│   ├── predict.py                  # Pemuatan model dan prediksi cluster
│   ├── recommendations.py          # Aturan rekomendasi per cluster
│   └── service.py                  # Integrasi hasil prediksi dan rekomendasi
├── tests/
│   └── test_service.py             # Unit test layanan
├── .gitignore
├── app.py                          # Entry point Streamlit
├── README.md
├── requirements.txt
└── test_prediction.py              # Pengujian prediksi sederhana
```

**Catatan implementasi:** Notebook menggunakan tiga fitur RFM dengan nama dan urutan yang sama dengan proses inferensi; `src/features.py` saat ini dipakai untuk penyiapan input prediksi aplikasi. Pemakaian fungsi yang persis sama secara langsung di notebook training perlu dipastikan bila dosen mensyaratkan satu modul bersama untuk training dan inferensi.

Dataset sumber dibaca langsung dari GitHub. Karena itu, folder `data/` atau `app/` pada contoh template dosen **tidak dipaksakan** apabila tidak sesuai struktur implementasi aktual.

## Keterbatasan

1. **Data sintetis:** hasil tidak dapat langsung digeneralisasi ke seluruh UMKM atau digunakan sebagai bukti efektivitas promosi pada bisnis nyata.
2. **Fitur terbatas:** model hanya menggunakan Recency, Frequency, dan Monetary; preferensi produk, penggunaan promo, margin, dan faktor musiman tidak dimasukkan sebagai input model final.
3. **Kualitas input:** prediksi bisa kurang representatif jika data RFM keliru, tidak lengkap, berada jauh di luar pola training, atau definisi periode transaksinya berbeda.
4. **Perubahan perilaku pelanggan:** model perlu dievaluasi ulang ketika profil transaksi berubah; hasil clustering tidak otomatis tetap relevan sepanjang waktu.
5. **Belum ada uji dampak promosi:** rekomendasi didasarkan pada interpretasi cluster, bukan hasil uji A/B, pengukuran konversi, atau peningkatan pendapatan yang telah terbukti.
6. **Bukan sistem CRM produksi:** aplikasi merupakan prototipe akademik; belum mencakup integrasi transaksi real-time, otentikasi pengguna, atau pemantauan model otomatis.

## Daftar periksa sebelum dikumpulkan

- [x] Repositori GitHub bersifat publik.
- [ ] **Setiap anggota memiliki commit** yang dapat ditelusuri sesuai kontribusinya.
- [x] Notebook berhasil dijalankan ulang dari awal sampai akhir tanpa galat.
- [x] Baseline K-Means dilaporkan dan dibandingkan dengan eksperimen improvement.
- [x] Holdout test digunakan untuk evaluasi final setelah model dipilih, bukan untuk optimasi model.
- [x] `artifacts/cluster_metadata.json` memuat versi model, fitur masukan, dan metrik; threshold ditandai tidak berlaku untuk K-Means.
- [x] Aplikasi publik dapat diakses dan enam fungsi utamanya telah diuji.
- [x] Tersedia validasi input yang tidak wajar serta pengujian unit layanan.
- [ ] Aplikasi diverifikasi secara khusus melalui browser ponsel.
- [ ] Jumlah baris tiap jenis masalah data cleaning dilengkapi dari notebook.
- [ ] Laporan akhir maksimal **6 halaman** telah diselesaikan.
- [ ] Video demonstrasi maksimal **5 menit** telah diselesaikan dan tautannya ditambahkan.

---

**Aplikasi:** https://segmentasi-pelanggan-umkm-rafi.streamlit.app/  
**Repository:** https://github.com/rafihabibi16/segmentasi-pelanggan-umkm  
**Sumber studi kasus:** https://github.com/nurhikam/mkb-ml-project/tree/main/kasus/05-segmentasi-umkm
