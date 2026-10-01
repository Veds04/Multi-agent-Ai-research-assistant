import streamlit as st

from pipeline import run_research_pipeline

st.set_page_config(page_title="Research Desk", page_icon="🖋", layout="wide")

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

    :root {
        --ink: #12161F;
        --panel: #181D27;
        --paper: #EAE6DA;
        --muted: #8D93A1;
        --brass: #C08A3E;
        --teal: #4F7C77;
        --border: #2A3340;
    }

    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
    .stApp { background-color: var(--ink); color: var(--paper); }
    section[data-testid="stSidebar"] { display: none; }

    .desk-header { border-bottom: 1px solid var(--border); padding-bottom: 1.1rem; margin-bottom: 1.8rem; }
    .desk-header h1 { font-family: 'Lora', serif; font-weight: 500; font-size: 2.1rem; color: var(--paper); margin-bottom: 0.15rem; }
    .desk-header p { color: var(--muted); font-size: 0.95rem; margin: 0; }

    /* Native bordered containers -> style them directly */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--panel);
        border: 1px solid var(--border) !important;
        border-radius: 6px;
    }

    .rail-title { font-size: 0.8rem; color: var(--muted); font-weight: 500; letter-spacing: 0.5px; margin-bottom: 0.9rem; }

    .stage-track { margin-top: 1.6rem; }
    .stage-item { display: flex; gap: 0.85rem; position: relative; padding-bottom: 1.3rem; }
    .stage-item:last-child { padding-bottom: 0; }
    .stage-item.has-line::after { content: ''; position: absolute; left: 13px; top: 28px; bottom: -4px; width: 1px; background: var(--border); }
    .stage-dot { width: 26px; height: 26px; min-width: 26px; border-radius: 50%; border: 1px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; color: var(--muted); background: var(--ink); }
    .stage-dot.done { border-color: var(--brass); color: var(--brass); }
    .stage-name { font-size: 0.92rem; color: var(--paper); line-height: 1.3; }
    .stage-sub { font-size: 0.78rem; color: var(--muted); }

    .dossier-topic { font-family: 'Lora', serif; font-size: 1.5rem; color: var(--paper); margin-bottom: 0.3rem; }
    .dossier-meta { color: var(--muted); font-size: 0.82rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 1.2rem; }
    .dossier-body, .dossier-body p, .dossier-body li { font-family: 'Lora', serif; font-size: 1.02rem; line-height: 1.7; color: var(--paper); }

    .critic-note { margin-top: 1.8rem; padding: 1rem 1.2rem; border-left: 3px solid var(--teal); background-color: rgba(79,124,119,0.08); border-radius: 0 4px 4px 0; }
    .critic-note .label { font-size: 0.78rem; color: var(--teal); margin-bottom: 0.4rem; font-weight: 500; }
    .critic-note .body { font-family: 'Lora', serif; font-size: 0.95rem; color: var(--paper); line-height: 1.6; }

    .empty-state { color: var(--muted); font-family: 'Lora', serif; font-style: italic; font-size: 1rem; text-align: center; padding: 3rem 0; }

    /* Loader */
    .loader-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3.5rem 0; }
    .loader-ring { width: 44px; height: 44px; border-radius: 50%; border: 3px solid var(--border); border-top-color: var(--brass); animation: spin 0.85s linear infinite; }
    .loader-caption { margin-top: 1.1rem; font-family: 'Lora', serif; font-style: italic; color: var(--muted); font-size: 0.95rem; animation: fade 1.8s ease-in-out infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes fade { 0%, 100% { opacity: 0.45; } 50% { opacity: 1; } }

    .stTextInput input { background-color: var(--ink) !important; color: var(--paper) !important; border: 1px solid var(--border) !important; border-radius: 4px !important; }
    .stButton button { background-color: var(--brass) !important; color: #15161A !important; border: none !important; border-radius: 4px !important; font-weight: 600 !important; width: 100%; }
    .stButton button:disabled { background-color: var(--border) !important; color: var(--muted) !important; }
    .streamlit-expanderHeader { background-color: var(--panel) !important; color: var(--muted) !important; border: 1px solid var(--border) !important; font-size: 0.85rem !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "topic" not in st.session_state:
    st.session_state.topic = None

STAGES = [
    ("Search", "Scanning current sources"),
    ("Read", "Scraping the strongest lead"),
    ("Draft", "Writing the report"),
    ("Review", "Checking it for gaps"),
]

st.markdown(
    """
    <div class="desk-header">
        <h1>Research Desk</h1>
        <p>Hand a topic to the desk — search, read, draft, and review run in sequence.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1, 2.1], gap="large")

# ---------------------------------------------------------------------------
# Left rail: intake + stage timeline
# ---------------------------------------------------------------------------
with left:
    with st.container(border=True):
        st.markdown('<div class="rail-title">NEW BRIEF</div>', unsafe_allow_html=True)
        topic = st.text_input(
            "Topic",
            placeholder="e.g. Impact of tariffs on semiconductor supply chains",
            label_visibility="collapsed",
        )
        run_clicked = st.button("Run research", disabled=not topic.strip())

        done = st.session_state.result is not None
        rows = []
        for i, (name, sub) in enumerate(STAGES, start=1):
            line_class = "has-line" if i < len(STAGES) else ""
            dot_class = "done" if done else ""
            mark = "✓" if done else f"{i:02d}"
            rows.append(
                f'<div class="stage-item {line_class}"><div class="stage-dot {dot_class}">{mark}</div>'
                f'<div><div class="stage-name">{name}</div><div class="stage-sub">{sub}</div></div></div>'
            )
        st.markdown(f'<div class="stage-track">{"".join(rows)}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Right panel: dossier
# ---------------------------------------------------------------------------
with right:
    with st.container(border=True):
        placeholder = st.empty()

        if run_clicked:
            with placeholder.container():
                st.markdown(
                    """
                    <div class="loader-wrap">
                        <div class="loader-ring"></div>
                        <div class="loader-caption">The desk is working through it...</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.session_state.result = run_research_pipeline(topic)
            st.session_state.topic = topic
            placeholder.empty()

        if st.session_state.result is None:
            with placeholder.container():
                st.markdown(
                    '<div class="empty-state">No brief open yet. Enter a topic on the left to begin.</div>',
                    unsafe_allow_html=True,
                )
        else:
            state = st.session_state.result
            with placeholder.container():
                st.markdown(f'<div class="dossier-topic">{st.session_state.topic}</div>', unsafe_allow_html=True)
                st.markdown(
                    '<div class="dossier-meta">Research dossier — compiled by Search, Read, Draft &amp; Review agents</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="dossier-body">', unsafe_allow_html=True)
                st.markdown(state.get("report", "_No report generated._"))
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div class="critic-note">
                        <div class="label">REVIEWER'S NOTE</div>
                        <div class="body">{state.get("feedback", "No feedback generated.")}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.result is not None:
        state = st.session_state.result
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Search results (raw)"):
            st.markdown(state.get("search_result", "_None_"))
        with st.expander("Scraped source (raw)"):
            st.markdown(state.get("scraped_content", "_None_"))