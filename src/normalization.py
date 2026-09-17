"""Conservative normalization of parsed OCR fields."""

from datetime import datetime
import re
import unicodedata


CRITICAL_FIELDS = (
    "normalized_full_name_latin",
    "normalized_passport_number",
    "normalized_date_of_birth",
)


def normalize_text(value: str | None) -> str | None:
    """Apply Unicode normalization, trim spaces, and uppercase Latin text."""

    if value is None:
        return None
    normalized = unicodedata.normalize("NFKC", value)
    normalized = re.sub(r"\s+", " ", normalized).strip().upper()
    return normalized or None


def normalize_passport_number(value: str | None) -> str | None:
    """Uppercase a document number and remove OCR-introduced whitespace."""

    normalized = normalize_text(value)
    return normalized.replace(" ", "") if normalized else None


def normalize_date(value: str | None) -> str | None:
    """Convert only supported unambiguous date formats to ISO format."""

    normalized = normalize_text(value)
    if normalized is None:
        return None

    for date_format in ("%d %b %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(normalized, date_format).date().isoformat()
        except ValueError:
            continue
    return None


def normalize_sex(value: str | None) -> str | None:
    """Map a small, explainable set of values to M, F, or X."""

    normalized = normalize_text(value)
    mapping = {
        "M": "M",
        "MALE": "M",
        "F": "F",
        "FEMALE": "F",
        "X": "X",
    }
    return mapping.get(normalized)


def normalize_ocr_fields(
    raw_fields: dict[str, str | None],
) -> dict[str, str | float | None]:
    """Return standardized values and a critical-field completeness score."""

    normalized: dict[str, str | float | None] = {
        "normalized_full_name_latin": normalize_text(
            raw_fields.get("raw_full_name_latin")
        ),
        "normalized_passport_number": normalize_passport_number(
            raw_fields.get("raw_passport_number")
        ),
        "normalized_date_of_birth": normalize_date(
            raw_fields.get("raw_date_of_birth")
        ),
        "normalized_sex": normalize_sex(raw_fields.get("raw_sex")),
        "normalized_place_of_birth": normalize_text(
            raw_fields.get("raw_place_of_birth")
        ),
        "normalized_expiry_date": normalize_date(
            raw_fields.get("raw_expiry_date")
        ),
        "verification_status": "UNVERIFIED",
    }
    completed = sum(bool(normalized[field]) for field in CRITICAL_FIELDS)
    normalized["critical_field_completeness"] = completed / len(CRITICAL_FIELDS)
    return normalized
