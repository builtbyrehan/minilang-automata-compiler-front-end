# main.py
# MiniLang Compiler Front-End Runner
# Connects lexical analysis, syntax analysis, and semantic analysis.

from parser import parse_code
from semantic_analyzer import analyze_semantics


def display_tokens(tokens):
    print("\nTOKEN STREAM")
    print("-" * 70)
    print(f"{'Token Type':<18} {'Value':<18} {'Line':<10} {'Column':<10}")
    print("-" * 70)

    if len(tokens) == 0:
        print("No tokens generated.")
        return

    for token_type, token_value, line, column in tokens:
        print(f"{token_type:<18} {token_value:<18} {line:<10} {column:<10}")


def display_errors(title, errors):
    print(f"\n{title}")
    print("-" * 70)

    if len(errors) == 0:
        print("No errors found.")
    else:
        for error in errors:
            print(error)


def display_symbol_table(symbol_table):
    print("\nSYMBOL TABLE")
    print("-" * 70)

    if len(symbol_table) == 0:
        print("No variables declared.")
        return

    print(f"{'Variable':<18} {'Type':<12} {'Line':<10} {'Column':<10}")
    print("-" * 70)

    for variable, details in symbol_table.items():
        print(
            f"{variable:<18} "
            f"{details['type']:<12} "
            f"{details['declared_line']:<10} "
            f"{details['declared_column']:<10}"
        )


def run_compiler(code):
    print("\nMINILANG COMPILER FRONT-END")
    print("=" * 70)

    tokens, syntax_errors, syntax_valid = parse_code(code)

    display_tokens(tokens)
    display_errors("LEXICAL / SYNTAX ERROR REPORT", syntax_errors)

    symbol_table = {}
    semantic_errors = []
    semantic_valid = False

    if syntax_valid:
        symbol_table, semantic_errors, semantic_valid = analyze_semantics(tokens)
        display_symbol_table(symbol_table)
        display_errors("SEMANTIC ERROR REPORT", semantic_errors)
    else:
        print("\nSEMANTIC ANALYSIS")
        print("-" * 70)
        print("Skipped because lexical/syntax analysis failed.")

    print("\nFINAL RESULT")
    print("-" * 70)

    if syntax_valid and semantic_valid:
        print("Lexical Analysis: Passed")
        print("Syntax Analysis: Passed")
        print("Semantic Analysis: Passed")
        print("Result: Valid MiniLang Code")
    else:
        print("Compilation Failed")

        if not syntax_valid:
            print("Reason: Lexical or syntax error found.")
        elif not semantic_valid:
            print("Reason: Semantic error found.")

        print("Result: Invalid MiniLang Code")


def get_multiline_input():
    print("\nEnter your MiniLang code below.")
    print("When finished, type END on a new line.")
    print("-" * 70)

    lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    return "\n".join(lines)


if __name__ == "__main__":
    print("MINILANG COMPILER FRONT-END")
    print("=" * 70)
    print("1. Run sample code")
    print("2. Enter custom MiniLang code")

    choice = input("\nEnter your choice 1 or 2: ")

    if choice == "1":
        sample_code = """
int marks = 85;
if marks > 50 {
    print(marks);
}
"""
        run_compiler(sample_code)

    elif choice == "2":
        user_code = get_multiline_input()
        run_compiler(user_code)

    else:
        print("Invalid choice. Please run again and choose 1 or 2.")