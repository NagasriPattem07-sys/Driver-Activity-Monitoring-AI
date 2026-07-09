import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from prediction import predict_driver
from report import generate_pdf


def driver_agent(sensor_dataframe):

    predictions = predict_driver(sensor_dataframe)

    counts = Counter(predictions)

    normal = counts.get("NORMAL", 0)
    slow = counts.get("SLOW", 0)
    aggressive = counts.get("AGGRESSIVE", 0)

    total = len(predictions)

    normal_percent = (normal / total) * 100
    slow_percent = (slow / total) * 100
    aggressive_percent = (aggressive / total) * 100

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

    elif slow_percent > 40:

        recommendation = (
            "Driver is overly cautious. "
            "Improve confidence while maintaining safety."
        )

    else:

        recommendation = (
            "Driving behaviour is smooth and safe."
        )

    st.header("🚗 Driver Analysis Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Windows", total)
    c2.metric("🟢 Normal", normal)
    c3.metric("🟡 Slow", slow)
    c4.metric("🔴 Aggressive", aggressive)

    st.divider()

    st.subheader("🏅 Driver Report Card")

    left, right = st.columns([2, 1])

    with left:

        st.metric("Safety Score", f"{safety_score:.1f}/100")

        st.progress(safety_score / 100)

    with right:

        st.metric("Driver Grade", grade)

    st.divider()

    st.subheader("📊 Behaviour Statistics")

    p1, p2, p3 = st.columns(3)

    p1.metric("🟢 Normal %", f"{normal_percent:.1f}%")
    p2.metric("🟡 Slow %", f"{slow_percent:.1f}%")
    p3.metric("🔴 Aggressive %", f"{aggressive_percent:.1f}%")

    st.divider()

    chart_df = pd.DataFrame({

        "Behaviour": ["Normal", "Slow", "Aggressive"],

        "Count": [normal, slow, aggressive]

    })

    left, right = st.columns(2)

    with left:

        fig = px.pie(

            chart_df,

            names="Behaviour",

            values="Count",

            hole=0.5,

            title="Behaviour Distribution"

        )

        st.plotly_chart(fig, width="stretch")

    with right:

        fig2 = px.bar(

            chart_df,

            x="Behaviour",

            y="Count",

            text_auto=True,

            title="Behaviour Count"

        )

        st.plotly_chart(fig2, width="stretch")

    st.divider()

    st.subheader("🚦 Driver Risk Meter")

    if aggressive_percent >= 50:

        st.error("🔴 HIGH RISK DRIVER")

    elif aggressive_percent >= 25:

        st.warning("🟡 MEDIUM RISK DRIVER")

    else:

        st.success("🟢 SAFE DRIVER")

    st.divider()

    st.subheader("🤖 AI Recommendation")

    st.info(recommendation)

    st.divider()

    st.subheader("🚗 Journey Summary")

    st.write(f"""
Trip Analysis

• Total Driving Windows : **{total}**

• Safe Driving : **{normal_percent:.1f}%**

• Moderate Driving : **{slow_percent:.1f}%**

• Aggressive Driving : **{aggressive_percent:.1f}%**

Overall Driver Grade : **{grade}**
""")

    st.divider()

    report = pd.DataFrame({

        "Window": range(1, total + 1),

        "Prediction": predictions

    })

    report["Risk"] = report["Prediction"].map({

        "NORMAL": "🟢 Low",

        "SLOW": "🟡 Medium",

        "AGGRESSIVE": "🔴 High"

    })

    st.subheader("📋 Prediction Report")

    st.dataframe(report.head(20), width="stretch")

    csv = report.to_csv(index=False).encode("utf-8")

    st.download_button(

        "⬇ Download CSV Report",

        csv,

        file_name="driver_prediction_report.csv",

        mime="text/csv"

    )

    pdf_file = generate_pdf(

        total,

        normal,

        slow,

        aggressive,

        safety_score,

        grade,

        recommendation

    )

    with open(pdf_file, "rb") as file:

        st.download_button(

            "📄 Download PDF Report",

            data=file,

            file_name="Driver_Report.pdf",

            mime="application/pdf"

        )

    st.divider()

    st.markdown("---")

    st.markdown(
        "<center><h4>🚗 Driver Activity Monitoring AI</h4></center>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<center>Built with ❤️ by <b>Pattem Nagasri</b></center>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<center>XGBoost • Streamlit • Machine Learning</center>",
        unsafe_allow_html=True
    )