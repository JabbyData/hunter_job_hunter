"""
Main module to run interface
"""

import os
from tools.web_interface import generate_web_interface, display_api_box
from tools.pdf_extractor import extract_text
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

    if uploaded_pdf is not None:
        text = extract_text(uploaded_pdf)
        hf_api_key = display_api_box()

        if len(hf_api_key) != 0:
            profile_analysis = extract_profile(hf_api_key=hf_api_key, text_resume=text)

            print("Profile extracted !")
            with open("profile_analyse.json", "w") as fp:
                json.dump(profile_analysis, fp)


if __name__ == "__main__":
    main()
