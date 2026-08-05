from pathlib import Path

from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text(file_path: str) -> tuple[str, float]:
    """
    Extract text from an image using Tesseract OCR.

    Returns:
        (text, confidence)
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    image = Image.open(path)

    text = pytesseract.image_to_string(image)

    confidence = 1.0 if text.strip() else 0.0

    return text, confidence
