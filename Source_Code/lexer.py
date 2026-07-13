# lexer.py
# MiniLang Lexical Analyzer
# Converts MiniLang source code into tokens using DFA-like character scanning.

KEYWORDS = {"int", "if", "print"}

OPERATORS = {"=", "+", "-", "*", "/", ">", "<"}

SYMBOLS = {
    ";": "SEMICOLON",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
}


def tokenize(code):
    """
    Convert MiniLang source code into a list of tokens.

    Each token has the following structure:

        (token_type, token_value, line, column)

    Returns:
        tuple:
            tokens: List of recognized tokens.
            errors: List of lexical error messages.
    """

    tokens = []
    errors = []

    position = 0
    line = 1
    column = 1

    while position < len(code):
        current_char = code[position]

        # --------------------------------------------------------------
        # Whitespace handling
        # --------------------------------------------------------------

        if current_char in {" ", "\t"}:
            position += 1
            column += 1
            continue

        # Handle Unix and Windows newline characters.
        if current_char == "\n":
            position += 1
            line += 1
            column = 1
            continue

        # Ignore a carriage return in CRLF-formatted input.
        if current_char == "\r":
            position += 1
            continue

        # --------------------------------------------------------------
        # Identifier or keyword
        # --------------------------------------------------------------

        if current_char.isalpha() or current_char == "_":
            start_column = column
            word = ""

            while position < len(code):
                current_char = code[position]

                if not (current_char.isalnum() or current_char == "_"):
                    break

                word += current_char
                position += 1
                column += 1

            if word in KEYWORDS:
                token_type = "KEYWORD"
            else:
                token_type = "IDENTIFIER"

            tokens.append(
                (token_type, word, line, start_column)
            )
            continue

        # --------------------------------------------------------------
        # Number or invalid numeric identifier
        # --------------------------------------------------------------

        if current_char.isdigit():
            start_column = column
            number = ""

            while (
                position < len(code)
                and code[position].isdigit()
            ):
                number += code[position]
                position += 1
                column += 1

            # Detect invalid identifiers such as 123abc or 5_marks.
            if (
                position < len(code)
                and (
                    code[position].isalpha()
                    or code[position] == "_"
                )
            ):
                invalid_identifier = number

                while (
                    position < len(code)
                    and (
                        code[position].isalnum()
                        or code[position] == "_"
                    )
                ):
                    invalid_identifier += code[position]
                    position += 1
                    column += 1

                errors.append(
                    f"Lexical Error at line {line}, "
                    f"column {start_column}: "
                    f"Invalid identifier '{invalid_identifier}'. "
                    "Identifiers cannot begin with a number."
                )

            else:
                tokens.append(
                    ("NUMBER", number, line, start_column)
                )

            continue

        # --------------------------------------------------------------
        # Operator
        # --------------------------------------------------------------

        if current_char in OPERATORS:
            tokens.append(
                ("OPERATOR", current_char, line, column)
            )

            position += 1
            column += 1
            continue

        # --------------------------------------------------------------
        # Symbols: ; ( ) { }
        # --------------------------------------------------------------

        if current_char in SYMBOLS:
            tokens.append(
                (
                    SYMBOLS[current_char],
                    current_char,
                    line,
                    column,
                )
            )

            position += 1
            column += 1
            continue

        # --------------------------------------------------------------
        # Unknown character
        # --------------------------------------------------------------

        errors.append(
            f"Lexical Error at line {line}, column {column}: "
            f"Unknown symbol '{current_char}'."
        )

        position += 1
        column += 1

    return tokens, errors


def main():
    """Run a basic lexical-analysis test."""

    sample_code = """
int marks = 85;

if marks > 50 {
    print(marks);
}
"""

    tokens, errors = tokenize(sample_code)

    print("TOKENS:")

    for token in tokens:
        print(token)

    print("\nERRORS:")

    if not errors:
        print("No lexical errors found.")
    else:
        for error in errors:
            print(error)


if __name__ == "__main__":
    main()