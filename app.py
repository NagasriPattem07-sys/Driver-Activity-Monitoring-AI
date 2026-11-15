from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from agent import driver_agent
from utils.styling import load_css, render

st.set_page_config(
    page_title="Driver Activity Monitoring AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# Sample trip used by the "Try sample trip" button
SAMPLE_PATH = Path(__file__).parent / "dataset" / "test_motion_data.csv"

# Three-colour speedometer mark (green / amber / red = driving states)
LOGO = '<svg width="40" height="40" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="44" height="44" rx="13" fill="#16233A" stroke="#223350"/><path d="M11.0 32.0 A14 14 0 0 1 14.9 16.2" fill="none" stroke="#34D399" stroke-width="3.4" stroke-linecap="round"/><path d="M15.8 15.4 A14 14 0 0 1 32.1 15.4" fill="none" stroke="#FBBF24" stroke-width="3.4" stroke-linecap="round"/><path d="M33.1 16.2 A14 14 0 0 1 37.0 32.0" fill="none" stroke="#F87171" stroke-width="3.4" stroke-linecap="round"/><line x1="24" y1="26.8" x2="28.5" y2="19.0" stroke="#22D3EE" stroke-width="2.6" stroke-linecap="round"/><circle cx="24" cy="26.8" r="2.8" fill="#E6EDF7"/></svg>'


# ==========================================
# HEADER
# ==========================================

render(f"""
<div class="app-header">
    <div class="app-brand">
        {LOGO}
        <div>
            <div class="app-title">Driver Activity Monitoring AI</div>
            <div class="app-sub">
                Machine-learning analysis of driving behaviour from motion-sensor data
            </div>
        </div>
    </div>
    <div class="chip chip-cyan">XGBOOST CLASSIFIER</div>
</div>
""")


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    render(f"""
    <div class="side-brand">
        {LOGO}
        <div>
            <div class="brand-name">Driver AI</div>
            <div class="brand-tag">BEHAVIOUR INTELLIGENCE</div>
        </div>
    </div>
    <div class="side-rule"></div>
    """)

    render('<div class="sidebar-label">HOW IT WORKS</div>')

    render("""
    <div class="flow-step">
        <div class="flow-num">1</div>
        <div><div class="flow-title">Upload</div>
        <div class="flow-desc">Motion-sensor CSV from a trip</div></div>
    </div>
    <div class="flow-step">
        <div class="flow-num">2</div>
        <div><div class="flow-title">Analyse</div>
        <div class="flow-desc">The model classifies each window of driving</div></div>
    </div>
    <div class="flow-step">
        <div class="flow-num">3</div>
        <div><div class="flow-title">Review</div>
        <div class="flow-desc">Safety score, risk level and report download</div></div>
    </div>
    """)

    render('<div class="sidebar-label">DRIVING STATES</div>')

    render("""
    <div class="state-row">
        <div class="state-dot" style="background:#34D399;"></div>
        <div><div class="state-name">Normal</div>
        <div class="state-desc">Smooth, steady driving</div></div>
    </div>
    <div class="state-row">
        <div class="state-dot" style="background:#FBBF24;"></div>
        <div><div class="state-name">Slow</div>
        <div class="state-desc">Hesitant or unnecessarily slow</div></div>
    </div>
    <div class="state-row">
        <div class="state-dot" style="background:#F87171;"></div>
        <div><div class="state-name">Aggressive</div>
        <div class="state-desc">Harsh braking, acceleration or steering</div></div>
    </div>
    """)

    render('<div class="sidebar-label">MODEL</div>')

    render("""
    <div class="model-card">
        <b>XGBoost</b>
        <span>Multi-class classifier</span>
    </div>
    <div class="side-foot">Built by Pattem Nagasri</div>
    """)


# ==========================================
# DATA SOURCE (upload or sample)
# ==========================================

render("""
<div class="section-title">Upload sensor data</div>
<div class="section-sub">
    CSV file with accelerometer and gyroscope readings (AccX to AccZ, GyroX to GyroZ).
</div>
""")

uploaded_file = st.file_uploader(
    "Sensor data (CSV)",
    type=["csv"],
    label_visibility="collapsed"
)

data = None
source_label = ""
using_sample = False

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)
    source_label = uploaded_file.name

elif st.session_state.get("use_sample") and SAMPLE_PATH.exists():

    data = pd.read_csv(SAMPLE_PATH)
    source_label = "Sample trip"
    using_sample = True


# ==========================================
# EMPTY STATE
# ==========================================

if data is None:

    if SAMPLE_PATH.exists():

        if st.button("Try sample trip"):
            st.session_state["use_sample"] = True
            st.rerun()

    render("""
    <div class="step-grid">
        <div class="step-card">
            <div class="step-num">STEP 1</div>
            <div class="step-title">Upload a trip</div>
            <div class="step-desc">
                Drop in a CSV of motion-sensor readings, or load the sample trip.
            </div>
        </div>
        <div class="step-card">
            <div class="step-num">STEP 2</div>
            <div class="step-title">Run the analysis</div>
            <div class="step-desc">
                The XGBoost model labels each window as Normal, Slow or Aggressive.
            </div>
        </div>
        <div class="step-card">
            <div class="step-num">STEP 3</div>
            <div class="step-title">Review and export</div>
            <div class="step-desc">
                See the safety score, risk level and recommendations, then download the report.
            </div>
        </div>
    </div>
    """)


# ==========================================
# LOADED STATE
# ==========================================

else:

    rows, cols = data.shape

    render(f"""
    <div class="file-pill">
        <span class="dot"></span>
        <b>{escape(source_label)}</b>
        <span class="sep"></span>{rows:,} rows
        <span class="sep"></span>{cols} columns
    </div>
    """)

    if using_sample:
        if st.button("Remove sample"):
            st.session_state["use_sample"] = False
            st.rerun()

    tab1, tab2 = st.tabs(["Data preview", "AI analysis"])

    with tab1:

        st.dataframe(
            data.head(20),
            width="stretch"
        )

        with st.expander("Column details"):

            st.dataframe(
                pd.DataFrame({
                    "Column": data.columns,
                    "Type": data.dtypes.astype(str).values
                }),
                width="stretch",
                hide_index=True
            )

    # Remember which dataset was analysed so the results stay on screen
    # when the user clicks filters or download buttons
    data_key = f"{source_label}|{rows}|{cols}"

    with tab2:

        if st.button("Analyze driver behaviour", type="primary"):
            st.session_state["analysed_key"] = data_key

        if st.session_state.get("analysed_key") == data_key:
            driver_agent(data)


# ==========================================
# FOOTER
# ==========================================

render("""
<div class="footer">
    Driver Activity Monitoring AI &nbsp;·&nbsp; XGBoost &nbsp;·&nbsp; Streamlit
    &nbsp;·&nbsp; Built by Pattem Nagasri
</div>
""")
