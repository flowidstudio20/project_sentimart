import pandas as pd
import textwrap
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.metrics_data import load_metrics

# CSS Injection for Performance Page (Modern, Simple, Flat with Blue Accents)
st.markdown("""
<style>
    .perf-card-container-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    
    /* Metrics card flat style */
    .perf-card-flat {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: border-color 0.15s ease;
    }
    
    .perf-card-flat:hover {
        border-color: #3b82f6;
    }
    
    .perf-badge-flat {
        font-size: 0.65rem;
        font-weight: 700;
        color: #1e40af;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        display: inline-block;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    
    .perf-value-flat {
        font-size: 1.7rem;
        font-weight: 700;
        color: #2563eb; /* Modern Blue */
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }
    
    .perf-desc-flat {
        font-size: 0.72rem;
        color: #64748b;
        line-height: 1.4;
        margin-top: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## Performa Model")
st.caption("Hasil evaluasi model IndoBERT terlatih pada dataset PRDECT-ID.")

metrics = load_metrics()
if metrics.get("is_demo"):
    st.markdown(textwrap.dedent("""
    <div style="background:#fffbeb; border:1px solid #fef3c7; border-radius:6px; padding:0.75rem 1rem; margin-bottom:1.2rem; font-size:0.78rem; color:#b45309;">
        Catatan: Menampilkan data estimasi (data proposal). Tempel berkas <code>metrics.json</code> ke folder <code>model/metrics.json</code> untuk melihat metrik latih asli.
    </div>
    """), unsafe_allow_html=True)

cm = metrics["confusion_matrix"]

# ---- 4 kartu metrik ----
c1, c2, c3, c4 = st.columns(4)
card_specs = [
    ("ACCURACY", metrics["accuracy"], "Akurasi total dari prediksi benar data uji.", c1),
    ("PRECISION", metrics["precision"], "Rasio ulasan positif terprediksi benar.", c2),
    ("RECALL", metrics["recall"], "Rasio ulasan positif aktual terdeteksi.", c3),
    ("F1-SCORE", metrics["f1"], "Rata-rata harmonis Precision & Recall.", c4),
]

for label, val, desc, col in card_specs:
    with col:
        st.markdown(textwrap.dedent(f"""
        <div class="perf-card-flat">
            <div>
                <div class="perf-badge-flat">{label}</div>
                <div class="perf-value-flat">{val*100:.2f}%</div>
            </div>
            <div class="perf-desc-flat">{desc}</div>
        </div>
        """), unsafe_allow_html=True)

st.write("")
col_cm, col_curve = st.columns(2)

# Common Plotly styling
plotly_layout_defaults = dict(
    font=dict(family="Plus Jakarta Sans", size=11, color="#475569"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

with col_cm:
    st.markdown('<div class="perf-card-container-flat">', unsafe_allow_html=True)
    st.markdown("**Confusion Matrix**")
    st.caption(f"Hasil pengujian pada data uji ({metrics.get('n_test', cm['tn']+cm['fp']+cm['fn']+cm['tp'])} sampel)")

    z = [[cm["tp"], cm["fn"]], [cm["fp"], cm["tn"]]]
    x_labels = ["Pred: Positif", "Pred: Negatif"]
    y_labels = ["Aktual: Positif", "Aktual: Negatif"]
    
    fig_cm = go.Figure(data=go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=[[0, "#eff6ff"], [1, "#2563eb"]], # Modern blue scale
        text=z, texttemplate="%{text}", textfont={"size": 16, "family": "Plus Jakarta Sans", "weight": "bold"},
        showscale=False,
    ))
    fig_cm.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), 
        height=260,
        **plotly_layout_defaults
    )
    st.plotly_chart(fig_cm, use_container_width=True)

    m1, m2 = st.columns(2)
    m1.metric("Klasifikasi Tepat", cm["tp"] + cm["tn"])
    m2.metric("Klasifikasi Salah", cm["fp"] + cm["fn"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_curve:
    st.markdown('<div class="perf-card-container-flat">', unsafe_allow_html=True)
    st.markdown("**Kurva Pelatihan (Loss)**")
    st.caption("Training Loss vs Validation Loss per epoch")

    epochs = list(range(1, len(metrics["train_loss"]) + 1))
    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(
        x=epochs, y=metrics["train_loss"], mode="lines+markers",
        name="Training Loss", line=dict(color="#2563eb", width=2.5),
        marker=dict(size=6)
    ))
    fig_curve.add_trace(go.Scatter(
        x=epochs, y=metrics["val_loss"], mode="lines+markers",
        name="Validation Loss", line=dict(color="#ef4444", width=2.5),
        marker=dict(size=6)
    ))
    fig_curve.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=240,
        xaxis=dict(title="Epoch", tickmode="linear", showgrid=False),
        yaxis=dict(title="Loss", gridcolor="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        **plotly_layout_defaults
    )
    st.plotly_chart(fig_curve, use_container_width=True)

    bcol1, bcol2 = st.columns(2)
    bcol1.metric("Best Val Loss", f"{min(metrics['val_loss']):.4f}")
    bcol2.metric("Total Epoch", len(metrics["train_loss"]))
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
with st.expander("Lihat perbandingan akurasi per epoch"):
    df_acc = pd.DataFrame({
        "Epoch": list(range(1, len(metrics["train_acc"]) + 1)),
        "Train Accuracy": metrics["train_acc"],
        "Val Accuracy": metrics["val_acc"],
    })
    fig_acc = px.line(
        df_acc, x="Epoch", y=["Train Accuracy", "Val Accuracy"],
        markers=True, color_discrete_sequence=["#2563eb", "#ef4444"],
    )
    fig_acc.update_layout(
        yaxis_title="Accuracy", 
        legend_title="",
        **plotly_layout_defaults
    )
    fig_acc.update_xaxes(tickmode="linear", showgrid=False)
    fig_acc.update_yaxes(gridcolor="#e2e8f0")
    st.plotly_chart(fig_acc, use_container_width=True)
    st.dataframe(df_acc, use_container_width=True, hide_index=True)
