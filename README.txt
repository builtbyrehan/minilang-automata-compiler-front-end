MINILANG: AUTOMATA-BASED COMPILER FRONT-END
===========================================

Topic Code:
F2 - Automata in Compiler Design

Course:
Theory of Automata

Project Description:
MiniLang is a small compiler front-end built using concepts from Theory of Automata.
It performs lexical analysis using DFA-based token recognition and syntax analysis using
CFG-based parsing rules.

Main Features:
1. Recognizes MiniLang tokens such as keywords, identifiers, numbers, operators, and symbols.
2. Generates a token stream from source code.
3. Checks syntax using Context-Free Grammar rules.
4. Detects lexical and syntax errors.
5. Supports console-based execution.
6. Supports Streamlit GUI demonstration.
7. Includes valid and invalid test cases.

Supported MiniLang Syntax:

int x = 10;
x = x + 5;
print(x);

if x > 5 {
    print(x);
}

Project Structure:

TOA_Project_F2_Rehan/
│
├── README.txt
├── Source_Code/
│   ├── lexer.py
│   ├── parser.py
│   ├── main.py
│   ├── grammar.py
│   ├── error_handler.py
│   ├── test_runner.py
│   └── app.py
│
├── Test_Cases/
│   ├── valid_cases.txt
│   ├── invalid_cases.txt
│   └── test_results.txt
│
├── Documentation/
│   ├── formal_definitions.txt
│   ├── grammar_rules.txt
│   └── computation_traces.txt
│
└── Diagrams/

How to Run Console Version:

1. Open PowerShell in the main project folder.

2. Run:

python Source_Code\main.py

3. Choose option 1 to run sample code.
4. Choose option 2 to enter custom MiniLang code.


How to Run Test Cases:

1. Go to Source_Code folder:

cd Source_Code

2. Run:

python test_runner.py


How to Run Streamlit GUI:

1. Install Streamlit if not installed:

pip install streamlit

2. From the main project folder, run:

python -m streamlit run Source_Code\app.py

OR if already inside Source_Code folder, run:

python -m streamlit run app.py


Valid Test Example:

int marks = 85;
if marks > 50 {
    print(marks);
}

Expected Result:
Lexical Analysis: Passed
Syntax Analysis: Passed
Result: Valid MiniLang Code


Invalid Test Example:

int x = 10
print(x);

Expected Result:
Syntax Error: Expected ;, found 'print'
Result: Invalid MiniLang Code


Automata Concepts Used:

1. Deterministic Finite Automata:
Used for lexical analysis and token recognition.

2. Context-Free Grammar:
Used for syntax analysis and structure validation.

3. Compiler Front-End:
The project integrates lexical analysis, syntax analysis, and error reporting.


Future Improvements:

1. Add while loops.
2. Add support for multiple data types.
3. Add parse tree visualization.
4. Add symbol table.
5. Add intermediate code generation.
6. Add advanced error recovery.