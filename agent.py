import streamlit as st
import plotly.express as px
import pandas as pd

from prediction import predict_driver
from collections import Counter


def driver_agent(sensor_dataframe):

    predictions = predict_driver(sensor_dataframe)

    counts = Counter(predictions)

    normal = counts.get("NORMAL", 0)
    slow = counts.get("SLOW", 0)
    aggressive = counts.get("AGGRESSIVE", 0)

    total = len(predictions)

    safety_score = ((normal + 0.5 * slow) / total) * 100

    st.header("🚗 Driver Analysis Dashboard")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Windows", total)
    c2.metric("🟢 Normal", normal)
    c3.metric("🟡 Slow", slow)
    c4.metric("🔴 Aggressive", aggressive)

    st.divider()

    st.subheader("Driver Safety Score")

    st.progress(safety_score / 100)

    st.markdown(
        f"<h2 style='text-align:center;color:green'>{safety_score:.1f}/100</h2>",
        unsafe_allow_html=True
    )

    if safety_score >= 80:
        st.success("Excellent Driving Behaviour 🚗")

    elif safety_score >= 60:
        st.warning("Moderate Driving Behaviour")

    else:
        st.error("Unsafe Driving Behaviour")

    st.divider()

    chart_data = pd.DataFrame({
        "Behaviour": ["NORMAL", "SLOW", "AGGRESSIVE"],
        "Count": [normal, slow, aggressive]
    })

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🥧 Behaviour Distribution")

        fig = px.pie(
            chart_data,
            names="Behaviour",
            values="Count",
            hole=0.45
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("📊 Behaviour Count")

        fig2 = px.bar(
            chart_data,
            x="Behaviour",
            y="Count",
            color="Behaviour"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI Recommendation")

    if aggressive > normal:

        st.error(
            "Driver shows frequent aggressive behaviour.\n\n"
            "• Reduce harsh braking\n"
            "• Avoid sudden acceleration\n"
            "• Maintain safe speed"
        )

    elif slow > aggressive:

        st.warning(
            "Driver is overly cautious.\n\n"
            "• Maintain traffic flow\n"
            "• Avoid unnecessary slow driving"
        )

    else:

        st.success(
            "Driver behaviour is smooth and safe.\n\n"
            "Continue driving responsibly."
        )

    st.divider()

    with st.expander("📋 Detailed Prediction Report"):

        for i, behaviour in enumerate(predictions, start=1):

            colA, colB = st.columns([1,4])

            colA.write(f"**{i}**")

            if behaviour == "NORMAL":

                colB.success("🟢 NORMAL")

            elif behaviour == "SLOW":

                colB.warning("🟡 SLOW")

            else:

                colB.error("🔴 AGGRESSIVE")