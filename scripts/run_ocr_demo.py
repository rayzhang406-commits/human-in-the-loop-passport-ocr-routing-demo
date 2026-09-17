"""Run Tesseract on the generated test card and save the raw output."""

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.ocr import extract_text  # noqa: E402


IMAGE_PATH = PROJECT_ROOT / "assets" / "synthetic_passport_test_card.png"
OUTPUT_PATH = PROJECT_ROOT / "data" / "generated" / "sample_ocr_raw.txt"


def main() -> None:
    """Extract and persist raw OCR text from the synthetic card."""

    raw_text = extract_text(IMAGE_PATH)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(raw_text + "\n", encoding="utf-8")
    print(raw_text)
    print(f"\nSaved raw OCR output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
