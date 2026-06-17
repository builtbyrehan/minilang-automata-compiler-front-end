# grammar.py
# Formal Grammar Rules for MiniLang
# This file stores the CFG production rules used by the parser.

MINILANG_GRAMMAR = {
    "Program": [
        "StatementList"
    ],

    "StatementList": [
        "Statement StatementList",
        "ε"
    ],

    "Statement": [
        "Declaration",
        "Assignment",
        "PrintStatement",
        "IfStatement"
    ],

    "Declaration": [
        "int id = number ;"
    ],

    "Assignment": [
        "id = Expression ;"
    ],

    "PrintStatement": [
        "print ( id ) ;"
    ],

    "IfStatement": [
        "if Condition { StatementList }"
    ],

    "Condition": [
        "id RelOp number"
    ],

    "Expression": [
        "id",
        "number",
        "id ArithOp number",
        "number ArithOp number",
        "id ArithOp id",
        "number ArithOp id"
    ],

    "RelOp": [
        ">",
        "<"
    ],

    "ArithOp": [
        "+",
        "-",
        "*",
        "/"
    ]
}


def display_grammar():
    print("MINILANG CONTEXT-FREE GRAMMAR")
    print("=" * 60)

    for non_terminal, productions in MINILANG_GRAMMAR.items():
        production_text = " | ".join(productions)
        print(f"{non_terminal} → {production_text}")


if __name__ == "__main__":
    display_grammar()