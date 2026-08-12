"""Authentication pages for the Streamlit frontend."""

import base64
import io

import streamlit as st
from PIL import Image

from ui.api_client import APIClientError, WasifyAPIClient


def _decode_annotated_image(image_base64: str | None) -> Image.Image | None:
    if not image_base64:
        return None
    image_bytes = base64.b64decode(image_base64)
    return Image.open(io.BytesIO(image_bytes))


def render_auth_pages(api_client: WasifyAPIClient) -> None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h1 style='text-align: center; color: white;'>♻️ Wasify</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: #9CA3AF;'>Please login or register to continue.</p>",
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

            if submit:
                if not username or not password:
                    st.warning("Please enter your username and password")
                else:
                    try:
                        result = api_client.login(username, password)
                        st.session_state["access_token"] = result["access_token"]
                        st.session_state["authentication_status"] = True
                        st.session_state["username"] = result["user"]["username"]
                        st.session_state["name"] = result["user"]["name"]
                        st.rerun()
                    except APIClientError as exc:
                        st.error(str(exc))

        with tab2:
            st.markdown("### Create an Account")
            with st.form("register_form"):
                new_name = st.text_input("Name")
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                submit_btn = st.form_submit_button("Register")

            if submit_btn:
                if new_name and new_username and new_password:
                    try:
                        result = api_client.register(new_username, new_name, new_password)
                        st.success("Registration successful! Logging you in...")
                        st.session_state["access_token"] = result["access_token"]
                        st.session_state["authentication_status"] = True
                        st.session_state["username"] = result["user"]["username"]
                        st.session_state["name"] = result["user"]["name"]
                        st.rerun()
                    except APIClientError as exc:
                        st.error(str(exc))
                else:
                    st.warning("Please fill out all fields.")
