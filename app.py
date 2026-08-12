"""Wasify Streamlit frontend entry point."""

import streamlit as st

from ui.api_client import WasifyAPIClient
from ui.auth_pages import render_auth_pages
from ui.dashboard import render_dashboard
from ui.styles import apply_custom_css

st.set_page_config(
    page_title="Wasify - AI Waste Detection",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_SESSION = {
    "authentication_status": None,
    "access_token": None,
    "name": None,
    "username": None,
    "camera_open": False,
    "image_data": None,
    "analysis_result": None,
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


def main() -> None:
    apply_custom_css()

    token = st.session_state.get("access_token")
    api_client = WasifyAPIClient(token=token)

    if st.session_state.get("authentication_status"):
        render_dashboard(api_client)
    else:
        render_auth_pages(api_client)


if __name__ == "__main__":
    main()
