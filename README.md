# MiniLang: Automata-Based Compiler Front-End

## Overview

**MiniLang** is a Theory of Automata project based on the topic **F2: Automata in Compiler Design**.
The project implements a mini compiler front-end for a small programming language using core automata concepts.

The system performs:

* Lexical Analysis using DFA-based token recognition
* Syntax Analysis using CFG-based parsing
* Semantic Analysis using a Symbol Table
* Error Detection and Reporting
* Console-based execution
* Streamlit-based GUI demonstration

This project connects theoretical automata concepts with a practical compiler design application.

---

## Project Title

**MiniLang: Automata-Based Compiler Front-End**

---

## Course Information

| Field         | Details                     |
| ------------- | --------------------------- |
| Course        | Theory of Automata          |
| Topic Code    | F2                          |
| Topic Name    | Automata in Compiler Design |
| Project Type  | Mini Compiler Front-End     |
| Language Used | Python                      |
| GUI Framework | Streamlit                   |

---

## Main Objective

The main objective of this project is to design and implement a small compiler front-end that demonstrates how automata theory is used in real compiler design.

The compiler front-end reads MiniLang source code, breaks it into tokens, checks whether the syntax is valid according to grammar rules, performs semantic validation using a symbol table, and reports errors if the code is invalid.

---

## Why This Project Matters

This project is important because it shows the practical use of Theory of Automata in compiler construction.

It demonstrates the connection between:

* Regular Languages
* Deterministic Finite Automata
* Context-Free Grammars
* Lexical Analysis
* Syntax Analysis
* Semantic Analysis
* Compiler Front-End Design

Instead of only explaining automata theory theoretically, this project applies it to a working mini-language compiler.

---

## Supported MiniLang Syntax

MiniLang currently supports:

```c
int x = 10;
x = x + 5;
print(x);

if x > 5 {
    print(x);
}
```

---

## Features

### 1. Lexical Analysis

The lexical analyzer scans the source code character by character and generates tokens.

Supported token types:

| Token Type | Examples                          |
| ---------- | --------------------------------- |
| Keyword    | `int`, `if`, `print`              |
| Identifier | `x`, `marks`, `total`             |
| Number     | `10`, `85`, `100`                 |
| Operator   | `=`, `+`, `-`, `*`, `/`, `>`, `<` |
| Symbols    | `;`, `(`, `)`, `{`, `}`           |

---

### 2. Syntax Analysis

The parser checks whether the generated token stream follows MiniLang grammar rules.

Example valid statement:

```c
int marks = 85;
```

Example invalid statement:

```c
int marks = 85
```

Error:

```text
Syntax Error: Expected ;, found 'print'
```

---

### 3. Semantic Analysis

The semantic analyzer checks meaning-related rules using a symbol table.

Semantic rules:

1. A variable must be declared before use.
2. A variable cannot be declared more than once.
3. Assignment is only valid for declared variables.
4. Print statement can only print declared variables.
5. If condition must use a declared variable.

Example invalid semantic code:

```c
print(y);
```

Error:

```text
Semantic Error: Variable 'y' used before declaration.
```

---

### 4. Symbol Table

The symbol table stores declared variables with their type and location.

Example:

| Variable | Type | Line | Column |
| -------- | ---- | ---- | ------ |
| x        | int  | 1    | 5      |
| marks    | int  | 1    | 5      |

---

### 5. Streamlit GUI

The project includes a Streamlit interface for live demonstration.

The GUI shows:

* Code editor
* Token stream
* Syntax errors
* Symbol table
* Semantic errors
* Final compiler result
* Grammar rules
* Supported syntax
* Project flow

---

## Compiler Flow

```text
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
```

---

## Automata Concepts Used

### Deterministic Finite Automata

DFA is used for lexical analysis.

The lexical analyzer recognizes:

* Keywords
* Identifiers
* Numbers
* Operators
* Separators

Formal DFA form:

```text
DFA = (Q, Σ, δ, q0, F)
```

Where:

| Symbol | Meaning                 |
| ------ | ----------------------- |
| Q      | Finite set of states    |
| Σ      | Input alphabet          |
| δ      | Transition function     |
| q0     | Initial state           |
| F      | Set of accepting states |

---

### Context-Free Grammar

CFG is used for syntax analysis.

Formal CFG form:

```text
CFG = (V, Σ, P, S)
```

Where:

| Symbol | Meaning                 |
| ------ | ----------------------- |
| V      | Set of non-terminals    |
| Σ      | Set of terminals        |
| P      | Set of production rules |
| S      | Start symbol            |

---

## MiniLang Grammar

```text
Program → StatementList

StatementList → Statement StatementList | ε

Statement → Declaration
          | Assignment
          | PrintStatement
          | IfStatement

Declaration → int id = number ;

Assignment → id = Expression ;

PrintStatement → print ( id ) ;

IfStatement → if Condition { StatementList }

Condition → id RelOp number

Expression → id
           | number
           | id ArithOp number
           | number ArithOp number
           | id ArithOp id
           | number ArithOp id

RelOp → > | <

ArithOp → + | - | * | /
```

---

## Project Structure

```text
TOA_Project_F2_Rehan/
│
├── README.md
├── README.txt
├── requirements.txt
│
├── Source_Code/
│   ├── lexer.py
│   ├── parser.py
│   ├── semantic_analyzer.py
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
```

---

## Installation

Clone or download the project folder.

Open PowerShell or terminal in the main project directory:

```powershell
cd TOA_Project_F2_Rehan
```

Install required packages:

```powershell
pip install -r requirements.txt
```

---

## How to Run Console Version

From the main project folder, run:

```powershell
python Source_Code\main.py
```

You will see:

```text
MINILANG COMPILER FRONT-END
1. Run sample code
2. Enter custom MiniLang code
```

Choose option `1` to run sample code.

Choose option `2` to enter your own MiniLang code.

When entering custom code, type `END` on a new line to finish input.

Example:

```c
int x = 10;
x = x + 5;
print(x);
END
```

---

## How to Run Streamlit GUI

From the main project folder, run:

```powershell
python -m streamlit run Source_Code\app.py
```

If you are already inside the `Source_Code` folder, run:

```powershell
python -m streamlit run app.py
```

---

## How to Run Test Cases

Go to the `Source_Code` folder:

```powershell
cd Source_Code
```

Run:

```powershell
python test_runner.py
```

Then return to the main folder:

```powershell
cd ..
```

The test results will be saved in:

```text
Test_Cases/test_results.txt
```

---

## Valid Test Cases

### Valid Case 1

```c
int x = 10;
print(x);
```

Expected result:

```text
Lexical Analysis: Passed
Syntax Analysis: Passed
Semantic Analysis: Passed
Result: Valid MiniLang Code
```

---

### Valid Case 2

```c
int marks = 85;
if marks > 50 {
    print(marks);
}
```

Expected result:

```text
Lexical Analysis: Passed
Syntax Analysis: Passed
Semantic Analysis: Passed
Result: Valid MiniLang Code
```

---

### Valid Case 3

```c
int x = 10;
x = x + 5;
print(x);
```

Expected result:

```text
Lexical Analysis: Passed
Syntax Analysis: Passed
Semantic Analysis: Passed
Result: Valid MiniLang Code
```

---

## Invalid Test Cases

### Invalid Case 1: Missing Semicolon

```c
int x = 10
print(x);
```

Expected error:

```text
Syntax Error: Expected ;, found 'print'
```

---

### Invalid Case 2: Invalid Identifier

```c
int 123 = 10;
```

Expected error:

```text
Syntax Error: Expected IDENTIFIER, found '123'
```

---

### Invalid Case 3: Incorrect Print Syntax

```c
print x;
```

Expected error:

```text
Syntax Error: Expected (, found 'x'
```

---

### Invalid Case 4: Missing Braces in If Statement

```c
if x > 5
    print(x);
```

Expected error:

```text
Syntax Error: Expected {, found 'print'
```

---

### Invalid Case 5: Variable Used Before Declaration

```c
print(y);
```

Expected error:

```text
Semantic Error: Variable 'y' used before declaration.
```

---

### Invalid Case 6: Assignment Before Declaration

```c
x = 10;
```

Expected error:

```text
Semantic Error: Variable 'x' used before declaration.
```

---

### Invalid Case 7: Duplicate Declaration

```c
int x = 10;
int x = 20;
```

Expected error:

```text
Semantic Error: Variable 'x' is already declared.
```

---

## Sample Output

```text
MINILANG COMPILER FRONT-END
======================================================================

TOKEN STREAM
----------------------------------------------------------------------
Token Type         Value              Line       Column
----------------------------------------------------------------------
KEYWORD            int                1          1
IDENTIFIER         x                  1          5
OPERATOR           =                  1          7
NUMBER             10                 1          9
SEMICOLON          ;                  1          11
KEYWORD            print              2          1
LPAREN             (                  2          6
IDENTIFIER         x                  2          7
RPAREN             )                  2          8
SEMICOLON          ;                  2          9

SYMBOL TABLE
----------------------------------------------------------------------
Variable           Type         Line       Column
----------------------------------------------------------------------
x                  int          1          5

FINAL RESULT
----------------------------------------------------------------------
Lexical Analysis: Passed
Syntax Analysis: Passed
Semantic Analysis: Passed
Result: Valid MiniLang Code
```

---

## Source Code Files

| File                   | Purpose                                             |
| ---------------------- | --------------------------------------------------- |
| `lexer.py`             | Performs lexical analysis and generates tokens      |
| `parser.py`            | Performs syntax analysis using grammar rules        |
| `semantic_analyzer.py` | Performs semantic analysis and manages symbol table |
| `grammar.py`           | Stores MiniLang CFG production rules                |
| `error_handler.py`     | Provides structured error formatting                |
| `main.py`              | Runs the console-based compiler front-end           |
| `test_runner.py`       | Runs valid and invalid test cases                   |
| `app.py`               | Runs the Streamlit GUI                              |

---

## Current Limitations

The current version of MiniLang is intentionally small and focused.

Limitations:

1. Supports only integer declarations.
2. Does not support floating-point numbers.
3. Does not support strings.
4. Does not support functions.
5. Does not support arrays.
6. Does not generate machine code.
7. Does not include advanced compiler optimization.
8. Parse tree visualization is not yet fully implemented.

---

## Future Improvements

Possible future improvements:

1. Add `while` loop support.
2. Add `else` block support.
3. Add string and float data types.
4. Add parse tree visualization.
5. Add intermediate code generation.
6. Add symbol table scope handling.
7. Add nested block scope validation.
8. Add better error recovery.
9. Add support for comments.
10. Add GitHub Actions for automated tests.

---

## Academic Relevance

This project is directly connected to Theory of Automata because it demonstrates how formal language concepts are applied in compiler design.

The lexical analyzer uses the idea of finite automata to recognize valid tokens.
The syntax analyzer uses context-free grammar rules to validate program structure.
The semantic analyzer adds compiler-level validation using a symbol table.

This makes the project a practical implementation of automata theory concepts.

---

## Project Description

An automata-based MiniLang compiler front-end built in Python. It includes DFA-based lexical analysis, CFG-based syntax analysis, semantic validation using a symbol table, error reporting, test cases, and a Streamlit GUI demo.

---

## Author

**Muhammad Rehan**

---

## License

This project is developed for academic learning and demonstration purposes.
