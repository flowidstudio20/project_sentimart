import streamlit as st
from utils.metrics_data import load_metrics

# ---------- Global style (Modern, Simple, Flat with Blue Accents) ----------
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    
    /* Minimalist Hero Section */
    .hero-container-flat {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
    }
    
    .hero-title-flat {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        line-height: 1.2;
        margin-bottom: 0.8rem;
        color: #0f172a;
    }
    
    .hero-subtitle-flat {
        font-size: 1.05rem;
        color: #475569;
        max-width: 780px;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }
    
    /* Clean Blue Badge */
    .badge-model-flat {
        display: inline-flex;
        align-items: center;
        background: #eff6ff;
        color: #1d4ed8;
        padding: 0.3rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
        border: 1px solid #bfdbfe;
    }
    
    .badge-status-dot-flat {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
        margin-right: 6px;
        display: inline-block;
    }

    /* Flat Metric Card */
    .stat-card-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .stat-card-flat:hover {
        border-color: #3b82f6;
    }
    
    .stat-value-flat {
        font-size: 2rem;
        font-weight: 700;
        color: #2563eb; /* Modern Blue */
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }
    
    .stat-label-flat {
        font-size: 0.85rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.2rem;
    }
    
    .stat-sub-flat {
        font-size: 0.75rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* Minimalist Pipeline Diagram */
    .pipeline-section-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .pipeline-title-flat {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1.2rem;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .pipeline-grid-flat {
        display: grid;
        grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
        align-items: center;
        gap: 0.4rem;
    }
    
    .pipeline-card-flat {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.9rem;
        text-align: center;
        transition: all 0.15s ease;
    }
    
    .pipeline-card-flat:hover {
        border-color: #3b82f6;
        background-color: #f0f9ff;
    }
    
    .pipeline-icon-svg {
        color: #2563eb; /* Modern Blue icon */
        margin-bottom: 0.4rem;
        display: flex;
        justify-content: center;
    }
    
    .pipeline-name-flat {
        font-size: 0.8rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .pipeline-desc-flat {
        font-size: 0.7rem;
        color: #64748b;
        margin-top: 0.15rem;
        line-height: 1.3;
    }
    
    .pipeline-arrow-flat {
        color: #3b82f6;
        font-size: 1rem;
        text-align: center;
    }

    /* Flat Feature Cards */
    .feature-card-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        height: 100%;
        transition: border-color 0.15s ease;
    }
    
    .feature-card-flat:hover {
        border-color: #3b82f6;
    }
    
    .feature-header-flat {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-icon-svg-wrapper {
        color: #2563eb; /* Modern Blue icon */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .feature-title-flat {
        font-weight: 600;
        font-size: 0.95rem;
        color: #0f172a;
    }
    
    .feature-desc-flat {
        font-size: 0.8rem;
        color: #475569;
        line-height: 1.5;
    }
    
    .cta-hint-flat {
        background: #f0f9ff;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        font-size: 0.8rem;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #2563eb;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

metrics = load_metrics()

# Hero Section (Simple & Flat)
status_lbl = "mode demo" if metrics.get("is_demo") else "model aktif"
st.markdown(f"""
<div class="hero-container-flat">
    <div class="badge-model-flat">
        <span class="badge-status-dot-flat"></span>
        IndoBERT · Fine-Tuned ({status_lbl})
    </div>
    <h1 class="hero-title-flat">Analisis Sentimen Ulasan E-Commerce</h1>
    <p class="hero-subtitle-flat">
        Aplikasi klasifikasi sentimen biner berbasis model NLP IndoBERT untuk memahami ulasan produk e-commerce berbahasa Indonesia.
    </p>
    <div class="cta-hint-flat">
        <span>Informasi:</span> Gunakan menu navigasi di sidebar kiri untuk mencoba fitur analisis ulasan.
    </div>
</div>
""", unsafe_allow_html=True)

# 3 Metrics Row (Flat Cards)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="stat-card-flat">
        <div class="stat-value-flat">5,400+</div>
        <div class="stat-label-flat">Dataset PRDECT-ID</div>
        <div class="stat-sub-flat">Ulasan asli dari 29 kategori produk e-commerce Indonesia.</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-card-flat">
        <div class="stat-value-flat">{metrics["accuracy"]*100:.2f}%</div>
        <div class="stat-label-flat">Akurasi Model</div>
        <div class="stat-sub-flat">Akurasi hasil pengujian model IndoBERT base di dataset uji.</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="stat-card-flat">
        <div class="stat-value-flat">2 Kelas</div>
        <div class="stat-label-flat">Sentimen</div>
        <div class="stat-sub-flat">Klasifikasi biner untuk memisahkan ulasan ke kelas Positif atau Negatif.</div>
    </div>
    """, unsafe_allow_html=True)

# NLP Pipeline Section (Flat with SVG outline icons)
st.markdown("""
<div class="pipeline-section-flat">
    <div class="pipeline-title-flat">Alur Kerja Sistem (NLP Pipeline)</div>
    <div class="pipeline-grid-flat">
        <!-- Step 1 -->
        <div class="pipeline-card-flat">
            <div class="pipeline-icon-svg">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
            </div>
            <div class="pipeline-name-flat">1. Input Teks</div>
            <div class="pipeline-desc-flat">Ulasan pelanggan e-commerce</div>
        </div>
        <div class="pipeline-arrow-flat">➔</div>
        <!-- Step 2 -->
        <div class="pipeline-card-flat">
            <div class="pipeline-icon-svg">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            </div>
            <div class="pipeline-name-flat">2. Normalisasi</div>
            <div class="pipeline-desc-flat">Perbaikan slang &amp; huruf ganda</div>
        </div>
        <div class="pipeline-arrow-flat">➔</div>
        <!-- Step 3 -->
        <div class="pipeline-card-flat">
            <div class="pipeline-icon-svg">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line></svg>
            </div>
            <div class="pipeline-name-flat">3. Token &amp; Model</div>
            <div class="pipeline-desc-flat">Klasifikasi dengan IndoBERT</div>
        </div>
        <div class="pipeline-arrow-flat">➔</div>
        <!-- Step 4 -->
        <div class="pipeline-card-flat">
            <div class="pipeline-icon-svg">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle></svg>
            </div>
            <div class="pipeline-name-flat">4. Hasil Kelas</div>
            <div class="pipeline-desc-flat">Keluaran kelas Positif / Negatif</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# App Features
st.markdown("<h4 style='color:#0f172a; margin-bottom:1rem; text-align:center;'>FITUR UTAMA APLIKASI</h4>", unsafe_allow_html=True)

r1c1, r1c2 = st.columns(2)
with r1c1:
    st.markdown("""
    <div class="feature-card-flat">
        <div class="feature-header-flat">
            <div class="feature-icon-svg-wrapper">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            <div class="feature-title-flat">Prediksi Sentimen Tunggal</div>
        </div>
        <p class="feature-desc-flat">
            Analisis real-time untuk satu teks ulasan produk e-commerce. Model akan menampilkan hasil kelas dan nilai probabilitas keyakinan.
        </p>
    </div>
    """, unsafe_allow_html=True)
with r1c2:
    st.markdown("""
    <div class="feature-card-flat">
        <div class="feature-header-flat">
            <div class="feature-icon-svg-wrapper">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"></path></svg>
            </div>
            <div class="feature-title-flat">Analisis Batch CSV</div>
        </div>
        <p class="feature-desc-flat">
            Unggah berkas CSV ulasan untuk memproses klasifikasi secara massal. Dapatkan visualisasi ringkasan dan download hasil prediksi CSV.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown("""
    <div class="feature-card-flat">
        <div class="feature-header-flat">
            <div class="feature-icon-svg-wrapper">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
            </div>
            <div class="feature-title-flat">Performa Evaluasi Model</div>
        </div>
        <p class="feature-desc-flat">
            Tinjau metrik hasil evaluasi model IndoBERT base melalui confusion matrix dan visualisasi kurva loss latihan/validasi.
        </p>
    </div>
    """, unsafe_allow_html=True)
with r2c2:
    st.markdown("""
    <div class="feature-card-flat">
        <div class="feature-header-flat">
            <div class="feature-icon-svg-wrapper">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
            </div>
            <div class="feature-title-flat">Informasi Proyek</div>
        </div>
        <p class="feature-desc-flat">
            Detail mengenai dataset ulasan PRDECT-ID yang digunakan, arsitektur dasar model, diagram metodologi, dan data pengembang.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Minimalist Footer
st.markdown("<hr style='margin:3rem 0 1.5rem 0; border:0; border-top:1px solid #e2e8f0;'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color:#94a3b8; font-size:0.75rem; padding-bottom: 2rem;">
    SentiMart • TI Politeknik Caltex Riau
</div>
""", unsafe_allow_html=True)
