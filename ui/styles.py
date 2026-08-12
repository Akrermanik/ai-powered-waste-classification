"""Streamlit UI styles."""

import streamlit as st


def apply_custom_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)),
                url("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        [data-testid="column"]:nth-of-type(2) > div {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.5);
        }
        [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: none !important;
            background-color: rgba(0,0,0,0.2);
            padding: 6px;
            border-radius: 12px;
        }
        [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 16px !important;
            color: #9CA3AF !important;
            border: none !important;
            background: transparent !important;
        }
        [aria-selected="true"] {
            background-color: #10B981 !important;
            color: white !important;
        }
        [data-baseweb="tab-highlight"] {
            display: none !important;
        }
        div[data-baseweb="input"] {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: white !important;
        }
        .stButton > button {
            background-color: #10B981 !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 23, 42, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        [data-testid="stMetricValue"] {
            color: #10B981 !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
        }
        [data-testid="stMetricLabel"] {
            color: #9CA3AF !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
