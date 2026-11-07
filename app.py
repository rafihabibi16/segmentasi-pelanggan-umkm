
"""
Aplikasi Segmentasi Pelanggan UMKM
Machine Learning - K-Means RFM
"""

import pandas as pd
import streamlit as st
from src.service import segment_customer
from src.dashboard import render_overview



# =====================================================
# 1. KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Customer Segmentation | UMKM",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. STYLING DASAR
# =====================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #FAF8F5;
        }

        h1, h2, h3 {
            color: #453428;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 16px;
            border-radius: 12px;
            border: 1px solid #E9E3DC;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 3. SIDEBAR
# =====================================================

with st.sidebar:

    st.title("☕ UMKM Analytics")

    st.caption(
        "Customer Intelligence & "
        "Promotion Recommendation"
    )

    st.divider()

    page = st.radio(
        "Navigasi",
        [
            "📊 Overview Segmen",
            "🔎 Analisis Pelanggan"
        ]
    )

    st.markdown("### Tentang Sistem")

    st.write(
        "Aplikasi ini membantu pemilik UMKM "
        "bakery dan coffee shop memahami "
        "karakteristik pelanggan dan "
        "menentukan strategi promosi."
    )

    st.markdown("**Model:** K-Means Clustering")
    st.markdown("**Fitur:** RFM")
    st.markdown("**Jumlah segmen:** 4")

    st.divider()

    st.caption(
        "Prototipe akademik berbasis dataset "
        "sintetis. Rekomendasi promosi "
        "belum diuji melalui kampanye nyata."
    )


# =====================================================
# NAVIGASI HALAMAN
# =====================================================

if page == "📊 Overview Segmen":
    render_overview()
    st.stop()

# =====================================================
# 4. HEADER
# =====================================================

st.title("Customer Segmentation Dashboard")

st.write(
    "Analisis segmentasi pelanggan dan "
    "rekomendasi strategi promosi "
    "berbasis Machine Learning."
)

st.divider()


# =====================================================
# 5. FORM INPUT PELANGGAN
# =====================================================

st.subheader("Analisis Pelanggan")

st.caption(
    "Masukkan ringkasan transaksi pelanggan "
    "selama enam bulan."
)

with st.form("customer_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        recency = st.number_input(
            "Recency (hari)",
            min_value=0,
            value=12,
            step=1,
            help=(
                "Jumlah hari sejak pelanggan "
                "terakhir bertransaksi."
            )
        )

    with col2:
        frequency = st.number_input(
            "Frequency (transaksi)",
            min_value=1,
            value=8,
            step=1,
            help=(
                "Jumlah transaksi pelanggan "
                "dalam enam bulan terakhir."
            )
        )

    with col3:
        monetary = st.number_input(
            "Monetary (Rp)",
            min_value=1,
            value=400000,
            step=10000,
            help=(
                "Total nilai belanja pelanggan "
                "dalam enam bulan terakhir."
            )
        )

    submitted = st.form_submit_button(
        "Analisis Segmen Pelanggan",
        type="primary",
        use_container_width=True
    )


# =====================================================
# 6. PREDIKSI MODEL
# =====================================================

if submitted:

    customer = {
        "hari_sejak_transaksi_terakhir": recency,
        "jumlah_transaksi_6bln": frequency,
        "total_belanja_rp": monetary
    }

    try:
        result = segment_customer(customer)

        st.session_state["result"] = result
        st.session_state["customer"] = customer

    except (ValueError, KeyError, FileNotFoundError) as error:

        st.session_state.pop("result", None)
        st.session_state.pop("customer", None)

        st.error(f"Prediksi gagal: {error}")


# =====================================================
# 7. TAMPILAN HASIL SEGMENTASI
# =====================================================

if "result" in st.session_state:

    result = st.session_state["result"]
    customer = st.session_state["customer"]

    st.divider()

    st.subheader("Hasil Segmentasi Pelanggan")

    st.success(
        f"Cluster {result['cluster_id']} — "
        f"{result['segment_name']}"
    )

    st.markdown("#### Ringkasan Data Pelanggan")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Recency",
        f"{customer['hari_sejak_transaksi_terakhir']} hari"
    )

    col2.metric(
        "Frequency",
        f"{customer['jumlah_transaksi_6bln']} transaksi"
    )

    col3.metric(
        "Monetary",
        "Rp" + format(
            customer["total_belanja_rp"], ","
        ).replace(",", ".")
    )

    st.markdown("#### Karakteristik Segmen")

    st.info(result["segment_description"])

    st.caption(
        "Karakteristik ini merupakan profil "
        "umum kelompok, bukan kepastian "
        "perilaku setiap pelanggan."
    )

    st.divider()

    # =================================================
    # 8. REKOMENDASI PROMOSI
    # =================================================

    promotion = result["promotion"]

    st.subheader("Rekomendasi Strategi Promosi")

    st.markdown(
        f"### {promotion['strategy']}"
    )

    st.markdown("**Rekomendasi:**")
    st.write(promotion["recommendation"])

    st.markdown("**Dasar Rekomendasi:**")
    st.write(promotion["reason"])

    st.markdown("**Indikator Evaluasi:**")
    st.write(promotion["success_metric"])

    st.caption(
        "Strategi bersifat rule-based "
        "berdasarkan hasil profiling cluster. "
        "Efektivitasnya perlu divalidasi "
        "melalui evaluasi kampanye."
    )

    
    # =================================================
    # 9. EKSPOR HASIL SEGMENTASI
    # =================================================

    st.divider()
    st.subheader("Unduh Hasil Analisis")

    export_data = {
        "recency_hari": customer[
            "hari_sejak_transaksi_terakhir"
        ],
        "frequency_6bln": customer[
            "jumlah_transaksi_6bln"
        ],
        "monetary_rp": customer[
            "total_belanja_rp"
        ],
        "cluster_id": result["cluster_id"],
        "nama_segmen": result["segment_name"],
        "karakteristik_segmen": result[
            "segment_description"
        ],
        "strategi_promosi": promotion["strategy"],
        "rekomendasi": promotion["recommendation"],
        "alasan": promotion["reason"],
        "indikator_evaluasi": promotion[
            "success_metric"
        ]
    }

    df_export = pd.DataFrame([export_data])

    csv_data = df_export.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Unduh Hasil Segmentasi (CSV)",
        data=csv_data,
        file_name="hasil_segmentasi_pelanggan.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "File CSV berisi data pelanggan, hasil "
        "segmentasi, dan rekomendasi promosi."
    )


else:

    st.info(
        "Isi formulir di atas, kemudian klik "
        "'Analisis Segmen Pelanggan' "
        "untuk melihat hasil."
    )


# =====================================================
# 9. FOOTER
# =====================================================

st.divider()

st.caption(
    "Customer Segmentation UMKM | "
    "K-Means RFM | Academic Prototype"
)
