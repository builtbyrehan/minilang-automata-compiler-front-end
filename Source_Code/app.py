# app.py
# Streamlit GUI for the MiniLang Compiler Front-End.

import streamlit as st

from grammar import MINILANG_GRAMMAR
from parser import parse_code
from semantic_analyzer import analyze_semantics
from visualizer import (
    build_compiler_flow_dot,
    build_lexer_dfa_dot,
    build_symbol_table_dot,
    build_token_stream_dot,
)


# ----------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------

st.set_page_config(
    page_title="MiniLang Compiler Front-End",
    page_icon="⚙️",
    layout="wide",
)


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------

def classify_frontend_errors(errors):
    """
    Separate lexical errors from syntax errors.

    Args:
        errors: Error messages returned by parse_code().

    Returns:
        Tuple containing lexical, syntax, and unclassified errors.
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


def build_token_rows(tokens):
    """Convert tokens into rows for a Streamlit dataframe."""

    token_rows = []

    for index, token in enumerate(tokens, start=1):
        token_type, token_value, line, column = token

        token_rows.append(
            {
                "#": index,
                "Token Type": token_type,
                "Value": token_value,
                "Line": line,
                "Column": column,
            }
        )

    return token_rows


def build_symbol_rows(symbol_table):
    """Convert the symbol table into Streamlit dataframe rows."""

    symbol_rows = []

    for variable_name, details in symbol_table.items():
        initialized = details.get("initialized", True)

        symbol_rows.append(
            {
                "Variable": variable_name,
                "Type": details.get("type", "Unknown"),
                "Declared Line": details.get("declared_line", "-"),
                "Declared Column": details.get(
                    "declared_column",
                    "-",
                ),
                "Initialized": "Yes" if initialized else "No",
            }
        )

    return symbol_rows


def display_error_messages(errors):
    """Display compiler errors using Streamlit error boxes."""

    for error in errors:
        st.error(error)


# ----------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------

if "compiler_tokens" not in st.session_state:
    st.session_state.compiler_tokens = []

if "compiler_symbol_table" not in st.session_state:
    st.session_state.compiler_symbol_table = {}

if "compiler_has_run" not in st.session_state:
    st.session_state.compiler_has_run = False


# ----------------------------------------------------------------------
# Application heading
# ----------------------------------------------------------------------

st.title("MiniLang: Automata-Based Compiler Front-End")

st.write(
    "This project demonstrates DFA-based lexical analysis, "
    "CFG-based syntax analysis, and semantic analysis using a symbol table."
)

st.divider()


# ----------------------------------------------------------------------
# Default program
# ----------------------------------------------------------------------

SAMPLE_CODE = """int marks = 85;

if marks > 50 {
    print(marks);
}
"""


# ----------------------------------------------------------------------
# Application tabs
# ----------------------------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Code Editor",
        "Grammar Rules",
        "Supported Syntax",
        "Project Flow",
        "Visualizations",
    ]
)


# ======================================================================
# Tab 1: Code editor
# ======================================================================

with tab1:
    st.subheader("MiniLang Code Editor")

    code = st.text_area(
        label="Write your MiniLang program here:",
        value=SAMPLE_CODE,
        height=250,
        key="minilang_source_code",
    )

    run_compiler = st.button(
        "Run Compiler",
        type="primary",
        width="content",
    )

    if run_compiler:
        # --------------------------------------------------------------
        # Lexical and syntax analysis
        # --------------------------------------------------------------

        tokens, frontend_errors, syntax_valid = parse_code(code)

        (
            lexical_errors,
            syntax_errors,
            other_errors,
        ) = classify_frontend_errors(frontend_errors)

        lexical_valid = len(lexical_errors) == 0

        # --------------------------------------------------------------
        # Semantic analysis
        # --------------------------------------------------------------

        symbol_table = {}
        semantic_errors = []
        semantic_valid = False

        if syntax_valid:
            (
                symbol_table,
                semantic_errors,
                semantic_valid,
            ) = analyze_semantics(tokens)

        # Store results for the visualization tab.
        st.session_state.compiler_tokens = tokens
        st.session_state.compiler_symbol_table = symbol_table
        st.session_state.compiler_has_run = True

        # --------------------------------------------------------------
        # Token stream
        # --------------------------------------------------------------

        st.divider()
        st.subheader("1. Token Stream")

        if tokens:
            token_rows = build_token_rows(tokens)

            st.dataframe(
                token_rows,
                width="stretch",
                hide_index=True,
            )

        else:
            st.warning(
                "No tokens were generated from the source code."
            )

        # --------------------------------------------------------------
        # Lexical analysis report
        # --------------------------------------------------------------

        st.subheader("2. Lexical Analysis Report")

        if lexical_errors:
            display_error_messages(lexical_errors)

        else:
            st.success(
                "Lexical analysis passed. "
                "No lexical errors found."
            )

        # --------------------------------------------------------------
        # Syntax analysis report
        # --------------------------------------------------------------

        st.subheader("3. Syntax Analysis Report")

        if lexical_errors:
            st.warning(
                "Syntax analysis was skipped because "
                "lexical analysis failed."
            )

        elif syntax_errors:
            display_error_messages(syntax_errors)

        elif other_errors:
            display_error_messages(other_errors)

        else:
            st.success(
                "Syntax analysis passed. "
                "No syntax errors found."
            )

        # --------------------------------------------------------------
        # Symbol table
        # --------------------------------------------------------------

        st.subheader("4. Symbol Table")

        if not syntax_valid:
            st.info(
                "The symbol table was not generated because "
                "lexical or syntax analysis failed."
            )

        elif symbol_table:
            symbol_rows = build_symbol_rows(symbol_table)

            st.dataframe(
                symbol_rows,
                width="stretch",
                hide_index=True,
            )

        else:
            st.info(
                "No variables are stored in the symbol table."
            )

        # --------------------------------------------------------------
        # Semantic analysis report
        # --------------------------------------------------------------

        st.subheader("5. Semantic Analysis Report")

        if not syntax_valid:
            st.warning(
                "Semantic analysis was skipped because "
                "lexical or syntax analysis failed."
            )

        elif semantic_errors:
            display_error_messages(semantic_errors)

        else:
            st.success(
                "Semantic analysis passed. "
                "No semantic errors found."
            )

        # --------------------------------------------------------------
        # Final compilation result
        # --------------------------------------------------------------

        st.subheader("6. Final Compilation Result")

        if lexical_valid and syntax_valid and semantic_valid:
            st.success(
                "Compilation Successful: Valid MiniLang Code"
            )

        else:
            st.error(
                "Compilation Failed: Invalid MiniLang Code"
            )

        status_columns = st.columns(3)

        with status_columns[0]:
            if lexical_valid:
                st.success("Lexical Analysis: Passed")
            else:
                st.error("Lexical Analysis: Failed")

        with status_columns[1]:
            if not lexical_valid:
                st.warning("Syntax Analysis: Skipped")

            elif syntax_valid:
                st.success("Syntax Analysis: Passed")

            else:
                st.error("Syntax Analysis: Failed")

        with status_columns[2]:
            if not syntax_valid:
                st.warning("Semantic Analysis: Skipped")

            elif semantic_valid:
                st.success("Semantic Analysis: Passed")

            else:
                st.error("Semantic Analysis: Failed")


# ======================================================================
# Tab 2: Grammar rules
# ======================================================================

with tab2:
    st.subheader("MiniLang Context-Free Grammar")

    st.write(
        "The following context-free grammar defines the supported "
        "MiniLang program structures."
    )

    for non_terminal, productions in MINILANG_GRAMMAR.items():
        production_text = " | ".join(productions)

        st.code(
            f"{non_terminal} → {production_text}",
            language=None,
        )


# ======================================================================
# Tab 3: Supported syntax
# ======================================================================

with tab3:
    st.subheader("Supported MiniLang Syntax")

    st.write("A complete valid MiniLang program is shown below:")

    st.code(
        """int x = 10;
x = x + 5;
print(x);

if x > 5 {
    print(x);
}
""",
        language="c",
    )

    st.subheader("Supported Statements")

    st.markdown(
        """
- **Declaration:** `int x = 10;`
- **Assignment:** `x = x + 5;`
- **Print statement:** `print(x);`
- **If statement:** `if x > 5 { print(x); }`
- **Arithmetic operators:** `+`, `-`, `*`, `/`
- **Relational operators:** `>`, `<`
"""
    )

    st.subheader("Semantic Rules")

    st.markdown(
        """
1. A variable must be declared before it is used.
2. A variable cannot be declared more than once.
3. Assignment is only valid for declared variables.
4. A print statement can only print a declared variable.
5. An if-condition must use a declared variable.
6. Every MiniLang variable has the `int` data type.
"""
    )

    st.subheader("Invalid Examples")

    st.code(
        """int 3marks = 4;
x = 10;
print(result);
int marks = 85
""",
        language="c",
    )


# ======================================================================
# Tab 4: Project flow
# ======================================================================

with tab4:
    st.subheader("Compiler Front-End Flow")

    st.code(
        """MiniLang Source Code
          │
          ▼
Lexical Analyzer
DFA-like token recognition
          │
          ▼
Token Stream
          │
          ▼
Syntax Analyzer
Recursive-descent parsing using CFG
          │
          ▼
Semantic Analyzer
Symbol-table validation
          │
          ▼
Final Compilation Result
Valid Code / Invalid Code
""",
        language=None,
    )

    st.subheader("Compiler Components")

    component_columns = st.columns(3)

    with component_columns[0]:
        st.markdown("### Lexical Analyzer")

        st.write(
            "Reads source-code characters and converts them into "
            "keywords, identifiers, numbers, operators, and symbols."
        )

    with component_columns[1]:
        st.markdown("### Syntax Analyzer")

        st.write(
            "Checks whether the token sequence follows the "
            "MiniLang context-free grammar."
        )

    with component_columns[2]:
        st.markdown("### Semantic Analyzer")

        st.write(
            "Builds the symbol table and verifies variable "
            "declaration and usage rules."
        )


# ======================================================================
# Tab 5: Visualizations
# ======================================================================

with tab5:
    st.subheader("MiniLang Compiler Visualizations")

    visualization_tabs = st.tabs(
        [
            "Lexer DFA",
            "Compiler Flow",
            "Token Stream",
            "Symbol Table",
        ]
    )

    with visualization_tabs[0]:
        st.write(
            "This diagram represents the DFA-like states used "
            "by the lexical analyzer."
        )

        st.graphviz_chart(
            build_lexer_dfa_dot(),
            width="stretch",
        )

    with visualization_tabs[1]:
        st.write(
            "This diagram shows the complete compiler "
            "front-end processing flow."
        )

        st.graphviz_chart(
            build_compiler_flow_dot(),
            width="stretch",
        )

    with visualization_tabs[2]:
        if st.session_state.compiler_has_run:
            st.graphviz_chart(
                build_token_stream_dot(
                    st.session_state.compiler_tokens
                ),
                width="stretch",
            )

        else:
            st.info(
                "Run the compiler first to generate a token-stream "
                "visualization."
            )

    with visualization_tabs[3]:
        if st.session_state.compiler_has_run:
            st.graphviz_chart(
                build_symbol_table_dot(
                    st.session_state.compiler_symbol_table
                ),
                width="stretch",
            )

        else:
            st.info(
                "Run the compiler first to generate a symbol-table "
                "visualization."
            )


# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------

st.divider()

st.caption(
    "MiniLang Compiler Front-End — Theory of Automata Project"
)