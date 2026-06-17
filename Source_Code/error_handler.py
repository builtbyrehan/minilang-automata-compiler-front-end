# error_handler.py
# Centralized error handling for MiniLang Compiler Front-End


def lexical_error(line, column, message):
    return {
        "phase": "Lexical Analysis",
        "line": line,
        "column": column,
        "message": message
    }


def syntax_error(line, column, expected, found):
    return {
        "phase": "Syntax Analysis",
        "line": line,
        "column": column,
        "message": f"Expected {expected}, found '{found}'"
    }


def format_error(error):
    return (
        f"{error['phase']} Error at line {error['line']}, "
        f"column {error['column']}: {error['message']}"
    )


def display_error_list(errors):
    if len(errors) == 0:
        print("No errors found.")
    else:
        for error in errors:
            if isinstance(error, dict):
                print(format_error(error))
            else:
                print(error)


if __name__ == "__main__":
    sample_error = syntax_error(
        line=1,
        column=11,
        expected="SEMICOLON ';'",
        found="print"
    )

    print(format_error(sample_error))