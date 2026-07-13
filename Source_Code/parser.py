# parser.py
# MiniLang Syntax Analyzer
# Checks whether a token stream follows MiniLang grammar rules.

from lexer import tokenize


class Parser:
    """Recursive-descent parser for the MiniLang language."""

    def __init__(self, tokens):
        """
        Initialize the parser.

        Args:
            tokens: List of tokens produced by the lexical analyzer.
        """

        self.tokens = tokens
        self.position = 0
        self.errors = []

    # ------------------------------------------------------------------
    # Token-handling methods
    # ------------------------------------------------------------------

    def current_token(self):
        """
        Return the token currently being examined.

        If all tokens have been processed, return an EOF token with a
        meaningful line and column location.
        """

        if self.position < len(self.tokens):
            return self.tokens[self.position]

        # Calculate a sensible EOF position from the final token.
        if self.tokens:
            _, token_value, line, column = self.tokens[-1]
            eof_column = column + len(str(token_value))

            return ("EOF", "EOF", line, eof_column)

        # Empty source code.
        return ("EOF", "EOF", 1, 1)

    def advance(self):
        """Move the parser to the next token."""

        if self.position < len(self.tokens):
            self.position += 1

    def match(self, expected_type, expected_value=None):
        """
        Match the current token with an expected token type and value.

        Args:
            expected_type: Required token type.
            expected_value: Optional required token value.

        Returns:
            True when the token matches; otherwise False.
        """

        token_type, token_value, line, column = self.current_token()

        # Successful match.
        if token_type == expected_type:
            if expected_value is None or token_value == expected_value:
                self.advance()
                return True

        # --------------------------------------------------------------
        # Errors involving a specific expected token value
        # --------------------------------------------------------------

        if expected_value is not None:
            if expected_value == ";":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    "Missing semicolon ';' after statement."
                )

            elif expected_value == "{":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    "Missing opening brace '{' after condition."
                )

            elif expected_value == "}":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    "Missing closing brace '}' after if-statement body."
                )

            elif expected_value == "(":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    "Missing opening parenthesis '(' after 'print'."
                )

            elif expected_value == ")":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    "Missing closing parenthesis ')' in print statement."
                )

            elif expected_value == "=":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Expected assignment operator '=', found "
                    f"'{token_value}'."
                )

            else:
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Expected '{expected_value}', found '{token_value}'."
                )

        # --------------------------------------------------------------
        # Errors involving only an expected token type
        # --------------------------------------------------------------

        else:
            if expected_type == "IDENTIFIER" and token_type == "NUMBER":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Invalid variable name '{token_value}'. "
                    "A numeric literal cannot be used as a variable name. "
                    "Expected an identifier."
                )

            elif expected_type == "IDENTIFIER":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Expected an identifier, found '{token_value}'."
                )

            elif expected_type == "NUMBER":
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Expected a number, found '{token_value}'."
                )

            else:
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Expected {expected_type}, found '{token_value}'."
                )

        return False

    # ------------------------------------------------------------------
    # Grammar methods
    # ------------------------------------------------------------------

    def parse_program(self):
        """
        Parse the complete MiniLang program.

        Grammar:
            Program → Statement*
        """

        while self.current_token()[0] != "EOF":
            starting_position = self.position

            if not self.parse_statement():
                self.synchronize()

            # Safety check to ensure that the parser always makes progress.
            # This prevents an infinite loop on unexpected closing braces or
            # other tokens that synchronization does not consume.
            if (
                self.position == starting_position
                and self.current_token()[0] != "EOF"
            ):
                self.advance()

        return len(self.errors) == 0

    def parse_statement(self):
        """
        Parse one MiniLang statement.

        Grammar:
            Statement → Declaration
                      | Assignment
                      | PrintStatement
                      | IfStatement
        """

        token_type, token_value, line, column = self.current_token()

        if token_type == "KEYWORD" and token_value == "int":
            return self.parse_declaration()

        if token_type == "IDENTIFIER":
            return self.parse_assignment()

        if token_type == "KEYWORD" and token_value == "print":
            return self.parse_print_statement()

        if token_type == "KEYWORD" and token_value == "if":
            return self.parse_if_statement()

        if token_type == "RBRACE":
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: "
                "Unexpected closing brace '}'."
            )

        elif token_type == "SEMICOLON":
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: "
                "Unexpected semicolon ';'."
            )

        else:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: "
                f"Invalid statement starting with '{token_value}'."
            )

        return False

    def parse_declaration(self):
        """
        Parse a variable declaration.

        Grammar:
            Declaration → int identifier = number ;
        """

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
        """
        Parse an assignment statement.

        Grammar:
            Assignment → identifier = Expression ;
        """

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
        """
        Parse a print statement.

        Grammar:
            PrintStatement → print ( identifier ) ;
        """

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
        """
        Parse an if statement.

        Grammar:
            IfStatement → if Condition { StatementList }

            StatementList → Statement*
        """

        if not self.match("KEYWORD", "if"):
            return False

        if not self.parse_condition():
            return False

        if not self.match("LBRACE", "{"):
            return False

        # Parse all statements inside the if block.
        while self.current_token()[0] not in {"RBRACE", "EOF"}:
            starting_position = self.position

            if not self.parse_statement():
                self.synchronize()

            # Prevent an infinite loop if no token was consumed.
            if (
                self.position == starting_position
                and self.current_token()[0] not in {"RBRACE", "EOF"}
            ):
                self.advance()

        if not self.match("RBRACE", "}"):
            return False

        return True

    def parse_condition(self):
        """
        Parse an if-statement condition.

        Grammar:
            Condition → identifier RelOp number

            RelOp → > | <
        """

        if not self.match("IDENTIFIER"):
            return False

        token_type, token_value, line, column = self.current_token()

        if token_type == "OPERATOR" and token_value in {">", "<"}:
            self.advance()

        else:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: "
                f"Expected relational operator '>' or '<', found "
                f"'{token_value}'."
            )
            return False

        if not self.match("NUMBER"):
            return False

        return True

    def parse_expression(self):
        """
        Parse an arithmetic expression.

        Grammar:
            Expression → Operand
                       | Operand ArithmeticOperator Operand

            Operand → identifier | number

            ArithmeticOperator → + | - | * | /
        """

        token_type, token_value, line, column = self.current_token()

        # First operand.
        if token_type not in {"IDENTIFIER", "NUMBER"}:
            self.errors.append(
                f"Syntax Error at line {line}, column {column}: "
                f"Expected an identifier or number in expression, "
                f"found '{token_value}'."
            )
            return False

        self.advance()

        token_type, token_value, line, column = self.current_token()

        # Optional arithmetic operator and second operand.
        if (
            token_type == "OPERATOR"
            and token_value in {"+", "-", "*", "/"}
        ):
            self.advance()

            token_type, token_value, line, column = self.current_token()

            if token_type not in {"IDENTIFIER", "NUMBER"}:
                self.errors.append(
                    f"Syntax Error at line {line}, column {column}: "
                    f"Expected an identifier or number after operator, "
                    f"found '{token_value}'."
                )
                return False

            self.advance()

        return True

    # ------------------------------------------------------------------
    # Error-recovery method
    # ------------------------------------------------------------------

    def synchronize(self):
        """
        Skip invalid tokens until a safe parsing point is reached.

        Safe points:
            - Semicolon
            - Closing brace
            - End of file
        """

        while self.current_token()[0] not in {
            "SEMICOLON",
            "RBRACE",
            "EOF",
        }:
            self.advance()

        # Consume a semicolon so parsing can continue with the next
        # statement. A closing brace is not consumed here because it may
        # belong to the current if statement.
        if self.current_token()[0] == "SEMICOLON":
            self.advance()


def parse_code(code):
    """
    Perform lexical and syntax analysis on MiniLang source code.

    Args:
        code: MiniLang source code as a string.

    Returns:
        tuple:
            tokens: Tokens generated by the lexer.
            errors: Lexical or syntax error messages.
            is_valid: True when the code contains no errors.
    """

    tokens, lexical_errors = tokenize(code)

    # Syntax analysis should not continue when lexical errors exist.
    if lexical_errors:
        return tokens, lexical_errors, False

    parser = Parser(tokens)
    is_valid = parser.parse_program()

    return tokens, parser.errors, is_valid


def main():
    """Run a basic parser test."""

    sample_code = """
int marks = 85;

if marks > 50 {
    print(marks);
}
"""

    tokens, errors, is_valid = parse_code(sample_code)

    print("TOKENS:")

    if tokens:
        for token in tokens:
            print(token)
    else:
        print("No tokens generated.")

    print("\nPARSER RESULT:")

    if is_valid:
        print("Syntax Analysis Passed.")
        print("MiniLang code is valid.")

    else:
        print("Syntax Analysis Failed.")

        for error in errors:
            print(error)


if __name__ == "__main__":
    main()