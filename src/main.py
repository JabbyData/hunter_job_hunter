"""
Main module to run interface
"""

import os
from tools.web_interface import (
    generate_web_interface,
    display_api_box,
    display_search_criteria,
    display_search_button,
)
from tools.pdf_extractor import extract_text_from_pdf
from tools.scraper import find_jobs
from agent.profile_extractor import extract_profile
import streamlit as st


def main():
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
    >>> main(arg_1, arg_2, arg_n)
        expected_output
    """

    generate_web_interface()

    # Profile extraction
    if "uploaded_pdf" in st.session_state and st.session_state.uploaded_pdf is not None:
        if "profile_analysis" not in st.session_state:
            text = extract_text_from_pdf(st.session_state.uploaded_pdf)
            st.session_state.profile_analysis = extract_profile(text_resume=text)
            print("Profile extracted !")
            print(st.session_state.profile_analysis)

            st.session_state.rec_analysis = st.session_state.rec_analysis.strip(
                "[]"
            ).split(",")

        st.subheader("📁 Recommended Job Positions")
        for job in st.session_state.rec_analysis:
            job = job.strip().strip('"')
            st.write(f"• {job}")

        if st.session_state.profile_analysis is not None:
            search_criteria = dict(display_search_criteria())
            print("Search criteria parsed !")

            if display_search_button():
                jobs = find_jobs(search_criteria)  # needs update
                jobs.to_csv(os.path.join("src", "data", "jobs.csv"), index=False)

        # Matching user and jobs profile
        # extract job info


if __name__ == "__main__":
    main()
