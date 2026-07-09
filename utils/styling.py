import streamlit as st

def load_css():

    st.markdown("""
    <style>

    .main{
        background:#0f172a;
    }

    h1,h2,h3,h4{
        color:white;
    }

    p{
        color:#d1d5db;
    }

    .stButton>button{
        width:100%;
        border-radius:12px;
        height:50px;
        font-size:18px;
        font-weight:bold;
        background:linear-gradient(90deg,#2563eb,#7c3aed);
        color:white;
        border:none;
    }

    .stButton>button:hover{
        background:linear-gradient(90deg,#1d4ed8,#6d28d9);
        color:white;
    }

    div[data-testid="metric-container"]{
        background:#1e293b;
        border-radius:15px;
        padding:15px;
        border:1px solid #334155;
        box-shadow:0px 3px 10px rgba(0,0,0,0.35);
    }

    div[data-testid="stDataFrame"]{
        border-radius:15px;
    }

    .hero{
        padding:20px;
        border-radius:18px;
        background:linear-gradient(90deg,#2563eb,#9333ea);
        text-align:center;
        color:white;
        margin-bottom:25px;
    }

    .hero h1{
        color:white;
        margin-bottom:5px;
    }

    .hero p{
        color:white;
        font-size:18px;
    }

    </style>
    """, unsafe_allow_html=True)