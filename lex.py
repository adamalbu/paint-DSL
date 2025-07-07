import ply.lex as lex

reserved = {
    "print" : "PRINT",
}

tokens = (
    "EQUALS",
    "STRING",
    "ID",
    "NEWLINE",
) + tuple(reserved.values())

t_EQUALS = r"="

def t_STRING(t):
    r'"[^"]*"'
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

with open('demo.paint', 'r') as file:
    data = file.read()
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break
