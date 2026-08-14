import streamlit as st
import requests
from PIL import Image
import io

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="K-Means Image Quantizer",
    page_icon="🎨",
    layout="centered"
)

st.markdown("""
<style>
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("K-Means Image Quantizer")
st.write("Reduce the number of colours in an image using K-Means clustering.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

col1, col2 = st.columns(2)

with col1:
    n_colours = st.number_input(
        "Number of colours",
        min_value=2,
        max_value=256,
        value=32,
        step=1
    )

with col2:
    max_iter = st.number_input(
        "Iterations",
        min_value=1,
        max_value=100,
        value=5,
        step=1
    )

if uploaded_file is not None:

    image_bytes = uploaded_file.getvalue()
    original_image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    if st.button("Quantize Image", type="primary"):

        files = {
            "image": (
                uploaded_file.name,
                image_bytes,
                uploaded_file.type
            )
        }

        params = {
            "n_colours": n_colours,
            "max_iter": max_iter
        }

        with st.spinner("Running K-Means..."):

            response = requests.post(
                f"{API_URL}/quantize",
                files=files,
                params=params
            )

        if response.status_code == 200:

            quantized_image = Image.open(
                io.BytesIO(response.content)
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original")
                st.image(
                    original_image,
                    use_container_width=True
                )

            with col2:
                st.subheader("Quantized")
                st.image(
                    quantized_image,
                    use_container_width=True
                )

        else:
            st.error(
                f"Quantization failed: {response.status_code}"
            )