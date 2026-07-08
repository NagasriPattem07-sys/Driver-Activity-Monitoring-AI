import streamlit as st
import pandas as pd

from agent import driver_agent

st.set_page_config(
    page_title="Driver Activity Monitoring AI",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Driver Activity Monitoring AI")

st.caption("AI-powered Driver Behaviour Analysis using Machine Learning")

st.divider()

uploaded_file = st.file_uploader(
    "📂 Upload Driving Sensor Dataset",
    type=["csv"]
)

if uploaded_file:

    data = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully.")

    with st.expander("Preview Dataset"):

        st.dataframe(data.head())

    st.divider()

    if st.button("🚀 Analyze Driver"):

        driver_agent(data)