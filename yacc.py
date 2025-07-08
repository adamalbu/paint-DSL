import ply.yacc as yacc
from lex import tokens
import ast

py_ast = ast.Module(body=[], type_ignores=[])

def p_program(p):
    """program : program command
               | command"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

    global py_ast
    py_ast = ast.Module(
        body=[ast.Expr(value=cmd, lineno=1, col_offset=0) for cmd in p[0]],
        type_ignores=[]
    )



def p_print(p):
    """command : PRINT expression"""
    p[0] = ast.Call(
        func=ast.Name(id='print', ctx=ast.Load(), lineno=1, col_offset=0),
        args=[p[2]],
        keywords=[],
        lineno=1,
        col_offset=0
    )

def p_string(p):
    """expression : STRING"""
    p[0] = ast.Constant(value=p[1][1:-1], lineno=1, col_offset=0)

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parse_and_execute(file_data, filename):
    parser.parse(file_data)
    exec(compile(py_ast, filename=filename, mode='exec'))