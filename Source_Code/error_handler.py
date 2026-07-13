# error_handler.py
# Centralized error handling utilities for the MiniLang Compiler Front-End.


def create_error(phase, line, column, message):
    """
    Create a structured compiler error.

    Args:
        phase: Compiler phase where the error occurred.
        line: Source-code line number.
        column: Source-code column number.
        message: Explanation of the error.

    Returns:
        Dictionary containing the error details.
    """

    return {
        "phase": phase,
        "line": line,
        "column": column,
        "message": message,
    }


def lexical_error(line, column, message):
    """
    Create a lexical-analysis error.

    Example:
        lexical_error(
            1,
            5,
            "Invalid identifier '3marks'."
        )
    """

    return create_error(
        phase="Lexical Analysis",
        line=line,
        column=column,
        message=message,
    )


def syntax_error(
    line,
    column,
    expected=None,
    found=None,
    message=None,
):
    """
    Create a syntax-analysis error.

    A custom message may be supplied. Otherwise, the message is generated
    using the expected and found token values.

    Example:
        syntax_error(
            line=1,
            column=11,
            expected="semicolon ';'",
            found="print",
        )
    """

    if message is None:
        if expected is not None and found is not None:
            message = (
                f"Expected {expected}, found '{found}'."
            )

        elif expected is not None:
            message = f"Expected {expected}."

        else:
            message = "Invalid syntax."

    return create_error(
        phase="Syntax Analysis",
        line=line,
        column=column,
        message=message,
    )


def semantic_error(line, column, message):
    """
    Create a semantic-analysis error.

    Example:
        semantic_error(
            2,
            1,
            "Variable 'x' is used before declaration."
        )
    """

    return create_error(
        phase="Semantic Analysis",
        line=line,
        column=column,
        message=message,
    )


def format_error(error):
    """
    Convert an error into a readable string.

    The function accepts:

    1. A structured error dictionary created by this module.
    2. An existing string error returned by the current lexer,
       parser, or semantic analyzer.

    Args:
        error: Error dictionary or error string.

    Returns:
        Formatted error message.
    """

    # Existing lexer/parser/semantic-analyzer errors are already strings.
    if isinstance(error, str):
        return error

    if not isinstance(error, dict):
        return f"Compiler Error: {error}"

    phase = error.get("phase", "Compiler")
    line = error.get("line", "?")
    column = error.get("column", "?")
    message = error.get("message", "Unknown error.")

    return (
        f"{phase} Error at line {line}, "
        f"column {column}: {message}"
    )


def format_error_list(errors):
    """
    Return a list of formatted error messages.

    Args:
        errors: List of error dictionaries or strings.

    Returns:
        List of formatted error strings.
    """

    return [format_error(error) for error in errors]


def display_error_list(errors):
    """
    Display compiler errors in the terminal.

    Args:
        errors: List of error dictionaries or strings.
    """

    if not errors:
        print("No errors found.")
        return

    for error_number, error in enumerate(errors, start=1):
        print(f"{error_number}. {format_error(error)}")


def errors_as_text(errors):
    """
    Convert all errors into a single multiline string.

    This is useful for displaying errors in Streamlit or saving them
    in a test-results file.

    Args:
        errors: List of error dictionaries or strings.

    Returns:
        Multiline string containing all formatted errors.
    """

    if not errors:
        return "No errors found."

    formatted_errors = []

    for error_number, error in enumerate(errors, start=1):
        formatted_errors.append(
            f"{error_number}. {format_error(error)}"
        )

    return "\n".join(formatted_errors)


def has_errors(errors):
    """
    Return True when the error list contains at least one error.
    """

    return len(errors) > 0


def main():
    """Run basic error-handler tests."""

    sample_lexical_error = lexical_error(
        line=1,
        column=5,
        message=(
            "Invalid identifier '3marks'. "
            "Identifiers cannot begin with a number."
        ),
    )

    sample_syntax_error = syntax_error(
        line=2,
        column=11,
        expected="semicolon ';'",
        found="print",
    )

    sample_custom_syntax_error = syntax_error(
        line=3,
        column=15,
        message="Missing closing parenthesis ')'.",
    )

    sample_semantic_error = semantic_error(
        line=4,
        column=1,
        message="Variable 'x' is used before declaration.",
    )

    sample_errors = [
        sample_lexical_error,
        sample_syntax_error,
        sample_custom_syntax_error,
        sample_semantic_error,
    ]

    print("MINILANG ERROR REPORT")
    print("=" * 70)

    display_error_list(sample_errors)

    print("\nERRORS AS TEXT")
    print("=" * 70)

    print(errors_as_text(sample_errors))


if __name__ == "__main__":
    main()