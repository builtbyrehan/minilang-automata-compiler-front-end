# main.py
# MiniLang Compiler Front-End Runner
# Connects lexical, syntax, and semantic analysis in a terminal interface.

from parser import parse_code
from semantic_analyzer import analyze_semantics


SEPARATOR_WIDTH = 78


def print_heading(title, character="="):
    """Display a formatted terminal heading."""

    print(f"\n{title}")
    print(character * SEPARATOR_WIDTH)


def classify_frontend_errors(errors):
    """
    Separate lexical errors from syntax errors.

    Args:
        errors: Error messages returned by parse_code().

    Returns:
        tuple:
            lexical_errors
            syntax_errors
            other_errors
    """

    lexical_errors = []
    syntax_errors = []
    other_errors = []

    for error in errors:
        error_text = str(error)

        if error_text.startswith("Lexical Error"):
            lexical_errors.append(error_text)

        elif error_text.startswith("Syntax Error"):
            syntax_errors.append(error_text)

        else:
            other_errors.append(error_text)

    return lexical_errors, syntax_errors, other_errors


def display_tokens(tokens):
    """Display the token stream in a formatted table."""

    print_heading("1. TOKEN STREAM", "-")

    if not tokens:
        print("No tokens generated.")
        return

    print(
        f"{'#':<6}"
        f"{'Token Type':<20}"
        f"{'Value':<22}"
        f"{'Line':<12}"
        f"{'Column':<12}"
    )
    print("-" * SEPARATOR_WIDTH)

    for index, token in enumerate(tokens, start=1):
        token_type, token_value, line, column = token

        print(
            f"{index:<6}"
            f"{token_type:<20}"
            f"{token_value:<22}"
            f"{line:<12}"
            f"{column:<12}"
        )


def display_error_report(title, errors, success_message):
    """
    Display an error report for one compiler phase.

    Args:
        title: Report heading.
        errors: Errors belonging to the phase.
        success_message: Message shown when there are no errors.
    """

    print_heading(title, "-")

    if not errors:
        print(success_message)
        return

    for index, error in enumerate(errors, start=1):
        print(f"{index}. {error}")


def display_symbol_table(symbol_table):
    """Display the semantic analyzer's symbol table."""

    print_heading("4. SYMBOL TABLE", "-")

    if not symbol_table:
        print("No variables declared.")
        return

    print(
        f"{'Variable':<20}"
        f"{'Type':<12}"
        f"{'Line':<12}"
        f"{'Column':<12}"
        f"{'Initialized':<14}"
    )
    print("-" * SEPARATOR_WIDTH)

    for variable_name, details in symbol_table.items():
        initialized = details.get("initialized", True)
        initialized_text = "Yes" if initialized else "No"

        print(
            f"{variable_name:<20}"
            f"{details.get('type', 'Unknown'):<12}"
            f"{details.get('declared_line', '-')!s:<12}"
            f"{details.get('declared_column', '-')!s:<12}"
            f"{initialized_text:<14}"
        )


def display_final_result(
    lexical_valid,
    syntax_valid,
    semantic_valid,
):
    """Display the final status of every compiler phase."""

    print_heading("6. FINAL COMPILATION RESULT", "-")

    if lexical_valid:
        print("Lexical Analysis:  Passed")
    else:
        print("Lexical Analysis:  Failed")

    if not lexical_valid:
        print("Syntax Analysis:   Skipped")
    elif syntax_valid:
        print("Syntax Analysis:   Passed")
    else:
        print("Syntax Analysis:   Failed")

    if not syntax_valid:
        print("Semantic Analysis: Skipped")
    elif semantic_valid:
        print("Semantic Analysis: Passed")
    else:
        print("Semantic Analysis: Failed")

    print("-" * SEPARATOR_WIDTH)

    if lexical_valid and syntax_valid and semantic_valid:
        print("Compilation Successful")
        print("Result: Valid MiniLang Code")
    else:
        print("Compilation Failed")
        print("Result: Invalid MiniLang Code")


def run_compiler(code):
    """
    Run all MiniLang compiler front-end phases.

    Args:
        code: MiniLang source code.
    """

    print_heading("MINILANG COMPILER FRONT-END")

    # ------------------------------------------------------------------
    # Lexical and syntax analysis
    # ------------------------------------------------------------------

    tokens, frontend_errors, syntax_valid = parse_code(code)

    lexical_errors, syntax_errors, other_errors = (
        classify_frontend_errors(frontend_errors)
    )

    lexical_valid = len(lexical_errors) == 0

    display_tokens(tokens)

    display_error_report(
        title="2. LEXICAL ANALYSIS REPORT",
        errors=lexical_errors,
        success_message=(
            "Lexical analysis passed. No lexical errors found."
        ),
    )

    print_heading("3. SYNTAX ANALYSIS REPORT", "-")

    if not lexical_valid:
        print(
            "Syntax analysis was skipped because lexical analysis failed."
        )

    elif syntax_errors:
        for index, error in enumerate(syntax_errors, start=1):
            print(f"{index}. {error}")

    elif other_errors:
        for index, error in enumerate(other_errors, start=1):
            print(f"{index}. {error}")

    else:
        print("Syntax analysis passed. No syntax errors found.")

    # ------------------------------------------------------------------
    # Semantic analysis
    # ------------------------------------------------------------------

    symbol_table = {}
    semantic_errors = []
    semantic_valid = False

    if syntax_valid:
        (
            symbol_table,
            semantic_errors,
            semantic_valid,
        ) = analyze_semantics(tokens)

        display_symbol_table(symbol_table)

        display_error_report(
            title="5. SEMANTIC ANALYSIS REPORT",
            errors=semantic_errors,
            success_message=(
                "Semantic analysis passed. No semantic errors found."
            ),
        )

    else:
        print_heading("4. SYMBOL TABLE", "-")
        print(
            "The symbol table was not generated because lexical or "
            "syntax analysis failed."
        )

        print_heading("5. SEMANTIC ANALYSIS REPORT", "-")
        print(
            "Semantic analysis was skipped because lexical or "
            "syntax analysis failed."
        )

    # ------------------------------------------------------------------
    # Final result
    # ------------------------------------------------------------------

    display_final_result(
        lexical_valid=lexical_valid,
        syntax_valid=syntax_valid,
        semantic_valid=semantic_valid,
    )


def get_multiline_input():
    """
    Read a multiline MiniLang program from the terminal.

    The user must enter END on a separate line to finish.
    """

    print_heading("ENTER MINILANG SOURCE CODE", "-")
    print("Type your MiniLang program below.")
    print("Enter END on a new line when finished.")
    print("-" * SEPARATOR_WIDTH)

    source_lines = []

    while True:
        try:
            line = input()

        except EOFError:
            break

        if line.strip().upper() == "END":
            break

        source_lines.append(line)

    return "\n".join(source_lines)


def display_menu():
    """Display the terminal application's main menu."""

    print_heading("MINILANG COMPILER FRONT-END")

    print("1. Run sample MiniLang code")
    print("2. Enter custom MiniLang code")
    print("3. Exit")


def main():
    """Run the MiniLang terminal application."""

    sample_code = """int marks = 85;

if marks > 50 {
    print(marks);
}
"""

    display_menu()

    choice = input("\nEnter your choice (1, 2, or 3): ").strip()

    if choice == "1":
        print_heading("SAMPLE MINILANG CODE", "-")
        print(sample_code)

        run_compiler(sample_code)

    elif choice == "2":
        user_code = get_multiline_input()

        if not user_code.strip():
            print("\nNo source code was entered.")
            return

        run_compiler(user_code)

    elif choice == "3":
        print("\nMiniLang compiler closed.")

    else:
        print(
            "\nInvalid choice. Run the program again and select "
            "1, 2, or 3."
        )


if __name__ == "__main__":
    main()