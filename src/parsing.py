"""Parse known field groups from raw OCR text without inventing values."""

import re


RAW_FIELD_NAMES = (
    "raw_full_name_latin",
    "raw_passport_number",
    "raw_date_of_birth",
    "raw_sex",
    "raw_place_of_birth",
    "raw_expiry_date",
)


def _line_after(lines: list[str], header: str) -> str | None:
    """Return the first non-empty line after an exact synthetic-card header."""

    try:
        header_index = lines.index(header)
    except ValueError:
        return None
    next_index = header_index + 1
    return lines[next_index] if next_index < len(lines) else None


def parse_ocr_text(raw_text: str) -> dict[str, str | None]:
    """Extract raw fields from the current synthetic test-card layout.

    A failed pattern returns ``None`` for the affected fields. The parser does
    not guess because an uncertain identity value should be reviewed by a
    person rather than silently repaired.
    """

    fields: dict[str, str | None] = {name: None for name in RAW_FIELD_NAMES}
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    name_passport = _line_after(lines, "FULL NAME PASSPORT NO")
    if name_passport:
        match = re.fullmatch(
            r"(?P<name>.+?)\s+(?P<passport>[A-Z0-9][A-Z0-9-]*\d[A-Z0-9-]*)",
            name_passport,
            flags=re.IGNORECASE,
        )
        if match:
            fields["raw_full_name_latin"] = match.group("name")
            fields["raw_passport_number"] = match.group("passport")

    birth_sex = _line_after(lines, "DATE OF BIRTH SEX")
    if birth_sex:
        match = re.fullmatch(
            r"(?P<birth>\d{1,2}\s+[A-Z]{3}\s+\d{4})\s+(?P<sex>[A-Z]+)",
            birth_sex,
            flags=re.IGNORECASE,
        )
        if match:
            fields["raw_date_of_birth"] = match.group("birth")
            fields["raw_sex"] = match.group("sex")

    place_expiry = _line_after(lines, "PLACE OF BIRTH EXPIRY DATE")
    if place_expiry:
        match = re.fullmatch(
            r"(?P<place>.+?)\s+(?P<expiry>\d{1,2}\s+[A-Z]{3}\s+\d{4})",
            place_expiry,
            flags=re.IGNORECASE,
        )
        if match:
            fields["raw_place_of_birth"] = match.group("place")
            fields["raw_expiry_date"] = match.group("expiry")

    return fields
