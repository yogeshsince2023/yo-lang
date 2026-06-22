import sys
import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .environment import Environment
from .errors import YOError

def print_usage():
    print("YO Language v1.0")
    print("Usage: python yo.py yourfile.yo")

def start_repl():
    print("YO v1.0 — Interactive Mode")
    print("Type 'exit' to quit, 'clear' to reset variables")
    
    global_env = Environment()
    interpreter = Interpreter()
    from . import errors
    
    while True:
        try:
            line = input("yo> ")
            if not line:
                continue
                
            stripped = line.strip()
            if stripped.lower() == "exit":
                break
            if stripped.lower() == "clear":
                global_env = Environment()
                print("Variables reset.")
                continue
                
            errors.CURRENT_SOURCE = line
            errors.CURRENT_FILENAME = "<repl>"
            
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            if not tokens:
                continue
                
            parser = Parser(tokens)
            ast = parser.parse()
            
            interpreter.evaluate(ast, global_env)
            
        except YOError as e:
            print(e)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting REPL.")
            break
        except Exception as e:
            print(f"Internal Interpreter Error: {e}")

def main():
    if len(sys.argv) < 2:
        start_repl()
        sys.exit(0)

    arg1 = sys.argv[1]
    if arg1 == "run":
        if len(sys.argv) < 3:
            print_usage()
            sys.exit(1)
        filename = sys.argv[2]
    else:
        filename = sys.argv[1]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    from . import errors
    errors.CURRENT_SOURCE = source
    errors.CURRENT_FILENAME = filename

    try:
        # Lexing
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()

        # Executing
        interpreter = Interpreter()
        global_env = Environment()
        interpreter.evaluate(ast, global_env)

    except YOError as e:
        # Print colorized beginner-friendly error
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"Internal Interpreter Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
