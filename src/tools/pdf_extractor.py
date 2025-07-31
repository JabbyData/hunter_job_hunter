"""
Module related to pdf extraction and features preparation
"""

import fitz


def extract_text_from_pdf(pdf_file) -> float:
    """
    Extract text content from a PDF file.

    Args:
        pdf_file (str): Path to the PDF file to extract text from.

    Returns:
        str: Extracted text content from the PDF file.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        PDFSyntaxError: If the PDF file is corrupted or invalid.

    Example:
        >> extract_text_from_pdf("resume.pdf")
        "John Doe\nSoftware Engineer\n..."
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # PyMuPDF
    text = ""
    for page in doc:
        text += page.get_text()
    return text
