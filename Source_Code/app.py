# app.py
# Streamlit GUI for the MiniLang Compiler Front-End.

import streamlit as st

from grammar import MINILANG_GRAMMAR
from parser import parse_code
from semantic_analyzer import analyze_semantics


# ----------------------------------------------------------------------
# Streamlit page configuration
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

    The lexer and parser currently return formatted error strings.

    Args:
        errors: List of lexical or syntax error messages.

    Returns:
        tuple:
            lexical_errors: Errors produced by lexical analysis.
            syntax_errors: Errors produced by syntax analysis.
            other_errors: Errors that could not be classified.
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
    """
    Convert compiler tokens into rows suitable for Streamlit tables.
    """

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
    """
    Convert symbol-table entries into rows suitable for Streamlit tables.
    """

    symbol_rows = []

    for variable_name, details in symbol_table.items():
        initialized = details.get("initialized", True)

        symbol_rows.append(
            {
                "Variable": variable_name,
                "Type": details.get("type", "Unknown"),
                "Declared Line": details.get("declared_line", "-"),
                "Declared Column": details.get("declared_column", "-"),
                "Initialized": "Yes" if initialized else "No",
            }
        )

    return symbol_rows


def display_error_messages(errors):
    """Display a list of compiler errors in Streamlit."""

    for error in errors:
        st.error(error)


# ----------------------------------------------------------------------
# Main heading and introduction
# ----------------------------------------------------------------------

st.title("MiniLang: Automata-Based Compiler Front-End")

st.write(
    "This project demonstrates DFA-based lexical analysis, "
    "CFG-based syntax analysis, and semantic analysis using a symbol table."
)

st.divider()


# ----------------------------------------------------------------------
# Default MiniLang program
# ----------------------------------------------------------------------

SAMPLE_CODE = """int marks = 85;

if marks > 50 {
    print(marks);
}
"""


# ----------------------------------------------------------------------
# Application tabs
# ----------------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Code Editor",
        "Grammar Rules",
        "Supported Syntax",
        "Project Flow",
    ]
)


# ======================================================================
# Tab 1: Code editor and compiler output
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
        use_container_width=False,
    )

    if run_compiler:
        # --------------------------------------------------------------
        # Lexical and syntax analysis
        # --------------------------------------------------------------

        tokens, frontend_errors, syntax_valid = parse_code(code)

        lexical_errors, syntax_errors, unclassified_errors = (
            classify_frontend_errors(frontend_errors)
        )

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

        # --------------------------------------------------------------
        # Token stream
        # --------------------------------------------------------------

        st.divider()
        st.subheader("1. Token Stream")

        if tokens:
            token_rows = build_token_rows(tokens)

            st.dataframe(
                token_rows,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning("No tokens were generated from the source code.")

        # --------------------------------------------------------------
        # Lexical analysis report
        # --------------------------------------------------------------

        st.subheader("2. Lexical Analysis Report")

        if lexical_errors:
            display_error_messages(lexical_errors)
        else:
            st.success("Lexical analysis passed. No lexical errors found.")

        # --------------------------------------------------------------
        # Syntax analysis report
        # --------------------------------------------------------------

        st.subheader("3. Syntax Analysis Report")

        if lexical_errors:
            st.warning(
                "Syntax analysis was skipped because lexical analysis failed."
            )

        elif syntax_errors:
            display_error_messages(syntax_errors)

        elif unclassified_errors:
            display_error_messages(unclassified_errors)

        else:
            st.success("Syntax analysis passed. No syntax errors found.")

        # --------------------------------------------------------------
        # Symbol table
        # --------------------------------------------------------------

        st.subheader("4. Symbol Table")

        if not syntax_valid:
            st.info(
                "The symbol table was not generated because syntax "
                "analysis did not pass."
            )

        elif symbol_table:
            symbol_rows = build_symbol_rows(symbol_table)

            st.dataframe(
                symbol_rows,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No variables are stored in the symbol table.")

        # --------------------------------------------------------------
        # Semantic analysis report
        # --------------------------------------------------------------

        st.subheader("5. Semantic Analysis Report")

        if not syntax_valid:
            st.warning(
                "Semantic analysis was skipped because lexical or syntax "
                "analysis failed."
            )

        elif semantic_errors:
            display_error_messages(semantic_errors)

        else:
            st.success(
                "Semantic analysis passed. No semantic errors found."
            )

        # --------------------------------------------------------------
        # Final compiler result
        # --------------------------------------------------------------

        st.subheader("6. Final Compilation Result")

        if lexical_valid and syntax_valid and semantic_valid:
            st.success("Compilation Successful: Valid MiniLang Code")

            status_columns = st.columns(3)

            with status_columns[0]:
                st.success("Lexical Analysis: Passed")

            with status_columns[1]:
                st.success("Syntax Analysis: Passed")

            with status_columns[2]:
                st.success("Semantic Analysis: Passed")

        else:
            st.error("Compilation Failed: Invalid MiniLang Code")

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
        "The following context-free grammar defines all supported "
        "MiniLang program structures."
    )

    for non_terminal, productions in MINILANG_GRAMMAR.items():
        production_text = " | ".join(productions)

        st.code(
            f"{non_terminal} → {production_text}",
            language=None,
        )


# ======================================================================
# Tab 3: Supported syntax and semantic rules
# ======================================================================

with tab3:
    st.subheader("Supported MiniLang Syntax")

    st.write("A complete valid MiniLang example is shown below:")

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
6. Every variable in MiniLang has the `int` data type.
"""
    )

    st.subheader("Invalid Examples")

    st.code(
        """int 3 = 4;        // Invalid variable name
x = 10;           // Variable x was not declared
print(result);    // Variable result was not declared
int x = 5         // Missing semicolon
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
Recursive-descent parsing using CFG rules
          │
          ▼
Semantic Analyzer
Symbol-table and declaration validation
          │
          ▼
Final Compilation Result
Valid MiniLang Code / Invalid MiniLang Code
""",
        language=None,
    )

    st.subheader("Compiler Components")

    component_columns = st.columns(3)

    with component_columns[0]:
        st.markdown("### Lexical Analyzer")
        st.write(
            "Reads source-code characters and converts them into tokens "
            "such as keywords, identifiers, numbers, operators, and symbols."
        )

    with component_columns[1]:
        st.markdown("### Syntax Analyzer")
        st.write(
            "Checks whether the token sequence follows the MiniLang "
            "context-free grammar."
        )

    with component_columns[2]:
        st.markdown("### Semantic Analyzer")
        st.write(
            "Builds the symbol table and checks variable declaration and "
            "usage rules."
        )


# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------



st.divider()

st.caption(
    "MiniLang Compiler Front-End — Theory of Automata Project"
)