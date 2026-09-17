"""Tests for OCR text parsing and conservative field normalization."""

from pathlib import Path

from src.normalization import normalize_date, normalize_ocr_fields
from src.parsing import parse_ocr_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def sample_text() -> str:
    return (
        PROJECT_ROOT / "data" / "generated" / "sample_ocr_raw.txt"
    ).read_text(encoding="utf-8")


def test_parse_verified_ocr_sample() -> None:
    parsed = parse_ocr_text(sample_text())

    assert parsed == {
        "raw_full_name_latin": "MAYA LIN",
        "raw_passport_number": "TEST-X7Q2M9",
        "raw_date_of_birth": "14 JUN 1998",
        "raw_sex": "F",
        "raw_place_of_birth": "SAMPLE CITY",
        "raw_expiry_date": "30 SEP 2031",
    }


def test_normalize_verified_ocr_sample() -> None:
    normalized = normalize_ocr_fields(parse_ocr_text(sample_text()))

    assert normalized["normalized_full_name_latin"] == "MAYA LIN"
    assert normalized["normalized_passport_number"] == "TEST-X7Q2M9"
    assert normalized["normalized_date_of_birth"] == "1998-06-14"
    assert normalized["normalized_expiry_date"] == "2031-09-30"
    assert normalized["critical_field_completeness"] == 1.0
    assert normalized["verification_status"] == "UNVERIFIED"


def test_ambiguous_numeric_date_is_not_guessed() -> None:
    assert normalize_date("04/05/1998") is None


def test_missing_identity_fields_reduce_completeness() -> None:
    normalized = normalize_ocr_fields(
        {
            "raw_full_name_latin": "  Maya   Lin ",
            "raw_passport_number": None,
            "raw_date_of_birth": "14 JUN 1998",
            "raw_sex": "female",
            "raw_place_of_birth": "sample city",
            "raw_expiry_date": "30 SEP 2031",
        }
    )

    assert normalized["normalized_full_name_latin"] == "MAYA LIN"
    assert normalized["normalized_sex"] == "F"
    assert normalized["critical_field_completeness"] == 2 / 3
