"""
Main module to run interface
"""

from tools.web_interface import generate_web_interface


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
    # Function implementation
    uploaded_pdf = generate_web_interface()
    if uploaded_pdf is not None:
        print(uploaded_pdf.name)
        print(type(uploaded_pdf))



if __name__ == "__main__":
    main()
