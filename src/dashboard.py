
"""
Dashboard analitik segmentasi pelanggan UMKM.

Menampilkan statistik hasil customer profiling
berdasarkan 7.000 pelanggan training.
"""

import json
from pathlib import Path
from src.recommendations import get_promotion_recommendation

import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent.parent

PROFILE_PATH = (
    PROJECT_DIR / "artifacts" / "cluster_profiles.json"
)


def load_cluster_profiles():
    """Membaca statistik cluster dari JSON."""

    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []

    for cluster_id, info in data["clusters"].items():
        records.append({
            "cluster": int(cluster_id),
            "nama": info["nama"],
            "jumlah_pelanggan": info["jumlah_pelanggan"],
            "persen_pelanggan": info["persen_pelanggan"],
            "recency_mean": info["recency_mean"],
            "frequency_mean": info["frequency_mean"],
            "monetary_mean": info["monetary_mean"],
            "promo_mean": info["promo_mean"],
            "kategori_acara_pct": info["kategori_acara_pct"]
        })

    df = pd.DataFrame(records).sort_values("cluster")

    if df["jumlah_pelanggan"].sum() != data["jumlah_training"]:
        raise ValueError(
            "Total pelanggan tidak sesuai metadata profiling."
        )

    if set(df["cluster"]) != {0, 1, 2, 3}:
        raise ValueError("ID cluster tidak lengkap.")

    return df, data


def render_overview():
    """Menampilkan halaman Overview Segmen."""

    st.title("Overview Segmentasi Pelanggan")

    st.write(
        "Ringkasan karakteristik pelanggan UMKM "
        "berdasarkan model K-Means RFM."
    )

    st.caption(
        "Sumber: customer profiling training set "
        "(7.000 pelanggan sintetis)."
    )

    try:
        df, data = load_cluster_profiles()
    except (OSError, ValueError, KeyError) as error:
        st.error(f"Gagal membaca profil cluster: {error}")
        return

    # ==============================================
    # A. KARTU KPI
    # ==============================================

    total = int(df["jumlah_pelanggan"].sum())

    segmen_terbesar = df.loc[
        df["jumlah_pelanggan"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Pelanggan Training",
        f"{total:,}".replace(",", ".")
    )

    col2.metric(
        "Jumlah Segmen",
        len(df)
    )

    col3.metric(
        "Segmen Terbesar",
        f"Cluster {int(segmen_terbesar['cluster'])}",
        delta=None
    )

    st.caption(
        f"Cluster {int(segmen_terbesar['cluster'])} "
        f"mewakili {segmen_terbesar['persen_pelanggan']:.2f}% "
        "pelanggan training."
    )

    st.divider()

    # ==============================================
    # B. DISTRIBUSI CLUSTER
    # ==============================================

    st.subheader("Distribusi Pelanggan")

    df_chart = df.copy()
    df_chart["label"] = df_chart["cluster"].apply(
        lambda x: f"Cluster {x}"
    )

    st.bar_chart(
        df_chart,
        x="label",
        y="jumlah_pelanggan",
        color="#80583F",
        height=330
    )

    st.caption(
        "Grafik menunjukkan jumlah pelanggan "
        "training pada masing-masing cluster."
    )

    st.divider()

    # ==============================================
    # C. PERBANDINGAN RECENCY & FREQUENCY
    # ==============================================

    st.subheader("Perbandingan Perilaku Transaksi")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("**Rata-rata Recency (hari)**")

        st.bar_chart(
            df_chart,
            x="label",
            y="recency_mean",
            color="#A67B5B",
            height=300
        )

    with col_right:
        st.markdown("**Rata-rata Frequency (transaksi)**")

        st.bar_chart(
            df_chart,
            x="label",
            y="frequency_mean",
            color="#6B8A75",
            height=300
        )

    st.divider()

    # ==============================================
    # D. PERBANDINGAN MONETARY
    # ==============================================

    st.subheader("Rata-rata Total Belanja Pelanggan")

    df_chart["monetary_juta"] = (
        df_chart["monetary_mean"] / 1_000_000
    )

    st.bar_chart(
        df_chart,
        x="label",
        y="monetary_juta",
        color="#80583F",
        height=320
    )

    st.caption(
        "Satuan grafik: juta rupiah per pelanggan "
        "selama enam bulan, berdasarkan rata-rata "
        "total belanja anggota cluster."
    )

    st.divider()

    # ==============================================
    # E. TABEL RINGKASAN SEGMEN
    # ==============================================

    st.subheader("Ringkasan Empat Segmen")

    tabel = df[
        [
            "cluster",
            "nama",
            "jumlah_pelanggan",
            "recency_mean",
            "frequency_mean",
            "monetary_mean",
            "promo_mean"
        ]
    ].copy()

    tabel.columns = [
        "Cluster",
        "Nama Segmen",
        "Pelanggan",
        "Recency (hari)",
        "Frequency",
        "Monetary (Rp)",
        "Penggunaan Promo (%)"
    ]

    st.dataframe(
        tabel,
        hide_index=True,
        use_container_width=True
    )

    
    # ==============================================
    # F. DETAIL SEGMEN DAN STRATEGI PROMOSI
    # ==============================================

    st.divider()
    st.subheader("Eksplorasi Detail Segmen")

    st.write(
        "Pilih segmen untuk melihat karakteristik "
        "pelanggan dan rekomendasi strategi promosi."
    )

    nama_segmen = dict(zip(df["cluster"], df["nama"]))

    selected_cluster = st.selectbox(
        "Pilih segmen pelanggan",
        options=df["cluster"].tolist(),
        format_func=lambda cid: (
            f"Cluster {cid} — {nama_segmen[cid]}"
        )
    )

    selected = df.loc[
        df["cluster"] == selected_cluster
    ].iloc[0]

    promotion = get_promotion_recommendation(
        int(selected_cluster)
    )

    st.markdown(f"### {selected['nama']}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Jumlah Pelanggan",
        f"{int(selected['jumlah_pelanggan']):,}"
        .replace(",", ".")
    )

    col2.metric(
        "Rata-rata Recency",
        f"{selected['recency_mean']:.1f} hari"
    )

    col3.metric(
        "Rata-rata Frequency",
        f"{selected['frequency_mean']:.1f} transaksi"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Rata-rata Monetary",
        "Rp" + f"{selected['monetary_mean']:,.0f}"
        .replace(",", ".")
    )

    col5.metric(
        "Rata-rata Penggunaan Promo",
        f"{selected['promo_mean']:.1f}%"
    )

    col6.metric(
        "Kategori Favorit Acara",
        f"{selected['kategori_acara_pct']:.1f}%"
    )

    st.markdown("#### Strategi Promosi yang Disarankan")

    st.markdown(f"**{promotion['strategy']}**")

    st.write(promotion["recommendation"])

    st.markdown("**Dasar rekomendasi:**")
    st.write(promotion["reason"])

    st.markdown("**Indikator keberhasilan:**")
    st.write(promotion["success_metric"])

    st.caption(
        "Statistik berasal dari data training. "
        "Rekomendasi bersifat rule-based dan "
        "efektivitasnya belum diuji pada kampanye nyata."
    )


    st.info(
        "Semua statistik merupakan ringkasan "
        "data training. Dashboard ini belum "
        "menampilkan transaksi pelanggan secara "
        "real-time dan belum mengukur efektivitas "
        "kampanye promosi."
    )

    st.divider()

    st.caption(
        "Customer Segmentation UMKM | "
        "K-Means RFM | Academic Prototype"
    )
