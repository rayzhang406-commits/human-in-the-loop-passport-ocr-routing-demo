"""Explainable historical matching and human-review routing rules."""

from __future__ import annotations

from collections.abc import Iterable

from src.normalization import normalize_date, normalize_passport_number, normalize_sex, normalize_text, normalize_ocr_fields


REQUIRED_IDENTITY_FIELDS = (
    "normalized_full_name_latin",
    "normalized_passport_number",
    "normalized_date_of_birth",
)

COMPARISON_FIELDS = (
    ("normalized_full_name_latin", "full_name_latin", "full name"),
    ("normalized_date_of_birth", "date_of_birth", "date of birth"),
    ("normalized_sex", "sex", "sex"),
    ("normalized_place_of_birth", "place_of_birth", "place of birth"),
)


def normalize_historical_customer(customer: dict[str, object]) -> dict[str, object]:
    """Create comparable normalized fields without mutating the source record."""

    return {
        **customer,
        "normalized_full_name_latin": normalize_text(customer.get("full_name_latin")),
        "normalized_passport_number": normalize_passport_number(
            customer.get("passport_number")
        ),
        "normalized_date_of_birth": normalize_date(customer.get("date_of_birth")),
        "normalized_sex": normalize_sex(customer.get("sex")),
        "normalized_place_of_birth": normalize_text(customer.get("place_of_birth")),
    }


def route_case(
    raw_case: dict[str, object], historical_customers: Iterable[dict[str, object]]
) -> dict[str, object]:
    """Normalize one OCR case and recommend a safe, explainable route.

    The result is always unverified. A route controls workflow handling only; it
    never overwrites a historical customer record.
    """

    raw_fields = {
        key: raw_case.get(key)
        for key in (
            "raw_full_name_latin",
            "raw_passport_number",
            "raw_date_of_birth",
            "raw_sex",
            "raw_place_of_birth",
            "raw_expiry_date",
        )
    }
    normalized = normalize_ocr_fields(raw_fields)
    result: dict[str, object] = {
        **raw_case,
        **normalized,
        "matched_customer_id": None,
        "candidate_count": 0,
        "routing_decision": None,
        "review_required": None,
        "decision_reason": None,
    }

    missing_fields = [field for field in REQUIRED_IDENTITY_FIELDS if not normalized[field]]
    if missing_fields:
        readable = ", ".join(
            field.removeprefix("normalized_").replace("_", " ")
            for field in missing_fields
        )
        result.update(
            {
                "routing_decision": "MANUAL_REVIEW",
                "review_required": True,
                "decision_reason": f"Missing or ambiguous required field(s): {readable}.",
            }
        )
        return result

    normalized_history = [
        normalize_historical_customer(customer) for customer in historical_customers
    ]
    passport_candidates = [
        customer
        for customer in normalized_history
        if customer["normalized_passport_number"]
        == normalized["normalized_passport_number"]
    ]
    result["candidate_count"] = len(passport_candidates)

    if len(passport_candidates) > 1:
        result.update(
            {
                "routing_decision": "MANUAL_REVIEW",
                "review_required": True,
                "decision_reason": "Multiple historical records share the normalized passport number.",
            }
        )
        return result

    if len(passport_candidates) == 1:
        candidate = passport_candidates[0]
        result["matched_customer_id"] = candidate["customer_id"]
        conflicts = [
            label
            for incoming_field, historical_field, label in COMPARISON_FIELDS
            if normalized[incoming_field]
            and candidate[f"normalized_{historical_field}"]
            and normalized[incoming_field]
            != candidate[f"normalized_{historical_field}"]
        ]
        if conflicts:
            result.update(
                {
                    "routing_decision": "CONFLICT",
                    "review_required": True,
                    "decision_reason": "Passport number matches a historical record, "
                    f"but conflicting field(s) exist: {', '.join(conflicts)}.",
                }
            )
        else:
            result.update(
                {
                    "routing_decision": "REUSE",
                    "review_required": False,
                    "decision_reason": "Passport number and available identity fields match one historical record.",
                }
            )
        return result

    identity_candidates = [
        customer
        for customer in normalized_history
        if customer["normalized_full_name_latin"] == normalized["normalized_full_name_latin"]
        and customer["normalized_date_of_birth"] == normalized["normalized_date_of_birth"]
    ]
    if identity_candidates:
        result.update(
            {
                "matched_customer_id": identity_candidates[0]["customer_id"],
                "candidate_count": len(identity_candidates),
                "routing_decision": "MANUAL_REVIEW",
                "review_required": True,
                "decision_reason": "Name and date of birth match history, but passport number differs; possible reissue requires review.",
            }
        )
        return result

    result.update(
        {
            "routing_decision": "CREATE",
            "review_required": False,
            "decision_reason": "Required fields are complete and no historical customer matches the passport number.",
        }
    )
    return result


def route_batch(
    raw_cases: Iterable[dict[str, object]], historical_customers: Iterable[dict[str, object]]
) -> list[dict[str, object]]:
    """Route an iterable of raw OCR cases against the same historical dataset."""

    historical_list = list(historical_customers)
    return [route_case(case, historical_list) for case in raw_cases]
