# test_runner.py
# Runs valid, invalid syntax, and invalid semantic MiniLang test cases.

from parser import parse_code
from semantic_analyzer import analyze_semantics


def read_test_cases(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    test_cases = content.split("---")
    return [case.strip() for case in test_cases if case.strip()]


def run_single_test(code):
    tokens, syntax_errors, syntax_valid = parse_code(code)

    symbol_table = {}
    semantic_errors = []
    semantic_valid = False

    if syntax_valid:
        symbol_table, semantic_errors, semantic_valid = analyze_semantics(tokens)

    final_valid = syntax_valid and semantic_valid

    return {
        "tokens": tokens,
        "syntax_errors": syntax_errors,
        "syntax_valid": syntax_valid,
        "symbol_table": symbol_table,
        "semantic_errors": semantic_errors,
        "semantic_valid": semantic_valid,
        "final_valid": final_valid
    }


def format_symbol_table(symbol_table):
    lines = []

    if len(symbol_table) == 0:
        lines.append("Symbol Table: Empty")
        return lines

    lines.append("Symbol Table:")

    for variable, details in symbol_table.items():
        lines.append(
            f"  {variable} → type={details['type']}, "
            f"line={details['declared_line']}, "
            f"column={details['declared_column']}"
        )

    return lines


def run_tests():
    valid_cases = read_test_cases("../Test_Cases/valid_cases.txt")
    invalid_cases = read_test_cases("../Test_Cases/invalid_cases.txt")

    results = []

    results.append("MINILANG COMPLETE TEST RESULTS")
    results.append("=" * 70)

    results.append("\nVALID TEST CASES")
    results.append("-" * 70)

    for index, code in enumerate(valid_cases, start=1):
        test_result = run_single_test(code)

        results.append(f"\nValid Case {index}:")
        results.append(code)

        if test_result["final_valid"]:
            results.append("Result: PASSED ✅")
            results.append("Lexical Analysis: Passed")
            results.append("Syntax Analysis: Passed")
            results.append("Semantic Analysis: Passed")
        else:
            results.append("Result: FAILED ❌")

            for error in test_result["syntax_errors"]:
                results.append(error)

            for error in test_result["semantic_errors"]:
                results.append(error)

        results.extend(format_symbol_table(test_result["symbol_table"]))

    results.append("\nINVALID TEST CASES")
    results.append("-" * 70)

    for index, code in enumerate(invalid_cases, start=1):
        test_result = run_single_test(code)

        results.append(f"\nInvalid Case {index}:")
        results.append(code)

        if not test_result["final_valid"]:
            results.append("Result: Correctly Detected Error ✅")

            if not test_result["syntax_valid"]:
                results.append("Detected Phase: Lexical/Syntax Analysis")

                for error in test_result["syntax_errors"]:
                    results.append(error)

            elif not test_result["semantic_valid"]:
                results.append("Detected Phase: Semantic Analysis")

                for error in test_result["semantic_errors"]:
                    results.append(error)

        else:
            results.append("Result: ERROR NOT DETECTED ❌")

        results.extend(format_symbol_table(test_result["symbol_table"]))

    with open("../Test_Cases/test_results.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(results))

    print("\n".join(results))


if __name__ == "__main__":
    run_tests()