import pandas as pd
import plotly.express as px
import streamlit as st


def show_charts(normal, slow, aggressive):

    chart_df = pd.DataFrame({
        "Behaviour": ["Normal", "Slow", "Aggressive"],
        "Count": [normal, slow, aggressive]
    })

    col1, col2 = st.columns(2)

    with col1:

        pie = px.pie(
            chart_df,
            names="Behaviour",
            values="Count",
            hole=0.45,
            title="Behaviour Distribution"
        )

        pie.update_traces(textposition="inside")

        st.plotly_chart(
            pie,
            width="stretch"
        )

    with col2:

        bar = px.bar(
            chart_df,
            x="Behaviour",
            y="Count",
            text_auto=True,
            title="Behaviour Count"
        )

        st.plotly_chart(
            bar,
            width="stretch"
        )