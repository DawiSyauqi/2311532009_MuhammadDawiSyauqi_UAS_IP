import streamlit as st
import time
from PIL import Image
import numpy as np
import io

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FruitVision – Fruit Ripeness Detector",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Root variables */
:root {
    --bg:          #f8fafc;   /* Slate 50 */
    --surface:     #ffffff;   /* Pure White */
    --surface2:    #f1f5f9;   /* Slate 100 */
    --border:      #e2e8f0;   /* Slate 200 */
    --primary:     #10b981;   /* Emerald Green for Fresh */
    --warn:        #ef4444;   /* Rose Red for Rotten */
    --info:        #3b82f6;   /* Blue for Unripe */
    --text:        #0f172a;   /* Slate 900 */
    --muted:       #64748b;   /* Slate 500 */
    --radius:      12px;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
}

/* Header background styling */
header[data-testid="stHeader"] {
    background-color: rgba(248, 250, 252, 0.8) !important;
    backdrop-filter: blur(8px);
}

/* Hide default header top bar decoration */
header[data-testid="stHeader"]::before {
    display: none;
}

/* Radio buttons & text inputs */
div[data-testid="stRadio"] label {
    color: var(--text) !important;
    font-size: 0.95rem;
}

/* Metric cards override */
div[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.06) !important;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out !important;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
}
div[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
}

/* Buttons styling */
button[kind="primary"], .stButton > button {
    background: var(--primary) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem 1.25rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
}
button[kind="primary"]:hover, .stButton > button:hover {
    background: #059669 !important;
    color: #ffffff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}

/* File uploader container */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"] section {
    background: transparent !important;
}
[data-testid="stFileUploader"] section * {
    color: var(--muted) !important;
}
[data-testid="stFileUploader"] button {
    background-color: #ffffff !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 500 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}
[data-testid="stFileUploader"] button:hover {
    background-color: var(--surface-hover) !important;
    border-color: #cbd5e1 !important;
    color: var(--text) !important;
}
[data-testid="stFileUploader"] button * {
    color: var(--text) !important;
}

/* Progress bars colors */
.stProgress > div > div {
    background: var(--primary) !important;
}

/* Custom cards styling */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
}
.card h3 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    margin: 0 0 0.5rem;
    font-size: 1.15rem;
    color: var(--text);
    font-weight: 700;
}
.card p {
    color: var(--muted);
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.5;
}

/* Tag pill colors */
.tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.tag-fresh   { background: #e6f4ea; color: #137333; border: 1px solid #c2e7c9; }
.tag-rotten  { background: #fce8e6; color: #c5221f; border: 1px solid #fad2cf; }
.tag-unripe  { background: #e8f0fe; color: #1a73e8; border: 1px solid #d2e3fc; }

/* Hero section title */
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    color: var(--text);
    letter-spacing: -0.02em;
}
.hero-accent {
    color: var(--primary);
}

/* Section heading styling */
.sec-head {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
    color: var(--text);
    letter-spacing: -0.01em;
}

/* Result box container styling */
.result-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.75rem;
    border-left: 5px solid var(--primary);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
    margin-bottom: 1.25rem;
}
.result-box.rotten { border-left-color: var(--warn); }
.result-box.unripe { border-left-color: var(--info); }

/* Confidence bar styling */
.conf-bg {
    background: #e2e8f0;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin-top: 6px;
}
.conf-fill {
    height: 100%;
    border-radius: 999px;
    background: var(--primary);
}
.conf-fill.rotten { background: var(--warn); }
.conf-fill.unripe { background: var(--info); }

/* Sidebar navigation label */
.nav-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* Divider colors */
hr {
    border-color: var(--border) !important;
}

/* Force colors on Streamlit native text elements */
[data-testid="stAppViewContainer"] h1, 
[data-testid="stAppViewContainer"] h2, 
[data-testid="stAppViewContainer"] h3, 
[data-testid="stAppViewContainer"] h4, 
[data-testid="stAppViewContainer"] h5, 
[data-testid="stAppViewContainer"] h6,
[data-testid="stAppViewContainer"] p, 
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] span:not(.tag) {
    color: var(--text);
}

/* Force markdown texts to be dark slate */
.stMarkdown p, .stMarkdown li, .stMarkdown strong, .stMarkdown em, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
    color: var(--text) !important;
}

/* Fix inputs background */
.stTextInput>div>div>input {
    background-color: var(--surface) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []   # list of {label, confidence, fruit, ripeness, time_ms}
if "total_tested" not in st.session_state:
    st.session_state.total_tested = 0
if "model" not in st.session_state:
    st.session_state.model = None

# ─── Load model (cached) ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from ultralytics import YOLO
        model = YOLO("best.pt")
        return model, None
    except Exception as e:
        return None, str(e)

# ─── Class metadata ────────────────────────────────────────────────────────────
CLASS_META = {
    # class_name (exact, lowercase) : (fruit, ripeness)
    "freshapples":    ("Apple",  "Fresh"),
    "rottenapples":   ("Apple",  "Rotten"),
    "unripe apple":   ("Apple",  "Unripe"),
    "freshbanana":    ("Banana", "Fresh"),
    "rottenbanana":   ("Banana", "Rotten"),
    "unripe banana":  ("Banana", "Unripe"),
    "freshoranges":   ("Orange", "Fresh"),
    "rottenoranges":  ("Orange", "Rotten"),
    "unripe orange":  ("Orange", "Unripe"),
}

FRUIT_EMOJI = {"Apple": "🍎", "Banana": "🍌", "Orange": "🍊"}
RIPENESS_CLASS = {"Fresh": "fresh", "Rotten": "rotten", "Unripe": "unripe"}
RIPENESS_TAG   = {"Fresh": "tag-fresh", "Rotten": "tag-rotten", "Unripe": "tag-unripe"}

def parse_label(label: str):
    """Return (fruit, ripeness) from raw class name."""
    label_clean = label.lower().strip()
    # exact match first
    if label_clean in CLASS_META:
        return CLASS_META[label_clean]
    # fallback: partial match
    for key, (fruit, ripeness) in CLASS_META.items():
        if key in label_clean or label_clean in key:
            return fruit, ripeness
    return label, "Unknown"

def color_for(ripeness):
    return {"Fresh": "#10b981", "Rotten": "#ef4444", "Unripe": "#3b82f6"}.get(ripeness, "#64748b")

# ─── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="nav-label">FruitVision v1.0</p>', unsafe_allow_html=True)
    st.markdown("### 🍃 Navigation")
    page = st.radio(
        "",
        ["🏠  Beranda", "🔍  Prediksi", "📊  Dashboard"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown('<p class="nav-label">Model info</p>', unsafe_allow_html=True)
    st.markdown("**Model:** YOLOv8 Classification")
    st.markdown("**Kelas:** 9 (3 buah × 3 kondisi)")
    st.markdown("**Dataset:** Kaggle ~39.900 gambar")
    st.markdown("---")
    st.markdown('<p class="nav-label" style="font-size:0.7rem">DIF60202 · Sem Genap 2025/2026</p>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — BERANDA
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Beranda":
    st.markdown("""
    <div style="padding: 2.5rem 0 1.5rem;">
        <p class="hero-title">Fruit<span class="hero-accent">Vision</span></p>
        <p style="color:#64748b; font-size:1.1rem; margin-top:0.4rem;">
            Deteksi kematangan buah secara otomatis dengan Deep Learning
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="card">
            <h3>🍎 Deteksi Akurat</h3>
            <p>Model YOLOv8 dilatih pada 39.900+ gambar buah dari dataset Kaggle dengan 9 kelas kondisi.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="card">
            <h3>⚡ Real-time</h3>
            <p>Inferensi cepat — unggah gambar atau gunakan kamera, hasil tampil dalam hitungan detik.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="card">
            <h3>📊 Analytics</h3>
            <p>Dashboard statistik menampilkan histori prediksi, distribusi kelas, dan waktu inferensi.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="sec-head">Kelas yang Dideteksi</p>', unsafe_allow_html=True)

    fruits = ["🍎 Apple", "🍌 Banana", "🍊 Orange"]
    conditions = [
        ("Fresh",  "tag-fresh",  "Buah segar dan siap dikonsumsi"),
        ("Rotten", "tag-rotten", "Buah busuk, tidak layak konsumsi"),
        ("Unripe", "tag-unripe", "Buah belum matang"),
    ]
    header_cols = st.columns([1.5, 1, 1, 1])
    header_cols[0].markdown("**Kondisi**")
    for i, f in enumerate(fruits):
        header_cols[i+1].markdown(f"**{f}**")

    for cond, tag, desc in conditions:
        row = st.columns([1.5, 1, 1, 1])
        row[0].markdown(
            f'<span class="tag {tag}">{cond}</span><br><small style="color:#64748b">{desc}</small>',
            unsafe_allow_html=True,
        )
        for i in range(3):
            row[i+1].markdown("✅")

    st.markdown("---")
    st.markdown("""
    <div class="card" style="margin-top: 2rem;">
        <p style="margin:0; font-size:0.9rem; color:var(--muted);">
            <strong style="color:var(--text);">👨‍💻 Dikembangkan oleh</strong><br>
            Muhammad Dawi Syauqi · 2311532009 <br>
            Program Studi Informatika · Universitas Andalas<br>
            Mata Kuliah DIF60202 – Image Processing · Semester Genap 2025/2026
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PREDIKSI
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍  Prediksi":
    st.markdown('<p class="sec-head">🔍 Prediksi Kematangan Buah</p>', unsafe_allow_html=True)

    # Load model
    with st.spinner("Memuat model YOLOv8…"):
        model, err = load_model()

    if err:
        st.error(f"❌ Gagal memuat model: {err}\n\nPastikan file **best.pt** ada di direktori yang sama dengan app.py.")
        st.stop()
    else:
        st.success("✅ Model berhasil dimuat")

    st.markdown("---")

    input_method = st.radio(
        "Pilih metode input:",
        ["📁 Upload Gambar", "📷 Gunakan Kamera"],
        horizontal=True,
    )

    uploaded_img = None

    if input_method == "📁 Upload Gambar":
        uploaded_file = st.file_uploader(
            "Unggah gambar buah (JPG / PNG / WEBP)",
            type=["jpg", "jpeg", "png", "webp"],
        )
        if uploaded_file:
            uploaded_img = Image.open(uploaded_file).convert("RGB")

    else:  # Kamera
        cam_img = st.camera_input("Ambil foto buah")
        if cam_img:
            uploaded_img = Image.open(cam_img).convert("RGB")

    # ── Run prediction ──────────────────────────────────────────────────────
    if uploaded_img is not None:
        col_orig, col_result = st.columns(2)

        with col_orig:
            st.markdown("**Gambar Asli**")
            st.image(uploaded_img, use_container_width=True)

        with col_result:
            st.markdown("**Hasil Prediksi**")
            with st.spinner("Menganalisis gambar…"):
                t0 = time.time()
                results = model(uploaded_img, verbose=False)
                elapsed_ms = (time.time() - t0) * 1000

            # Parse results
            probs = results[0].probs
            top1_idx = int(probs.top1)
            top1_conf = float(probs.top1conf)
            names = results[0].names  # dict {idx: class_name}
            top_label = names[top1_idx]
            fruit, ripeness = parse_label(top_label)
            emoji = FRUIT_EMOJI.get(fruit, "🍑")
            rclass = RIPENESS_CLASS.get(ripeness, "fresh")
            col_hex = color_for(ripeness)

            # Top-5
            top5_idx  = probs.top5
            top5_conf = probs.top5conf.tolist()

            # Save to session
            st.session_state.history.append({
                "label": top_label,
                "fruit": fruit,
                "ripeness": ripeness,
                "confidence": top1_conf,
                "time_ms": elapsed_ms,
            })
            st.session_state.total_tested += 1

            # Result box
            st.markdown(f"""
            <div class="result-box {rclass}">
                <div style="font-size:2.5rem">{emoji}</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1.6rem; font-weight:700; margin:0.25rem 0;">
                    {fruit}
                </div>
                <span class="tag tag-{rclass}">{ripeness}</span>
                <p style="margin-top:0.75rem; color:var(--muted); font-size:0.85rem;">
                    ⏱ Waktu inferensi: <strong style="color:var(--text)">{elapsed_ms:.1f} ms</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Confidence score utama
            st.markdown(f"**Confidence Score:** `{top1_conf*100:.2f}%`")
            st.progress(top1_conf)

            # Top-5 breakdown
            st.markdown("**Top-5 Prediksi:**")
            for idx, conf in zip(top5_idx, top5_conf):
                lbl = names[idx]
                f2, r2 = parse_label(lbl)
                rc2 = RIPENESS_CLASS.get(r2, "fresh")
                st.markdown(f"""
                <div style="margin-bottom:0.5rem;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                        <span>{FRUIT_EMOJI.get(f2,'🍑')} {f2} – <span class="tag tag-{rc2}" style="font-size:0.7rem">{r2}</span></span>
                        <span style="color:var(--muted)">{conf*100:.1f}%</span>
                    </div>
                    <div class="conf-bg"><div class="conf-fill {rc2}" style="width:{conf*100:.1f}%"></div></div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊  Dashboard":
    st.markdown('<p class="sec-head">📊 Dashboard Statistik</p>', unsafe_allow_html=True)

    history = st.session_state.history
    total = len(history)

    # ── Top metrics ──────────────────────────────────────────────────────────
    avg_conf = np.mean([h["confidence"] for h in history]) if history else 0
    avg_time = np.mean([h["time_ms"]    for h in history]) if history else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Diuji",       total)
    m2.metric("Rata-rata Confidence", f"{avg_conf*100:.1f}%" if history else "—")
    m3.metric("Rata-rata Inferensi",  f"{avg_time:.0f} ms"   if history else "—")
    m4.metric("Kelas Tersedia",   "9")

    st.markdown("---")

    if not history:
        st.info("Belum ada prediksi. Pergi ke halaman **Prediksi** untuk mencoba model.")
    else:
        import collections

        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("**Distribusi Buah**")
            fruit_count = collections.Counter(h["fruit"] for h in history)
            for fruit, cnt in fruit_count.most_common():
                pct = cnt / total
                emoji = FRUIT_EMOJI.get(fruit, "🍑")
                st.markdown(f"""
                <div style="margin-bottom:0.6rem;">
                    <div style="display:flex;justify-content:space-between;font-size:0.9rem;">
                        <span>{emoji} {fruit}</span><span style="color:var(--muted)">{cnt} ({pct*100:.0f}%)</span>
                    </div>
                    <div class="conf-bg"><div class="conf-fill" style="width:{pct*100:.1f}%"></div></div>
                </div>""", unsafe_allow_html=True)

        with col_r:
            st.markdown("**Distribusi Kondisi**")
            ripe_count = collections.Counter(h["ripeness"] for h in history)
            for ripe, cnt in ripe_count.most_common():
                pct = cnt / total
                rc = RIPENESS_CLASS.get(ripe, "fresh")
                st.markdown(f"""
                <div style="margin-bottom:0.6rem;">
                    <div style="display:flex;justify-content:space-between;font-size:0.9rem;">
                        <span class="tag tag-{rc}">{ripe}</span><span style="color:var(--muted)">{cnt} ({pct*100:.0f}%)</span>
                    </div>
                    <div class="conf-bg"><div class="conf-fill {rc}" style="width:{pct*100:.1f}%"></div></div>
                </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Riwayat Prediksi**")

        rows = []
        for i, h in enumerate(reversed(history), 1):
            emoji = FRUIT_EMOJI.get(h["fruit"], "🍑")
            rows.append({
                "#": total - i + 1,
                "Buah": f"{emoji} {h['fruit']}",
                "Kondisi": h["ripeness"],
                "Confidence": f"{h['confidence']*100:.2f}%",
                "Waktu (ms)": f"{h['time_ms']:.1f}",
            })

        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Hapus Riwayat"):
            st.session_state.history = []
            st.session_state.total_tested = 0
            st.rerun()
