import streamlit as st
from utils.model_loader import predict_sentiment, model_is_available

# CSS Injection for Modern Minimalist Prediction Page
st.markdown("""
<style>
    /* Button Customization (Outlined / Flat - Modern Blue) */
    button[kind="primary"] {
        background-color: #2563eb !important; /* Flat modern blue */
        color: #ffffff !important;
        border: 1px solid #2563eb !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: background-color 0.15s ease !important;
    }
    button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }

    button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: background-color 0.15s ease !important;
    }
    button[kind="secondary"]:hover {
        background-color: #f8fafc !important;
        border-color: #94a3b8 !important;
        color: #0f172a !important;
    }

    /* Example tags layout */
    .example-section button[kind="secondary"] {
        background-color: #f8fafc !important;
        color: #475569 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        padding: 0.5rem 0.75rem !important;
        text-align: left !important;
        min-height: 55px !important;
        white-space: normal !important;
        line-height: 1.4 !important;
        font-weight: 400 !important;
        display: block !important;
    }
    .example-section button[kind="secondary"]:hover {
        background-color: #f0f9ff !important;
        border-color: #3b82f6 !important;
        color: #1d4ed8 !important;
    }

    /* Flat Alert Banners */
    .result-card-pos-flat {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 1.25rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .result-card-neg-flat {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1.25rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .result-icon-svg {
        display: flex;
        align-items: center;
        flex-shrink: 0;
    }

    .result-icon-svg.pos {
        color: #16a34a;
    }

    .result-icon-svg.neg {
        color: #dc2626;
    }

    .result-label-header-flat {
        font-size: 0.65rem;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.1rem;
    }

    .result-label-pos-flat {
        color: #16a34a;
        font-weight: 700;
        font-size: 1.3rem;
        line-height: 1;
    }

    .result-label-neg-flat {
        color: #dc2626;
        font-weight: 700;
        font-size: 1.3rem;
        line-height: 1;
    }

    /* Probs Container */
    .probs-container-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
    }
    
    .probs-header-flat {
        font-size: 0.85rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .prob-item-flat {
        margin-bottom: 0.85rem;
    }
    
    .prob-item-flat:last-child {
        margin-bottom: 0;
    }

    .prob-label-row-flat {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.3rem;
    }

    .prob-bar-bg-flat {
        background-color: #f1f5f9;
        height: 8px;
        border-radius: 99px;
        overflow: hidden;
        width: 100%;
    }

    .prob-bar-fill-flat {
        height: 100%;
        border-radius: 99px;
    }

    .prob-bar-fill-flat.pos {
        background-color: #10b981;
    }

    .prob-bar-fill-flat.neg {
        background-color: #ef4444;
    }
    
    .card-input-container-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Prediksi Sentimen")
st.caption("Ketik atau pilih contoh ulasan produk e-commerce berbahasa Indonesia untuk menganalisis sentimen.")

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

# Input Form
st.markdown('<div class="card-input-container-flat">', unsafe_allow_html=True)
st.markdown("<b style='color:#334155; font-size:0.88rem;'>Teks Ulasan</b>", unsafe_allow_html=True)
text = st.text_area(
    label="review_input",
    value=st.session_state.review_text,
    placeholder="Masukkan ulasan di sini... Contoh: Barang sangat bagus, pengiriman super cepat, seller ramah.",
    height=120,
    label_visibility="collapsed",
)

col_left, col_reset, col_submit = st.columns([3.2, 0.9, 1.4])
with col_left:
    st.markdown(f"<span style='font-size:0.75rem; color:#94a3b8; font-weight:500;'>{len(text)} karakter</span>", unsafe_allow_html=True)
with col_reset:
    reset_clicked = st.button("Reset", icon=":material/refresh:", use_container_width=True)
with col_submit:
    submit_clicked = st.button("Analisis", icon=":material/search:", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if reset_clicked:
    st.session_state.review_text = ""
    st.rerun()

# Examples (Modern Outlined Tags)
st.markdown("<h6 style='color:#64748b; font-size:0.75rem; letter-spacing:0.04em; text-transform:uppercase; margin-bottom:0.6rem;'>PILIH CONTOH ULASAN</h6>", unsafe_allow_html=True)
examples = [
    "Produk sangat bagus, pengiriman cepat and packing aman. Seller ramah dan responsif!",
    "Kecewa banget, barang datang rusak dan berbeda dari foto. Sudah komplain tapi tidak ada tanggapan.",
    "Kualitas standar sesuai harga, pengiriman lumayan cepat 3 hari sampai. Lumayan lah.",
]

st.markdown('<div class="example-section">', unsafe_allow_html=True)
ex_cols = st.columns(3)
for i, ex in enumerate(examples):
    with ex_cols[i]:
        if st.button(ex, key=f"ex_{i}", use_container_width=True):
            st.session_state.review_text = ex
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# Result Display
if submit_clicked:
    if not text.strip():
        st.warning("Masukkan teks ulasan terlebih dahulu.")
    else:
        with st.spinner("Menganalisis sentimen..."):
            label, confidence, probs = predict_sentiment(text)

        prob_pos = probs['Positive'] * 100
        prob_neg = probs['Negative'] * 100

        if label == "Positive":
            # Outlined checklist icon for positive
            st.markdown(f"""
            <div class="result-card-pos-flat">
                <div class="result-icon-svg pos">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                </div>
                <div>
                    <div class="result-label-header-flat">Hasil Klasifikasi</div>
                    <div class="result-label-pos-flat">POSITIF</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Outlined alert icon for negative
            st.markdown(f"""
            <div class="result-card-neg-flat">
                <div class="result-icon-svg neg">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                </div>
                <div>
                    <div class="result-label-header-flat">Hasil Klasifikasi</div>
                    <div class="result-label-neg-flat">NEGATIF</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Probabilities Custom Dashboard
        st.markdown(f"""
        <div class="probs-container-flat">
            <div class="probs-header-flat">Probabilitas Kepercayaan Model</div>
            
            <div class="prob-item-flat">
                <div class="prob-label-row-flat">
                    <span>Sentimen Positif</span>
                    <span>{prob_pos:.2f}%</span>
                </div>
                <div class="prob-bar-bg-flat">
                    <div class="prob-bar-fill-flat pos" style="width: {prob_pos}%;"></div>
                </div>
            </div>
            
            <div class="prob-item-flat" style="margin-top: 1rem;">
                <div class="prob-label-row-flat">
                    <span>Sentimen Negatif</span>
                    <span>{prob_neg:.2f}%</span>
                </div>
                <div class="prob-bar-bg-flat">
                    <div class="prob-bar-fill-flat neg" style="width: {prob_neg}%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:#f8fafc; border:1px dashed #e2e8f0; border-radius:10px; padding:1.5rem; text-align:center; color:#94a3b8; font-size:0.85rem;">
        Hasil analisis sentimen akan ditampilkan di sini.
    </div>
    """, unsafe_allow_html=True)

if not model_is_available():
    st.markdown("""
    <div style="background:#fffbeb; border:1px solid #fef3c7; border-radius:6px; padding:0.75rem 1rem; margin-top:1.5rem; font-size:0.75rem; color:#b45309;">
        Sistem berjalan dalam mode demo. Letakkan model terlatih Anda di folder <code>model/indobert_sentiment_final/</code> untuk analisis aktual.
    </div>
    """, unsafe_allow_html=True)
