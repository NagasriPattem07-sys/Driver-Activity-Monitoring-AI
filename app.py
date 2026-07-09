import streamlit as st
import pandas as pd
from agent import driver_agent
from utils.styling import load_css

st.set_page_config(
    page_title="Driver Activity Monitoring AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

st.markdown("""
<div class="hero">
<h1>🚗 Driver Activity Monitoring AI</h1>
<p>AI Powered Driver Behaviour Analysis using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:

    st.title("🚘 Driver AI")

    st.markdown("---")

    st.info("""
Upload a driving sensor dataset and let the AI analyze:

✅ Driving Behaviour

✅ Safety Score

✅ Risk Level

✅ AI Recommendations

✅ Download Report
""")

    st.markdown("---")

    st.success("Model : XGBoost")

    st.success("Prediction : Multi-Class")

    st.success("Developer : Pattem Nagasri")

st.subheader("📂 Upload Driving Sensor Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.success("✅ Dataset uploaded successfully.")

    tab1, tab2 = st.tabs([
        "📄 Dataset Preview",
        "🤖 AI Analysis"
    ])

    with tab1:

        st.dataframe(
            data.head(20),
            width="stretch"
        )

        st.write("Dataset Shape")

        c1, c2 = st.columns(2)

        c1.metric("Rows", data.shape[0])

        c2.metric("Columns", data.shape[1])

        st.write("Columns")

        st.write(list(data.columns))

    with tab2:

        if st.button("🚀 Analyze Driver Behaviour"):

            driver_agent(data)

else:

    st.info("Please upload a CSV dataset to begin analysis.")

st.markdown("---")

st.caption("🚗 Driver Activity Monitoring AI")

st.caption("Built with ❤️ by Pattem Nagasri")