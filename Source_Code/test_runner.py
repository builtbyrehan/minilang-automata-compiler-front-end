# test_runner.py
# Runs valid and invalid MiniLang test cases and saves a detailed report.

from pathlib import Path

from parser import parse_code
from semantic_analyzer import analyze_semantics


# ----------------------------------------------------------------------
# File paths
# ----------------------------------------------------------------------

SOURCE_CODE_DIRECTORY = Path(__file__).resolve().parent
PROJECT_DIRECTORY = SOURCE_CODE_DIRECTORY.parent
TEST_CASES_DIRECTORY = PROJECT_DIRECTORY / "Test_Cases"

VALID_CASES_FILE = TEST_CASES_DIRECTORY / "valid_cases.txt"
INVALID_CASES_FILE = TEST_CASES_DIRECTORY / "invalid_cases.txt"
RESULTS_FILE = TEST_CASES_DIRECTORY / "test_results.txt"


# ----------------------------------------------------------------------
# Test-case loading
# ----------------------------------------------------------------------

def read_test_cases(file_path):
    """
    Read MiniLang test cases from a text file.

    Test cases must be separated by:

        ---

    Args:
        file_path: Path to the test-case file.

    Returns:
        List of non-empty MiniLang programs.

    Raises:
        FileNotFoundError: If the test-case file does not exist.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Test-case file was not found: {file_path}"
        )

    content = file_path.read_text(encoding="utf-8")

    test_cases = content.split("---")

    return [
        test_case.strip()
        for test_case in test_cases
        if test_case.strip()
    ]


# ----------------------------------------------------------------------
# Error classification
# ----------------------------------------------------------------------

def classify_frontend_errors(errors):
    """
    Separate lexical errors from syntax errors.

    Args:
        errors: Errors returned by parse_code().

    Returns:
        Tuple containing:
            lexical_errors
            syntax_errors
            other_errors
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


# ----------------------------------------------------------------------
# Single-test execution
# ----------------------------------------------------------------------

def run_single_test(code):
    """
    Run one MiniLang program through all compiler phases.

    Args:
        code: MiniLang source code.

    Returns:
        Dictionary containing tokens, errors, phase statuses,
        symbol-table data, and final validity.
    """

    tokens, frontend_errors, syntax_valid = parse_code(code)

    (
        lexical_errors,
        syntax_errors,
        other_errors,
    ) = classify_frontend_errors(frontend_errors)

    lexical_valid = len(lexical_errors) == 0

    symbol_table = {}
    semantic_errors = []
    semantic_valid = False

    if syntax_valid:
        (
            symbol_table,
            semantic_errors,
            semantic_valid,
        ) = analyze_semantics(tokens)

    final_valid = (
        lexical_valid
        and syntax_valid
        and semantic_valid
    )

    return {
        "tokens": tokens,
        "frontend_errors": frontend_errors,
        "lexical_errors": lexical_errors,
        "syntax_errors": syntax_errors,
        "other_errors": other_errors,
        "lexical_valid": lexical_valid,
        "syntax_valid": syntax_valid,
        "symbol_table": symbol_table,
        "semantic_errors": semantic_errors,
        "semantic_valid": semantic_valid,
        "final_valid": final_valid,
    }


# ----------------------------------------------------------------------
# Report-formatting methods
# ----------------------------------------------------------------------

def format_symbol_table(symbol_table):
    """
    Format the symbol table as report lines.

    Args:
        symbol_table: Semantic analyzer's symbol table.

    Returns:
        List of formatted strings.
    """

    lines = []

    if not symbol_table:
        lines.append("Symbol Table: Empty")
        return lines

    lines.append("Symbol Table:")

    for variable_name, details in symbol_table.items():
        initialized = details.get("initialized", True)
        initialized_text = "Yes" if initialized else "No"

        lines.append(
            f"  {variable_name} -> "
            f"type={details.get('type', 'Unknown')}, "
            f"line={details.get('declared_line', '-')}, "
            f"column={details.get('declared_column', '-')}, "
            f"initialized={initialized_text}"
        )

    return lines


def format_phase_status(test_result):
    """
    Format compiler-phase statuses for one test result.

    Args:
        test_result: Dictionary returned by run_single_test().

    Returns:
        List of formatted status lines.
    """

    lines = []

    if test_result["lexical_valid"]:
        lines.append("Lexical Analysis: Passed")
    else:
        lines.append("Lexical Analysis: Failed")

    if not test_result["lexical_valid"]:
        lines.append("Syntax Analysis: Skipped")
    elif test_result["syntax_valid"]:
        lines.append("Syntax Analysis: Passed")
    else:
        lines.append("Syntax Analysis: Failed")

    if not test_result["syntax_valid"]:
        lines.append("Semantic Analysis: Skipped")
    elif test_result["semantic_valid"]:
        lines.append("Semantic Analysis: Passed")
    else:
        lines.append("Semantic Analysis: Failed")

    return lines


def format_errors(test_result):
    """
    Collect all compiler errors for one test result.

    Args:
        test_result: Dictionary returned by run_single_test().

    Returns:
        List of formatted error lines.
    """

    errors = []

    errors.extend(test_result["lexical_errors"])
    errors.extend(test_result["syntax_errors"])
    errors.extend(test_result["other_errors"])
    errors.extend(test_result["semantic_errors"])

    if not errors:
        return ["No compiler errors found."]

    return [
        f"{index}. {error}"
        for index, error in enumerate(errors, start=1)
    ]


# ----------------------------------------------------------------------
# Valid-case processing
# ----------------------------------------------------------------------

def process_valid_cases(valid_cases, results):
    """
    Run test cases that are expected to be valid.

    Returns:
        Tuple containing passed and failed test counts.
    """

    passed_count = 0
    failed_count = 0

    results.append("")
    results.append("VALID TEST CASES")
    results.append("=" * 78)

    if not valid_cases:
        results.append("No valid test cases were found.")
        return passed_count, failed_count

    for index, code in enumerate(valid_cases, start=1):
        test_result = run_single_test(code)

        results.append("")
        results.append(f"Valid Case {index}")
        results.append("-" * 78)
        results.append(code)
        results.append("-" * 78)

        results.extend(format_phase_status(test_result))

        if test_result["final_valid"]:
            results.append("Test Result: PASSED")
            results.append(
                "The valid MiniLang program was accepted correctly."
            )
            passed_count += 1

        else:
            results.append("Test Result: FAILED")
            results.append(
                "The program was expected to be valid, "
                "but the compiler rejected it."
            )
            results.append("Errors:")
            results.extend(format_errors(test_result))
            failed_count += 1

        results.extend(
            format_symbol_table(test_result["symbol_table"])
        )

    return passed_count, failed_count


# ----------------------------------------------------------------------
# Invalid-case processing
# ----------------------------------------------------------------------

def process_invalid_cases(invalid_cases, results):
    """
    Run test cases that are expected to be invalid.

    Returns:
        Tuple containing passed and failed test counts.
    """

    passed_count = 0
    failed_count = 0

    results.append("")
    results.append("INVALID TEST CASES")
    results.append("=" * 78)

    if not invalid_cases:
        results.append("No invalid test cases were found.")
        return passed_count, failed_count

    for index, code in enumerate(invalid_cases, start=1):
        test_result = run_single_test(code)

        results.append("")
        results.append(f"Invalid Case {index}")
        results.append("-" * 78)
        results.append(code)
        results.append("-" * 78)

        results.extend(format_phase_status(test_result))

        if not test_result["final_valid"]:
            results.append("Test Result: PASSED")
            results.append(
                "The invalid MiniLang program was rejected correctly."
            )

            if not test_result["lexical_valid"]:
                results.append(
                    "Detected Phase: Lexical Analysis"
                )

            elif not test_result["syntax_valid"]:
                results.append(
                    "Detected Phase: Syntax Analysis"
                )

            elif not test_result["semantic_valid"]:
                results.append(
                    "Detected Phase: Semantic Analysis"
                )

            results.append("Detected Errors:")
            results.extend(format_errors(test_result))

            passed_count += 1

        else:
            results.append("Test Result: FAILED")
            results.append(
                "The program was expected to be invalid, "
                "but the compiler accepted it."
            )

            failed_count += 1

        results.extend(
            format_symbol_table(test_result["symbol_table"])
        )

    return passed_count, failed_count


# ----------------------------------------------------------------------
# Complete test execution
# ----------------------------------------------------------------------

def run_tests():
    """
    Run all valid and invalid MiniLang test cases.

    The full report is printed in the terminal and written to:

        Test_Cases/test_results.txt
    """

    try:
        valid_cases = read_test_cases(VALID_CASES_FILE)
        invalid_cases = read_test_cases(INVALID_CASES_FILE)

    except (FileNotFoundError, OSError) as error:
        print("Unable to run MiniLang tests.")
        print(error)
        return False

    results = [
        "MINILANG COMPLETE TEST RESULTS",
        "=" * 78,
        f"Valid test cases loaded: {len(valid_cases)}",
        f"Invalid test cases loaded: {len(invalid_cases)}",
    ]

    valid_passed, valid_failed = process_valid_cases(
        valid_cases,
        results,
    )

    invalid_passed, invalid_failed = process_invalid_cases(
        invalid_cases,
        results,
    )

    total_tests = len(valid_cases) + len(invalid_cases)
    total_passed = valid_passed + invalid_passed
    total_failed = valid_failed + invalid_failed

    results.append("")
    results.append("TEST SUMMARY")
    results.append("=" * 78)
    results.append(f"Total Tests:           {total_tests}")
    results.append(f"Total Passed:          {total_passed}")
    results.append(f"Total Failed:          {total_failed}")
    results.append(f"Valid Cases Passed:    {valid_passed}")
    results.append(f"Valid Cases Failed:    {valid_failed}")
    results.append(f"Invalid Cases Passed:  {invalid_passed}")
    results.append(f"Invalid Cases Failed:  {invalid_failed}")

    if total_failed == 0:
        results.append("")
        results.append("Overall Result: ALL TESTS PASSED")
    else:
        results.append("")
        results.append("Overall Result: SOME TESTS FAILED")

    report_text = "\n".join(results)

    try:
        TEST_CASES_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        RESULTS_FILE.write_text(
            report_text,
            encoding="utf-8",
        )

    except OSError as error:
        print(report_text)
        print()
        print(
            "Tests completed, but the results file could not be written."
        )
        print(error)
        return False

    print(report_text)
    print()
    print(f"Test report saved to: {RESULTS_FILE}")

    return total_failed == 0


def main():
    """Run the MiniLang automated test suite."""

    all_tests_passed = run_tests()

    if all_tests_passed:
        print("\nAutomated testing completed successfully.")
    else:
        print("\nAutomated testing completed with failures.")


if __name__ == "__main__":
    main()