# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc
from ast import *

#reserve word
reserved = {
    'if'   : 'IF',
    'else' : 'ELSE',
    'loop' : 'LOOP',
    'fn'   : 'FN',
    }

#token
tokens = (
    'NAME','NUMBER',
    'ADD','MIN','MUL','DIV','EQUALS',
    'LPAREN','RPAREN',
    'ID'
    ) + tuple(reserved.values())

# Tokens
t_ADD     = r'\+'
t_MIN     = r'-'
t_MUL     = r'\*'
t_DIV     = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Ignored characters
t_ignore = " \t"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]'
    t.type = reserved.get(t.value,'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Build the lexer
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left','ADD','MIN'),
    ('left','MUL','DIV'),
    ('right','UMINUS'),
    )

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression ADD expression
                  | expression MIN expression
                  | expression MUL expression
                  | expression DIV expression'''
    if   p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    'expression : MIN expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_error(p):
    print(f"Syntax error at {p.value!r}")

def p_loop(p):
    'expression : loop statement'

yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    yacc.parse(s)