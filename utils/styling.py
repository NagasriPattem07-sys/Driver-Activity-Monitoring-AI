import textwrap

import streamlit as st


def _flatten(markup: str) -> str:
    """
    Strip indentation and blank lines so Markdown never treats indented
    HTML as a code block.
    """
    lines = textwrap.dedent(markup).splitlines()
    return "\n".join(line.strip() for line in lines if line.strip())


def render(markup: str):
    """Render a block of HTML safely."""
    st.markdown(_flatten(markup), unsafe_allow_html=True)


FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
"""

CSS = """
<style>

/* ===== DESIGN TOKENS: Midnight Navy + Signal Cyan ===== */
:root {
    --bg: #0B1220;
    --surface: #111B2E;
    --surface-2: #16233A;
    --line: #223350;
    --text: #E6EDF7;
    --muted: #8DA0BC;
    --cyan: #22D3EE;
    --green: #34D399;
    --amber: #FBBF24;
    --red: #F87171;
}

/* ===== BASE ===== */
.stApp {
    background: var(--bg);
    color: var(--text);
}

.stApp, .stMarkdown, .stMarkdown p, button, input, textarea,
[data-testid="stMetric"], [data-testid="stFileUploader"],
[data-testid="stSidebar"] label {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5,
.app-title, .brand-name, .step-title, .section-title {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.3px;
}

.stMarkdown p, .stCaption, label {
    color: #C5D2E6;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2.2rem;
    max-width: 1250px;
}

/* ===== HIDE STREAMLIT CHROME ===== */
[data-testid="stAppDeployButton"],
.stDeployButton,
#MainMenu,
[data-testid="stMainMenu"],
footer {
    display: none !important;
}

hr {
    border-color: var(--line) !important;
}

/* ===== TOP HEADER ===== */
.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 14px;
    padding: 16px 20px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    margin-bottom: 26px;
}

.app-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.app-title {
    font-size: 22px;
    font-weight: 700;
    line-height: 1.2;
}

.app-sub {
    color: var(--muted);
    font-size: 13px;
    margin-top: 2px;
}

.chip {
    display: inline-block;
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.4px;
    color: var(--muted);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 5px 12px;
}

.chip-cyan {
    color: var(--cyan);
    border-color: rgba(34, 211, 238, 0.4);
    background: rgba(34, 211, 238, 0.07);
}

/* ===== SECTIONS ===== */
.section-title {
    font-size: 20px;
    font-weight: 600;
    margin: 4px 0 4px 0;
}

.section-sub {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 14px;
}

/* ===== FILE PILL ===== */
.file-pill {
    display: inline-flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 10px 16px;
    color: var(--muted);
    font-size: 13.5px;
    margin: 10px 0 18px 0;
}

.file-pill b {
    color: var(--text);
    font-weight: 600;
}

.file-pill .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--green);
}

.file-pill .sep {
    width: 1px;
    height: 14px;
    background: var(--line);
}

/* ===== STEP CARDS (empty state) ===== */
.step-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 16px;
    margin-top: 22px;
}

.step-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 2px solid var(--cyan);
    border-radius: 14px;
    padding: 20px 22px;
}

.step-num {
    color: var(--cyan);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.step-title {
    font-size: 17px;
    font-weight: 600;
    margin: 6px 0 4px 0;
}

.step-desc {
    color: var(--muted);
    font-size: 13.5px;
    line-height: 1.55;
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploaderDropzone"] {
    background: var(--surface);
    border: 1px dashed #2B4266;
    border-radius: 14px;
    transition: border-color 0.2s ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--cyan);
}

/* ===== BUTTONS ===== */
.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1.3rem;
    background: var(--surface-2);
    color: var(--text);
    border: 1px solid var(--line);
    transition: all 0.2s ease;
}

.stButton > button p,
.stDownloadButton > button p {
    color: inherit !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: var(--cyan);
    color: var(--cyan);
}

.stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    background: var(--cyan);
    color: #06202B;
    border: 1px solid var(--cyan);
    font-weight: 700;
}

.stButton > button[kind="primary"] p,
button[data-testid="stBaseButton-primary"] p {
    color: #06202B !important;
}

.stButton > button[kind="primary"]:hover,
button[data-testid="stBaseButton-primary"]:hover {
    background: #67E8F9;
    border-color: #67E8F9;
    color: #06202B;
}

/* ===== TABS ===== */
button[data-baseweb="tab"] {
    font-weight: 600;
}

[data-baseweb="tab-highlight"] {
    background: var(--cyan) !important;
}

/* ===== METRICS, TABLES, ALERTS ===== */
div[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 16px 18px;
}

div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] * {
    color: var(--muted) !important;
    font-weight: 500;
}

div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] > div {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text) !important;
    font-weight: 600;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
}

/* ===== RESULTS DASHBOARD ===== */
[class*="st-key-panel"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 18px 20px 14px 20px;
    margin-bottom: 8px;
}

.result-head {
    margin: 10px 0 14px 0;
}

.panel-label {
    color: var(--muted);
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-bottom: 4px;
}

.panel-sub {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 6px;
}

.score-foot {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    padding: 2px 0 8px 0;
}

.grade-badge, .risk-chip {
    font-size: 13px;
    font-weight: 700;
    color: var(--c);
    border: 1px solid var(--c);
    border-radius: 20px;
    padding: 6px 14px;
    background: color-mix(in srgb, var(--c) 12%, transparent);
}

.status-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 14px;
}

.status-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 2px solid var(--c);
    border-radius: 14px;
    padding: 16px 18px;
}

.status-name {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--c);
}

.status-pct {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 600;
    color: var(--text);
    line-height: 1.1;
    margin-top: 8px;
}

.status-count {
    color: var(--muted);
    font-size: 12.5px;
    margin-top: 2px;
}

.bar {
    height: 6px;
    background: var(--surface-2);
    border-radius: 6px;
    margin-top: 12px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: var(--c);
    border-radius: 6px;
}

.insight-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
}

.insight-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 14px 18px;
}

.insight-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 600;
    color: var(--text);
}

.insight-label {
    color: var(--muted);
    font-size: 12.5px;
    margin-top: 2px;
}

.reco-lead {
    color: var(--text);
    font-size: 16px;
    line-height: 1.55;
    margin: 8px 0 14px 0;
}

.tip-list {
    margin: 0;
    padding-left: 20px;
    color: #C5D2E6;
    font-size: 14px;
    line-height: 1.9;
}

.tip-list li::marker {
    color: var(--c);
}

@media (max-width: 900px) {
    .status-grid {
        grid-template-columns: 1fr;
    }
}

/* ===== PATCH: equal heights, calc box, cyan selection fallbacks ===== */
.right-stack {
    display: flex;
    flex-direction: column;
    gap: 14px;
    min-height: 341px;
}

.right-stack .status-grid,
.right-stack .insight-grid {
    margin-bottom: 0;
    flex: 1;
}

.st-key-panel_mix {
    min-height: 383px;
}

.calc-box {
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--line);
}

.calc-title {
    color: var(--muted);
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 1.4px;
    margin-bottom: 8px;
}

.calc-row {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    font-size: 12.5px;
    padding: 3px 0;
    color: var(--muted);
}

.calc-row span:first-child {
    color: var(--text);
    font-weight: 600;
    flex: 0 0 auto;
}

.calc-row span:last-child {
    text-align: right;
}

.calc-note {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.5;
    margin-top: 8px;
    font-style: italic;
}

.right-stack .status-card,
.right-stack .insight-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* selected tab: cyan (current Streamlit uses data-selected on role="tab") */
[data-testid="stTabs"] [role="tab"][data-selected],
[data-testid="stTabs"] [role="tab"][data-selected] *,
[data-testid="stTabs"] [role="tab"][data-hovered],
[data-testid="stTabs"] [role="tab"][data-hovered] * {
    color: var(--cyan) !important;
}

[data-testid="stTabs"] [role="tab"][data-selected] .react-aria-SelectionIndicator {
    background-color: var(--cyan) !important;
}

/* older Streamlit versions (baseweb tabs) */
button[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] * {
    color: var(--cyan) !important;
}

[data-baseweb="tab-highlight"],
div[data-baseweb="tab-highlight"] {
    background-color: var(--cyan) !important;
}

/* selected filter button (segmented control): cyan instead of red */
button[kind="segmented_controlActive"],
button[data-testid="stBaseButton-segmented_controlActive"] {
    background: rgba(34, 211, 238, 0.14) !important;
    border-color: var(--cyan) !important;
    color: var(--cyan) !important;
}

button[kind="segmented_controlActive"] *,
button[data-testid="stBaseButton-segmented_controlActive"] * {
    color: var(--cyan) !important;
}

@media (max-width: 900px) {
    .right-stack {
        min-height: 0;
    }
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #0D1626;
    border-right: 1px solid var(--line);
}

.side-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
}

.brand-name {
    font-size: 22px;
    font-weight: 700;
    line-height: 1.1;
}

.brand-tag {
    color: var(--cyan);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.7px;
    margin-top: 3px;
}

.side-rule {
    height: 1px;
    background: var(--line);
    margin: 18px 0 6px 0;
}

.sidebar-label {
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 22px 0 12px 0;
}

.flow-step {
    position: relative;
    display: flex;
    gap: 12px;
    padding-bottom: 16px;
}

.flow-step:not(:last-child)::after {
    content: "";
    position: absolute;
    left: 11px;
    top: 26px;
    bottom: 2px;
    width: 1px;
    background: var(--line);
}

.flow-num {
    flex: 0 0 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--surface-2);
    border: 1px solid #2B4266;
    color: var(--cyan);
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
}

.flow-title {
    color: var(--text);
    font-size: 13px;
    font-weight: 600;
}

.flow-desc {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.5;
}

.state-row {
    display: flex;
    gap: 10px;
    padding: 6px 0;
}

.state-dot {
    flex: 0 0 9px;
    height: 9px;
    border-radius: 50%;
    margin-top: 5px;
}

.state-name {
    color: var(--text);
    font-size: 13px;
    font-weight: 600;
}

.state-desc {
    color: var(--muted);
    font-size: 12px;
    line-height: 1.45;
}

.model-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 12px 14px;
}

.model-card b {
    color: var(--text);
    font-size: 14px;
}

.model-card span {
    display: block;
    color: var(--muted);
    font-size: 12px;
    margin-top: 2px;
}

.side-foot {
    color: #5F7391;
    font-size: 11.5px;
    margin-top: 26px;
}

.footer {
    color: var(--muted);
    text-align: center;
    font-size: 12.5px;
    padding: 34px 0 10px 0;
    border-top: 1px solid var(--line);
    margin-top: 40px;
}

</style>
"""


def load_css():
    """Inject fonts and the Midnight Navy + Signal Cyan theme."""
    st.markdown(_flatten(FONTS), unsafe_allow_html=True)
    st.markdown(CSS, unsafe_allow_html=True)
