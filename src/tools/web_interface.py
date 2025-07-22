"""
Module to set-up web-interface
"""

import streamlit as st
import emojis


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
    # Function implementation
    title = emojis.encode("Hunter_J_Hunter : your AI career Assistant :robot:")
    st.write(title)
