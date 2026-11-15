from collections import Counter
from html import escape
from itertools import groupby
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from prediction import predict_driver
from report import generate_pdf
from utils.styling import render


# ==========================================
# THEME CONSTANTS (Midnight Navy + Signal Cyan)
# ==========================================

GREEN = "#34D399"
AMBER = "#FBBF24"
RED = "#F87171"
CYAN = "#22D3EE"
TEXT = "#E6EDF7"
MUTED = "#8DA0BC"
LINE = "#223350"

# (display name, model label, colour)
STATES = [
    ("Normal", "NORMAL", GREEN),
    ("Slow", "SLOW", AMBER),
    ("Aggressive", "AGGRESSIVE", RED),
]

# Practical tips shown under the recommendation
TIPS = {
    "AGGRESSIVE": [
        "Brake more smoothly.",
        "Maintain a safe following distance.",
        "Avoid harsh steering.",
    ],
    "SLOW": [
        "Increase confidence while driving.",
        "Maintain better traffic flow.",
        "Avoid unnecessary slowdowns.",
    ],
    "NORMAL": [
        "Excellent driving behaviour. Keep it up.",
    ],
}


# ==========================================
# HELPERS
# ==========================================

def aggressive_streaks(predictions):
    """Returns (number of aggressive episodes, longest episode in windows)."""
    lengths = [
        len(list(group))
        for label, group in groupby(predictions)
        if label == "AGGRESSIVE"
    ]
    return len(lengths), (max(lengths) if lengths else 0)


def make_gauge(score):
    """Safety-score gauge: green >= 80, amber >= 60, red below."""
    colour = GREEN if score >= 80 else AMBER if score >= 60 else RED

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "valueformat": ".1f",
            "font": {"size": 46, "family": "Space Grotesk", "color": TEXT},
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickcolor": LINE,
                "tickfont": {"size": 11, "color": MUTED},
            },
            "bar": {"color": colour, "thickness": 0.3},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 60], "color": "rgba(248,113,113,0.24)"},
                {"range": [60, 80], "color": "rgba(251,191,36,0.24)"},
                {"range": [80, 100], "color": "rgba(52,211,153,0.24)"},
            ],
        },
    ))

    fig.update_layout(
        height=240,
        margin=dict(l=30, r=30, t=20, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT),
    )
    return fig


def make_timeline(predictions):
    """One coloured bar per window, in trip order."""
    total = len(predictions)
    fig = go.Figure()

    for name, key, colour in STATES:
        xs = [i + 1 for i, p in enumerate(predictions) if p == key]
        fig.add_trace(go.Bar(
            x=xs,
            y=[1] * len(xs),
            name=name,
            width=1,
            marker=dict(color=colour, line=dict(width=0)),
            hovertemplate=f"Window %{{x}}<br>{name}<extra></extra>",
        ))

    fig.update_layout(
        barmode="overlay",
        bargap=0,
        height=190,
        margin=dict(l=0, r=0, t=34, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT),
        hoverlabel=dict(bgcolor="#16233A", font_color=TEXT),
        yaxis=dict(visible=False, range=[0, 1]),
        xaxis=dict(
            title="Window",
            range=[0.5, total + 0.5],
            showgrid=False,
            linecolor=LINE,
            tickfont=dict(color=MUTED),
            title_font=dict(color=MUTED, size=12),
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, font=dict(color=TEXT),
        ),
    )
    return fig


def make_donut(normal, slow, aggressive, total):
    fig = go.Figure(go.Pie(
        labels=["Normal", "Slow", "Aggressive"],
        values=[normal, slow, aggressive],
        hole=0.68,
        sort=False,
        textinfo="none",
        marker=dict(colors=[GREEN, AMBER, RED], line=dict(color="#111B2E", width=3)),
        hovertemplate="%{label}: %{value} windows (%{percent})<extra></extra>",
    ))

    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:12px;color:{MUTED}'>windows</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=28, family="Space Grotesk", color=TEXT),
    )

    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT),
        legend=dict(
            orientation="h", yanchor="top", y=-0.02,
            xanchor="center", x=0.5, font=dict(color=TEXT),
        ),
    )
    return fig


def status_card(name, colour, count, percent):
    return f"""
    <div class="status-card" style="--c:{colour};">
        <div class="status-name"><span class="status-dot"></span>{name}</div>
        <div class="status-pct">{percent:.1f}%</div>
        <div class="status-count">{count:,} windows</div>
        <div class="bar"><div class="bar-fill" style="width:{percent:.1f}%;"></div></div>
    </div>
    """


def style_report(df):
    """Colour the Prediction and Risk columns (falls back to plain table)."""
    palette = {
        "Normal": GREEN, "Low": GREEN,
        "Slow": AMBER, "Medium": AMBER,
        "Aggressive": RED, "High": RED,
    }

    def paint(value):
        colour = palette.get(value)
        return f"color: {colour}; font-weight: 600" if colour else ""

    try:
        styler = df.style
        apply = styler.map if hasattr(styler, "map") else styler.applymap
        return apply(paint, subset=["Prediction", "Risk"])
    except Exception:
        return df


# ==========================================
# MAIN DASHBOARD
# ==========================================

def driver_agent(sensor_dataframe):

    predictions = [str(p) for p in predict_driver(sensor_dataframe)]

    total = len(predictions)

    if total == 0:
        st.warning("No driving windows could be analysed from this file.")
        return

    counts = Counter(predictions)

    normal = counts.get("NORMAL", 0)
    slow = counts.get("SLOW", 0)
    aggressive = counts.get("AGGRESSIVE", 0)

    normal_percent = (normal / total) * 100
    slow_percent = (slow / total) * 100
    aggressive_percent = (aggressive / total) * 100

    # ---- scoring logic (unchanged) ----
    safety_score = ((normal + (0.5 * slow)) / total) * 100

    if safety_score >= 90:
        grade = "A+"
    elif safety_score >= 80:
        grade = "A"
    elif safety_score >= 70:
        grade = "B"
    elif safety_score >= 60:
        grade = "C"
    else:
        grade = "D"

    if aggressive_percent > 30:
        recommendation = (
            "Frequent aggressive driving detected. "
            "Reduce harsh braking, sudden acceleration "
            "and maintain a constant speed."
        )
        focus = "AGGRESSIVE"

    elif slow_percent > 40:
        recommendation = (
            "Driver is overly cautious. "
            "Improve confidence while maintaining safety."
        )
        focus = "SLOW"

    else:
        recommendation = "Driving behaviour is smooth and safe."
        focus = "NORMAL"

    if aggressive_percent >= 50:
        risk_label, risk_colour = "High risk", RED
    elif aggressive_percent >= 25:
        risk_label, risk_colour = "Medium risk", AMBER
    else:
        risk_label, risk_colour = "Low risk", GREEN

    grade_colour = {
        "A+": GREEN, "A": GREEN, "B": CYAN, "C": AMBER, "D": RED
    }[grade]

    focus_colour = {"AGGRESSIVE": RED, "SLOW": AMBER, "NORMAL": GREEN}[focus]

    episodes, longest = aggressive_streaks(predictions)

    # ---- header ----
    render(f"""
    <div class="result-head">
        <div class="section-title">Driver analysis</div>
        <div class="section-sub" style="margin-bottom:0;">
            {total:,} driving windows analysed
        </div>
    </div>
    """)

    # ---- row 1: score + status cards ----
    left, right = st.columns([1, 1.45], gap="medium")

    with left:
        with st.container(key="panel_score"):

            render('<div class="panel-label">SAFETY SCORE</div>')

            st.plotly_chart(
                make_gauge(safety_score),
                width="stretch",
                theme=None,
                config={"displayModeBar": False},
            )

            render(f"""
            <div class="score-foot">
                <div class="grade-badge" style="--c:{grade_colour};">Grade {grade}</div>
                <div class="risk-chip" style="--c:{risk_colour};">{risk_label}</div>
            </div>
            """)

    with right:

        cards = "".join(
            status_card(name, colour, counts.get(key, 0),
                        (counts.get(key, 0) / total) * 100)
            for name, key, colour in STATES
        )

        render(f"""
        <div class="right-stack">
        <div class="status-grid">{cards}</div>
        <div class="insight-grid">
            <div class="insight-card">
                <div class="insight-val">{episodes}</div>
                <div class="insight-label">Aggressive episodes</div>
            </div>
            <div class="insight-card">
                <div class="insight-val">{longest}</div>
                <div class="insight-label">Longest aggressive stretch (windows)</div>
            </div>
        </div>
        </div>
        """)

    # ---- row 2: timeline ----
    with st.container(key="panel_timeline"):

        render("""
        <div class="panel-label">BEHAVIOUR TIMELINE</div>
        <div class="panel-sub">Each bar is one analysed window, in trip order.</div>
        """)

        st.plotly_chart(
            make_timeline(predictions),
            width="stretch",
            theme=None,
            config={"displayModeBar": False},
        )

    # ---- row 3: mix + recommendation ----
    mix, reco = st.columns([1, 1.2], gap="medium")

    with mix:
        with st.container(key="panel_mix"):

            render('<div class="panel-label">BEHAVIOUR MIX</div>')

            st.plotly_chart(
                make_donut(normal, slow, aggressive, total),
                width="stretch",
                theme=None,
                config={"displayModeBar": False},
            )

    with reco:
        with st.container(key="panel_reco"):

            tips = "".join(f"<li>{escape(t)}</li>" for t in TIPS[focus])

            render(f"""
            <div class="panel-label">AI RECOMMENDATION</div>
            <div class="reco-lead">{escape(recommendation)}</div>
            <ul class="tip-list" style="--c:{focus_colour};">{tips}</ul>
            <div class="calc-box">
                <div class="calc-title">How the score is calculated</div>
                <div class="calc-row"><span>Safety score</span>
                    <span>(Normal + &frac12; &times; Slow) &divide; total windows</span></div>
                <div class="calc-row"><span>Grade</span>
                    <span>A+ 90 &middot; A 80 &middot; B 70 &middot; C 60 &middot; D below 60</span></div>
                <div class="calc-row"><span>Risk</span>
                    <span>Share of aggressive windows: High 50%+, Medium 25%+</span></div>
                <div class="calc-note">
                    Risk looks only at aggressive driving, so a trip can earn a low
                    grade and still carry medium risk.
                </div>
            </div>
            """)

    # ---- report table + downloads ----
    report = pd.DataFrame({
        "Window": range(1, total + 1),
        "Prediction": [p.title() for p in predictions],
    })

    report["Risk"] = report["Prediction"].map({
        "Normal": "Low",
        "Slow": "Medium",
        "Aggressive": "High",
    })

    with st.container(key="panel_table"):

        render('<div class="panel-label">WINDOW-BY-WINDOW PREDICTIONS</div>')

        choice = st.segmented_control(
            "Show",
            ["All", "Normal", "Slow", "Aggressive"],
            default="All",
            label_visibility="collapsed",
            key="driver_filter",
        )

        view = report if choice in (None, "All") else report[
            report["Prediction"] == choice
        ]

        st.dataframe(
            style_report(view),
            width="stretch",
            hide_index=True,
            height=340,
            column_config={
                "Window": st.column_config.NumberColumn("Window", width="small"),
                "Prediction": st.column_config.TextColumn("Prediction", width="medium"),
                "Risk": st.column_config.TextColumn("Risk", width="small"),
            },
        )

        csv = report.to_csv(index=False).encode("utf-8")

        pdf_file = generate_pdf(
            total,
            normal,
            slow,
            aggressive,
            safety_score,
            grade,
            recommendation,
        )

        d1, d2, _ = st.columns([1, 1, 2])

        with d1:
            st.download_button(
                "Download CSV report",
                csv,
                file_name="driver_prediction_report.csv",
                mime="text/csv",
            )

        with d2:
            st.download_button(
                "Download PDF report",
                data=Path(pdf_file).read_bytes(),
                file_name="Driver_Report.pdf",
                mime="application/pdf",
            )
