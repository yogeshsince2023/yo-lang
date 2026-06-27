import sys
import importlib
from typing import Any
from .errors import YOError, UndefinedVariable, TypeMismatch, DivisionByZero
from .environment import Environment
from .parser import (
    TaskDecl
)

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Task:
    """Wrapper to represent custom YO functions/tasks with their closures."""
    def __init__(self, declaration: TaskDecl, closure_env: Environment):
        self.declaration = declaration
        self.closure_env = closure_env

def get_yo_type(val) -> str:
    """Returns a string representing the type of value in YO."""
    if isinstance(val, bool):
        return 'BOOL'
    if isinstance(val, (int, float)):
        return 'NUMBER'
    if isinstance(val, str):
        return 'STRING'
    if isinstance(val, list):
        return 'LIST'
    if val is None:
        return 'null'
    return type(val).__name__

class Interpreter:
    def evaluate(self, node: Any, env: Environment) -> Any:
        if node is None:
            return None
            
        node_type = type(node).__name__
        
        if node_type == "Program":
            result = None
            for stmt in node.statements:
                result = self.evaluate(stmt, env)
            return result
            
        elif node_type == "VarDecl":
            val = self.evaluate(node.expression, env)
            env.define(node.name, val)
            return val
            
        elif node_type == "AssignStmt":
            val = self.evaluate(node.expression, env)
            if env.has(node.name):
                env.set(node.name, val)
            else:
                raise UndefinedVariable(node.name, suggestion=env.similar_name(node.name), line=node.line)
            return val
            
        elif node_type == "SayStmt":
            val = self.evaluate(node.expression, env)
            print(val)
            return val
            
        elif node_type == "AskExpr":
            return input()
            
        elif node_type == "LiteralExpr":
            return node.value
            
        elif node_type == "ListExpr":
            return [self.evaluate(elem, env) for elem in node.elements]
            
        elif node_type == "IdentifierExpr":
            return env.get(node.name, line=node.line)
            
        elif node_type == "WhenStmt":
            cond = self.evaluate(node.condition, env)
            if bool(cond):
                result = None
                for stmt in node.then_branch:
                    result = self.evaluate(stmt, env)
                return result
            elif node.else_branch is not None:
                result = None
                for stmt in node.else_branch:
                    result = self.evaluate(stmt, env)
                return result
            return None
            
        elif node_type == "RepeatStmt":
            count = self.evaluate(node.count_expr, env)
            if not isinstance(count, (int, float)):
                raise TypeMismatch("NUMBER", get_yo_type(count), node.line)
            
            iterations = int(count)
            result = None
            for _ in range(iterations):
                for stmt in node.body:
                    result = self.evaluate(stmt, env)
            return result
            
        elif node_type == "ForEachStmt":
            lst = self.evaluate(node.list_expr, env)
            if not isinstance(lst, list):
                raise TypeMismatch("LIST", get_yo_type(lst), node.line)
                
            result = None
            for item in lst:
                # Create loop iteration scope
                loop_env = Environment(parent=env)
                loop_env.define(node.item_name, item)
                for stmt in node.body:
                    result = self.evaluate(stmt, loop_env)
            return result
            
        elif node_type == "TaskDecl":
            # Save function with closure env
            env.define(node.name, Task(node, env))
            return None
            
        elif node_type == "ReturnStmt":
            val = self.evaluate(node.expression, env) if node.expression is not None else None
            raise ReturnSignal(val)
            
        elif node_type == "UseStmt":
            libname = node.libname
            try:
                import os
                package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if package_root not in sys.path:
                    sys.path.insert(0, package_root)
                module = importlib.import_module(f"yo.stdlib.{libname}_lib")
            except ImportError as e:
                try:
                    module = importlib.import_module(f"stdlib.{libname}_lib")
                except ImportError:
                    raise YOError(f"Could not load library yo/stdlib/{libname}_lib.py: {e}")
                
            lib_dict_name = f"{libname.upper()}_LIB"
            if hasattr(module, lib_dict_name):
                lib_dict = getattr(module, lib_dict_name)
                for func_name, func in lib_dict.items():
                    # Wrap function to forward unpacked arguments as a tuple to the list-based lambda
                    def wrapped_func(*args, f=func):
                        return f(args)
                    env.define(f"{libname}.{func_name}", wrapped_func)
            else:
                # Expose public callable attributes in namespace
                for attr_name in dir(module):
                    if not attr_name.startswith('_'):
                        attr = getattr(module, attr_name)
                        if callable(attr):
                            env.define(f"{libname}.{attr_name}", attr)
            return None
            
        elif node_type == "CallExpr":
            callee_val = env.get(node.callee, line=node.line)
            args_vals = [self.evaluate(arg, env) for arg in node.args]
            
            if isinstance(callee_val, Task):
                decl = callee_val.declaration
                if len(args_vals) != len(decl.params):
                    raise TypeMismatch(
                        expected=f"{len(decl.params)} arguments", 
                        got=f"{len(args_vals)} arguments", 
                        line=node.line
                    )
                # Create task environment
                child_env = Environment(parent=callee_val.closure_env)
                for param, arg_val in zip(decl.params, args_vals):
                    child_env.define(param, arg_val)
                try:
                    for stmt in decl.body:
                        self.evaluate(stmt, child_env)
                except ReturnSignal as sig:
                    return sig.value
                return None
            elif callable(callee_val):
                try:
                    return callee_val(*args_vals)
                except Exception as e:
                    raise YOError(f"Error in native function '{node.callee}': {e}")
            else:
                raise TypeMismatch("TASK", get_yo_type(callee_val), node.line)
                
        elif node_type == "UnaryExpr":
            right = self.evaluate(node.right, env)
            if node.op == "NOT":
                return not bool(right)
            elif node.op == "-":
                if not isinstance(right, (int, float)):
                    raise TypeMismatch("NUMBER", get_yo_type(right), node.line)
                return -right
            raise YOError(f"Unknown unary operator '{node.op}'")
            
        elif node_type == "BinaryExpr":
            left = self.evaluate(node.left, env)
            
            # Short-circuit logical operations
            if node.op == "AND":
                if not bool(left):
                    return left
                return self.evaluate(node.right, env)
            if node.op == "OR":
                if bool(left):
                    return left
                return self.evaluate(node.right, env)
                
            right = self.evaluate(node.right, env)
            
            if node.op == "+":
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                if isinstance(left, list) and isinstance(right, list):
                    return left + right
                raise TypeMismatch(f"{get_yo_type(left)}", get_yo_type(right), node.line)
                
            elif node.op == "-":
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeMismatch("NUMBER", f"{get_yo_type(left)} and {get_yo_type(right)}", node.line)
                return left - right
                
            elif node.op == "*":
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeMismatch("NUMBER", f"{get_yo_type(left)} and {get_yo_type(right)}", node.line)
                return left * right
                
            elif node.op == "/":
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeMismatch("NUMBER", f"{get_yo_type(left)} and {get_yo_type(right)}", node.line)
                if right == 0:
                    raise DivisionByZero(node.line)
                return left / right
                
            elif node.op == "%":
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeMismatch("NUMBER", f"{get_yo_type(left)} and {get_yo_type(right)}", node.line)
                if right == 0:
                    raise DivisionByZero(node.line)
                return left % right
                
            elif node.op == "==":
                return left == right
            elif node.op == "!=":
                return left != right
                
            elif node.op in {">", "<", ">=", "<="}:
                is_num_left = isinstance(left, (int, float)) and not isinstance(left, bool)
                is_num_right = isinstance(right, (int, float)) and not isinstance(right, bool)
                if is_num_left and is_num_right:
                    pass
                elif not isinstance(left, type(right)):
                    raise TypeMismatch(get_yo_type(left), get_yo_type(right), node.line)
                if node.op == ">":
                    return left > right
                elif node.op == "<":
                    return left < right
                elif node.op == ">=":
                    return left >= right
                elif node.op == "<=":
                    return left <= right
            
            raise YOError(f"Unknown binary operator '{node.op}'")
            
        raise YOError(f"Unknown AST node type '{node_type}'")
