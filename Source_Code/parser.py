# parser.py
# MiniLang Syntax Analyzer
# This file checks whether the token stream follows MiniLang grammar rules.

from lexer import tokenize


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ("EOF", "EOF", -1, -1)

    def advance(self):
        self.position += 1

    def match(self, expected_type, expected_value=None):
        token_type, token_value, line, column = self.current_token()

        if token_type == expected_type:
            if expected_value is None or token_value == expected_value:
                self.advance()
                return True

        if expected_value:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: Expected {expected_value}, found '{token_value}'"
            )
        else:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: Expected {expected_type}, found '{token_value}'"
            )

        return False

    def parse_program(self):
        while self.current_token()[0] != "EOF":
            if not self.parse_statement():
                self.synchronize()

        return len(self.errors) == 0

    def parse_statement(self):
        token_type, token_value, line, column = self.current_token()

        if token_type == "KEYWORD" and token_value == "int":
            return self.parse_declaration()

        elif token_type == "IDENTIFIER":
            return self.parse_assignment()

        elif token_type == "KEYWORD" and token_value == "print":
            return self.parse_print_statement()

        elif token_type == "KEYWORD" and token_value == "if":
            return self.parse_if_statement()

        else:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: Invalid statement starting with '{token_value}'"
            )
            return False

    def parse_declaration(self):
        # Grammar: Declaration → int id = number ;
        if not self.match("KEYWORD", "int"):
            return False

        if not self.match("IDENTIFIER"):
            return False

        if not self.match("OPERATOR", "="):
            return False

        if not self.match("NUMBER"):
            return False

        if not self.match("SEMICOLON", ";"):
            return False

        return True

    def parse_assignment(self):
        # Grammar: Assignment → id = Expression ;
        if not self.match("IDENTIFIER"):
            return False

        if not self.match("OPERATOR", "="):
            return False

        if not self.parse_expression():
            return False

        if not self.match("SEMICOLON", ";"):
            return False

        return True

    def parse_print_statement(self):
        # Grammar: PrintStatement → print ( id ) ;
        if not self.match("KEYWORD", "print"):
            return False

        if not self.match("LPAREN", "("):
            return False

        if not self.match("IDENTIFIER"):
            return False

        if not self.match("RPAREN", ")"):
            return False

        if not self.match("SEMICOLON", ";"):
            return False

        return True

    def parse_if_statement(self):
        # Grammar: IfStatement → if Condition { StatementList }
        if not self.match("KEYWORD", "if"):
            return False

        if not self.parse_condition():
            return False

        if not self.match("LBRACE", "{"):
            return False

        while self.current_token()[0] != "RBRACE" and self.current_token()[0] != "EOF":
            if not self.parse_statement():
                self.synchronize()

        if not self.match("RBRACE", "}"):
            return False

        return True

    def parse_condition(self):
        # Grammar: Condition → id RelOp number
        if not self.match("IDENTIFIER"):
            return False

        token_type, token_value, line, column = self.current_token()

        if token_type == "OPERATOR" and token_value in [">", "<"]:
            self.advance()
        else:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: Expected relational operator '>' or '<'"
            )
            return False

        if not self.match("NUMBER"):
            return False

        return True

    def parse_expression(self):
        # Grammar: Expression → id | number | id Op number | number Op number
        token_type, token_value, line, column = self.current_token()

        if token_type not in ["IDENTIFIER", "NUMBER"]:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: Expected identifier or number in expression"
            )
            return False

        self.advance()

        token_type, token_value, line, column = self.current_token()

        if token_type == "OPERATOR" and token_value in ["+", "-", "*", "/"]:
            self.advance()

            token_type, token_value, line, column = self.current_token()

            if token_type not in ["IDENTIFIER", "NUMBER"]:
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: Expected identifier or number after operator"
                )
                return False

            self.advance()

        return True

    def synchronize(self):
        # Simple error recovery:
        # Skip tokens until semicolon or closing brace is found.
        while self.current_token()[0] not in ["SEMICOLON", "RBRACE", "EOF"]:
            self.advance()

        if self.current_token()[0] == "SEMICOLON":
            self.advance()


def parse_code(code):
    tokens, lexical_errors = tokenize(code)

    if lexical_errors:
        return tokens, lexical_errors, False

    parser = Parser(tokens)
    is_valid = parser.parse_program()

    return tokens, parser.errors, is_valid


# Temporary testing code
if __name__ == "__main__":
    sample_code = """
int marks = 85;
if marks > 50 {
    print(marks);
}
"""

    tokens, errors, is_valid = parse_code(sample_code)

    print("TOKENS:")
    for token in tokens:
        print(token)

    print("\nPARSER RESULT:")
    if is_valid:
        print("Syntax Analysis Passed.")
        print("MiniLang code is valid.")
    else:
        print("Syntax Analysis Failed.")
        for error in errors:
            print(error)