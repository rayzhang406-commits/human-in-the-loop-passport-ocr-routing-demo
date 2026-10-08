# Demo Walkthrough

This walkthrough uses generated data and demonstrates the routing logic.

## Suggested narration

**0-10 seconds - scope**

"This demo starts with OCR text and routes the resulting fields to the next
record-processing step."

**10-25 seconds - OCR evidence**

Show the synthetic test card and click **Run OCR on synthetic card**.

"OCR gives me text, not confirmed customer data. The raw result stays visible
so I can trace where each field came from."

**25-38 seconds - data quality**

Show the parsed-and-standardized table.

"The pipeline standardizes formatting conservatively. For example, it converts
an unambiguous date to ISO format, but leaves an ambiguous date unresolved
instead of guessing."

**38-52 seconds - reuse**

In **Historical matching and review routing**, select `CASE-018`.

"This case contains lower-case text and an extra space in the passport number.
After standardization, it matches one historical record, so the workflow
recommends reuse."

**52-68 seconds - conflict and review**

Select `CASE-038`, then `CASE-047`.

"Here, the passport number matches history but another identity field
conflicts, so the system routes the case for review. This second case has an
incomplete or ambiguous core field and also goes to review."

**68-82 seconds - close**

Show the batch summary.

"The generated cases make the routing decisions and their reasons easy to
inspect."

## Recording checklist

- Show one `REUSE`, one `CONFLICT`, and one `MANUAL_REVIEW` case.
- Do not present generated results as real OCR accuracy or production effects.
- Remove browser bookmarks, notifications, and unrelated windows before capture.
