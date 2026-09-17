"""Checks for the committed synthetic OCR demonstration sample."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_saved_ocr_output_contains_expected_synthetic_fields() -> None:
    """The verified sample should contain the key values shown on the test card."""

    raw_text = (
        PROJECT_ROOT / "data" / "generated" / "sample_ocr_raw.txt"
    ).read_text(encoding="utf-8")

    expected_values = {
        "MAYA LIN",
        "TEST-X7Q2M9",
        "14 JUN 1998",
        "30 SEP 2031",
    }

    assert all(value in raw_text for value in expected_values)
