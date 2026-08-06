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

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT
    )

    text = pytesseract.image_to_string(image)


    confidences = [
        int(c)
        for c in data["conf"]
        if c != "-1"
    ]


    if confidences:
        confidence = sum(confidences) / len(confidences) / 100
    else:
        confidence = 0.0
    return text, confidence
