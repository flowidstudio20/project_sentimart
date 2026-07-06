import io
import re
import textwrap
import requests
from urllib.parse import urlparse
import pandas as pd
import streamlit as st
import plotly.express as px
from bs4 import BeautifulSoup
from utils.model_loader import predict_batch, model_is_available

# CSS Injection for Modern Minimalist URL Predict Page
st.markdown("""
<style>
    /* Card Container */
    .url-card-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1.2rem;
    }
    
    .url-info-box {
        background-color: #f0f9ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        color: #1e40af;
        font-size: 0.82rem;
        line-height: 1.5;
    }
    
    .url-warning-box {
        background-color: #fffbeb;
        border: 1px solid #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        color: #b45309;
        font-size: 0.82rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Analisis URL")
st.caption("Masukkan tautan (link) website umum atau artikel untuk mengekstrak dan menganalisis sentimen kontennya.")

# URL Form
st.markdown('<div class="url-card-flat">', unsafe_allow_html=True)
st.markdown("<b style='color:#334155; font-size:0.88rem;'>Masukkan Link URL</b>", unsafe_allow_html=True)
st.write("")

input_url = st.text_input(
    label="url_input",
    placeholder="Contoh: https://id.wikipedia.org/wiki/Kecerdasan_buatan atau link produk e-commerce...",
    label_visibility="collapsed"
)

col_run, col_clear = st.columns([1.2, 4])
with col_run:
    run_clicked = st.button("Analisis URL", icon=":material/web:", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if run_clicked:
    if not input_url.strip():
        st.warning("Masukkan link URL terlebih dahulu.")
    elif not re.match(r'^https?://', input_url.strip()):
        st.error("Format URL tidak valid. URL harus dimulai dengan http:// atau https://")
    else:
        url = input_url.strip()
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        # Check if it is a major Indonesian e-commerce domain
        is_ecommerce = any(eco in domain for eco in [
            "shopee.co.id", "shopee.com", "tokopedia.com", "tokopedia.link",
            "lazada.co.id", "bukalapak.com", "blibli.com"
        ])

        extracted_texts = []
        source_type = ""

        if is_ecommerce:
            source_type = "Simulasi E-Commerce (Cloudflare Bypass)"
            st.markdown(textwrap.dedent(f"""
            <div class="url-warning-box">
                <strong>🛡️ Informasi Proteksi Bot E-Commerce:</strong><br>
                Domain <b>{domain}</b> terdeteksi sebagai e-commerce besar. Website ini menggunakan proteksi anti-bot ketat (seperti Cloudflare, CAPTCHA, JavaScript challenge, dan session cookie).<br><br>
                Untuk menunjukkan alur kerja NLP pada produk tersebut, sistem akan <b>mensimulasikan ekstraksi ulasan</b> untuk link produk ini.
            </div>
            """), unsafe_allow_html=True)

            # Simulated product reviews
            extracted_texts = [
                "Barang bagus banget, sesuai deskripsi dan pengiriman cepat!",
                "Kecewa, bahannya tipis sekali dan jahitan tidak rapi. Respon penjual juga lambat.",
                "Kualitas standar sesuai harga, lumayan untuk dipakai harian. Pengiriman biasa saja.",
                "Sangat recommended! Packing sangat aman berlapis bubble wrap. Terima kasih seller.",
                "Kurang puas, ukuran kekecilan padahal sudah pesan ukuran L. Seller tidak responsif saat ditanya.",
                "Harga murah tapi kualitasnya tidak murahan. Jahitan rapi, respon cepat.",
                "Barang sampai dalam kondisi penyok karena kurir tidak hati-hati, tapi isi aman. Kualitas oke.",
                "Ukurannya pas, bahan adem, enak dipakai. Nanti bakal order warna lain lagi.",
                "Kecewa berat, pesan hitam dikirim navy. Minta retur tapi tidak dibalas chatnya.",
                "Mantap lah, bintang 5 untuk pelayanan toko dan kecepatan pengiriman kurir.",
            ]
        else:
            source_type = "Scraping HTML Nyata"
            st.markdown(textwrap.dedent(f"""
            <div class="url-info-box">
                <strong>🌐 Melakukan Scraping Nyata:</strong><br>
                Membaca halaman <b>{domain}</b> secara langsung dan mengekstrak semua paragraf teks (panjang > 15 karakter) yang ditemukan di struktur HTML.
            </div>
            """), unsafe_allow_html=True)

            with st.spinner("Menghubungi server dan mengunduh konten..."):
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    }
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code != 200:
                        st.error(f"Gagal mengambil halaman web. Server mengembalikan status code: {response.status_code}")
                        st.stop()

                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Try to extract elements
                    p_elements = soup.find_all('p')
                    for p in p_elements:
                        text_content = p.get_text().strip()
                        # Filter out very short texts
                        if len(text_content) > 25:
                            # Clean whitespace
                            text_content = re.sub(r'\s+', ' ', text_content)
                            extracted_texts.append(text_content)
                    
                    # If few paragraphs, look inside div class/id containing common tags
                    if len(extracted_texts) < 3:
                        div_elements = soup.find_all('div', class_=re.compile(r'review|comment|content|text', re.I))
                        for div in div_elements:
                            text_content = div.get_text().strip()
                            if 25 < len(text_content) < 500:
                                text_content = re.sub(r'\s+', ' ', text_content)
                                if text_content not in extracted_texts:
                                    extracted_texts.append(text_content)

                except Exception as e:
                    st.error(f"Gagal mengkoneksi ke URL. Pastikan URL valid dan server mengijinkan akses. Error detail: {e}")
                    st.stop()

        if not extracted_texts:
            st.warning("Tidak ditemukan paragraf teks ulasan atau konten berita yang memadai untuk dianalisis pada link tersebut.")
        else:
            # Limit to first 15 for demo performance
            max_limit = min(len(extracted_texts), 15)
            texts_to_analyze = extracted_texts[:max_limit]
            
            st.info(f"Berhasil mengekstrak {len(extracted_texts)} baris teks. Memulai analisis sentimen untuk {max_limit} baris pertama...")
            
            # Run batch classification
            progress_bar = st.progress(0.0, text="Menganalisis sentimen...")
            def _cb(frac):
                progress_bar.progress(frac, text=f"Menganalisis... {int(frac*100)}%")
            
            results = predict_batch(texts_to_analyze, progress_callback=_cb)
            progress_bar.empty()

            # Compile dataframe
            df_results = pd.DataFrame({
                "Teks Terkstrak": texts_to_analyze,
                "Sentimen": [r[0] for r in results],
                "Confidence": [round(r[1] * 100, 2) for r in results]
            })

            st.success(f"Analisis Sentimen URL Selesai!")
            
            # Show summary stats
            sent_counts = df_results["Sentimen"].value_counts().reindex(["Positive", "Negative"]).fillna(0)
            
            sc1, sc2 = st.columns(2)
            with sc1:
                st.metric("Total Teks Teranalisis", len(df_results))
            with sc2:
                positive_pct = (sent_counts["Positive"] / len(df_results)) * 100
                st.metric("Persentase Positif", f"{positive_pct:.1f}%")

            # Chart and Table
            c_pie, c_table = st.columns([1, 1.5])
            
            with c_pie:
                fig_pie = px.pie(
                    names=["Positif", "Negatif"],
                    values=[sent_counts.get("Positive", 0), sent_counts.get("Negative", 0)],
                    color=["Positif", "Negatif"],
                    color_discrete_map={"Positif": "#10b981", "Negatif": "#ef4444"},
                    title="Distribusi Sentimen Konten URL",
                    hole=0.45,
                )
                fig_pie.update_layout(
                    font=dict(family="Plus Jakarta Sans", size=11, color="#475569"),
                    title_font=dict(family="Outfit", size=13, color="#0f172a"),
                    margin=dict(l=10, r=10, t=40, b=10),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with c_table:
                st.markdown("<b style='color:#334155; font-size:0.85rem;'>Daftar Teks & Sentimen</b>", unsafe_allow_html=True)
                st.dataframe(df_results, use_container_width=True, height=240)

            # Download Option
            csv_buffer = io.StringIO()
            df_results.to_csv(csv_buffer, index=False)
            
            st.write("")
            st.download_button(
                label="Unduh Hasil Klasifikasi URL (CSV)",
                data=csv_buffer.getvalue(),
                file_name=f"hasil_sentimen_url_{domain}.csv",
                mime="text/csv",
                icon=":material/download:",
                use_container_width=True
            )
else:
    st.markdown(textwrap.dedent("""
    <div style="background:#f8fafc; border:1px dashed #e2e8f0; border-radius:10px; padding:2.5rem; text-align:center; color:#94a3b8; font-size:0.85rem;">
        🔗 Masukkan link URL website di atas lalu klik <b>Analisis URL</b> untuk mendeteksi sentimen teks.
    </div>
    """), unsafe_allow_html=True)

if not model_is_available():
    st.markdown(textwrap.dedent("""
    <div style="background:#fffbeb; border:1px solid #fef3c7; border-radius:6px; padding:0.75rem 1rem; margin-top:1.5rem; font-size:0.75rem; color:#b45309;">
        Sistem berjalan dalam mode demo. Unggah model terlatih ke folder <code>model/indobert_sentiment_final/</code> untuk menggunakan model IndoBERT asli.
    </div>
    """), unsafe_allow_html=True)
