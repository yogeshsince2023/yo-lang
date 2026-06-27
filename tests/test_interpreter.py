import pytest
import io
import sys
import contextlib
from yo.lexer import Lexer
from yo.parser import Parser
from yo.interpreter import Interpreter
from yo.environment import Environment
from yo.errors import UndefinedVariable, TypeMismatch, DivisionByZero

def run_yo(code: str) -> str:
    """Helper to run YO code and return its captured stdout."""
    # Setup error globals
    from yo import errors
    errors.CURRENT_SOURCE = code
    errors.CURRENT_FILENAME = "<test>"
    errors.USE_COLOR = False

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    env = Environment()
    
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        interpreter.evaluate(ast, env)
    return f.getvalue()

# ─── 1. Variables ───

def test_variable_declaration():
    code = """
    make x = 10
    say x
    """
    assert run_yo(code).strip() == "10"

def test_variable_reassignment():
    code = """
    make x = 10
    x = 20
    say x
    """
    assert run_yo(code).strip() == "20"

# ─── 2. Arithmetic & Expressions ───

def test_arithmetic_ops():
    code = """
    say 2 + 3 * 4
    say (2 + 3) * 4
    """
    assert run_yo(code).split() == ["14", "20"]

# ─── 3. Conditions (When/Otherwise) ───

@pytest.mark.parametrize("value,expected", [
    ("5", "greater"),
    ("3", "less or equal"),
])
def test_when_conditions(value, expected):
    code = f"""
    make x = {value}
    when x > 3 {{
        say "greater"
    }} else {{
        say "less or equal"
    }}
    """
    assert run_yo(code).strip() == expected

# ─── 4. Loops (Repeat, For Each) ───

def test_repeat_loop():
    code = """
    repeat 3 times {
        say "loop"
    }
    """
    assert run_yo(code).split() == ["loop", "loop", "loop"]

def test_for_each_loop():
    code = """
    make lst = [1, 2, 3]
    for each num in lst {
        say num * 2
    }
    """
    assert run_yo(code).split() == ["2", "4", "6"]

# ─── 5. Tasks (Functions) & Recursion ───

def test_task_declaration_and_call():
    code = """
    task greet(name) {
        say "hello " + name
    }
    greet("Alice")
    """
    assert run_yo(code).strip() == "hello Alice"

def test_task_return_value():
    code = """
    task double(n) {
        return n * 2
    }
    make val = double(15)
    say val
    """
    assert run_yo(code).strip() == "30"

def test_task_recursion():
    code = """
    task fact(n) {
        when n <= 1 {
            return 1
        }
        return n * fact(n - 1)
    }
    say fact(5)
    """
    assert run_yo(code).strip() == "120"

# ─── 6. Standard Libraries ───

def test_math_library():
    code = """
    use math
    say math.round(3.6)
    say math.floor(3.6)
    say math.power(2, 3)
    """
    assert run_yo(code).split() == ["4", "3", "8"]

def test_text_library():
    code = """
    use text
    say text.upper("hello")
    say text.length("yo")
    say text.trim("  spaced  ")
    """
    assert run_yo(code).split() == ["HELLO", "2", "spaced"]

def test_list_library():
    code = """
    use list
    make my_list = [10, 20, 30]
    say list.count(my_list)
    say list.sum(my_list)
    """
    assert run_yo(code).split() == ["3", "60"]

# ─── 7. Errors & Exceptions ───

def test_error_undefined_variable():
    code = "say non_existent"
    with pytest.raises(UndefinedVariable):
        run_yo(code)

def test_error_type_mismatch():
    code = "say 5 + [1, 2]"
    with pytest.raises(TypeMismatch):
        run_yo(code)

def test_error_division_by_zero():
    code = "say 10 / 0"
    with pytest.raises(DivisionByZero):
        run_yo(code)
