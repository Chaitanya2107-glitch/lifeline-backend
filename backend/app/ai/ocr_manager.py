from app.ai.tesseract_engine import extract_text as tesseract_extract
# Future import:
# from app.ai.vision_engine import extract_text as vision_extract


def extract_text(file_path: str) -> str:
    """
    Extract text using the best available OCR engine.
    """

    text, confidence = tesseract_extract(file_path)

    print(f"OCR Confidence: {confidence}")

    if confidence >= 0.7:
        return text

    # Future fallback:
    # return vision_extract(file_path)

    return text
