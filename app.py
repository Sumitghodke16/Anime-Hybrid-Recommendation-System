import streamlit as st
import pandas as pd
import pickle
import html
import base64
import os

# =====================================================
# PAGE CONFIG  (must be FIRST streamlit call)
# =====================================================

st.set_page_config(
    page_title="Anime Hybrid Recommendation System",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =====================================================
# BACKGROUND IMAGE
# =====================================================

def get_base64_image(path: str) -> str:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


bg_b64 = get_base64_image("anime_back.png")
BG_CSS = (
    f"url('data:image/png;base64,{bg_b64}')"
    if bg_b64
    else "linear-gradient(135deg, #0d0d1a 0%, #1a0a2e 50%, #0d1a0d 100%)"
)


# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ── Background ── */
.stApp {{
    background: {BG_CSS} center center / cover fixed !important;
    min-height: 100vh;
}}

.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(5, 5, 15, 0.82);
    z-index: 0;
    pointer-events: none;
}}

/* ── Kill ALL Streamlit white/grey boxes ── */
.block-container {{
    position: relative;
    z-index: 1;
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1280px;
    background: transparent !important;
}}

div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="column"],
.element-container,
.stMarkdown {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* ── Text input — dark bg, always white text ── */
div[data-testid="stTextInput"] input {{
    background-color: #12152a !important;
    color: #f0f2f8 !important;
    border: 1.5px solid rgba(255,75,75,0.35) !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
    caret-color: #ff4b4b !important;
}}

div[data-testid="stTextInput"] input::placeholder {{
    color: rgba(160,170,195,0.55) !important;
}}

div[data-testid="stTextInput"] input:focus {{
    border-color: #ff4b4b !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(255,75,75,0.15) !important;
    background-color: #12152a !important;
    color: #f0f2f8 !important;
}}

/* ── Labels ── */
div[data-testid="stTextInput"] label,
div[data-testid="stSlider"] label {{
    color: #c0c8d8 !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
}}

/* ── Slider value / tick text ── */
div[data-testid="stSlider"] p,
div[data-testid="stSlider"] span {{
    color: #c0c8d8 !important;
}}

/* ── Button ── */
div[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, #ff4b4b 0%, #c0392b 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(255,75,75,0.25) !important;
    transition: opacity 0.2s, transform 0.1s !important;
}}

div[data-testid="stButton"] > button:hover {{
    opacity: 0.87 !important;
    transform: translateY(-1px) !important;
}}

/* ── Expander ── */
div[data-testid="stExpander"] {{
    background: rgba(14,17,32,0.80) !important;
    border: 1px solid rgba(255,75,75,0.15) !important;
    border-radius: 10px !important;
}}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary p {{
    color: #b0bcd0 !important;
}}

/* ── Header ── */
.app-header {{
    text-align: center;
    padding: 1rem 0 0.5rem 0;
}}

.app-header h1 {{
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0 0 0.2rem 0;
    background: linear-gradient(90deg,#ff4b4b 0%,#ff8c42 55%,#ff4b4b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.app-header p {{
    color: #a8b4c4;
    font-size: 0.92rem;
    margin: 0;
}}

.app-divider {{
    border: none;
    border-top: 1px solid rgba(255,255,255,0.07);
    margin: 0.6rem 0 1rem 0;
}}

/* ── Column panels — styled directly on Streamlit's column divs ── */
div[data-testid="column"] > div:first-child {{
    background: rgba(12,15,28,0.90) !important;
    border: 1px solid rgba(255,75,75,0.17) !important;
    border-radius: 14px !important;
    padding: 1.3rem 1.5rem !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
}}

.panel-title {{
    font-size: 0.76rem;
    font-weight: 700;
    color: #ff4b4b;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
}}

/* ── Suggestions ── */
.sug-label {{
    font-size: 0.73rem;
    font-weight: 600;
    color: #7a8499;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 8px 0 5px 0;
}}

.sug-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 4px;
}}

.sug-pill {{
    display: inline-block;
    background: rgba(255,75,75,0.09);
    border: 1px solid rgba(255,75,75,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    color: #d0d8e8;
    font-size: 0.80rem;
}}

/* ── Scrollable results ── */
.results-scroll {{
    max-height: 520px;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: 5px;
    scrollbar-width: thin;
    scrollbar-color: #ff4b4b rgba(255,255,255,0.04);
}}

.results-scroll::-webkit-scrollbar {{ width: 5px; }}
.results-scroll::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.04); border-radius:3px; }}
.results-scroll::-webkit-scrollbar-thumb {{ background: #ff4b4b; border-radius:3px; }}

/* ── Rec card ── */
.rec-card {{
    background: rgba(18,22,40,0.92);
    border: 1px solid rgba(255,255,255,0.05);
    border-left: 3px solid #ff4b4b;
    border-radius: 10px;
    padding: 9px 13px 8px 13px;
    margin-bottom: 7px;
    transition: border-left-color 0.2s, background 0.2s;
}}

.rec-card:hover {{
    border-left-color: #ff8c42;
    background: rgba(24,28,50,0.96);
}}

.rec-rank {{
    font-size: 0.67rem;
    font-weight: 700;
    color: #ff4b4b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 2px;
}}

.rec-title {{
    font-size: 0.96rem;
    font-weight: 700;
    color: #f0f2f8;
    margin-bottom: 5px;
    line-height: 1.3;
}}

.rec-meta {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 5px;
}}

.meta-badge {{
    font-size: 0.76rem;
    color: #8a96aa;
    display: flex;
    align-items: center;
    gap: 3px;
    white-space: nowrap;
}}

.meta-badge .val {{
    color: #c8d0e0;
    font-weight: 600;
}}

.genre-tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}}

.genre-tag {{
    background: rgba(255,75,75,0.09);
    border: 1px solid rgba(255,75,75,0.16);
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 0.70rem;
    color: #9aa4b8;
}}

/* ── Selected anime card ── */
.input-card {{
    background: rgba(255,75,75,0.07);
    border: 1px solid rgba(255,75,75,0.26);
    border-radius: 10px;
    padding: 9px 13px;
    margin-bottom: 11px;
}}

.ic-label {{
    font-size: 0.67rem;
    font-weight: 700;
    color: #ff4b4b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 2px;
}}

.ic-name {{
    font-size: 1.02rem;
    font-weight: 700;
    color: #f0f2f8;
    margin-bottom: 2px;
}}

.ic-meta {{ font-size: 0.79rem; color: #8a96aa; }}

/* ── Custom alerts ── */
.custom-info {{
    background: rgba(30,80,160,0.13);
    border: 1px solid rgba(80,130,255,0.20);
    border-radius: 8px;
    padding: 10px 14px;
    color: #8ab0e0;
    font-size: 0.86rem;
}}

.custom-error {{
    background: rgba(180,30,30,0.15);
    border: 1px solid rgba(255,80,80,0.30);
    border-radius: 8px;
    padding: 10px 14px;
    color: #f07070;
    font-size: 0.86rem;
}}

/* ── Footer ── */
.footer {{
    text-align: center;
    color: rgba(140,150,170,0.42);
    font-size: 0.72rem;
    padding: 1rem 0 0.4rem 0;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {{
    visibility: hidden !important;
    height: 0 !important;
    display: none !important;
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_resource(show_spinner="Loading recommendation engine…")
def load_data():
    anime_df   = pickle.load(open("anime_data.pkl",  "rb"))
    cosine_sim = pickle.load(open("cosine_sim.pkl",  "rb"))
    indices    = pickle.load(open("indices.pkl",     "rb"))

    anime_df["_search"] = (
        anime_df["name"]
        .astype(str)
        .apply(html.unescape)
        .str.strip()
        .str.lower()
    )

    if "rating_score" not in anime_df.columns:
        r = anime_df["rating"].fillna(0)
        anime_df["rating_score"] = (r - r.min()) / (r.max() - r.min() + 1e-9)

    if "popularity_score" not in anime_df.columns:
        import numpy as np
        m = anime_df["members"]
        log_m = np.log1p(m.clip(lower=1))
        anime_df["popularity_score"] = (log_m - log_m.min()) / (log_m.max() - log_m.min() + 1e-9)

    return anime_df, cosine_sim, indices


anime_df, cosine_sim, indices = load_data()


# =====================================================
# HELPERS
# =====================================================

def resolve_anime_name(raw: str):
    """Return exact DataFrame name key or None — case / entity insensitive."""
    norm = html.unescape(raw).strip().lower()
    exact = anime_df[anime_df["_search"] == norm]
    if not exact.empty:
        return exact.iloc[0]["name"]
    starts = anime_df[anime_df["_search"].str.startswith(norm, na=False)]
    if not starts.empty:
        return starts.iloc[0]["name"]
    contains = anime_df[anime_df["_search"].str.contains(norm, na=False, regex=False)]
    if not contains.empty:
        return contains.iloc[0]["name"]
    return None


def hybrid_recommend(anime_name, top_n=5, cw=0.6, rw=0.2, pw=0.2):
    try:
        idx = indices[anime_name]
    except KeyError:
        return None

    scored = []
    for anime_idx, sim in enumerate(cosine_sim[idx]):
        if anime_idx == idx:
            continue
        row = anime_df.iloc[anime_idx]
        score = (
            cw * float(sim)
            + rw * float(row.get("rating_score",    0))
            + pw * float(row.get("popularity_score", 0))
        )
        scored.append((anime_idx, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    scored = scored[:top_n]

    result = anime_df[
        ["name", "genre", "type", "episodes", "rating", "members"]
    ].iloc[[r[0] for r in scored]].copy()
    result["hybrid_score"] = [r[1] for r in scored]
    return result


def rating_stars(rating) -> str:
    try:
        f = round(float(rating) / 2)
        return "★" * f + "☆" * (5 - f)
    except Exception:
        return "—"


def fmt_members(val) -> str:
    try:
        v = float(val)
        return f"{v/1000:.1f}k" if v >= 1000 else str(int(v))
    except Exception:
        return str(val)


def genre_tags_html(genre_str: str) -> str:
    if not genre_str or str(genre_str).lower() in ("nan", "n/a", ""):
        return ""
    return "".join(
        f'<span class="genre-tag">{html.escape(g.strip())}</span>'
        for g in str(genre_str).split(",") if g.strip()
    )


def build_cards_html(results: pd.DataFrame) -> str:
    """Build entire scrollable results block as one HTML string."""
    parts = ['<div class="results-scroll">']
    for rank, (_, row) in enumerate(results.iterrows(), start=1):
        name  = html.unescape(str(row.get("name", "Unknown")))
        genre = str(row.get("genre", ""))
        rtype = str(row.get("type", "N/A"))
        eps   = str(row.get("episodes", "N/A"))
        score = float(row.get("hybrid_score", 0))
        try:
            rating_disp = f"{float(row.get('rating', 0)):.2f}"
        except Exception:
            rating_disp = "N/A"
        parts.append(f"""
<div class="rec-card">
  <div class="rec-rank">#{rank}&nbsp;·&nbsp;Score {score:.3f}</div>
  <div class="rec-title">{html.escape(name)}</div>
  <div class="rec-meta">
    <span class="meta-badge">⭐ <span class="val">{rating_disp}</span></span>
    <span class="meta-badge">{rating_stars(row.get('rating',0))}</span>
    <span class="meta-badge">📺 <span class="val">{html.escape(rtype)}</span></span>
    <span class="meta-badge">🎬 <span class="val">{html.escape(eps)} ep</span></span>
    <span class="meta-badge">👥 <span class="val">{fmt_members(row.get('members','N/A'))}</span></span>
  </div>
  <div class="genre-tags">{genre_tags_html(genre)}</div>
</div>""")
    parts.append("</div>")
    return "".join(parts)


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="app-header">
    <h1>🎌 Anime Recommendation Engine</h1>
    <p>Hybrid filtering &nbsp;·&nbsp; Content similarity + Rating + Popularity</p>
</div>
<hr class="app-divider">
""", unsafe_allow_html=True)


# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([1, 1.55], gap="large")

# ── Default weights ──
cw, rw, pw = 0.6, 0.2, 0.2

# ─────────────────────────────────────────────────────
# LEFT
# ─────────────────────────────────────────────────────

with left_col:
    # Use st.container() — Streamlit renders it as one real div we can style
    with st.container():
        st.markdown('<div class="panel-title">🔍 Search</div>', unsafe_allow_html=True)

        anime_input = st.text_input(
            "Anime title",
            placeholder="e.g. Death Note, Naruto, Attack on Titan",
            key="anime_input",
        )

        # Live suggestions while typing
        if anime_input and anime_input.strip():
            term = html.unescape(anime_input).strip().lower()
            suggestions = (
                anime_df[anime_df["_search"].str.contains(term, na=False, regex=False)]
                ["name"].head(6).tolist()
            )
            if suggestions:
                pills = "".join(
                    f'<span class="sug-pill">{html.escape(s)}</span>' for s in suggestions
                )
                st.markdown(
                    f'<div class="sug-label">Suggestions</div>'
                    f'<div class="sug-row">{pills}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        top_n = st.slider(
            "Number of recommendations",
            min_value=1, max_value=10, value=5, step=1, format="%d",
        )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        get_btn = st.button("🚀  Get Recommendations", use_container_width=True)

    with st.expander("⚙️ Advanced — Adjust hybrid weights"):
        cw = st.slider("Content similarity weight", 0.0, 1.0, 0.6, 0.05, key="cw")
        rw = st.slider("Rating weight",             0.0, 1.0, 0.2, 0.05, key="rw")
        pw = st.slider("Popularity weight",         0.0, 1.0, 0.2, 0.05, key="pw")
        total = round(cw + rw + pw, 4)
        if abs(total - 1.0) > 0.01:
            st.markdown(
                f'<div class="custom-error">⚠️ Weights sum to {total:.2f} — ideally 1.0.</div>',
                unsafe_allow_html=True,
            )

    # done


# ─────────────────────────────────────────────────────
# RIGHT
# ─────────────────────────────────────────────────────

with right_col:
    with st.container():
        st.markdown('<div class="panel-title">⭐ Recommendations</div>', unsafe_allow_html=True)

        if get_btn:
            raw = (anime_input or "").strip()

            if not raw:
                st.markdown(
                    '<div class="custom-error">⚠️ Please enter an anime title.</div>',
                    unsafe_allow_html=True,
                )
            else:
                resolved = resolve_anime_name(raw)

                if resolved is None:
                    st.markdown(
                        f'<div class="custom-error">❌ <strong>"{html.escape(raw)}"</strong> '
                        f'not found. Try a suggestion from the left panel.</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    # Show matched anime info
                    irow = anime_df[anime_df["name"] == resolved].iloc[0]
                    try:
                        ir_disp = f"{float(irow.get('rating', 'N/A')):.2f}"
                    except Exception:
                        ir_disp = "N/A"
                    itype = html.escape(str(irow.get("type", "N/A")))

                    st.markdown(
                        f'<div class="input-card">'
                        f'<div class="ic-label">Selected Anime</div>'
                        f'<div class="ic-name">{html.escape(html.unescape(str(resolved)))}</div>'
                        f'<div class="ic-meta">⭐ {ir_disp}&nbsp;&nbsp;·&nbsp;&nbsp;{itype}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    results = hybrid_recommend(resolved, top_n=top_n, cw=cw, rw=rw, pw=pw)

                    if results is None or results.empty:
                        st.markdown(
                            '<div class="custom-error">No recommendations found.</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(build_cards_html(results), unsafe_allow_html=True)

        else:
            st.markdown(
                '<div class="custom-info">💡 Type an anime title on the left and click '
                '<strong>Get Recommendations</strong>.</div>',
                unsafe_allow_html=True,
            )

    pass  # done


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    Anime Hybrid Recommendation System &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp;
    Content-Based + Rating + Popularity Hybrid Filtering
</div>
""", unsafe_allow_html=True)