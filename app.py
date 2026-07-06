import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="SentiMart - Analisis Sentimen E-Commerce",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

pages = [
    st.Page("views/home.py", title="Beranda", icon=":material/home:", default=True),
    st.Page("views/predict.py", title="Prediksi", icon=":material/search:"),
    st.Page("views/batch.py", title="Analisis Batch", icon=":material/database:"),
    st.Page("views/url_predict.py", title="Analisis URL", icon=":material/link:"),
    st.Page("views/performance.py", title="Performa Model", icon=":material/show_chart:"),
    st.Page("views/about.py", title="Tentang", icon=":material/info:"),
]

pg = st.navigation(pages)
pg.run()

