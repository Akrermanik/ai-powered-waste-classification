"""Main dashboard UI for authenticated users."""

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


def render_dashboard(api_client: WasifyAPIClient) -> None:
    st.title("♻️ Wasify AI Dashboard")
    st.markdown(
        f"Welcome to the **Wasify AI** object detection platform, "
        f"*{st.session_state.get('name', 'User')}*. "
        "Upload an image or use your camera to classify waste via the FastAPI backend."
    )

    try:
        health = api_client.health()
        if not health.get("model_ready"):
            st.warning(
                "Model missing on the API server. Ensure waste_model.pt exists and restart the API."
            )
    except Exception:
        st.error(
            "Cannot reach the FastAPI backend. Start it with: "
            "`uvicorn api.main:app --reload`"
        )
        return

    st.sidebar.header("⚙️ Configuration")
    conf_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

    st.sidebar.markdown("### Image Input")

    if not st.session_state.camera_open:
        if st.sidebar.button("Open Camera 📸", use_container_width=True):
            st.session_state.camera_open = True
            st.session_state.image_data = None
            st.session_state.analysis_result = None
            st.rerun()
    else:
        if st.sidebar.button("Close Camera ❌", use_container_width=True):
            st.session_state.camera_open = False
            st.rerun()

        camera_img = st.sidebar.camera_input("Capture Image", label_visibility="collapsed")
        if camera_img:
            st.session_state.image_data = camera_img
            st.session_state.camera_open = False
            st.session_state.analysis_result = None
            st.rerun()

    st.sidebar.markdown(
        "<p style='text-align: center; margin: 10px 0; color: #6B7280; font-weight: bold;'>OR</p>",
        unsafe_allow_html=True,
    )

    upload_img = st.sidebar.file_uploader(
        "Upload Image 🖼️", type=["jpg", "jpeg", "png", "webp"]
    )
    if upload_img and st.session_state.image_data != upload_img:
        st.session_state.image_data = upload_img
        st.session_state.analysis_result = None

    if st.session_state.image_data is not None and not st.session_state.camera_open:
        img_preview = Image.open(st.session_state.image_data)

        st.divider()
        st.subheader("Model Inference")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("#### Original Uploaded Image")
                st.image(img_preview, use_container_width=True)
                analyze_button = st.button("ANALYZE", type="primary", use_container_width=True)

        if analyze_button:
            with st.spinner("Classifying with YOLO via FastAPI..."):
                try:
                    result = api_client.predict(img_preview, confidence=conf_threshold)
                    annotated = _decode_annotated_image(result.get("annotated_image_base64"))
                    summary = result["summary"]
                    st.session_state.analysis_result = {
                        "image": annotated,
                        "label": summary["label"],
                        "confidence": summary["confidence"],
                        "object_count": summary["object_count"],
                        "inference_time_ms": result["inference_time_ms"],
                    }
                except APIClientError as exc:
                    st.error(f"Failed to analyze: {exc}")

        with col2:
            with st.container(border=True):
                st.markdown("#### AI Detection Result")
                if st.session_state.analysis_result is not None:
                    res = st.session_state.analysis_result
                    if res["image"] is not None:
                        st.image(res["image"], use_container_width=True)
                else:
                    st.info("Click ANALYZE to view results here.")

        if st.session_state.analysis_result is not None:
            st.divider()
            st.subheader("Confidence Score & Analytics")

            with st.container(border=True):
                res = st.session_state.analysis_result

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if res["label"] == "No Objects Detected":
                        st.warning("⚠️ No waste objects were detected in the image.")
                    else:
                        st.success(f"✅ Detected Class: **{res['label']}**")
                with col_b:
                    st.metric(label="AI Confidence", value=f"{res['confidence'] * 100:.1f}%")
                with col_c:
                    st.metric(
                        label="Inference Time",
                        value=f"{int(res.get('inference_time_ms', 0))} ms",
                    )

                st.metric(label="Objects Detected", value=res.get("object_count", 0))

                if st.button("New Scan", key="new_scan", use_container_width=True):
                    st.session_state.image_data = None
                    st.session_state.analysis_result = None
                    st.rerun()

    st.divider()

    try:
        history_response = api_client.get_history()
        history = history_response.get("items", [])
    except APIClientError as exc:
        st.error(f"Could not load history: {exc}")
        history = []

    if history:
        st.subheader("Classification History 🕰️")
        for item in history:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; color: white;">{item['label']}</span>
                        <span style="color: #10B981; font-weight: bold;">{item['confidence'] * 100:.1f}%</span>
                    </div>
                    <div style="color: #9CA3AF; font-size: 13px; margin-top: 6px;">{item['timestamp']}</div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state["authentication_status"] = False
        st.session_state["access_token"] = None
        st.session_state["username"] = None
        st.session_state["name"] = None
        st.session_state["image_data"] = None
        st.session_state["analysis_result"] = None
        st.rerun()
