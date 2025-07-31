"""
Module to set-up web-interface
"""

import streamlit as st
import math


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

    st.session_state.uploaded_pdf = uploaded_file


def display_api_box():
    st.markdown("### 🔑 API Configuration")

    api_key = st.text_input(
        "Please enter your HugginFace API key:",
        type="password",
        placeholder="Enter your HugginFace API key here...",
        help="This key will be used to access external services",
    )

    return api_key


def display_search_criteria():
    st.markdown("### 🔍 Search Criteria")

    job_title = st.text_input(
        "Job Title/Position",
        placeholder="ex Data Scientist",
        help="Enter the job title or position you're looking for.",
    )

    country = st.text_input(
        "Country",
        placeholder="ex France",
        help="Enter your preferred job country location.",
    )

    city = st.text_input(
        "City", placeholder="ex Paris", help="Enter your preferred job city location."
    )

    seniority = st.selectbox(
        "Seniority",
        ["Any", "Internship", "Entry level", "Mid-senior level", "Associate"],
        help="Select your experience level.",
    )

    job_type = st.selectbox(
        "Job Type",
        ["Any", "Fulltime", "Parttime", "Internship", "Contract"],
        help="Select your preferred job type.",
    )

    industry = st.text_input(
        "Industry", placeholder="ex Technology", help="Enter your preferred industry."
    )

    min_salary = st.text_input(
        "Max Salary",
        placeholder="ex 2000",
        help="Enter your minimum expected salary in euros.",
    )

    max_distance = st.slider(
        "Maximum Distance (km)",
        min_value=0,
        max_value=100,
        value=25,
        step=1,
        help="Maximum distance from your location in kilometers.",
    )

    return {
        "job_title": job_title,
        "country": country,
        "city": city,
        "seniority": seniority,
        "job_type": job_type,
        "industry": industry,
        "min_salary": min_salary,
        "max_distance": math.ceil(max_distance * 0.621371),  # convert to miles
    }


def display_search_button():
    """
    Displays a search button for job hunting.

    Returns:
        bool: True if the search button is clicked, False otherwise.
    """
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_clicked = st.button(
            "🔍 Start Job Search",
            type="primary",
            help="Click to start searching for jobs based on your criteria",
            use_container_width=True,
        )

    return search_clicked
