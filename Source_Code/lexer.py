# lexer.py
# MiniLang Lexical Analyzer
# This file converts source code into tokens using DFA-like character scanning.

KEYWORDS = ["int", "if", "print"]

OPERATORS = ["=", "+", "-", "*", "/", ">", "<"]

SYMBOLS = {
    ";": "SEMICOLON",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE"
}


def tokenize(code):
    tokens = []
    errors = []

    i = 0
    line = 1
    column = 1

    while i < len(code):
        char = code[i]

        # Ignore spaces and tabs
        if char == " " or char == "\t":
            i += 1
            column += 1
            continue

        # Handle new line
        if char == "\n":
            i += 1
            line += 1
            column = 1
            continue

        # Identifier or Keyword
        if char.isalpha() or char == "_":
            start_column = column
            word = ""

            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                word += code[i]
                i += 1
                column += 1

            if word in KEYWORDS:
                tokens.append(("KEYWORD", word, line, start_column))
            else:
                tokens.append(("IDENTIFIER", word, line, start_column))

            continue

        # Number
        if char.isdigit():
            start_column = column
            number = ""

            while i < len(code) and code[i].isdigit():
                number += code[i]
                i += 1
                column += 1

            # Example: 123abc is invalid in MiniLang
            if i < len(code) and (code[i].isalpha() or code[i] == "_"):
                invalid_word = number

                while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                    invalid_word += code[i]
                    i += 1
                    column += 1

                errors.append(
                    f"Lexical Error at line {line}, column {start_column}: Invalid identifier '{invalid_word}'"
                )
            else:
                tokens.append(("NUMBER", number, line, start_column))

            continue

        # Operator
        if char in OPERATORS:
            tokens.append(("OPERATOR", char, line, column))
            i += 1
            column += 1
            continue

        # Symbols like ; ( ) { }
        if char in SYMBOLS:
            tokens.append((SYMBOLS[char], char, line, column))
            i += 1
            column += 1
            continue

        # Unknown character
        errors.append(
            f"Lexical Error at line {line}, column {column}: Unknown symbol '{char}'"
        )
        i += 1
        column += 1

    return tokens, errors


# Temporary testing code
# This will run only when lexer.py is executed directly.
if __name__ == "__main__":
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
    if len(errors) == 0:
        print("No lexical errors found.")
    else:
        for error in errors:
            print(error)