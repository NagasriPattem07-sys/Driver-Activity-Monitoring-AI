import streamlit as st


def show_ai_insights(
    normal_percent,
    slow_percent,
    aggressive_percent,
    safety_score,
    total
):

    if aggressive_percent > 40:

        driver_type = "Aggressive Driver"

    elif slow_percent > 50:

        driver_type = "Overly Cautious Driver"

    else:

        driver_type = "Balanced Driver"

    confidence = max(
        normal_percent,
        slow_percent,
        aggressive_percent
    )

    st.subheader("🧠 AI Trip Intelligence")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"""
### 🚗 Trip Summary

**Driver Type**

{driver_type}

**Model**

XGBoost Classifier

**Confidence**

{confidence:.1f}%

**Windows Analysed**

{total}
""")

    with col2:

        st.success(f"""
### 🤖 AI Coach

Normal : {normal_percent:.1f}%

Slow : {slow_percent:.1f}%

Aggressive : {aggressive_percent:.1f}%

Safety Score

{safety_score:.1f}/100
""")

    st.divider()

    st.subheader("📌 AI Recommendations")

    recommendations = []

    if aggressive_percent > 30:

        recommendations.extend([
            "Reduce sudden acceleration.",
            "Brake more smoothly.",
            "Maintain safe following distance.",
            "Avoid harsh steering."
        ])

    if slow_percent > 40:

        recommendations.extend([
            "Increase confidence while driving.",
            "Maintain better traffic flow.",
            "Avoid unnecessary slowdowns."
        ])

    if normal_percent > 60:

        recommendations.append(
            "Excellent driving behaviour. Keep it up!"
        )

    for tip in recommendations:

        st.write(f"✅ {tip}")