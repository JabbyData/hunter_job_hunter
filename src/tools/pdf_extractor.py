"""
Module related to pdf extraction and features preparation
"""

from pdfminer.high_level import extract_text

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
    # Function implementation
    text = extract_text(pdf_file)
    return text

# def (arg_1: str, arg_2: np.array, arg_n: int = 0) -> float:
#     """
#     Brief description of what the function does.
    
#     Args:
#         arg_1 (str): Description of the first parameter.
#         arg_2 (np.array): Description of the second parameter.
#         arg_n (int)(optional): Description of the third parameter.
    
#     Returns:
#         float: Description of the return value.
    
#     Raises:
#         ExceptionType: Description of the exception that might be raised.
    
#     Example:
#     >>> function_name(arg_1, arg_2, arg_n)
#     expected_output
#     """
#     # Function implementation
#     pass

