import os
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

# Global source code references to format line snippets in errors
CURRENT_SOURCE = None
CURRENT_FILENAME = None

# Flag to toggle color output (set False for web/API usage)
USE_COLOR = True

def _c(color_code, text):
    """Apply color only when USE_COLOR is True."""
    if USE_COLOR:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text

def get_line_snippet(line, filename=None):
    """Retrieve the exact line of code where the error occurred."""
    global CURRENT_SOURCE, CURRENT_FILENAME
    if CURRENT_SOURCE:
        lines = CURRENT_SOURCE.splitlines()
        if 1 <= line <= len(lines):
            return lines[line - 1].strip()
    
    fname = filename or CURRENT_FILENAME
    if fname and os.path.exists(fname):
        try:
            with open(fname, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if 1 <= line <= len(lines):
                return lines[line - 1].strip()
        except Exception:
            pass
    return "Unavailable"

class YOError(Exception):
    """Base class for all YO language exceptions."""
    def __init__(self, filename=None):
        self.filename = filename or CURRENT_FILENAME
        super().__init__()

class UndefinedVariable(YOError):
    def __init__(self, name, suggestion=None, line=7, filename=None):
        self.name = name
        self.suggestion = suggestion
        self.line = line
        super().__init__(filename)

    def __str__(self):
        snippet = get_line_snippet(self.line, self.filename)
        title = _c(f"{Fore.RED}{Style.BRIGHT}", "❌ YO Error — Undefined Variable")
        details = f"     '{self.name}' was used but never made."
        
        if self.name == "let":
            fix_msg = "Use 'make' instead of 'let' for variable declaration."
        elif self.name == "print":
            fix_msg = "Use 'say' instead of 'print' to display values."
        elif self.name == "def":
            fix_msg = "Use 'task' instead of 'def' to define functions."
        elif self.suggestion:
            fix_msg = f"Did you mean '{self.suggestion}'? If not, add `make {self.name} = ...` before line {self.line}"
        else:
            fix_msg = f"Add `make {self.name} = ...` before line {self.line}"
            
        fix = _c(f"{Fore.GREEN}{Style.BRIGHT}", f"     Fix: {fix_msg}")
        line_info = _c(Fore.YELLOW, f"     Line {self.line}: {snippet}")
        return f"{title}\n{details}\n{fix}\n{line_info}"

class InvalidSyntax(YOError):
    def __init__(self, line, text, suggestion=None, filename=None):
        self.line = line
        self.text = text
        self.suggestion = suggestion
        super().__init__(filename)

    def __str__(self):
        snippet = get_line_snippet(self.line, self.filename)
        title = _c(f"{Fore.RED}{Style.BRIGHT}", "❌ YO Error — Invalid Syntax")
        details = f"     Could not understand '{self.text.strip()}' on line {self.line}."
        
        # Detect common mistakes in the text or snippet
        check_text = snippet.lower() if snippet != "Unavailable" else self.text.lower()
        
        fix_suggestion = self.suggestion
        if not fix_suggestion:
            if "let " in check_text:
                fix_suggestion = "Use 'make' instead of 'let' for variable declaration."
            elif "print" in check_text:
                fix_suggestion = "Use 'say' instead of 'print' to display values."
            elif "def " in check_text:
                fix_suggestion = "Use 'task' instead of 'def' to define functions."
            elif "when" in check_text and "{" not in check_text:
                fix_suggestion = "Missing opening brace '{' after 'when' condition."
            elif "repeat" in check_text and "{" not in check_text:
                fix_suggestion = "Missing opening brace '{' after 'repeat' count."
            else:
                fix_suggestion = f"Check syntax structure on line {self.line}."
                
        fix = _c(f"{Fore.GREEN}{Style.BRIGHT}", f"     Fix: {fix_suggestion}")
        line_info = _c(Fore.YELLOW, f"     Line {self.line}: {snippet}")
        return f"{title}\n{details}\n{fix}\n{line_info}"

class TypeMismatch(YOError):
    def __init__(self, expected, got, line, filename=None):
        self.expected = expected
        self.got = got
        self.line = line
        super().__init__(filename)

    def __str__(self):
        snippet = get_line_snippet(self.line, self.filename)
        title = _c(f"{Fore.RED}{Style.BRIGHT}", "❌ YO Error — Type Mismatch")
        
        # Detect the operation in the code snippet
        op = None
        for possible_op in ["==", "!=", ">=", "<=", "+", "-", "*", "/", "%", ">", "<"]:
            if possible_op in snippet:
                op = possible_op
                break
                
        if op:
            details = f"     Type clash on operation '{op}': expected '{self.expected}', but got '{self.got}'."
            fix_msg = f"Ensure both sides of '{op}' are compatible (e.g. both numbers)."
        else:
            details = f"     Expected type '{self.expected}' on line {self.line}, but got '{self.got}'."
            fix_msg = f"Convert or use value of type '{self.expected}'."
            
        fix = _c(f"{Fore.GREEN}{Style.BRIGHT}", f"     Fix: {fix_msg}")
        line_info = _c(Fore.YELLOW, f"     Line {self.line}: {snippet}")
        return f"{title}\n{details}\n{fix}\n{line_info}"

class DivisionByZero(YOError):
    def __init__(self, line, filename=None):
        self.line = line
        super().__init__(filename)

    def __str__(self):
        snippet = get_line_snippet(self.line, self.filename)
        title = _c(f"{Fore.RED}{Style.BRIGHT}", "❌ YO Error — Division By Zero")
        details = f"     Cannot divide by zero on line {self.line}."
        fix = _c(f"{Fore.GREEN}{Style.BRIGHT}", f"     Fix: Ensure the denominator is not zero before line {self.line}")
        line_info = _c(Fore.YELLOW, f"     Line {self.line}: {snippet}")
        return f"{title}\n{details}\n{fix}\n{line_info}"
