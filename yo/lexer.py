from .errors import InvalidSyntax

class Token:
    def __init__(self, type_, value, line):
        self.type = type_      # string (e.g., "MAKE", "IDENTIFIER", "NUMBER", "+")
        self.value = value    # parsed python value (e.g., str, int, float, bool)
        self.line = line      # line number (1-indexed)

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line})"

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.length = len(source_code)

    def tokenize(self):
        tokens = []
        keywords = {
            'make', 'task', 'when', 'else', 'repeat', 'times', 
            'for', 'each', 'in', 'say', 'ask', 'use', 'return', 
            'and', 'or', 'not'
        }
        
        while self.position < self.length:
            char = self.source[self.position]

            # Newlines
            if char == '\n':
                self.line += 1
                self.position += 1
                continue

            # Whitespace
            if char.isspace():
                self.position += 1
                continue

            # Comments: # until end of line
            if char == '#':
                while self.position < self.length and self.source[self.position] != '\n':
                    self.position += 1
                continue

            # Double character operators/symbols
            if self.position + 1 < self.length:
                two_chars = self.source[self.position : self.position + 2]
                if two_chars in {'==', '!=', '>=', '<='}:
                    tokens.append(Token(two_chars, two_chars, self.line))
                    self.position += 2
                    continue

            # Single character operators/symbols
            if char in {'=', '+', '-', '*', '/', '%', '>', '<', '(', ')', '{', '}', '[', ']', ',', '.'}:
                tokens.append(Token(char, char, self.line))
                self.position += 1
                continue

            # Strings (double-quoted)
            if char == '"':
                start_pos = self.position
                self.position += 1  # skip leading quote
                string_val = []
                closed = False
                while self.position < self.length:
                    curr = self.source[self.position]
                    if curr == '\n':
                        self.line += 1
                    if curr == '"':
                        self.position += 1
                        closed = True
                        break
                    # Handle escape character
                    if curr == '\\' and self.position + 1 < self.length:
                        next_char = self.source[self.position + 1]
                        if next_char == 'n':
                            string_val.append('\n')
                        elif next_char == 't':
                            string_val.append('\t')
                        else:
                            string_val.append(next_char)
                        self.position += 2
                    else:
                        string_val.append(curr)
                        self.position += 1
                
                if not closed:
                    raise InvalidSyntax(
                        self.line, 
                        self.source[start_pos:self.position], 
                        "Close your string with a double quote '\"'"
                    )
                
                tokens.append(Token("STRING", "".join(string_val), self.line))
                continue

            # Numbers (ints and floats)
            if char.isdigit():
                num_str = []
                has_dot = False
                while self.position < self.length:
                    curr = self.source[self.position]
                    if curr.isdigit():
                        num_str.append(curr)
                        self.position += 1
                    elif curr == '.' and not has_dot:
                        # Peek to ensure it is a float digit
                        if self.position + 1 < self.length and self.source[self.position + 1].isdigit():
                            num_str.append('.')
                            has_dot = True
                            self.position += 2  # consume dot and the digit after it
                            num_str.append(self.source[self.position - 1])
                        else:
                            break
                    else:
                        break
                
                val_str = "".join(num_str)
                if has_dot:
                    tokens.append(Token("NUMBER", float(val_str), self.line))
                else:
                    tokens.append(Token("NUMBER", int(val_str), self.line))
                continue

            # Identifiers and keywords
            if char.isalpha() or char == '_':
                ident_chars = []
                while self.position < self.length:
                    curr = self.source[self.position]
                    if curr.isalnum() or curr == '_':
                        ident_chars.append(curr)
                        self.position += 1
                    else:
                        break
                
                ident_str = "".join(ident_chars)
                if ident_str in keywords:
                    tokens.append(Token(ident_str.upper(), ident_str, self.line))
                elif ident_str == 'true':
                    tokens.append(Token("BOOL", True, self.line))
                elif ident_str == 'false':
                    tokens.append(Token("BOOL", False, self.line))
                else:
                    tokens.append(Token("IDENTIFIER", ident_str, self.line))
                continue

            # Unknown character
            raise InvalidSyntax(self.line, char, f"Unexpected character '{char}'")

        return tokens
