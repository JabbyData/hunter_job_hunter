"""
Module to set-up web-interface
"""

import streamlit as st


def generate_web_interface():
    """
    Brief description of what the function does.

    Args:
        arg_1 (str): Description of the first parameter.
        arg_2 (np.array): Description of the second parameter.
        arg_n (int)(optional): Description of the third parameter.

    Returns:
        float: Description of the return value.

    Raises:
        ExceptionType: Description of the exception that might be raised.

    Example:
    >>> function_name(arg_1, arg_2, arg_n)
    expected_output
    """
    title = "🎯 Welcome to Hunter_J_Hunter !"
    st.title(title)
    st.markdown("<h3 style='text-align: center;'> Your AI Career Assistant</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # File upload section
    st.markdown("### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type="pdf", #autmatically handle pdf file upload
        help="Upload your resume in PDF format"
    )

    if uploaded_file is not None:
        
        st.success(f"✅ File uploaded: {uploaded_file.name}")
    else:
        st.info("👆 Please upload a PDF file to get started")
        
    return uploaded_file

