# Demo Walkthrough

This 60-90 second walkthrough presents the public demo as an independent,
synthetic companion project. It does not present the app as a production system.

## Suggested narration

**0-10 seconds - scope**

"This is an independent synthetic demo of the decision layer after document
OCR. It contains no real documents, client data, or production code."

**10-25 seconds - OCR evidence**

Show the synthetic test card and click **Run OCR on synthetic card**.

"OCR gives me text, not confirmed customer data. I keep the raw result visible
so an operations user can trace where a field came from."

**25-38 seconds - data quality**

Show the parsed-and-standardized table.

"The pipeline standardizes formatting conservatively. For example, it converts
an unambiguous date to ISO format, but it leaves an ambiguous date unresolved
instead of guessing."

**38-52 seconds - safe reuse**

In **Historical matching and review routing**, select `CASE-018`.

"This case contains lower-case text and an extra space in the passport number.
After standardization, it safely matches one synthetic historical record, so the
workflow recommends reuse while keeping the result unverified."

**52-68 seconds - conflict and review**

Select `CASE-038`, then `CASE-047`.

"Here, the passport number matches history but the identity information
conflicts, so the system escalates rather than overwriting a record. This second
case has an incomplete or ambiguous core field and goes directly to human
review."

**68-82 seconds - close**

Show the three batch metrics.

"The metrics are calculated from generated data and are illustrative only. The
main purpose is to demonstrate an explainable, human-in-the-loop OCR workflow."

## Recording checklist

- Keep the synthetic-data notice visible at least once.
- Show one `REUSE`, one `CONFLICT`, and one `MANUAL_REVIEW` case.
- Do not call synthetic metrics production results or OCR accuracy.
- Remove browser bookmarks, notifications, and unrelated windows before capture.
