"""Generate reproducible synthetic customers and mock OCR processing cases."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import random

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
SEED = 20260917


def iso_date_for(index: int) -> str:
    """Create a deterministic, clearly synthetic date of birth."""

    return date(1980 + index % 20, (index % 12) + 1, (index % 27) + 1).isoformat()


def ocr_date(iso_value: str) -> str:
    """Format an ISO date in the OCR-style format used by the demo card."""

    return date.fromisoformat(iso_value).strftime("%d %b %Y").upper()


def make_person(index: int) -> dict[str, str]:
    """Create a non-real identity record marked with synthetic identifiers."""

    return {
        "full_name_latin": f"SAMPLE TRAVELER {index:03d}",
        "passport_number": f"TEST-P{index:04d}",
        "date_of_birth": iso_date_for(index),
        "sex": "F" if index % 2 else "M",
        "place_of_birth": f"SAMPLE CITY {(index % 5) + 1}",
        "expiry_date": date(2030 + index % 4, (index % 12) + 1, 28).isoformat(),
    }


def make_historical_customers() -> pd.DataFrame:
    """Build 24 verified synthetic historical records."""

    rows = []
    for index in range(1, 25):
        person = make_person(index)
        rows.append(
            {
                "customer_id": f"CUST-{index:03d}",
                **person,
                "verification_status": "VERIFIED_SYNTHETIC",
            }
        )
    return pd.DataFrame(rows)


def raw_record(person: dict[str, str]) -> dict[str, str]:
    """Return the raw OCR-shaped representation of a synthetic person."""

    return {
        "raw_full_name_latin": person["full_name_latin"],
        "raw_passport_number": person["passport_number"],
        "raw_date_of_birth": ocr_date(person["date_of_birth"]),
        "raw_sex": person["sex"],
        "raw_place_of_birth": person["place_of_birth"],
        "raw_expiry_date": ocr_date(person["expiry_date"]),
    }


def make_cases() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create 60 mock OCR cases plus a separate, test-only expected outcome."""

    combined: list[dict[str, str | bool | None]] = []

    def add_case(
        person: dict[str, str],
        scenario: str,
        decision: str,
        review_required: bool,
        error_type: str,
        changes: dict[str, str | None] | None = None,
    ) -> None:
        raw = raw_record(person)
        if changes:
            raw.update(changes)
        case_number = len(combined) + 1
        combined.append(
            {
                "case_id": f"CASE-{case_number:03d}",
                "document_type": "SYNTHETIC_PASSPORT_TEST_CARD",
                "ocr_source": "MOCK_OCR",
                **raw,
                "simulated_error_type": error_type,
                "generator_scenario": scenario,
                "expected_routing_decision": decision,
                "expected_review_required": review_required,
            }
        )

    # 18 safe reuse cases: the same historical customer, with harmless OCR variation.
    for index in range(1, 19):
        person = make_person(index)
        variation = index % 3
        if variation == 0:
            changes = {
                "raw_full_name_latin": f"  {person['full_name_latin'].lower()}  ",
                "raw_passport_number": person["passport_number"].replace("-", "- "),
            }
            error_type = "EXTRA_WHITESPACE"
        elif variation == 1:
            changes = {
                "raw_date_of_birth": person["date_of_birth"],
                "raw_sex": "female" if person["sex"] == "F" else "male",
                "raw_place_of_birth": person["place_of_birth"].lower(),
            }
            error_type = "FORMAT_VARIATION"
        else:
            changes = {}
            error_type = "NONE"
        add_case(person, "REUSE", "REUSE", False, error_type, changes)

    # 14 complete cases that have no historical match and can be newly created.
    for index in range(101, 115):
        person = make_person(index)
        add_case(person, "CREATE", "CREATE", False, "NONE")

    # 12 conflicts: same passport as history, but a non-empty identity field differs.
    for index in range(19, 25):
        person = make_person(index)
        add_case(
            person,
            "CONFLICT_NAME",
            "CONFLICT",
            True,
            "IDENTITY_CONFLICT",
            {"raw_full_name_latin": f"CONFLICT TRAVELER {index:03d}"},
        )
        changed_birth_year = str(int(person["date_of_birth"][:4]) - 1)
        add_case(
            person,
            "CONFLICT_DOB",
            "CONFLICT",
            True,
            "IDENTITY_CONFLICT",
            {"raw_date_of_birth": ocr_date(changed_birth_year + person["date_of_birth"][4:])},
        )

    # 16 cases deliberately lack a safe identity key or contain an ambiguous date.
    manual_specs = [
        ("MISSING_PASSPORT", "raw_passport_number", None),
        ("MISSING_PASSPORT", "raw_passport_number", None),
        ("MISSING_PASSPORT", "raw_passport_number", None),
        ("MISSING_PASSPORT", "raw_passport_number", None),
        ("MISSING_PASSPORT", "raw_passport_number", None),
        ("MISSING_PASSPORT", "raw_passport_number", None),
        ("MISSING_NAME", "raw_full_name_latin", None),
        ("MISSING_NAME", "raw_full_name_latin", None),
        ("MISSING_NAME", "raw_full_name_latin", None),
        ("MISSING_NAME", "raw_full_name_latin", None),
        ("MISSING_NAME", "raw_full_name_latin", None),
        ("AMBIGUOUS_DOB", "raw_date_of_birth", "04/05/1998"),
        ("AMBIGUOUS_DOB", "raw_date_of_birth", "04/05/1998"),
        ("AMBIGUOUS_DOB", "raw_date_of_birth", "04/05/1998"),
        ("UNREADABLE_DOB", "raw_date_of_birth", "NOT READABLE"),
        ("UNREADABLE_DOB", "raw_date_of_birth", "NOT READABLE"),
    ]
    for offset, (error_type, field, value) in enumerate(manual_specs, start=201):
        person = make_person(offset)
        add_case(
            person,
            "MANUAL_REVIEW",
            "MANUAL_REVIEW",
            True,
            error_type,
            {field: value},
        )

    if len(combined) != 60:
        raise AssertionError("The demo requires exactly 60 processing cases.")

    random.Random(SEED).shuffle(combined)
    cases = pd.DataFrame(
        [
            {
                key: row[key]
                for key in (
                    "case_id",
                    "document_type",
                    "ocr_source",
                    "raw_full_name_latin",
                    "raw_passport_number",
                    "raw_date_of_birth",
                    "raw_sex",
                    "raw_place_of_birth",
                    "raw_expiry_date",
                    "simulated_error_type",
                )
            }
            for row in combined
        ]
    )
    expectations = pd.DataFrame(
        [
            {
                "case_id": row["case_id"],
                "generator_scenario": row["generator_scenario"],
                "expected_routing_decision": row["expected_routing_decision"],
                "expected_review_required": row["expected_review_required"],
            }
            for row in combined
        ]
    )
    return cases, expectations


def write_generated_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Write all public synthetic datasets and return them for validation."""

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    historical = make_historical_customers()
    cases, expectations = make_cases()
    historical.to_csv(GENERATED_DIR / "historical_customers.csv", index=False)
    cases.to_csv(GENERATED_DIR / "mock_ocr_cases.csv", index=False)
    expectations.to_csv(GENERATED_DIR / "test_case_expectations.csv", index=False)
    return historical, cases, expectations


if __name__ == "__main__":
    historical, cases, expectations = write_generated_data()
    print(f"Created {len(historical)} historical customers and {len(cases)} mock OCR cases.")
    print(expectations["expected_routing_decision"].value_counts().sort_index().to_string())
