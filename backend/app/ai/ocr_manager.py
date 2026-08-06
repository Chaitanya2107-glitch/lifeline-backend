import time

from app.ai.tesseract_engine import extract_text as tesseract_extract
from app.utils.logger import logger


def extract_text(file_path: str) -> str:
    """
    Extract text using the best available OCR engine.
    """

    start_time = time.time()

    logger.info(
        "OCR request started | Provider: Tesseract | File: {}",
        file_path
    )

    try:
        text, confidence = tesseract_extract(file_path)

        duration = round(time.time() - start_time, 2)

        logger.info(
            "OCR completed | Confidence: {:.2f} | Duration: {} seconds",
            confidence,
            duration
        )

        if confidence >= 0.7:
            return text

        logger.warning(
            "OCR confidence below threshold ({:.2f}). Using Tesseract output because no fallback provider is configured.",
            confidence
        )

        return text

    except Exception as e:

        duration = round(time.time() - start_time, 2)

        logger.error(
            "OCR failed | Duration: {} seconds | Error: {}",
            duration,
            str(e)
        )

        raise
