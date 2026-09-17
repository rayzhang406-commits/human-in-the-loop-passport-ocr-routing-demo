"""Small adapter around the local open-source Tesseract executable."""

from pathlib import Path
import shutil
import subprocess


class OCRUnavailableError(RuntimeError):
    """Raised when the optional local OCR executable is unavailable."""


def tesseract_path() -> str | None:
    """Return the installed Tesseract path, if available."""

    return shutil.which("tesseract")


def extract_text(image_path: str | Path) -> str:
    """Extract English text from a synthetic test image.

    This function only returns raw OCR text. Field parsing, normalization, and
    business decisions belong to separate modules.
    """

    executable = tesseract_path()
    if executable is None:
        raise OCRUnavailableError(
            "Tesseract is not installed. Use the provided mock OCR results or "
            "install the optional local OCR dependency."
        )

    image = Path(image_path)
    if not image.is_file():
        raise FileNotFoundError(f"Synthetic test image not found: {image}")

    completed = subprocess.run(
        [executable, str(image), "stdout", "-l", "eng", "--psm", "6"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()
