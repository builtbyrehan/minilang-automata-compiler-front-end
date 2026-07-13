# visualizer.py
# Visualization utilities for the MiniLang Compiler Front-End.

from pathlib import Path


# ----------------------------------------------------------------------
# General utility
# ----------------------------------------------------------------------

def escape_dot_text(value):
    """
    Escape a value so it can safely appear inside a Graphviz label.
    """

    text = str(value)

    return (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("|", "\\|")
    )


# ----------------------------------------------------------------------
# Lexer DFA visualization
# ----------------------------------------------------------------------

def build_lexer_dfa_dot():
    """
    Return the MiniLang lexical analyzer DFA as Graphviz DOT source.
    """

    return r"""
digraph LexerDFA {
    rankdir=LR;

    graph [
        label="MiniLang Lexical Analyzer DFA",
        labelloc="t",
        fontsize=20,
        fontname="Arial"
    ];

    node [
        shape=circle,
        fontname="Arial",
        fontsize=12
    ];

    edge [
        fontname="Arial",
        fontsize=10
    ];

    start [
        shape=point
    ];

    q0 [
        label="q0\nStart"
    ];

    q_identifier [
        label="q1\nIdentifier / Keyword",
        shape=doublecircle
    ];

    q_number [
        label="q2\nNumber",
        shape=doublecircle
    ];

    q_operator [
        label="q3\nOperator",
        shape=doublecircle
    ];

    q_symbol [
        label="q4\nSymbol",
        shape=doublecircle
    ];

    q_whitespace [
        label="q5\nWhitespace"
    ];

    q_invalid_identifier [
        label="q6\nInvalid Identifier",
        shape=doublecircle
    ];

    q_error [
        label="q7\nLexical Error",
        shape=doublecircle
    ];

    start -> q0;

    q0 -> q_identifier [
        label="letter or _"
    ];

    q_identifier -> q_identifier [
        label="letter, digit or _"
    ];

    q0 -> q_number [
        label="digit"
    ];

    q_number -> q_number [
        label="digit"
    ];

    q_number -> q_invalid_identifier [
        label="letter or _"
    ];

    q_invalid_identifier -> q_invalid_identifier [
        label="letter, digit or _"
    ];

    q0 -> q_operator [
        label="= + - * / > <"
    ];

    q0 -> q_symbol [
        label="; ( ) { }"
    ];

    q0 -> q_whitespace [
        label="space, tab or newline"
    ];

    q_whitespace -> q0 [
        label="continue scanning"
    ];

    q0 -> q_error [
        label="unknown character"
    ];
}
""".strip()


# ----------------------------------------------------------------------
# Compiler flow visualization
# ----------------------------------------------------------------------

def build_compiler_flow_dot():
    """
    Return the compiler front-end flow as Graphviz DOT source.
    """

    return r"""
digraph CompilerFlow {
    rankdir=TB;

    graph [
        label="MiniLang Compiler Front-End Flow",
        labelloc="t",
        fontsize=20,
        fontname="Arial",
        nodesep=0.45,
        ranksep=0.55
    ];

    node [
        shape=box,
        style="rounded",
        fontname="Arial",
        fontsize=12,
        margin="0.18,0.10"
    ];

    edge [
        fontname="Arial",
        fontsize=10
    ];

    source [
        label="MiniLang Source Code"
    ];

    lexer [
        label="Lexical Analyzer\nDFA-like character scanning"
    ];

    lexical_decision [
        label="Lexical Errors?",
        shape=diamond
    ];

    tokens [
        label="Token Stream"
    ];

    parser [
        label="Syntax Analyzer\nRecursive-descent parser and CFG"
    ];

    syntax_decision [
        label="Syntax Valid?",
        shape=diamond
    ];

    semantic [
        label="Semantic Analyzer\nSymbol-table validation"
    ];

    semantic_decision [
        label="Semantic Valid?",
        shape=diamond
    ];

    valid [
        label="Valid MiniLang Code",
        shape=doublecircle
    ];

    invalid [
        label="Invalid MiniLang Code",
        shape=doublecircle
    ];

    source -> lexer;
    lexer -> lexical_decision;

    lexical_decision -> invalid [
        label="Yes"
    ];

    lexical_decision -> tokens [
        label="No"
    ];

    tokens -> parser;
    parser -> syntax_decision;

    syntax_decision -> invalid [
        label="No"
    ];

    syntax_decision -> semantic [
        label="Yes"
    ];

    semantic -> semantic_decision;

    semantic_decision -> valid [
        label="Yes"
    ];

    semantic_decision -> invalid [
        label="No"
    ];
}
""".strip()


# ----------------------------------------------------------------------
# Token-stream visualization
# ----------------------------------------------------------------------

def build_token_stream_dot(tokens):
    """
    Build a left-to-right Graphviz diagram for a token stream.

    Args:
        tokens: Tokens generated by lexer.py.

    Returns:
        Graphviz DOT source.
    """

    lines = [
        "digraph TokenStream {",
        "    rankdir=LR;",
        "",
        "    graph [",
        '        label="MiniLang Token Stream",',
        '        labelloc="t",',
        "        fontsize=20,",
        '        fontname="Arial"',
        "    ];",
        "",
        "    node [",
        "        shape=record,",
        '        fontname="Arial",',
        "        fontsize=10",
        "    ];",
        "",
        "    edge [",
        '        fontname="Arial",',
        "        fontsize=9",
        "    ];",
        "",
    ]

    if not tokens:
        lines.extend(
            [
                '    empty [label="No tokens generated"];',
                "}",
            ]
        )

        return "\n".join(lines)

    for index, token in enumerate(tokens):
        token_type, token_value, line, column = token

        safe_type = escape_dot_text(token_type)
        safe_value = escape_dot_text(token_value)
        safe_line = escape_dot_text(line)
        safe_column = escape_dot_text(column)

        label = (
            f"{{Token {index + 1}"
            f"|Type: {safe_type}"
            f"|Value: {safe_value}"
            f"|Line: {safe_line}"
            f"|Column: {safe_column}}}"
        )

        lines.append(
            f'    token_{index} [label="{label}"];'
        )

    lines.append("")

    for index in range(len(tokens) - 1):
        lines.append(
            f"    token_{index} -> token_{index + 1};"
        )

    lines.append("}")

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Symbol-table visualization
# ----------------------------------------------------------------------

def build_symbol_table_dot(symbol_table):
    """
    Build a Graphviz diagram for the semantic symbol table.

    Args:
        symbol_table: Symbol table generated by semantic_analyzer.py.

    Returns:
        Graphviz DOT source.
    """

    lines = [
        "digraph SymbolTable {",
        "    rankdir=TB;",
        "",
        "    graph [",
        '        label="MiniLang Symbol Table",',
        '        labelloc="t",',
        "        fontsize=20,",
        '        fontname="Arial"',
        "    ];",
        "",
        "    node [",
        "        shape=record,",
        '        fontname="Arial",',
        "        fontsize=11",
        "    ];",
        "",
    ]

    if not symbol_table:
        lines.extend(
            [
                (
                    '    empty [label="Symbol Table'
                    '|No variables declared"];'
                ),
                "}",
            ]
        )

        return "\n".join(lines)

    table_fields = [
        "Variable | Type | Line | Column | Initialized"
    ]

    for variable_name, details in symbol_table.items():
        safe_variable = escape_dot_text(variable_name)

        safe_type = escape_dot_text(
            details.get("type", "Unknown")
        )

        safe_line = escape_dot_text(
            details.get("declared_line", "-")
        )

        safe_column = escape_dot_text(
            details.get("declared_column", "-")
        )

        initialized = details.get("initialized", True)
        initialized_text = "Yes" if initialized else "No"

        table_fields.append(
            f"{safe_variable} | "
            f"{safe_type} | "
            f"{safe_line} | "
            f"{safe_column} | "
            f"{initialized_text}"
        )

    table_label = "{" + "|".join(table_fields) + "}"

    lines.append(
        f'    symbol_table [label="{table_label}"];'
    )

    lines.append("}")

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Streamlit visualization function
# ----------------------------------------------------------------------

def display_visualizations(tokens=None, symbol_table=None):
    """
    Display MiniLang diagrams in Streamlit.

    Args:
        tokens: Optional token stream.
        symbol_table: Optional semantic symbol table.
    """

    import streamlit as st

    st.subheader("Lexical Analyzer DFA")

    st.graphviz_chart(
        build_lexer_dfa_dot(),
        width="stretch",
    )

    st.subheader("Compiler Front-End Flow")

    st.graphviz_chart(
        build_compiler_flow_dot(),
        width="stretch",
    )

    if tokens is not None:
        st.subheader("Token Stream Visualization")

        st.graphviz_chart(
            build_token_stream_dot(tokens),
            width="stretch",
        )

    if symbol_table is not None:
        st.subheader("Symbol Table Visualization")

        st.graphviz_chart(
            build_symbol_table_dot(symbol_table),
            width="stretch",
        )


# ----------------------------------------------------------------------
# DOT-file export
# ----------------------------------------------------------------------

def save_dot_file(dot_source, output_path):
    """
    Save Graphviz DOT source to a file.

    Args:
        dot_source: Graphviz DOT text.
        output_path: Destination path.

    Returns:
        Path of the generated file.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        dot_source,
        encoding="utf-8",
    )

    return output_path


def export_default_diagrams():
    """
    Export default MiniLang diagrams into the Diagrams directory.
    """

    source_code_directory = Path(__file__).resolve().parent
    project_directory = source_code_directory.parent

    diagrams_directory = (
        project_directory / "Diagrams"
    )

    lexer_path = save_dot_file(
        build_lexer_dfa_dot(),
        diagrams_directory / "lexer_dfa.dot",
    )

    compiler_flow_path = save_dot_file(
        build_compiler_flow_dot(),
        diagrams_directory / "compiler_flow.dot",
    )

    return [
        lexer_path,
        compiler_flow_path,
    ]


# ----------------------------------------------------------------------
# Standalone test
# ----------------------------------------------------------------------

def main():
    """Generate sample Graphviz DOT files."""

    sample_tokens = [
        ("KEYWORD", "int", 1, 1),
        ("IDENTIFIER", "marks", 1, 5),
        ("OPERATOR", "=", 1, 11),
        ("NUMBER", "85", 1, 13),
        ("SEMICOLON", ";", 1, 15),
    ]

    sample_symbol_table = {
        "marks": {
            "type": "int",
            "declared_line": 1,
            "declared_column": 5,
            "initialized": True,
        }
    }

    generated_files = export_default_diagrams()

    source_code_directory = Path(__file__).resolve().parent
    project_directory = source_code_directory.parent

    diagrams_directory = (
        project_directory / "Diagrams"
    )

    token_stream_path = save_dot_file(
        build_token_stream_dot(sample_tokens),
        diagrams_directory / "sample_token_stream.dot",
    )

    symbol_table_path = save_dot_file(
        build_symbol_table_dot(sample_symbol_table),
        diagrams_directory / "sample_symbol_table.dot",
    )

    generated_files.extend(
        [
            token_stream_path,
            symbol_table_path,
        ]
    )

    print("MINILANG VISUALIZER")
    print("=" * 70)
    print("The following diagram files were generated:")

    for file_path in generated_files:
        print(f"- {file_path}")


if __name__ == "__main__":
    main()