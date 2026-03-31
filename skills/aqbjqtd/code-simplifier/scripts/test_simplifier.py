#!/usr/bin/env python3
"""
Test script for code-simplifier skill.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.code_simplifier import CodeSimplifier


def test_complex_code():
    """Test with complex nested code."""
    complex_code = """
def process_data(items):
    result = []
    for item in items:
        if item is not None:
            if 'status' in item:
                if item['status'] == 'active':
                    if 'data' in item:
                        data = item['data']
                        if isinstance(data, dict):
                            if 'value' in data:
                                value = data['value']
                                if value > 0:
                                    processed = {
                                        'id': item.get('id'),
                                        'value': value * 2,
                                        'status': 'processed'
                                    }
                                    result.append(processed)
                                else:
                                    print('Invalid value')
                            else:
                                print('Missing value')
                        else:
                            print('Invalid data type')
                    else:
                        print('Missing data')
                else:
                    print('Inactive item')
            else:
                print('Missing status')
        else:
            print('None item')
    return result
"""

    print("Testing complex nested code...")
    simplifier = CodeSimplifier()

    # Analyze
    metrics = simplifier.analyze(complex_code)
    print(f"Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
    print(f"Nesting Depth: {metrics.nesting_depth}")
    print(f"Line Count: {metrics.line_count}")

    # Generate suggestions
    suggestions = simplifier.generate_suggestions(complex_code)
    print(f"\nFound {len(suggestions)} suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion.pattern_name}: {suggestion.description}")

    # Simplify
    simplified = simplifier.simplify(complex_code, apply_changes=True)
    print(f"\nSimplified code length: {len(simplified)} chars")

    return len(suggestions) > 0


def test_duplicate_code():
    """Test with duplicate code patterns."""
    duplicate_code = """
def calculate_total(items):
    total = 0
    for item in items:
        if item['price'] > 0 and item['quantity'] > 0:
            total += item['price'] * item['quantity']
    return total

def calculate_tax(items, rate):
    tax = 0
    for item in items:
        if item['price'] > 0 and item['quantity'] > 0:
            tax += item['price'] * item['quantity'] * rate
    return tax
"""

    print("\nTesting duplicate code detection...")
    simplifier = CodeSimplifier()

    suggestions = simplifier.generate_suggestions(duplicate_code)

    duplicate_found = False
    for suggestion in suggestions:
        if "Duplicate" in suggestion.pattern_name:
            duplicate_found = True
            print(f"Found duplicate code: {suggestion.description}")

    return duplicate_found


def test_type_hints():
    """Test type hint detection."""
    code_without_hints = """
def process_data(data):
    result = {}
    for key, value in data.items():
        result[key] = str(value)
    return result
"""

    print("\nTesting type hint detection...")
    simplifier = CodeSimplifier()

    suggestions = simplifier.generate_suggestions(code_without_hints)

    type_hint_found = False
    for suggestion in suggestions:
        if "Type Hints" in suggestion.pattern_name:
            type_hint_found = True
            print(f"Found missing type hints: {suggestion.description}")

    return type_hint_found


def test_boolean_expressions():
    """Test complex boolean expression detection."""
    complex_boolean = """
def is_valid_user(user):
    if user and user.active and user.verified and user.subscription and user.subscription.valid:
        return True
    return False
"""

    print("\nTesting boolean expression detection...")
    simplifier = CodeSimplifier()

    suggestions = simplifier.generate_suggestions(complex_boolean)

    boolean_found = False
    for suggestion in suggestions:
        if "Boolean" in suggestion.pattern_name:
            boolean_found = True
            print(f"Found complex boolean: {suggestion.description}")

    return boolean_found


def main():
    """Run all tests."""
    print("=" * 60)
    print("Code Simplifier Skill - Test Suite")
    print("=" * 60)

    tests = [
        ("Complex Nested Code", test_complex_code),
        ("Duplicate Code Detection", test_duplicate_code),
        ("Type Hint Detection", test_type_hints),
        ("Boolean Expression Detection", test_boolean_expressions),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'=' * 40}")
        print(f"Test: {test_name}")
        print("=" * 40)

        try:
            result = test_func()
            results.append((test_name, result, "PASS" if result else "FAIL"))
            print(f"Result: {'PASS' if result else 'FAIL'}")
        except Exception as e:
            results.append((test_name, False, f"ERROR: {e}"))
            print(f"Result: ERROR - {e}")

    # Summary
    print(f"\n{'=' * 60}")
    print("Test Summary:")
    print("=" * 60)

    passed = 0
    for test_name, result, status in results:
        print(f"{test_name:30} {status}")
        if status == "PASS":
            passed += 1

    print(f"\nTotal: {len(tests)} tests, {passed} passed, {len(tests) - passed} failed")

    if passed == len(tests):
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[FAILURE] Some tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
