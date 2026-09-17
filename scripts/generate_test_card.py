"""Generate an obviously synthetic, non-valid OCR test card."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "assets" / "synthetic_passport_test_card.png"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a common local font with a portable Pillow fallback."""

    candidates = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default(size=size)


def generate_card(output_path: Path = DEFAULT_OUTPUT) -> Path:
    """Create one deterministic test card with no real identity data."""

    width, height = 1400, 900
    image = Image.new("RGB", (width, height), "#F7FAFC")
    draw = ImageDraw.Draw(image)

    navy = "#17324D"
    blue = "#DCEAF5"
    red = "#B42318"
    gray = "#52606D"

    draw.rounded_rectangle(
        (40, 40, width - 40, height - 40),
        radius=28,
        fill="white",
        outline=navy,
        width=5,
    )
    draw.rounded_rectangle(
        (40, 40, width - 40, 145),
        radius=28,
        fill=red,
    )
    draw.rectangle((40, 105, width - 40, 145), fill=red)

    draw.text(
        (width / 2, 92),
        "SYNTHETIC TEST CARD - NOT VALID",
        fill="white",
        font=load_font(42, bold=True),
        anchor="mm",
    )
    draw.text(
        (95, 195),
        "PASSPORT-LIKE OCR INPUT",
        fill=navy,
        font=load_font(44, bold=True),
    )
    draw.text(
        (95, 260),
        "Independent software demonstration / No government issuer",
        fill=gray,
        font=load_font(25),
    )

    fields = [
        ("FULL NAME", "MAYA LIN"),
        ("PASSPORT NO", "TEST-X7Q2M9"),
        ("DATE OF BIRTH", "14 JUN 1998"),
        ("SEX", "F"),
        ("PLACE OF BIRTH", "SAMPLE CITY"),
        ("EXPIRY DATE", "30 SEP 2031"),
    ]

    top = 340
    label_font = load_font(24, bold=True)
    value_font = load_font(34)
    for index, (label, value) in enumerate(fields):
        row = index // 2
        column = index % 2
        x = 95 + column * 635
        y = top + row * 145
        draw.rounded_rectangle(
            (x, y, x + 575, y + 110),
            radius=12,
            fill=blue,
            outline="#A8BED0",
            width=2,
        )
        draw.text((x + 24, y + 16), label, fill=gray, font=label_font)
        draw.text((x + 24, y + 52), value, fill=navy, font=value_font)

    draw.text(
        (width / 2, 825),
        "Generated solely for OCR testing. No real person or travel document.",
        fill=red,
        font=load_font(25, bold=True),
        anchor="mm",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG", optimize=True)
    return output_path


if __name__ == "__main__":
    result = generate_card()
    print(f"Created synthetic test card: {result}")
