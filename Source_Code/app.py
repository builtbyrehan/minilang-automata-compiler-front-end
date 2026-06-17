# app.py
# Streamlit GUI for MiniLang Compiler Front-End

import streamlit as st
from parser import parse_code
from grammar import MINILANG_GRAMMAR
from semantic_analyzer import analyze_semantics


st.set_page_config(
    page_title="MiniLang Compiler Front-End",
    page_icon="⚙️",
    layout="wide"
)


st.title("MiniLang: Automata-Based Compiler Front-End")

st.write(
    "This project demonstrates DFA-based lexical analysis, "
    "CFG-based syntax analysis, and semantic analysis using a symbol table."
)


sample_code = """int marks = 85;
if marks > 50 {
    print(marks);
}
"""


tab1, tab2, tab3, tab4 = st.tabs(
    ["Code Editor", "Grammar Rules", "Supported Syntax", "Project Flow"]
)


with tab1:
    st.subheader("MiniLang Code Editor")

    code = st.text_area(
        "Write your MiniLang program here:",
        value=sample_code,
        height=230
    )

    if st.button("Run Compiler"):
        tokens, syntax_errors, syntax_valid = parse_code(code)

        symbol_table = {}
        semantic_errors = []
        semantic_valid = False

        if syntax_valid:
            symbol_table, semantic_errors, semantic_valid = analyze_semantics(tokens)

        st.subheader("Token Stream")

        if tokens:
            token_data = []

            for token_type, token_value, line, column in tokens:
                token_data.append(
                    {
                        "Token Type": token_type,
                        "Value": token_value,
                        "Line": line,
                        "Column": column
                    }
                )

            st.table(token_data)
        else:
            st.warning("No tokens generated.")

        st.subheader("Lexical / Syntax Error Report")

        if syntax_errors:
            for error in syntax_errors:
                st.error(error)
        else:
            st.success("No lexical or syntax errors found.")

        st.subheader("Symbol Table")

        if symbol_table:
            symbol_rows = []

            for variable, details in symbol_table.items():
                symbol_rows.append(
                    {
                        "Variable": variable,
                        "Type": details["type"],
                        "Declared Line": details["declared_line"],
                        "Declared Column": details["declared_column"]
                    }
                )

            st.table(symbol_rows)
        else:
            st.info("No variables stored in symbol table.")

        st.subheader("Semantic Error Report")

        if not syntax_valid:
            st.warning("Semantic analysis skipped because syntax analysis failed.")
        elif semantic_errors:
            for error in semantic_errors:
                st.error(error)
        else:
            st.success("No semantic errors found.")

        st.subheader("Final Result")

        if syntax_valid and semantic_valid:
            st.success("Lexical Analysis: Passed")
            st.success("Syntax Analysis: Passed")
            st.success("Semantic Analysis: Passed")
            st.success("Result: Valid MiniLang Code")
        else:
            st.error("Compilation Failed")
            st.error("Result: Invalid MiniLang Code")


with tab2:
    st.subheader("MiniLang Context-Free Grammar")

    for non_terminal, productions in MINILANG_GRAMMAR.items():
        production_text = " | ".join(productions)
        st.code(f"{non_terminal} → {production_text}")


with tab3:
    st.subheader("Supported MiniLang Syntax")

    st.code(
        """
int x = 10;
x = x + 5;
print(x);

if x > 5 {
    print(x);
}
""",
        language="c"
    )

    st.subheader("Semantic Rules")

    st.write("MiniLang now checks the following semantic rules:")

    st.markdown(
        """
1. A variable must be declared before use.
2. A variable cannot be declared more than once.
3. Assignment is only valid for declared variables.
4. Print statement can only print declared variables.
5. If condition must use a declared variable.
"""
    )


with tab4:
    st.subheader("Compiler Front-End Flow")

    st.code(
        """
Source Code
    ↓
Lexical Analyzer
DFA-based token recognition
    ↓
Token Stream
    ↓
Syntax Analyzer
CFG-based parsing
    ↓
Semantic Analyzer
Symbol table validation
    ↓
Final Result
Valid Code / Invalid Code
"""
    )