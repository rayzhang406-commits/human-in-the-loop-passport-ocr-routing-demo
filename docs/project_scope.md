# Project Scope

## Project objective

Demonstrate how uncertain OCR-derived identity fields can be normalized,
compared with historical records, and routed to an appropriate next step.

## User story

As an operations user, I want a passport OCR result to be compared with
historical customer data so that the system can recommend whether to create a
record, reuse an existing record, or escalate a conflict without silently
overwriting identity information.

## Core decisions

| Decision | Meaning | Human review |
|---|---|---|
| `CREATE` | Required fields are complete and no historical customer matches | Not automatically escalated |
| `REUSE` | Normalized identity keys match and known identity fields do not conflict | Not automatically escalated |
| `CONFLICT` | A strong candidate exists but one or more non-empty identity fields disagree | Required |
| `MANUAL_REVIEW` | Key fields are missing or the case is otherwise unsafe to classify | Required |

Each decision is a routing recommendation, not identity confirmation.

## Acceptance criteria

- The demo runs using only generated data and repository files.
- Synthetic data can be regenerated with a fixed random seed.
- Raw and normalized field values remain separately visible.
- Every routing decision includes a human-readable reason.
- Conflicting values are never silently overwritten.
- The Streamlit page can demonstrate one reuse case and one review case in under 90 seconds.
