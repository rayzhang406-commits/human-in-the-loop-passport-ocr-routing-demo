# Data Dictionary

The first version uses three logical datasets. Final column names may be refined before data generation.

## Historical customers

| Field | Type | Purpose |
|---|---|---|
| `customer_id` | string | Synthetic permanent customer identifier |
| `full_name_latin` | string | Verified historical Latin-script name |
| `passport_number` | string | Verified historical passport number |
| `date_of_birth` | date | Verified date of birth |
| `sex` | string | Standardized categorical value |
| `place_of_birth` | string | Historical birthplace value |
| `verification_status` | string | Indicates the status of the historical record |
| `expiry_date` | date | Historical passport expiry date |

## Mock OCR cases

| Field | Type | Purpose |
|---|---|---|
| `case_id` | string | Synthetic processing-case identifier |
| `document_type` | string | Always identifies an obviously synthetic test document |
| `ocr_source` | string | `MOCK_OCR` for generated batch data; separate from the live OCR sample |
| `raw_full_name_latin` | string or null | Name returned by mock OCR |
| `raw_passport_number` | string or null | Passport number returned by mock OCR |
| `raw_date_of_birth` | string or null | Unparsed date returned by mock OCR |
| `raw_sex` | string or null | Raw categorical value |
| `raw_place_of_birth` | string or null | Raw birthplace value |
| `raw_expiry_date` | string or null | Unparsed expiry date |
| `simulated_error_type` | string | Controlled synthetic OCR issue or `NONE` |

## Test-only expectations

`test_case_expectations.csv` contains the generator scenario and expected routing
result for each synthetic case. It is a test oracle only: the matching engine
must calculate decisions from OCR and historical fields, never from this file.

## Processed decisions

| Field | Type | Purpose |
|---|---|---|
| `case_id` | string | Links the result to the mock OCR case |
| `normalized_full_name_latin` | string or null | Conservatively standardized name |
| `normalized_passport_number` | string or null | Conservatively standardized passport number |
| `normalized_date_of_birth` | date or null | Parsed date when unambiguous |
| `critical_field_completeness` | float | Share of required values present after normalization |
| `matched_customer_id` | string or null | Best deterministic historical match |
| `routing_decision` | string | `CREATE`, `REUSE`, `CONFLICT`, or `MANUAL_REVIEW` |
| `review_required` | boolean | Whether a person must review the case |
| `decision_reason` | string | Human-readable explanation of the applied rule |
| `verification_status` | string | Always `UNVERIFIED` for OCR-derived results |

## Initial metric definitions

- **Critical-field completeness:** non-null normalized values across name, passport number, and date of birth divided by all expected critical values.
- **Automatic reuse rate:** cases routed to `REUSE` divided by all processed cases.
- **Human-review rate:** cases with `review_required = true` divided by all processed cases.

These values describe only the generated demonstration dataset.
