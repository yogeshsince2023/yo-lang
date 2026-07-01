"""
YO Error Reference — detailed explanations, examples, and fix suggestions
for every error code in the YO language.

Usage:  yo explain E003
"""

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# Re-use the color helper from errors.py
from .errors import USE_COLOR

def _c(color_code, text):
    if USE_COLOR:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text


ERROR_REFERENCE = {
    "E001": {
        "title": "Undefined Variable",
        "description": (
            "You tried to use a variable that hasn't been created yet.\n"
            "In YO, every variable must be declared with 'make' before\n"
            "it can be read or used in an expression."
        ),
        "example_bad_code": (
            'say greeting          # ❌ "greeting" was never made\n'
        ),
        "example_fixed_code": (
            'make greeting = "Hello, YO!"\n'
            'say greeting          # ✅ Now it works\n'
        ),
        "common_mistakes": [
            "Using 'let' or 'var' instead of 'make'.",
            "Misspelling a variable name (e.g. 'nmae' instead of 'name').",
            "Using a variable outside the scope where it was defined.",
        ],
        "related_codes": ["E002"],
    },

    "E002": {
        "title": "Invalid Syntax",
        "description": (
            "YO could not understand a line in your program.\n"
            "This usually means a keyword is misspelled, a brace\n"
            "is missing, or you used syntax from another language."
        ),
        "example_bad_code": (
            'let x = 5             # ❌ YO uses "make", not "let"\n'
            'print("hello")        # ❌ YO uses "say", not "print"\n'
        ),
        "example_fixed_code": (
            'make x = 5            # ✅ Correct\n'
            'say "hello"           # ✅ Correct\n'
        ),
        "common_mistakes": [
            "Using 'let', 'var', or 'const' instead of 'make'.",
            "Using 'print()' or 'console.log()' instead of 'say'.",
            "Using 'def' or 'function' instead of 'task'.",
            "Missing '{' or '}' around a block.",
        ],
        "related_codes": ["E001"],
    },

    "E003": {
        "title": "Type Mismatch",
        "description": (
            "An operation received values of incompatible types.\n"
            "For example, you cannot subtract a string from a number,\n"
            "or compare a list to a boolean."
        ),
        "example_bad_code": (
            'make score = 100\n'
            'say score - "fifty"   # ❌ Cannot subtract STRING from NUMBER\n'
        ),
        "example_fixed_code": (
            'make score = 100\n'
            'say score - 50        # ✅ Both sides are numbers\n'
        ),
        "common_mistakes": [
            "Mixing numbers and strings in arithmetic (-, *, /).",
            "Forgetting that 'ask()' returns a STRING — wrap it with a conversion.",
            "Passing the wrong number of arguments to a task.",
        ],
        "related_codes": ["E004"],
    },

    "E004": {
        "title": "Division By Zero",
        "description": (
            "Your program tried to divide a number by zero.\n"
            "Division by zero is mathematically undefined, so YO\n"
            "stops and reports this error."
        ),
        "example_bad_code": (
            'make result = 10 / 0  # ❌ Cannot divide by zero\n'
        ),
        "example_fixed_code": (
            'make divisor = 0\n'
            'when divisor != 0 {\n'
            '    say 10 / divisor  # ✅ Safe: checked first\n'
            '} else {\n'
            '    say "Cannot divide by zero!"\n'
            '}\n'
        ),
        "common_mistakes": [
            "Using a variable as a divisor without checking if it's zero.",
            "Modulo (%) by zero — this triggers the same error.",
        ],
        "related_codes": ["E003"],
    },
}


def format_reference_entry(code: str) -> str:
    """Return a colorized, detailed explanation for a given error code."""
    code = code.upper()
    if code not in ERROR_REFERENCE:
        available = ", ".join(sorted(ERROR_REFERENCE.keys()))
        return (
            _c(f"{Fore.RED}{Style.BRIGHT}", f"Unknown error code '{code}'.\n")
            + f"Available codes: {available}"
        )

    entry = ERROR_REFERENCE[code]

    header = _c(
        f"{Fore.CYAN}{Style.BRIGHT}",
        f"\n{'═' * 55}\n"
        f"  [{code}] {entry['title']}\n"
        f"{'═' * 55}"
    )

    desc = _c(Fore.WHITE, f"\n  {entry['description']}")

    bad_label = _c(f"{Fore.RED}{Style.BRIGHT}", "\n  ✗ Broken Code:")
    bad_code = ""
    for line in entry["example_bad_code"].splitlines():
        bad_code += _c(Fore.RED, f"    {line}") + "\n"

    fix_label = _c(f"{Fore.GREEN}{Style.BRIGHT}", "\n  ✓ Fixed Code:")
    fix_code = ""
    for line in entry["example_fixed_code"].splitlines():
        fix_code += _c(Fore.GREEN, f"    {line}") + "\n"

    mistakes_label = _c(f"{Fore.YELLOW}{Style.BRIGHT}", "  ⚠ Common Mistakes:")
    mistakes = ""
    for m in entry.get("common_mistakes", []):
        mistakes += _c(Fore.YELLOW, f"    • {m}") + "\n"

    related = ""
    if entry.get("related_codes"):
        codes_str = ", ".join(entry["related_codes"])
        related = _c(Fore.CYAN, f"\n  See also: {codes_str}")

    footer = _c(f"{Fore.CYAN}{Style.BRIGHT}", f"\n{'═' * 55}\n")

    return (
        f"{header}\n"
        f"{desc}\n"
        f"{bad_label}\n{bad_code}"
        f"{fix_label}\n{fix_code}"
        f"{mistakes_label}\n{mistakes}"
        f"{related}"
        f"{footer}"
    )
