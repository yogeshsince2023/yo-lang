"""
YO Language Playground — Flask API
Runs YO code and returns captured output.
"""
import sys
import os
import io
import traceback

# Add project root to path so we can import the yo package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file

app = Flask(__name__)


@app.route("/")
def index():
    """Serve the playground HTML page."""
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    return send_file(html_path)


@app.route("/run", methods=["POST"])
def run_code():
    """Execute YO code and return captured stdout/stderr."""
    data = request.get_json()
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"output": "", "error": ""})

    # Capture stdout
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured_out = io.StringIO()
    captured_err = io.StringIO()
    sys.stdout = captured_out
    sys.stderr = captured_err

    try:
        from yo.lexer import Lexer
        from yo.parser import Parser
        from yo.interpreter import Interpreter
        from yo.environment import Environment
        from yo import errors

        errors.CURRENT_SOURCE = code
        errors.CURRENT_FILENAME = "<playground>"

        # Disable colorama for web output
        errors.USE_COLOR = False

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        env = Environment()
        interpreter.evaluate(ast, env)

        output = captured_out.getvalue()
        error = ""

    except Exception as e:
        output = captured_out.getvalue()
        # Strip ANSI codes from error messages
        error_msg = str(e)
        import re
        error_msg = re.sub(r'\x1b\[[0-9;]*m', '', error_msg)
        error = error_msg

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        # Re-enable color for CLI use
        try:
            from yo import errors
            errors.USE_COLOR = True
        except:
            pass

    return jsonify({"output": output, "error": error})


if __name__ == "__main__":
    print("🚀 YO Playground running at http://localhost:5000")
    app.run(debug=True, port=5000)
