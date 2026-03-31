#!/usr/bin/env python3
"""
Demo: How to use the code-simplifier skill
"""

import sys
import os

# Add the skill directory to path
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(skill_dir)

from scripts.code_simplifier import CodeSimplifier


def demonstrate_basic_usage():
    """Demonstrate basic usage of code-simplifier."""
    print("=" * 60)
    print("Code Simplifier Skill - Basic Usage Demo")
    print("=" * 60)

    # Example 1: Complex nested code
    complex_code = """
def validate_and_process_order(order):
    if order is not None:
        if 'items' in order:
            items = order['items']
            if isinstance(items, list):
                if len(items) > 0:
                    for item in items:
                        if 'id' in item:
                            if 'price' in item:
                                if item['price'] > 0:
                                    if 'quantity' in item:
                                        if item['quantity'] > 0:
                                            # Process item
                                            pass
                                        else:
                                            return {'error': 'Invalid quantity'}
                                    else:
                                        return {'error': 'Missing quantity'}
                                else:
                                    return {'error': 'Invalid price'}
                            else:
                                return {'error': 'Missing price'}
                        else:
                            return {'error': 'Missing item id'}
                    return {'success': True}
                else:
                    return {'error': 'No items'}
            else:
                return {'error': 'Items must be a list'}
        else:
            return {'error': 'Missing items'}
    else:
        return {'error': 'No order provided'}
"""

    print("\n1. Analyzing complex nested code...")
    simplifier = CodeSimplifier()
    metrics = simplifier.analyze(complex_code)

    print(f"   Cyclomatic Complexity: {metrics.cyclomatic_complexity} (High)")
    print(f"   Maximum Nesting Depth: {metrics.nesting_depth} (Very High)")
    print(f"   Function Length: {metrics.line_count} lines")

    # Generate suggestions
    suggestions = simplifier.generate_suggestions(complex_code)
    print(f"\n2. Generated {len(suggestions)} refactoring suggestions:")

    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n   Suggestion {i}: {suggestion.pattern_name}")
        print(f"   - {suggestion.description}")
        print(f"   - Location: Lines {suggestion.location[0]}-{suggestion.location[1]}")
        print(f"   - Complexity Reduction: {suggestion.complexity_reduction} points")
        print(f"   - Risk Level: {suggestion.risk_level}")

    # Simplify the code
    print("\n3. Applying simplifications...")
    simplified = simplifier.simplify(complex_code, apply_changes=True)

    print("\n4. Simplified code preview:")
    print("-" * 40)
    lines = simplified.split("\n")
    for i, line in enumerate(lines[:20], 1):
        print(f"{i:3}: {line}")
    print("...")
    print("-" * 40)

    return True


def demonstrate_advanced_features():
    """Demonstrate advanced features."""
    print("\n" + "=" * 60)
    print("Advanced Features Demo")
    print("=" * 60)

    # Example 2: Code with multiple issues
    problematic_code = """
def calculate(data):
    r = 0
    for d in data:
        if d and d.v and d.v > 0:
            r += d.v * 2
    return r

def process(data):
    r = 0
    for d in data:
        if d and d.v and d.v > 0:
            r += d.v * 3
    return r
"""

    print("\n1. Code with multiple issues:")
    print(problematic_code)

    simplifier = CodeSimplifier()
    metrics = simplifier.analyze(problematic_code)

    print(f"\n2. Analysis Results:")
    print(f"   - Cyclomatic Complexity: {metrics.cyclomatic_complexity}")
    print(f"   - Duplication Score: {metrics.duplication_score:.1f}%")

    suggestions = simplifier.generate_suggestions(problematic_code)

    print(f"\n3. Issues detected:")
    for suggestion in suggestions:
        print(f"   - {suggestion.pattern_name}: {suggestion.description}")

    return True


def demonstrate_integration():
    """Demonstrate integration with development workflow."""
    print("\n" + "=" * 60)
    print("Integration Demo")
    print("=" * 60)

    print("\n1. Command-line usage examples:")
    print("""
   # Analyze code complexity
   python scripts/code_simplifier.py myfile.py --analyze
   
   # Generate refactoring suggestions
   python scripts/code_simplifier.py myfile.py --suggest --format=json
   
   # Simplify code and save output
   python scripts/code_simplifier.py myfile.py --simplify --output=simplified.py
   
   # Batch process directory
   for file in *.py; do
     python scripts/code_simplifier.py "$file" --simplify --output="simplified/$file"
   done
    """)

    print("\n2. Integration with CI/CD:")
    print("""
   # GitHub Actions example
   - name: Code Quality Check
     run: |
       python scripts/code_simplifier.py src/ --analyze --fail-on-complexity=15
       
   # Pre-commit hook
   # .git/hooks/pre-commit
   STAGED_FILES=$(git diff --cached --name-only -- "*.py")
   for file in $STAGED_FILES; do
     python scripts/code_simplifier.py "$file" --analyze
   done
    """)

    print("\n3. IDE Integration:")
    print("""
   # VS Code Task
   {
     "label": "Simplify Code",
     "type": "shell",
     "command": "python ${workspaceFolder}/scripts/code_simplifier.py ${file} --simplify",
     "problemMatcher": []
   }
    """)

    return True


def main():
    """Run all demonstrations."""
    try:
        demonstrate_basic_usage()
        demonstrate_advanced_features()
        demonstrate_integration()

        print("\n" + "=" * 60)
        print("Demo Complete!")
        print("=" * 60)
        print("\nThe code-simplifier skill provides:")
        print("1. Automated code complexity analysis")
        print("2. Intelligent refactoring suggestions")
        print("3. Safe code simplification")
        print("4. Integration with development workflows")
        print("\nUse '/code-simplifier' to access this skill!")

        return 0

    except Exception as e:
        print(f"\nError during demo: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
