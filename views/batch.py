import io
import pandas as pd
import streamlit as st
import plotly.express as px
from utils.model_loader import predict_batch, model_is_available

# CSS Injection for Batch Page (Modern & Simple)
st.markdown("""
<style>
    /* Card Container */
    .batch-card-container-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    /* File Uploader override */
    [data-testid="stFileUploader"] {
        border: 1px dashed #cbd5e1 !important;
        background-color: #f8fafc !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        transition: border-color 0.15s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #2563eb !important;
        background-color: #eff6ff !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Analisis Batch")
st.caption("Unggah file CSV berisi ulasan produk untuk memproses klasifikasi sentimen secara massal.")

# Upload Container
st.markdown('<div class="batch-card-container-flat">', unsafe_allow_html=True)
uploaded = st.file_uploader(
    "Seret dan letakkan file CSV di sini, atau klik untuk memilih file",
    type=["csv"],
    help="Maks: 20MB · Kolom teks harus ada",
)
st.caption("Format: CSV • Maks: 20MB • Harus mengandung minimal satu kolom teks ulasan.")
st.caption("Gunakan file contoh di folder proyek Anda: `sample_data/contoh_ulasan.csv` untuk mencoba.")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Gagal membaca CSV: {e}")
        st.stop()

    if df.empty:
        st.warning("File CSV kosong.")
        st.stop()

    st.write("")
    
    st.markdown('<div class="batch-card-container-flat">', unsafe_allow_html=True)
    st.markdown("<b style='color:#334155; font-size:0.88rem;'>Konfigurasi Analisis</b>", unsafe_allow_html=True)
    st.write("")
    
    text_col = st.selectbox(
        "Pilih kolom yang berisi teks ulasan:",
        options=list(df.columns),
        index=0,
    )

    max_rows = st.slider("Jumlah baris yang diproses (batasi untuk demo cepat)", 1, len(df), min(len(df), 200))
    run = st.button("Jalankan Analisis Batch", icon=":material/play_arrow:", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if run:
        subset = df.head(max_rows).copy()
        texts = subset[text_col].astype(str).tolist()

        progress_bar = st.progress(0.0, text="Memproses ulasan...")

        def _cb(frac):
            progress_bar.progress(frac, text=f"Memproses ulasan... {int(frac*100)}%")

        results = predict_batch(texts, progress_callback=_cb)
        progress_bar.empty()

        subset["Sentimen"] = [r[0] for r in results]
        subset["Confidence"] = [round(r[1] * 100, 2) for r in results]

        st.success(f"Selesai. {len(subset)} ulasan berhasil dianalisis.")

        st.markdown("#### Hasil Analisis")
        st.dataframe(subset, use_container_width=True, height=320)

        st.write("")
        col_pie, col_bar = st.columns(2)
        sent_counts = subset["Sentimen"].value_counts().reindex(["Positive", "Negative"]).fillna(0)

        # Plotly chart settings for simple look
        plotly_layout_defaults = dict(
            font=dict(family="Plus Jakarta Sans", size=11, color="#475569"),
            title_font=dict(family="Outfit", size=14, color="#0f172a"),
            margin=dict(l=15, r=15, t=40, b=15),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )

        with col_pie:
            fig_pie = px.pie(
                names=["Positif", "Negatif"],
                values=[sent_counts.get("Positive", 0), sent_counts.get("Negative", 0)],
                color=["Positif", "Negatif"],
                color_discrete_map={"Positif": "#10b981", "Negatif": "#ef4444"},
                title="Proporsi Sentimen",
                hole=0.45,
            )
            fig_pie.update_layout(**plotly_layout_defaults)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_bar:
            fig_bar = px.bar(
                x=["Positif", "Negatif"],
                y=[sent_counts.get("Positive", 0), sent_counts.get("Negative", 0)],
                color=["Positif", "Negatif"],
                color_discrete_map={"Positif": "#10b981", "Negatif": "#ef4444"},
                labels={"x": "Sentimen", "y": "Jumlah Ulasan"},
                title="Distribusi Sentimen",
            )
            fig_bar.update_layout(showlegend=False, **plotly_layout_defaults)
            fig_bar.update_xaxes(showgrid=False)
            fig_bar.update_yaxes(gridcolor="#e2e8f0")
            st.plotly_chart(fig_bar, use_container_width=True)

        csv_buffer = io.StringIO()
        subset.to_csv(csv_buffer, index=False)
        
        st.write("")
        st.download_button(
            label="Unduh Hasil Analisis (CSV)",
            data=csv_buffer.getvalue(),
            file_name="hasil_analisis_sentimen.csv",
            mime="text/csv",
            icon=":material/download:",
            use_container_width=True,
        )
else:
    st.markdown("""
    <div style="background:#f8fafc; border:1px dashed #e2e8f0; border-radius:10px; padding:2rem; text-align:center; color:#94a3b8; font-size:0.85rem;">
        Unggah file CSV di atas untuk memulai analisis.
    </div>
    """, unsafe_allow_html=True)

if not model_is_available():
    st.markdown("""
    <div style="background:#fffbeb; border:1px solid #fef3c7; border-radius:6px; padding:0.75rem 1rem; margin-top:1.5rem; font-size:0.75rem; color:#b45309;">
        Sistem berjalan dalam mode demo. Unggah model terlatih ke folder <code>model/indobert_sentiment_final/</code> untuk menggunakan model IndoBERT asli.
    </div>
    """, unsafe_allow_html=True)
