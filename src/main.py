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
import json


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
    uploaded_pdf = generate_web_interface()

    # Profile extraction
    if uploaded_pdf is not None:
        # text = extract_text_from_pdf(uploaded_pdf)
        # hf_api_key = display_api_box()

        # if len(hf_api_key) != 0:
        #     os.environ["HUGGINGFACEHUB_API_KEY"] = hf_api_key
        #     profile_analysis = extract_profile(text_resume=text)

        #     print("Profile extracted !")
        #     with open(os.path.join("src", "data", "profile_analysis.json"), "w") as fp:
        #         json.dump(profile_analysis, fp)

        # Job parsing
        search_criteria = display_search_criteria()
        print("Search criteria parsed !")
        # with open(os.path.join("src", "data", "search_criteria.json"), "w") as fp:
        #     json.dump(search_criteria, fp)

        if display_search_button():
            jobs = find_jobs(search_criteria)
            print(jobs["description"][0])


if __name__ == "__main__":
    main()
