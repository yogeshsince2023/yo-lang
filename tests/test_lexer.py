import pytest
from yo.lexer import Lexer, Token
from yo.errors import InvalidSyntax

def test_lexer_variable_declaration():
    """Test that 'make x = 5' produces correct tokens."""
    lexer = Lexer("make x = 5")
    tokens = lexer.tokenize()
    
    assert len(tokens) == 4
    
    assert tokens[0].type == "MAKE"
    assert tokens[0].value == "make"
    assert tokens[0].line == 1
    
    assert tokens[1].type == "IDENTIFIER"
    assert tokens[1].value == "x"
    assert tokens[1].line == 1
    
    assert tokens[2].type == "="
    assert tokens[2].value == "="
    assert tokens[2].line == 1
    
    assert tokens[3].type == "NUMBER"
    assert tokens[3].value == 5
    assert tokens[3].line == 1

@pytest.mark.parametrize("source,expected_types,expected_values", [
    ("say \"hello\"", ["SAY", "STRING"], ["say", "hello"]),
    ("true and false", ["BOOL", "AND", "BOOL"], [True, "and", False]),
    ("10 + 5.5", ["NUMBER", "+", "NUMBER"], [10, "+", 5.5]),
    ("when x == y {}", ["WHEN", "IDENTIFIER", "==", "IDENTIFIER", "{", "}"], ["when", "x", "==", "y", "{", "}"]),
    ("repeat 3 times", ["REPEAT", "NUMBER", "TIMES"], ["repeat", 3, "times"]),
    ("for each x in [1, 2]", ["FOR", "EACH", "IDENTIFIER", "IN", "[", "NUMBER", ",", "NUMBER", "]"], ["for", "each", "x", "in", "[", 1, ",", 2, "]"]),
])
def test_lexer_parameterized(source, expected_types, expected_values):
    """Test that various source strings produce correct token types and values."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert len(tokens) == len(expected_types)
    for i, token in enumerate(tokens):
        assert token.type == expected_types[i]
        assert token.value == expected_values[i]

def test_lexer_multiline():
    """Test that multi-line inputs track line numbers correctly."""
    source = "make a = 1\nsay a\n# comment on line 3\nmake b = 2"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Expected line numbers:
    # make a = 1 (line 1) -> 4 tokens
    # say a (line 2) -> 2 tokens
    # make b = 2 (line 4) -> 4 tokens
    assert len(tokens) == 10
    
    # line numbers check
    for t in tokens[:4]:
        assert t.line == 1
    for t in tokens[4:6]:
        assert t.line == 2
    for t in tokens[6:]:
        assert t.line == 4

def test_lexer_string_escapes():
    """Test escape sequences inside strings."""
    lexer = Lexer('"line\\nline"')
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].type == "STRING"
    assert tokens[0].value == "line\nline"

def test_lexer_invalid_string():
    """Test that unterminated string raises InvalidSyntax."""
    lexer = Lexer('"unterminated string')
    with pytest.raises(InvalidSyntax) as exc_info:
        lexer.tokenize()
    assert "Close your string" in str(exc_info.value)

def test_lexer_unexpected_char():
    """Test that unexpected characters raise InvalidSyntax."""
    lexer = Lexer("make x = $")
    with pytest.raises(InvalidSyntax) as exc_info:
        lexer.tokenize()
    assert "Unexpected character" in str(exc_info.value)
