
# Segmentasi Pelanggan UMKM Menggunakan K-Means Clustering


## Demo Aplikasi

**Aplikasi Streamlit:**  
https://segmentasi-pelanggan-umkm-rafi.streamlit.app/

**Repository GitHub:**  
https://github.com/rafihabibi16/segmentasi-pelanggan-umkm

Aplikasi merupakan prototipe akademik segmentasi pelanggan UMKM bakery dan coffee shop menggunakan K-Means RFM.

Fitur utama:
- Dashboard analitik empat segmen pelanggan.
- Visualisasi distribusi dan karakteristik RFM.
- Eksplorasi detail segmen dan strategi promosi.
- Prediksi segmen pelanggan baru.
- Rekomendasi promosi berbasis profil cluster.
- Ekspor hasil analisis dalam format CSV.

Aplikasi telah diuji melalui deployment publik di Streamlit Community Cloud.


Proyek Machine Learning untuk segmentasi pelanggan UMKM bakery dan coffee shop berdasarkan perilaku transaksi menggunakan pendekatan RFM (Recency, Frequency, Monetary).

Sistem dilengkapi dashboard analitik berbasis Streamlit dan rekomendasi strategi promosi untuk setiap segmen pelanggan.

> **Status:** Prototipe akademik menggunakan dataset sintetis. Rekomendasi pemasaran belum divalidasi melalui kampanye nyata.

## 1. Latar Belakang

UMKM yang memberikan promosi seragam kepada seluruh pelanggan berisiko menggunakan anggaran pemasaran secara kurang efisien karena perilaku pelanggan berbeda-beda.

Proyek ini menerapkan unsupervised learning untuk mengidentifikasi kelompok pelanggan berdasarkan aktivitas dan nilai belanja, kemudian menerjemahkan hasil clustering menjadi rekomendasi promosi yang dapat dipertimbangkan oleh pemilik UMKM.

## 2. Tujuan

- Mengidentifikasi pola perilaku pelanggan menggunakan RFM.
- Membandingkan sejumlah konfigurasi K-Means.
- Menghasilkan segmen pelanggan yang dapat diinterpretasikan.
- Memberikan rekomendasi promosi berbasis profil segmen.
- Menyediakan aplikasi web untuk analisis pelanggan baru.

## 3. Dataset

Dataset sintetis berasal dari studi kasus Segmentasi Pelanggan UMKM pada repositori tugas Machine Learning.

Sumber:
https://github.com/nurhikam/mkb-ml-project/tree/main/kasus/05-segmentasi-umkm

Ringkasan pengolahan:
- Data mentah: 10.150 baris.
- Pelanggan unik setelah deduplikasi: 10.000.
- Training: 7.000 pelanggan (70%).
- Validation: 1.500 pelanggan (15%).
- Holdout test: 1.500 pelanggan (15%).

Data cleaning mencakup pemeriksaan duplikasi, nilai hilang, format nominal rupiah, konsistensi kategori wilayah, dan anomali numerik.

## 4. Metodologi Machine Learning

### Fitur Model

| Fitur | Deskripsi |
|---|---|
| Recency | Hari sejak transaksi terakhir |
| Frequency | Jumlah transaksi selama enam bulan |
| Monetary | Total belanja enam bulan dalam rupiah |

Algoritma final: **K-Means Clustering (k=4)**.

Pipeline:
1. StandardScaler.
2. K-Means dengan random_state=42 dan n_init=10.

StandardScaler dilatih hanya menggunakan training set. Validation dan test tidak digunakan untuk fitting model.

### Eksperimen

Konfigurasi yang diuji:
- Baseline RFM + StandardScaler + K-Means.
- Log1p + StandardScaler + K-Means.
- RFM + persentase penggunaan promo.
- Variasi jumlah cluster k=2 hingga k=8.
- Stabilitas terhadap perubahan inisialisasi.
- Stabilitas melalui resampling data training.
- Sensitivitas terhadap anomali recency.

Pemilihan model mempertimbangkan silhouette, stabilitas, interpretabilitas, dan kegunaan bisnis.

## 5. Evaluasi Model Final

| Dataset | Jumlah Pelanggan | Silhouette |
|---|---:|---:|
| Training (sampel evaluasi) | 1.500 | 0,5525 |
| Validation | 1.500 | 0,5619 |
| Holdout Test | 1.500 | 0,5497 |

Model final memperoleh rata-rata ARI 0,9951 pada eksperimen resampling training.

> Silhouette mengukur karakteristik pemisahan cluster, bukan akurasi klasifikasi. Evaluasi ini tidak membuktikan efektivitas promosi maupun kemampuan model menghadapi data drift.

## 6. Hasil Segmentasi

| Cluster | Nama Segmen | Strategi Utama |
|---|---|---|
| 0 | Aktif Berorientasi Promo | Bundling kopi dan roti |
| 1 | Pelanggan Kurang Aktif | Voucher reaktivasi |
| 2 | Pembeli Produk Acara Bernilai Tinggi | Penawaran pre-order kue dan paket snack |
| 3 | Pelanggan Rutin Bernilai Tinggi | Reward loyalitas |

Penamaan cluster didasarkan pada customer profiling training set.

Penggunaan promo dan kategori favorit digunakan sebagai informasi pendukung interpretasi, bukan fitur input model final.

## 7. Fitur Aplikasi

Aplikasi Streamlit menyediakan:
- Dashboard overview empat segmen.
- Visualisasi distribusi pelanggan dan rata-rata RFM.
- Eksplorasi profil setiap segmen.
- Prediksi segmen satu pelanggan baru.
- Rekomendasi promosi berbasis aturan (rule-based).
- Ekspor hasil analisis ke CSV.
- Validasi input dan penanganan kesalahan dasar.

Aplikasi belum terhubung dengan database atau transaksi real-time.

## 8. Instalasi dan Menjalankan Aplikasi

Persyaratan: Python 3.13 dan file model pada folder `artifacts`.

### Membuat virtual environment (Windows)

    py -m venv .venv
    .venv\Scripts\activate.bat

### Menginstal dependensi

    python -m pip install -r requirements.txt

### Menjalankan aplikasi

    python -m streamlit run app.py

Buka http://localhost:8501 pada browser.

### Menjalankan pengujian otomatis

    python -m unittest discover -s tests -p "test_*.py" -v

Model `.joblib` harus berasal dari sumber tepercaya dan menggunakan versi dependensi yang kompatibel.

## 9. Contoh Penggunaan

Masukkan data pelanggan:
- Recency: 12 hari.
- Frequency: 8 transaksi.
- Monetary: Rp400.000.

Hasil prediksi model:
- Cluster: 0.
- Segmen: Aktif Berorientasi Promo.
- Strategi: Bundling dan Promo Pembelian Berulang.

Profil segmen merupakan kecenderungan kelompok, bukan kepastian perilaku individu.

## 10. Keterbatasan

- Dataset bersifat sintetis.
- Model dilatih menggunakan data ringkasan pelanggan, bukan transaksi real-time.
- Pelanggan tanpa riwayat transaksi belum didukung.
- Evaluasi menggunakan random split, bukan pengujian temporal.
- Rekomendasi promosi belum diuji menggunakan A/B testing.
- Efektivitas bisnis dan dampak finansial belum dapat disimpulkan.

## 11. Deployment


## 11. Deployment

Aplikasi telah di-deploy menggunakan Streamlit Community Cloud.

**Live Application:**  
https://segmentasi-pelanggan-umkm-rafi.streamlit.app/

Konfigurasi deployment:
- Repository: rafihabibi16/segmentasi-pelanggan-umkm
- Branch: main
- Entry point: app.py
- Framework: Streamlit
- Model: StandardScaler + K-Means (k=4)

Pengujian aplikasi publik mencakup akses halaman, dashboard Overview, eksplorasi segmen, prediksi pelanggan baru, rekomendasi promosi, dan ekspor CSV.

Aplikasi menggunakan model yang sudah dilatih dan disimpan sebagai file `.joblib`, tanpa melakukan training ulang ketika digunakan.


## 12. Dokumentasi Eksperimen


## 12. Dokumentasi Eksperimen

Notebook eksperimen Machine Learning tersedia di folder:

[`notebooks/`](notebooks/)

Notebook mendokumentasikan:
1. Data understanding dan audit kualitas data.
2. Data cleaning dan exploratory data analysis.
3. Pembagian training, validation, dan holdout test.
4. Feature selection RFM.
5. Baseline K-Means untuk k=2 hingga k=8.
6. Customer profiling dan interpretasi bisnis.
7. Eksperimen transformasi Log1p.
8. Eksperimen penambahan fitur promo.
9. Evaluasi stabilitas dan sensitivitas model.
10. Evaluasi final pada holdout test set.

Model final menggunakan StandardScaler dan K-Means dengan k=4.

Silhouette akhir:
- Training (sampel 1.500): 0,5525.
- Validation (1.500): 0,5619.
- Holdout test (1.500): 0,5497.

Untuk menjalankan ulang eksperimen, gunakan notebook dan dataset sumber yang dijelaskan pada bagian Dataset.

Catatan: proses reproduksi memerlukan penyesuaian apabila terdapat path Google Drive khusus lingkungan Google Colab.


## 13. Informasi Tim

Nama anggota dan pembagian tugas akan dilengkapi sebelum pengumpulan.
