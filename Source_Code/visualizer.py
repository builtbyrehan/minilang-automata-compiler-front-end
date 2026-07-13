# visualizer.py
# Responsive visualization utilities for the MiniLang Compiler Front-End.

from html import escape
from pathlib import Path


# ----------------------------------------------------------------------
# Text escaping
# ----------------------------------------------------------------------

def escape_dot_text(value):
    """
    Escape plain text for use inside a standard Graphviz label.
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


def escape_html_text(value):
    """
    Escape a value for use inside a Graphviz HTML-like table label.
    """

    return escape(str(value), quote=True)


# ----------------------------------------------------------------------
# Lexer DFA
# ----------------------------------------------------------------------

def build_lexer_dfa_dot():
    """
    Build a compact lexer DFA that fits the Streamlit viewport.
    """

    return r"""
digraph LexerDFA {
    rankdir=TB;

    graph [
        label="MiniLang Lexical Analyzer DFA",
        labelloc="t",
        fontsize=18,
        fontname="Arial",
        pad=0.20,
        margin=0.05,
        nodesep=0.35,
        ranksep=0.50,
        ratio="compress"
    ];

    node [
        shape=circle,
        fontname="Arial",
        fontsize=9,
        width=1.20,
        height=1.20,
        fixedsize=true
    ];

    edge [
        fontname="Arial",
        fontsize=8,
        arrowsize=0.70
    ];

    start [
        shape=point,
        width=0.12,
        height=0.12
    ];

    q0 [
        label="q0\nStart"
    ];

    q_identifier [
        label="q1\nIdentifier\nor Keyword",
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
        label="q5\nWhitespace",
        shape=circle
    ];

    q_invalid_identifier [
        label="q6\nInvalid\nIdentifier",
        shape=doublecircle
    ];

    q_error [
        label="q7\nLexical\nError",
        shape=doublecircle
    ];

    start -> q0;

    q0 -> q_identifier [
        label="letter or _"
    ];

    q0 -> q_number [
        label="digit"
    ];

    q0 -> q_operator [
        label="= + - * / > <"
    ];

    q0 -> q_symbol [
        label="; ( ) { }"
    ];

    q0 -> q_whitespace [
        label="space, tab,\nor newline"
    ];

    q0 -> q_error [
        label="unknown\ncharacter"
    ];

    q_identifier -> q_identifier [
        label="letter, digit or _"
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

    q_whitespace -> q0 [
        label="continue",
        constraint=false
    ];

    {
        rank=same;
        q_identifier;
        q_number;
        q_operator;
        q_symbol;
    }

    {
        rank=same;
        q_invalid_identifier;
        q_whitespace;
        q_error;
    }
}
""".strip()


# ----------------------------------------------------------------------
# Compiler flow
# ----------------------------------------------------------------------

def build_compiler_flow_dot():
    """
    Build a compact compiler-flow diagram.

    Final states use double-bordered boxes instead of large circles so the
    diagram remains readable and fits within the page.
    """

    return r"""
digraph CompilerFlow {
    rankdir=TB;

    graph [
        label="MiniLang Compiler Front-End Flow",
        labelloc="t",
        fontsize=18,
        fontname="Arial",
        pad=0.20,
        margin=0.05,
        nodesep=0.45,
        ranksep=0.38,
        ratio="compress"
    ];

    node [
        shape=box,
        style="rounded",
        fontname="Arial",
        fontsize=10,
        margin="0.16,0.09",
        width=2.65
    ];

    edge [
        fontname="Arial",
        fontsize=9,
        arrowsize=0.75
    ];

    source [
        label="MiniLang Source Code"
    ];

    lexer [
        label="Lexical Analyzer\nDFA-like character scanning"
    ];

    lexical_decision [
        label="Lexical errors?",
        shape=diamond,
        width=2.15,
        height=0.85
    ];

    tokens [
        label="Token Stream",
        width=1.80
    ];

    parser [
        label="Syntax Analyzer\nRecursive-descent parser using CFG"
    ];

    syntax_decision [
        label="Syntax valid?",
        shape=diamond,
        width=2.15,
        height=0.85
    ];

    semantic [
        label="Semantic Analyzer\nSymbol-table validation"
    ];

    semantic_decision [
        label="Semantic valid?",
        shape=diamond,
        width=2.15,
        height=0.85
    ];

    valid [
        label="Valid MiniLang Code",
        shape=box,
        style="rounded,bold",
        peripheries=2,
        width=2.40
    ];

    invalid [
        label="Invalid MiniLang Code",
        shape=box,
        style="rounded,bold",
        peripheries=2,
        width=2.40
    ];

    source -> lexer;
    lexer -> lexical_decision;

    lexical_decision -> tokens [
        label="No"
    ];

    lexical_decision -> invalid [
        label="Yes",
        constraint=false
    ];

    tokens -> parser;
    parser -> syntax_decision;

    syntax_decision -> semantic [
        label="Yes"
    ];

    syntax_decision -> invalid [
        label="No",
        constraint=false
    ];

    semantic -> semantic_decision;

    semantic_decision -> valid [
        label="Yes"
    ];

    semantic_decision -> invalid [
        label="No"
    ];

    {
        rank=same;
        valid;
        invalid;
    }
}
""".strip()


# ----------------------------------------------------------------------
# Token-stream visualization
# ----------------------------------------------------------------------

def build_token_stream_dot(tokens):
    """
    Build a responsive token-stream table.

    The former implementation placed every token in one horizontal chain.
    That became unreadable when a program contained many tokens. This version
    displays one compact row per token.
    """

    lines = [
        "digraph TokenStream {",
        "    rankdir=TB;",
        "",
        "    graph [",
        '        label="MiniLang Token Stream",',
        '        labelloc="t",',
        "        fontsize=18,",
        '        fontname="Arial",',
        "        pad=0.20,",
        "        margin=0.05",
        "    ];",
        "",
        "    node [",
        "        shape=plain,",
        '        fontname="Arial"',
        "    ];",
        "",
    ]

    if not tokens:
        lines.extend(
            [
                "    token_table [",
                "        label=<",
                '            <TABLE BORDER="1" CELLBORDER="1" '
                'CELLSPACING="0" CELLPADDING="8">',
                '                <TR><TD>No tokens generated</TD></TR>',
                "            </TABLE>",
                "        >",
                "    ];",
                "}",
            ]
        )

        return "\n".join(lines)

    lines.extend(
        [
            "    token_table [",
            "        label=<",
            '            <TABLE BORDER="1" CELLBORDER="1" '
            'CELLSPACING="0" CELLPADDING="7">',
            "",
            '                <TR>',
            '                    <TD BGCOLOR="#DCE6F1"><B>#</B></TD>',
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Token Type</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Value</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Line</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Column</B></TD>'
            ),
            '                </TR>',
            "",
        ]
    )

    for index, token in enumerate(tokens, start=1):
        token_type, token_value, line, column = token

        safe_type = escape_html_text(token_type)
        safe_value = escape_html_text(token_value)
        safe_line = escape_html_text(line)
        safe_column = escape_html_text(column)

        lines.extend(
            [
                "                <TR>",
                f"                    <TD>{index}</TD>",
                f"                    <TD>{safe_type}</TD>",
                f"                    <TD>{safe_value}</TD>",
                f"                    <TD>{safe_line}</TD>",
                f"                    <TD>{safe_column}</TD>",
                "                </TR>",
            ]
        )

    lines.extend(
        [
            "",
            "            </TABLE>",
            "        >",
            "    ];",
            "}",
        ]
    )

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Symbol-table visualization
# ----------------------------------------------------------------------

def build_symbol_table_dot(symbol_table):
    """
    Build a proper horizontal symbol-table visualization.

    Each variable occupies one row instead of stacking every individual field
    vertically.
    """

    lines = [
        "digraph SymbolTable {",
        "    rankdir=TB;",
        "",
        "    graph [",
        '        label="MiniLang Symbol Table",',
        '        labelloc="t",',
        "        fontsize=18,",
        '        fontname="Arial",',
        "        pad=0.20,",
        "        margin=0.05",
        "    ];",
        "",
        "    node [",
        "        shape=plain,",
        '        fontname="Arial"',
        "    ];",
        "",
    ]

    if not symbol_table:
        lines.extend(
            [
                "    symbol_table [",
                "        label=<",
                '            <TABLE BORDER="1" CELLBORDER="1" '
                'CELLSPACING="0" CELLPADDING="8">',
                (
                    '                <TR><TD>'
                    'No variables declared</TD></TR>'
                ),
                "            </TABLE>",
                "        >",
                "    ];",
                "}",
            ]
        )

        return "\n".join(lines)

    lines.extend(
        [
            "    symbol_table [",
            "        label=<",
            '            <TABLE BORDER="1" CELLBORDER="1" '
            'CELLSPACING="0" CELLPADDING="8">',
            "",
            '                <TR>',
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Variable</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Type</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Declared Line</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Declared Column</B></TD>'
            ),
            (
                '                    <TD BGCOLOR="#DCE6F1">'
                '<B>Initialized</B></TD>'
            ),
            '                </TR>',
            "",
        ]
    )

    for variable_name, details in symbol_table.items():
        safe_variable = escape_html_text(variable_name)
        safe_type = escape_html_text(
            details.get("type", "Unknown")
        )
        safe_line = escape_html_text(
            details.get("declared_line", "-")
        )
        safe_column = escape_html_text(
            details.get("declared_column", "-")
        )

        initialized = details.get("initialized", True)
        initialized_text = "Yes" if initialized else "No"

        lines.extend(
            [
                "                <TR>",
                f"                    <TD>{safe_variable}</TD>",
                f"                    <TD>{safe_type}</TD>",
                f"                    <TD>{safe_line}</TD>",
                f"                    <TD>{safe_column}</TD>",
                (
                    "                    "
                    f"<TD>{initialized_text}</TD>"
                ),
                "                </TR>",
            ]
        )

    lines.extend(
        [
            "",
            "            </TABLE>",
            "        >",
            "    ];",
            "}",
        ]
    )

    return "\n".join(lines)


# ----------------------------------------------------------------------
# Streamlit renderer
# ----------------------------------------------------------------------

def display_visualizations(tokens=None, symbol_table=None):
    """
    Display all MiniLang visualizations in Streamlit.
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
        st.subheader("Token Stream")

        st.graphviz_chart(
            build_token_stream_dot(tokens),
            width="stretch",
        )

    if symbol_table is not None:
        st.subheader("Symbol Table")

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
    Export the default lexer and compiler-flow diagrams.
    """

    source_directory = Path(__file__).resolve().parent
    project_directory = source_directory.parent
    diagrams_directory = project_directory / "Diagrams"

    lexer_path = save_dot_file(
        build_lexer_dfa_dot(),
        diagrams_directory / "lexer_dfa.dot",
    )

    compiler_path = save_dot_file(
        build_compiler_flow_dot(),
        diagrams_directory / "compiler_flow.dot",
    )

    return [
        lexer_path,
        compiler_path,
    ]


# ----------------------------------------------------------------------
# Standalone test
# ----------------------------------------------------------------------

def main():
    """
    Generate responsive sample diagram files.
    """

    sample_tokens = [
        ("KEYWORD", "int", 1, 1),
        ("IDENTIFIER", "marks", 1, 5),
        ("OPERATOR", "=", 1, 11),
        ("NUMBER", "85", 1, 13),
        ("SEMICOLON", ";", 1, 15),
        ("KEYWORD", "if", 3, 1),
        ("IDENTIFIER", "marks", 3, 4),
        ("OPERATOR", ">", 3, 10),
        ("NUMBER", "50", 3, 12),
        ("LBRACE", "{", 3, 15),
        ("KEYWORD", "print", 4, 5),
        ("LPAREN", "(", 4, 10),
        ("IDENTIFIER", "marks", 4, 11),
        ("RPAREN", ")", 4, 16),
        ("SEMICOLON", ";", 4, 17),
        ("RBRACE", "}", 5, 1),
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

    source_directory = Path(__file__).resolve().parent
    project_directory = source_directory.parent
    diagrams_directory = project_directory / "Diagrams"

    token_path = save_dot_file(
        build_token_stream_dot(sample_tokens),
        diagrams_directory / "sample_token_stream.dot",
    )

    symbol_path = save_dot_file(
        build_symbol_table_dot(sample_symbol_table),
        diagrams_directory / "sample_symbol_table.dot",
    )

    generated_files.extend(
        [
            token_path,
            symbol_path,
        ]
    )

    print("MINILANG RESPONSIVE VISUALIZER")
    print("=" * 70)
    print("The following files were generated:")

    for file_path in generated_files:
        print(f"- {file_path}")


if __name__ == "__main__":
    main()