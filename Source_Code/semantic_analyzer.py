# semantic_analyzer.py
# Semantic Analyzer and Symbol Table for MiniLang Compiler Front-End

class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.symbol_table = {}
        self.errors = []

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ("EOF", "EOF", -1, -1)

    def advance(self):
        self.position += 1

    def add_error(self, line, column, message):
        self.errors.append(
            f"Semantic Error at line {line}, column {column}: {message}"
        )

    def analyze(self):
        while self.current_token()[0] != "EOF":
            token_type, token_value, line, column = self.current_token()

            if token_type == "KEYWORD" and token_value == "int":
                self.analyze_declaration()

            elif token_type == "IDENTIFIER":
                self.analyze_assignment()

            elif token_type == "KEYWORD" and token_value == "print":
                self.analyze_print_statement()

            elif token_type == "KEYWORD" and token_value == "if":
                self.analyze_if_statement()

            else:
                self.advance()

        return self.symbol_table, self.errors

    def analyze_declaration(self):
        # Expected syntax already checked by parser:
        # int id = number ;

        self.advance()  # Skip int

        token_type, token_value, line, column = self.current_token()

        if token_type == "IDENTIFIER":
            variable_name = token_value

            if variable_name in self.symbol_table:
                self.add_error(
                    line,
                    column,
                    f"Variable '{variable_name}' is already declared."
                )
            else:
                self.symbol_table[variable_name] = {
                    "type": "int",
                    "declared_line": line,
                    "declared_column": column
                }

        # Move until semicolon
        while self.current_token()[0] not in ["SEMICOLON", "EOF"]:
            self.advance()

        if self.current_token()[0] == "SEMICOLON":
            self.advance()

    def analyze_assignment(self):
        # Expected syntax:
        # id = Expression ;

        token_type, token_value, line, column = self.current_token()

        variable_name = token_value

        if variable_name not in self.symbol_table:
            self.add_error(
                line,
                column,
                f"Variable '{variable_name}' used before declaration."
            )

        self.advance()

        # Check identifiers used inside expression
        while self.current_token()[0] not in ["SEMICOLON", "EOF"]:
            token_type, token_value, line, column = self.current_token()

            if token_type == "IDENTIFIER":
                if token_value not in self.symbol_table:
                    self.add_error(
                        line,
                        column,
                        f"Variable '{token_value}' used before declaration."
                    )

            self.advance()

        if self.current_token()[0] == "SEMICOLON":
            self.advance()

    def analyze_print_statement(self):
        # Expected syntax:
        # print ( id ) ;

        self.advance()  # Skip print

        while self.current_token()[0] not in ["SEMICOLON", "EOF"]:
            token_type, token_value, line, column = self.current_token()

            if token_type == "IDENTIFIER":
                if token_value not in self.symbol_table:
                    self.add_error(
                        line,
                        column,
                        f"Variable '{token_value}' used before declaration."
                    )

            self.advance()

        if self.current_token()[0] == "SEMICOLON":
            self.advance()

    def analyze_if_statement(self):
        # Expected syntax:
        # if id RelOp number { StatementList }

        self.advance()  # Skip if

        while self.current_token()[0] not in ["LBRACE", "EOF"]:
            token_type, token_value, line, column = self.current_token()

            if token_type == "IDENTIFIER":
                if token_value not in self.symbol_table:
                    self.add_error(
                        line,
                        column,
                        f"Variable '{token_value}' used before declaration."
                    )

            self.advance()

        if self.current_token()[0] == "LBRACE":
            self.advance()


def analyze_semantics(tokens):
    analyzer = SemanticAnalyzer(tokens)
    symbol_table, errors = analyzer.analyze()

    is_semantically_valid = len(errors) == 0

    return symbol_table, errors, is_semantically_valid


if __name__ == "__main__":
    from parser import parse_code

    sample_code = """
int x = 10;
x = x + 5;
print(x);
"""

    tokens, syntax_errors, syntax_valid = parse_code(sample_code)

    if syntax_valid:
        symbol_table, semantic_errors, semantic_valid = analyze_semantics(tokens)

        print("SYMBOL TABLE")
        print("=" * 50)
        for name, details in symbol_table.items():
            print(name, "→", details)

        print("\nSEMANTIC ERRORS")
        print("=" * 50)

        if semantic_valid:
            print("No semantic errors found.")
        else:
            for error in semantic_errors:
                print(error)
    else:
        print("Syntax errors found. Semantic analysis skipped.")