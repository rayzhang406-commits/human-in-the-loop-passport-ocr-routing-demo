"""Tests proving that the routing engine calculates expected synthetic outcomes."""

from pathlib import Path

import pandas as pd

from src.matching import route_batch, route_case
from src.metrics import calculate_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "data" / "generated"


def load_inputs() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    historical = pd.read_csv(
        GENERATED_DIR / "historical_customers.csv", keep_default_na=False
    )
    cases = pd.read_csv(GENERATED_DIR / "mock_ocr_cases.csv", keep_default_na=False)
    return cases.to_dict(orient="records"), historical.to_dict(orient="records")


def test_routing_engine_matches_separate_test_expectations() -> None:
    cases, historical = load_inputs()
    routed = pd.DataFrame(route_batch(cases, historical))
    expectations = pd.read_csv(GENERATED_DIR / "test_case_expectations.csv")
    compared = routed.merge(expectations, on="case_id", validate="one_to_one")

    assert compared["routing_decision"].equals(
        compared["expected_routing_decision"]
    )
    assert compared["review_required"].equals(compared["expected_review_required"])


def test_same_identity_with_different_passport_requires_review() -> None:
    _, historical = load_inputs()
    original = historical[0]
    result = route_case(
        {
            "raw_full_name_latin": original["full_name_latin"],
            "raw_passport_number": "TEST-NEW-0001",
            "raw_date_of_birth": original["date_of_birth"],
            "raw_sex": original["sex"],
            "raw_place_of_birth": original["place_of_birth"],
            "raw_expiry_date": "30 SEP 2031",
        },
        historical,
    )

    assert result["routing_decision"] == "MANUAL_REVIEW"
    assert result["review_required"] is True
    assert result["matched_customer_id"] == original["customer_id"]


def test_batch_metrics_are_calculated_from_routing_output() -> None:
    cases, historical = load_inputs()
    routed = pd.DataFrame(route_batch(cases, historical))
    metrics = calculate_metrics(routed)

    assert metrics["total_cases"] == 60
    assert metrics["automatic_reuse_rate"] == 18 / 60
    assert metrics["human_review_rate"] == 28 / 60
