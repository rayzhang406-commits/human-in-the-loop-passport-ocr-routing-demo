"""Streamlit entry point for the synthetic passport matching demo."""

from pathlib import Path

import streamlit as st

from src.ocr import OCRUnavailableError, extract_text, tesseract_path


PROJECT_ROOT = Path(__file__).resolve().parent
TEST_CARD_PATH = PROJECT_ROOT / "assets" / "synthetic_passport_test_card.png"
SAVED_OCR_PATH = PROJECT_ROOT / "data" / "generated" / "sample_ocr_raw.txt"


st.set_page_config(
    page_title="Passport OCR Record Matching Demo",
    page_icon="🔎",
    layout="wide",
)

st.title("Passport OCR Record Matching Demo")
st.caption("Synthetic data only · Independent portfolio demonstration")

st.warning(
    "All OCR-derived fields remain UNVERIFIED. Routing results are recommendations, "
    "not automatic identity confirmation."
)

st.subheader("1. Open-source OCR input")
image_column, result_column = st.columns([1.1, 0.9])

with image_column:
    st.image(TEST_CARD_PATH, caption="Synthetic test card — not a real document")

with result_column:
    if tesseract_path():
        st.success("Local OCR engine available: Tesseract")
    else:
        st.info("Tesseract is unavailable; the saved synthetic sample remains viewable.")

    if "ocr_raw_text" not in st.session_state and SAVED_OCR_PATH.is_file():
        st.session_state.ocr_raw_text = SAVED_OCR_PATH.read_text(encoding="utf-8")
        st.session_state.ocr_result_source = "Saved verified sample"

    if st.button("Run OCR on synthetic card", type="primary"):
        try:
            st.session_state.ocr_raw_text = extract_text(TEST_CARD_PATH)
            st.session_state.ocr_result_source = "Live local Tesseract run"
        except OCRUnavailableError as error:
            st.error(str(error))

    st.markdown("**Raw OCR output**")
    st.code(st.session_state.get("ocr_raw_text", "No OCR output available yet."))
    if "ocr_result_source" in st.session_state:
        st.caption(f"Result source: {st.session_state.ocr_result_source}")

st.subheader("Next processing stages")
st.write(
    "Raw OCR fields → field standardization → historical customer matching → "
    "create, reuse, conflict, or human review"
)
