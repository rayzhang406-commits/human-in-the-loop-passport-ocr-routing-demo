"""Streamlit entry point for the synthetic passport matching demo."""

import streamlit as st


st.set_page_config(
    page_title="Passport OCR Record Matching Demo",
    page_icon="🔎",
    layout="wide",
)

st.title("Passport OCR Record Matching Demo")
st.caption("Synthetic data only · Independent portfolio demonstration")

st.info(
    "The repository skeleton is ready. The next stage will add synthetic cases, "
    "field normalization, matching rules, and review routing."
)

st.subheader("Planned decision flow")
st.write(
    "Mock OCR result → field standardization → historical customer matching → "
    "create, reuse, conflict, or human review"
)

st.warning(
    "All OCR-derived fields remain UNVERIFIED. Routing results are recommendations, "
    "not automatic identity confirmation."
)
