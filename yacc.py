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
        body=p[0],
        type_ignores=[]
    )

def p_print(p):
    'command : PRINT expression'
    p[0] = ast.Expr(
        value=ast.Call(
            func=ast.Name(id='print', ctx=ast.Load(), lineno=p.lineno(1), col_offset=p.lexpos(1)),
            args=[p[2]],
            keywords=[],
            lineno=p.lineno(1),
            col_offset=p.lexpos(1)
        ),
        lineno=p.lineno(1),
        col_offset=p.lexpos(1)
    )

def p_assign(p):
    'command : ID EQUALS expression'
    p[0] = ast.Assign(
        targets=[ast.Name(id=p[1], ctx=ast.Store(), lineno=p.lineno(1), col_offset=p.lexpos(1))],
        value=p[3],
        lineno=p.lineno(2),
        col_offset=p.lexpos(2)
    )

def p_load(p):
    'expression : ID'
    p[0] = ast.Name(id=p[1], ctx=ast.Load(), lineno=p.lineno(1), col_offset=p.lexpos(1))

def p_expression_string(p):
    'expression : STRING'
    p[0] = ast.Constant(value=p[1][1:-1], lineno=p.lineno(1), col_offset=p.lexpos(1))  # Remove quotes


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