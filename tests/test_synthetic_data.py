"""Data-quality checks for the public synthetic batch dataset."""

from pathlib import Path

import pandas as pd

from scripts.generate_synthetic_data import make_cases, make_historical_customers


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_generated_data_has_expected_sizes_and_unique_ids() -> None:
    historical = make_historical_customers()
    cases, expectations = make_cases()

    assert len(historical) == 24
    assert len(cases) == 60
    assert len(expectations) == 60
    assert cases["case_id"].is_unique
    assert set(cases["case_id"]) == set(expectations["case_id"])


def test_expected_routing_distribution_is_intentional() -> None:
    _, expectations = make_cases()
    counts = expectations["expected_routing_decision"].value_counts().to_dict()

    assert counts == {
        "REUSE": 18,
        "CREATE": 14,
        "CONFLICT": 12,
        "MANUAL_REVIEW": 16,
    }


def test_batch_data_is_explicitly_synthetic() -> None:
    cases, _ = make_cases()
    historical = make_historical_customers()

    assert cases["document_type"].eq("SYNTHETIC_PASSPORT_TEST_CARD").all()
    assert cases["ocr_source"].eq("MOCK_OCR").all()
    assert historical["verification_status"].eq("VERIFIED_SYNTHETIC").all()
    assert historical["passport_number"].str.startswith("TEST-").all()


def test_committed_csvs_match_the_generator() -> None:
    expected_historical = make_historical_customers()
    expected_cases, expected_expectations = make_cases()

    actual_historical = pd.read_csv(
        PROJECT_ROOT / "data" / "generated" / "historical_customers.csv",
        keep_default_na=False,
    )
    actual_cases = pd.read_csv(
        PROJECT_ROOT / "data" / "generated" / "mock_ocr_cases.csv",
        keep_default_na=False,
    )
    actual_expectations = pd.read_csv(
        PROJECT_ROOT / "data" / "generated" / "test_case_expectations.csv",
        keep_default_na=False,
    )

    pd.testing.assert_frame_equal(actual_historical, expected_historical)
    pd.testing.assert_frame_equal(actual_cases, expected_cases.fillna(""))
    pd.testing.assert_frame_equal(actual_expectations, expected_expectations)
