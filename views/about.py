import streamlit as st

# CSS Injection for About Page (Minimalist, Outlined with Blue Accents)
st.markdown("""
<style>
    .about-section-card-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    .section-title-flat {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.85rem;
        border-left: 3px solid #2563eb; /* Modern Blue Accent */
        padding-left: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Team Member Cards */
    .team-card-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem 1rem;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.15s ease;
    }
    
    .team-card-flat:hover {
        border-color: #3b82f6;
    }
    
    .avatar-circle-flat {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin: 0 auto 0.75rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
        font-weight: 700;
        color: #2563eb; /* Modern Blue text */
        background-color: #eff6ff; /* Soft Blue background */
        border: 1px solid #bfdbfe;
    }
    
    .team-name-flat {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.15rem;
        line-height: 1.3;
    }
    
    .team-id-flat {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-bottom: 0.75rem;
    }
    
    .team-role-flat {
        font-size: 0.7rem;
        color: #1e40af;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
        line-height: 1.2;
        display: inline-block;
    }
    
    /* Project Banner Box (Modern Dark Blue) */
    .project-header-card-flat {
        background-color: #1e3a8a; /* Modern Dark Blue */
        border-radius: 10px;
        padding: 1.5rem;
        color: #f8fafc;
        margin-bottom: 1.5rem;
    }
    
    .project-header-card-flat h3 {
        color: #ffffff !important;
        margin-top: 0;
        font-size: 1.25rem;
        font-weight: 700;
        line-height: 1.3;
    }
    
    /* Custom List Outline */
    .custom-list-flat {
        list-style-type: none;
        padding-left: 0;
        margin: 0;
    }
    
    .custom-list-flat li {
        position: relative;
        padding-left: 1rem;
        margin-bottom: 0.4rem;
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.4;
    }
    
    .custom-list-flat li::before {
        content: "•";
        position: absolute;
        left: 0;
        color: #2563eb; /* Modern Blue list bullet */
        font-weight: bold;
    }
    
    .methodology-step-flat {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
    }
    
    .methodology-step-flat:last-child {
        margin-bottom: 0;
    }
    
    .step-number-flat {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background-color: #2563eb; /* Modern Blue step badge */
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    .step-content-flat {
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Tentang SentiMart")
st.caption("Detail proyek akhir, metadata dataset, arsitektur model NLP, dan tim pengembang.")

# Project Title Header
st.markdown("""
<div class="project-header-card-flat">
    <div style="font-size: 0.65rem; font-weight:700; color: #cbd5e1; text-transform:uppercase; letter-spacing:0.05em; margin-bottom: 0.3rem;">Judul Proyek Akhir</div>
    <h3>"Analisis Sentimen Ulasan Pengguna E-Commerce Indonesia Menggunakan IndoBERT"</h3>
    <div style="font-size: 0.8rem; color: #e2e8f0; margin-top: 0.4rem; line-height: 1.4;">
        Proyek Akhir Praktikum Natural Language Processing (NLP) — Teknik Informatika, Politeknik Caltex Riau.
    </div>
</div>
""", unsafe_allow_html=True)

col_dataset, col_model = st.columns(2)

with col_dataset:
    st.markdown('<div class="about-section-card-flat">', unsafe_allow_html=True)
    st.markdown('<div class="section-title-flat">Dataset PRDECT-ID</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="custom-list-flat">
        <li><b>Nama:</b> PRDECT-ID Dataset</li>
        <li><b>Sumber:</b> Hugging Face — <code>ZakyF/PRDECT-ID</code></li>
        <li><b>Lisensi:</b> Creative Commons Attribution 4.0 (CC BY 4.0)</li>
        <li><b>Ukuran:</b> 5.400 ulasan (dari 29 kategori produk e-commerce)</li>
        <li><b>Sentimen Positif:</b> 2.579 ulasan (rating dominan 4-5)</li>
        <li><b>Sentimen Negatif:</b> 2.821 ulasan (rating dominan 1-2)</li>
        <li><b>Fitur Dipakai:</b> Customer Review, Customer Rating, Sentiment</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_model:
    st.markdown('<div class="about-section-card-flat">', unsafe_allow_html=True)
    st.markdown('<div class="section-title-flat">Arsitektur &amp; Model</div>', unsafe_allow_html=True)
    st.markdown("""
    <ul class="custom-list-flat">
        <li><b>Base Model:</b> <code>indobenchmark/indobert-base-p1</code></li>
        <li><b>Metode:</b> Fine-tuning (Sequence Classification)</li>
        <li><b>Arsitektur:</b> BERT-Base (12 Transformer blocks, 768 hidden, 12 heads) + Linear classifier head di atas representasi token <code>[CLS]</code></li>
        <li><b>Max Token Length:</b> 128 tokens</li>
        <li><b>Baseline Pembanding:</b> TF-IDF + Logistic Regression</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Methodology Section
st.markdown('<div class="about-section-card-flat">', unsafe_allow_html=True)
st.markdown('<div class="section-title-flat">Metodologi Penelitian</div>', unsafe_allow_html=True)

steps = [
    "<b>Eksplorasi &amp; Memuat Data (EDA):</b> Membaca dataset PRDECT-ID dan menganalisis distribusi kelas sentimen.",
    "<b>Pembersihan &amp; Normalisasi:</b> Menghapus pengulangan huruf berlebih dan memetakan slang kata (misal: 'gw' -> 'aku').",
    "<b>Pembagian Dataset (Split):</b> Membagi ulasan secara terstratifikasi (Stratified Split) dengan rasio 80% Latih dan 20% Uji.",
    "<b>Fine-Tuning IndoBERT:</b> Melatih model dasar IndoBERT base selama 5 epoch dengan Learning Rate 2e-5 dan Batch Size 16.",
    "<b>Evaluasi Model:</b> Mengukur nilai Accuracy, Precision, Recall, F1-Score, dan menghitung visualisasi Confusion Matrix.",
    "<b>Deployment:</b> Mengemas model terlatih ke dalam aplikasi web interaktif berbasis Streamlit menggunakan virtual environment."
]

for idx, step in enumerate(steps):
    st.markdown(f"""
    <div class="methodology-step-flat">
        <div class="step-number-flat">{idx+1}</div>
        <div class="step-content-flat">{step}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Team Section
st.markdown("<h4 style='color:#0f172a; text-align:center; margin-bottom:1.2rem; margin-top: 1rem;'>TIM PENGEMBANG — KELOMPOK 5, 3TIB</h4>", unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("""
    <div class="team-card-flat">
        <div>
            <div class="avatar-circle-flat">EG</div>
            <div class="team-name-flat">Elviana Golina</div>
            <div class="team-id-flat">NIM. 2355301057</div>
        </div>
        <div class="team-role-flat">Data Modelling &amp; Laporan</div>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
    <div class="team-card-flat">
        <div>
            <div class="avatar-circle-flat">HZ</div>
            <div class="team-name-flat">Hadid Zarid Nawfal</div>
            <div class="team-id-flat">NIM. 2355301079</div>
        </div>
        <div class="team-role-flat">Wireframe &amp; Laporan</div>
    </div>
    """, unsafe_allow_html=True)
with t3:
    st.markdown("""
    <div class="team-card-flat">
        <div>
            <div class="avatar-circle-flat">HW</div>
            <div class="team-name-flat">Hardana Wijaya</div>
            <div class="team-id-flat">NIM. 2355301080</div>
        </div>
        <div class="team-role-flat">Deploy &amp; Frontend Dev</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.75rem; margin-top: 0.8rem;">
    Dosen Pengampu: Yuliska, S.T., M.Eng. &nbsp;•&nbsp; Instruktur Laboratorium: Oky Firnanda, S.Tr.Kom
</div>
""", unsafe_allow_html=True)
