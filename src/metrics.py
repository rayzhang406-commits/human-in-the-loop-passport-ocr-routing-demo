"""Small, clearly defined workflow metrics for the Streamlit demo."""

from __future__ import annotations

import pandas as pd


def calculate_metrics(routed_cases: pd.DataFrame) -> dict[str, float | int]:
    """Calculate metrics from routing output, not from expected test labels."""

    total_cases = len(routed_cases)
    if total_cases == 0:
        raise ValueError("Cannot calculate workflow metrics for an empty dataset.")

    return {
        "total_cases": total_cases,
        "critical_field_completeness": float(
            routed_cases["critical_field_completeness"].mean()
        ),
        "automatic_reuse_rate": float(
            routed_cases["routing_decision"].eq("REUSE").mean()
        ),
        "human_review_rate": float(routed_cases["review_required"].mean()),
        "conflict_rate": float(
            routed_cases["routing_decision"].eq("CONFLICT").mean()
        ),
    }
