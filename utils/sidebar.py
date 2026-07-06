import streamlit as st
from utils.model_loader import model_is_available, get_model_debug_info


def render_sidebar():
    # Inject Google Fonts & Global CSS styles (Modern & Simple, outline-based)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

        /* Global Font override */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            letter-spacing: -0.01em !important;
        }

        /* Scrollbar styles */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f8fafc;
        }
        ::-webkit-scrollbar-thumb {
            background: #e2e8f0;
            border-radius: 99px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #cbd5e1;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
            font-size: 1.4rem !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            margin-bottom: 0.1rem !important;
        }

        /* Modern Outline status card */
        .status-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.75rem 0.9rem;
            margin: 0.5rem 0 1.2rem 0;
        }

        .status-header {
            font-size: 0.65rem;
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.4rem;
        }

        .status-body {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .status-indicator {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            display: inline-block;
        }

        .status-indicator.ready {
            background-color: #10b981;
        }

        .status-indicator.demo {
            background-color: #f59e0b;
        }

        .status-info {
            display: flex;
            flex-direction: column;
        }

        .status-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: #334155;
            line-height: 1.2;
        }

        .status-desc {
            font-size: 0.7rem;
            color: #64748b;
            margin-top: 0.05rem;
        }
        
        /* Minimalist input styling */
        .stTextArea textarea {
            border-radius: 6px !important;
            border: 1px solid #cbd5e1 !important;
            font-size: 0.88rem !important;
            transition: border-color 0.15s ease !important;
        }
        
        .stTextArea textarea:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### SentiMart")
        st.caption("Analisis Sentimen Ulasan • v1.0")
        st.markdown("")

        if model_is_available():
            st.markdown("""
            <div class="status-card">
                <div class="status-header">Status Sistem</div>
                <div class="status-body">
                    <div class="status-indicator ready"></div>
                    <div class="status-info">
                        <span class="status-title">Model IndoBERT</span>
                        <span class="status-desc" style="color: #10b981; font-weight: 500;">Aktif</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-card">
                <div class="status-header">Status Sistem</div>
                <div class="status-body">
                    <div class="status-indicator demo"></div>
                    <div class="status-info">
                        <span class="status-title">Mode Demo</span>
                        <span class="status-desc" style="color: #d97706; font-weight: 500;">Heuristik Teks</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔍 Diagnostik Model"):
                info = get_model_debug_info()
                st.caption(f"Path dicari: `{info['expected_model_dir']}`")
                st.write("Folder `model/`?", "✅ Ya" if info["model_root_exists"] else "❌ Tidak")
                st.write("Subfolder model?", "✅ Ya" if info["model_dir_exists"] else "❌ Tidak")
                if info["files_in_model_root"]:
                    st.caption(f"Isi `model/`: {info['files_in_model_root']}")
                if info["suspicious_small_files"]:
                    st.error("Terdeteksi pointer LFS (file asli belum terunduh): " + str(info["suspicious_small_files"]))
        
        st.markdown("<hr style='margin: 0.5rem 0 1.5rem 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
