"""
Module to set-up web-interface
"""

import streamlit as st


def generate_web_interface():
    """
    Generates a Streamlit web interface for the Hunter Job Hunter application.

    This function creates a user-friendly web interface with a title, description,
    and file upload functionality for PDF resumes.

    Returns:
        streamlit.runtime.uploaded_file_manager.UploadedFile or None:
            The uploaded PDF file object if a file is uploaded, None otherwise.

    Example:
        >>> uploaded_file = generate_web_interface()
        >>> if uploaded_file:
        ...     print(f"File uploaded: {uploaded_file.name}")
    """
    title = "🎯 Welcome to Hunter_J_Hunter !"
    st.title(title)
    st.markdown(
        "<h3 style='text-align: center;'> Your AI Career Assistant</h3>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # File upload section
    st.markdown("### 📄 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",  # autmatically handle pdf file upload
        help="Upload your resume in PDF format",
    )

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
    else:
        st.info("👆 Please upload a PDF file to get started")

    return uploaded_file


def display_api_box():
    st.markdown("### 🔑 API Configuration")

    api_key = st.text_input(
        "Please enter your HugginFace API key:",
        type="password",
        placeholder="Enter your HugginFace API key here...",
        help="This key will be used to access external services",
    )

    return api_key
