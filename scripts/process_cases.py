"""Route the public mock OCR batch and write derived demo outputs."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.matching import route_batch  # noqa: E402
from src.metrics import calculate_metrics  # noqa: E402


GENERATED_DIR = PROJECT_ROOT / "data" / "generated"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def process_cases() -> tuple[pd.DataFrame, dict[str, float | int]]:
    """Read synthetic inputs, route them, and write reproducible outputs."""

    historical = pd.read_csv(
        GENERATED_DIR / "historical_customers.csv", keep_default_na=False
    )
    raw_cases = pd.read_csv(
        GENERATED_DIR / "mock_ocr_cases.csv", keep_default_na=False
    )
    routed = pd.DataFrame(
        route_batch(raw_cases.to_dict(orient="records"), historical.to_dict(orient="records"))
    )
    metrics = calculate_metrics(routed)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    routed.to_csv(PROCESSED_DIR / "routed_cases.csv", index=False)
    (PROCESSED_DIR / "routing_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    return routed, metrics


if __name__ == "__main__":
    routed_cases, summary = process_cases()
    print(f"Processed {len(routed_cases)} mock OCR cases.")
    for metric, value in summary.items():
        print(f"{metric}: {value}")
