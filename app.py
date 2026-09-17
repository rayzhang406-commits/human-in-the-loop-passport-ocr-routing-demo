"""Streamlit entry point for the synthetic passport matching demo."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.normalization import normalize_ocr_fields
from src.ocr import OCRUnavailableError, extract_text, tesseract_path
from src.parsing import parse_ocr_text


PROJECT_ROOT = Path(__file__).resolve().parent
TEST_CARD_PATH = PROJECT_ROOT / "assets" / "synthetic_passport_test_card.png"
SAVED_OCR_PATH = PROJECT_ROOT / "data" / "generated" / "sample_ocr_raw.txt"
HISTORICAL_CUSTOMERS_PATH = PROJECT_ROOT / "data" / "generated" / "historical_customers.csv"
MOCK_CASES_PATH = PROJECT_ROOT / "data" / "generated" / "mock_ocr_cases.csv"


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
current_text = st.session_state.get("ocr_raw_text", "")
if current_text:
    raw_fields = parse_ocr_text(current_text)
    normalized_fields = normalize_ocr_fields(raw_fields)

    field_mapping = [
        ("Full name", "raw_full_name_latin", "normalized_full_name_latin"),
        ("Passport number", "raw_passport_number", "normalized_passport_number"),
        ("Date of birth", "raw_date_of_birth", "normalized_date_of_birth"),
        ("Sex", "raw_sex", "normalized_sex"),
        ("Place of birth", "raw_place_of_birth", "normalized_place_of_birth"),
        ("Expiry date", "raw_expiry_date", "normalized_expiry_date"),
    ]
    comparison = pd.DataFrame(
        [
            {
                "Field": label,
                "Raw value": raw_fields[raw_key],
                "Normalized value": normalized_fields[normalized_key],
                "Status": "Ready"
                if normalized_fields[normalized_key]
                else "Needs review",
            }
            for label, raw_key, normalized_key in field_mapping
        ]
    )

    st.subheader("2. Parsed and standardized fields")
    st.caption(
        "Raw values preserve OCR evidence. Normalized values are used by later "
        "matching rules. Missing or ambiguous values are not guessed."
    )
    st.dataframe(comparison, hide_index=True, width="stretch")

    completeness = float(normalized_fields["critical_field_completeness"])
    metric_column, status_column = st.columns([0.35, 0.65])
    with metric_column:
        st.metric("Critical-field completeness", f"{completeness:.0%}")
    with status_column:
        st.info(
            "Verification status: UNVERIFIED. Historical matching and routing "
            "will be added in the next stage."
        )
else:
    st.write(
        "Run OCR first. The next stages will standardize fields, compare historical "
        "customers, and route the case."
    )

st.subheader("3. Synthetic batch data staged for routing")
if HISTORICAL_CUSTOMERS_PATH.is_file() and MOCK_CASES_PATH.is_file():
    historical_customers = pd.read_csv(HISTORICAL_CUSTOMERS_PATH, keep_default_na=False)
    mock_cases = pd.read_csv(MOCK_CASES_PATH, keep_default_na=False)

    customer_metric, case_metric = st.columns(2)
    customer_metric.metric("Historical customer records", len(historical_customers))
    case_metric.metric("Mock OCR cases", len(mock_cases))
    st.caption(
        "All batch records are generated from a fixed seed and explicitly marked "
        "synthetic. The routing engine will process these cases in the next stage."
    )
    st.dataframe(
        mock_cases[
            [
                "case_id",
                "raw_full_name_latin",
                "raw_passport_number",
                "raw_date_of_birth",
                "simulated_error_type",
            ]
        ].head(8),
        hide_index=True,
        width="stretch",
    )
else:
    st.info("Run scripts/generate_synthetic_data.py to create the batch dataset.")
