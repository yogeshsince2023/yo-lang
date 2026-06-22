from dataclasses import dataclass, field
from typing import List, Any, Optional
from errors import InvalidSyntax
from lexer import Token

@dataclass
class ASTNode:
    pass

@dataclass
class Program(ASTNode):
    statements: List[Any]
    type: str = "Program"

@dataclass
class VarDecl(ASTNode):
    name: str
    expression: Any
    line: int
    type: str = "VarDecl"

@dataclass
class SayStmt(ASTNode):
    expression: Any
    line: int
    type: str = "SayStmt"

@dataclass
class AskExpr(ASTNode):
    line: int
    type: str = "AskExpr"

@dataclass
class WhenStmt(ASTNode):
    condition: Any
    then_branch: List[Any]
    else_branch: Optional[List[Any]]
    line: int
    type: str = "WhenStmt"

@dataclass
class RepeatStmt(ASTNode):
    count_expr: Any
    body: List[Any]
    line: int
    type: str = "RepeatStmt"

@dataclass
class ForEachStmt(ASTNode):
    item_name: str
    list_expr: Any
    body: List[Any]
    line: int
    type: str = "ForEachStmt"

@dataclass
class TaskDecl(ASTNode):
    name: str
    params: List[str]
    body: List[Any]
    line: int
    type: str = "TaskDecl"

@dataclass
class CallExpr(ASTNode):
    callee: str
    args: List[Any]
    line: int
    type: str = "CallExpr"

@dataclass
class ReturnStmt(ASTNode):
    expression: Optional[Any]
    line: int
    type: str = "ReturnStmt"

@dataclass
class UseStmt(ASTNode):
    libname: str
    line: int
    type: str = "UseStmt"

@dataclass
class AssignStmt(ASTNode):
    name: str
    expression: Any
    line: int
    type: str = "AssignStmt"

@dataclass
class BinaryExpr(ASTNode):
    left: Any
    op: str
    right: Any
    line: int
    type: str = "BinaryExpr"

@dataclass
class UnaryExpr(ASTNode):
    op: str
    right: Any
    line: int
    type: str = "UnaryExpr"

@dataclass
class LiteralExpr(ASTNode):
    value: Any
    line: int
    type: str = "LiteralExpr"

@dataclass
class IdentifierExpr(ASTNode):
    name: str
    line: int
    type: str = "IdentifierExpr"

@dataclass
class ListExpr(ASTNode):
    elements: List[Any]
    line: int
    type: str = "ListExpr"


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements = []
        while not self.is_at_end():
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements=statements)

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def peek(self) -> Optional[Token]:
        if self.is_at_end():
            return None
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type_: str) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def match(self, *types: str) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def consume(self, type_: str, message: str) -> Token:
        if self.check(type_):
            return self.advance()
        token = self.peek()
        line = token.line if token else (self.tokens[-1].line if self.tokens else 1)
        val = token.value if token else "EOF"
        raise InvalidSyntax(line, str(val), message)

    def statement(self) -> Any:
        if self.match("MAKE"):
            return self.var_declaration()
        if self.match("SAY"):
            return self.say_statement()
        if self.match("WHEN"):
            return self.when_statement()
        if self.match("REPEAT"):
            return self.repeat_statement()
        if self.match("FOR"):
            return self.for_statement()
        if self.match("TASK"):
            return self.task_declaration()
        if self.match("RETURN"):
            return self.return_statement()
        if self.match("USE"):
            return self.use_statement()
        
        return self.expression_statement()

    def var_declaration(self) -> VarDecl:
        line = self.previous().line
        name_tok = self.consume("IDENTIFIER", "Expect variable name after 'make'")
        self.consume("=", "Expect '=' after variable name in declaration")
        expr = self.expression()
        return VarDecl(name=name_tok.value, expression=expr, line=line)

    def say_statement(self) -> SayStmt:
        line = self.previous().line
        expr = self.expression()
        return SayStmt(expression=expr, line=line)

    def when_statement(self) -> WhenStmt:
        line = self.previous().line
        condition = self.expression()
        
        self.consume("{", "Expect '{' before then-branch block")
        then_branch = self.block()
        
        else_branch = None
        if self.match("ELSE"):
            if self.match("{"):
                else_branch = self.block()
            elif self.check("WHEN"):
                self.advance()
                else_branch = [self.when_statement()]
            else:
                token = self.peek()
                raise InvalidSyntax(
                    token.line if token else line, 
                    str(token.value if token else "EOF"), 
                    "Expect '{' or 'when' after 'else'"
                )
        return WhenStmt(condition=condition, then_branch=then_branch, else_branch=else_branch, line=line)

    def block(self) -> List[Any]:
        statements = []
        while not self.check("}") and not self.is_at_end():
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        self.consume("}", "Expect '}' to close block")
        return statements

    def repeat_statement(self) -> RepeatStmt:
        line = self.previous().line
        count_expr = self.expression()
        self.consume("TIMES", "Expect 'times' after repeat count expression")
        self.consume("{", "Expect '{' before repeat block")
        body = self.block()
        return RepeatStmt(count_expr=count_expr, body=body, line=line)

    def for_statement(self) -> ForEachStmt:
        line = self.previous().line
        self.consume("EACH", "Expect 'each' after 'for'")
        item_tok = self.consume("IDENTIFIER", "Expect variable name after 'for each'")
        self.consume("IN", "Expect 'in' after variable name")
        list_expr = self.expression()
        self.consume("{", "Expect '{' before for-loop body")
        body = self.block()
        return ForEachStmt(item_name=item_tok.value, list_expr=list_expr, body=body, line=line)

    def task_declaration(self) -> TaskDecl:
        line = self.previous().line
        name_tok = self.consume("IDENTIFIER", "Expect task name after 'task'")
        self.consume("(", "Expect '(' after task name")
        
        params = []
        if not self.check(")"):
            params.append(self.consume("IDENTIFIER", "Expect parameter name").value)
            while self.match(","):
                params.append(self.consume("IDENTIFIER", "Expect parameter name").value)
                
        self.consume(")", "Expect ')' after parameter list")
        self.consume("{", "Expect '{' before task body block")
        body = self.block()
        return TaskDecl(name=name_tok.value, params=params, body=body, line=line)

    def return_statement(self) -> ReturnStmt:
        line = self.previous().line
        expr = None
        if not self.check("}") and not self.peek_is_statement_start():
            expr = self.expression()
        return ReturnStmt(expression=expr, line=line)

    def peek_is_statement_start(self) -> bool:
        token = self.peek()
        if not token:
            return True
        return token.type in {"MAKE", "SAY", "WHEN", "ELSE", "REPEAT", "TIMES", "FOR", "EACH", "IN", "TASK", "RETURN", "USE"}

    def use_statement(self) -> UseStmt:
        line = self.previous().line
        lib_tok = self.consume("IDENTIFIER", "Expect library name after 'use'")
        return UseStmt(libname=lib_tok.value, line=line)

    def expression_statement(self) -> Any:
        return self.expression()

    def expression(self) -> Any:
        return self.assignment()

    def assignment(self) -> Any:
        expr = self.logical_or()
        
        if self.match("="):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, IdentifierExpr):
                return AssignStmt(name=expr.name, expression=value, line=equals.line)
            raise InvalidSyntax(equals.line, "=", "Invalid assignment target")
            
        return expr

    def logical_or(self) -> Any:
        expr = self.logical_and()
        while self.match("OR"):
            op = self.previous().type
            right = self.logical_and()
            expr = BinaryExpr(left=expr, op=op, right=right, line=self.previous().line)
        return expr

    def logical_and(self) -> Any:
        expr = self.equality()
        while self.match("AND"):
            op = self.previous().type
            right = self.equality()
            expr = BinaryExpr(left=expr, op=op, right=right, line=self.previous().line)
        return expr

    def equality(self) -> Any:
        expr = self.comparison()
        while self.match("==", "!="):
            op = self.previous().type
            right = self.comparison()
            expr = BinaryExpr(left=expr, op=op, right=right, line=self.previous().line)
        return expr

    def comparison(self) -> Any:
        expr = self.term()
        while self.match(">", "<", ">=", "<="):
            op = self.previous().type
            right = self.term()
            expr = BinaryExpr(left=expr, op=op, right=right, line=self.previous().line)
        return expr

    def term(self) -> Any:
        expr = self.factor()
        while self.match("+", "-"):
            op = self.previous().type
            right = self.factor()
            expr = BinaryExpr(left=expr, op=op, right=right, line=self.previous().line)
        return expr

    def factor(self) -> Any:
        expr = self.unary()
        while self.match("*", "/", "%"):
            op = self.previous().type
            right = self.unary()
            expr = BinaryExpr(left=expr, op=op, right=right, line=self.previous().line)
        return expr

    def unary(self) -> Any:
        if self.match("NOT", "-"):
            op = self.previous().type
            right = self.unary()
            return UnaryExpr(op=op, right=right, line=self.previous().line)
        return self.call()

    def call(self) -> Any:
        expr = self.primary()
        
        while True:
            if self.match("("):
                expr = self.finish_call(expr)
            elif self.match("."):
                dot_line = self.previous().line
                member = self.consume("IDENTIFIER", "Expect member name after '.'")
                if isinstance(expr, IdentifierExpr):
                    expr = IdentifierExpr(name=f"{expr.name}.{member.value}", line=dot_line)
                else:
                    raise InvalidSyntax(dot_line, ".", "Member access only supported on identifiers/modules")
            else:
                break
                
        return expr

    def finish_call(self, callee: Any) -> CallExpr:
        line = self.previous().line
        args = []
        if not self.check(")"):
            args.append(self.expression())
            while self.match(","):
                args.append(self.expression())
        self.consume(")", "Expect ')' after arguments")
        
        if isinstance(callee, IdentifierExpr):
            return CallExpr(callee=callee.name, args=args, line=line)
        else:
            raise InvalidSyntax(line, "(", "Can only call functions directly")

    def primary(self) -> Any:
        if self.match("ASK"):
            line = self.previous().line
            self.consume("(", "Expect '(' after 'ask'")
            self.consume(")", "Expect ')' after 'ask('")
            return AskExpr(line=line)
            
        if self.match("BOOL"):
            return LiteralExpr(value=self.previous().value, line=self.previous().line)
            
        if self.match("NUMBER"):
            return LiteralExpr(value=self.previous().value, line=self.previous().line)
            
        if self.match("STRING"):
            return LiteralExpr(value=self.previous().value, line=self.previous().line)
            
        if self.match("IDENTIFIER"):
            return IdentifierExpr(name=self.previous().value, line=self.previous().line)
            
        if self.match("("):
            expr = self.expression()
            self.consume(")", "Expect ')' after expression")
            return expr
            
        if self.match("["):
            line = self.previous().line
            elements = []
            if not self.check("]"):
                elements.append(self.expression())
                while self.match(","):
                    elements.append(self.expression())
            self.consume("]", "Expect ']' after list elements")
            return ListExpr(elements=elements, line=line)
            
        token = self.peek()
        line = token.line if token else (self.tokens[-1].line if self.tokens else 1)
        val = token.value if token else "EOF"
        raise InvalidSyntax(line, str(val), f"Expect expression, got '{val}'")
