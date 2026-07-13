# grammar.py
# Formal Context-Free Grammar for MiniLang.
# These production rules describe the syntax implemented by parser.py.


MINILANG_GRAMMAR = {
    "Program": [
        "StatementList",
    ],

    "StatementList": [
        "Statement StatementList",
        "ε",
    ],

    "Statement": [
        "Declaration",
        "Assignment",
        "PrintStatement",
        "IfStatement",
    ],

    "Declaration": [
        "int id = number ;",
    ],

    "Assignment": [
        "id = Expression ;",
    ],

    "PrintStatement": [
        "print ( id ) ;",
    ],

    "IfStatement": [
        "if Condition { StatementList }",
    ],

    "Condition": [
        "id RelOp number",
    ],

    "Expression": [
        "Operand",
        "Operand ArithOp Operand",
    ],

    "Operand": [
        "id",
        "number",
    ],

    "RelOp": [
        ">",
        "<",
    ],

    "ArithOp": [
        "+",
        "-",
        "*",
        "/",
    ],
}


def display_grammar():
    """Display the complete MiniLang context-free grammar."""

    print("MINILANG CONTEXT-FREE GRAMMAR")
    print("=" * 70)

    for non_terminal, productions in MINILANG_GRAMMAR.items():
        production_text = " | ".join(productions)
        print(f"{non_terminal:<15} → {production_text}")


def get_productions(non_terminal):
    """
    Return the production rules for a given non-terminal.

    Args:
        non_terminal: Name of the grammar non-terminal.

    Returns:
        List of productions. Returns an empty list when the
        non-terminal does not exist.
    """

    return MINILANG_GRAMMAR.get(non_terminal, [])


def grammar_as_text():
    """
    Return the complete grammar as formatted text.

    This function can be used by the Streamlit interface or visualizer.
    """

    grammar_lines = []

    for non_terminal, productions in MINILANG_GRAMMAR.items():
        production_text = " | ".join(productions)
        grammar_lines.append(
            f"{non_terminal} → {production_text}"
        )

    return "\n".join(grammar_lines)


def main():
    """Run a basic grammar display test."""

    display_grammar()


if __name__ == "__main__":
    main()