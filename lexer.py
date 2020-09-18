import ply.lex as lex

#reserve word
reserved = {
    'if'      : 'IF',
    'else'    : 'ELSE',
    'loop'    : 'LOOP',
    'fn'      : 'FN',
    'let'     : 'LET',
    'as'      : 'AS',
    'extern'  : 'EXTERN',
    'return'  : 'RETURN',
}

#token
tokens = (
    'NUMBER',
    'ADD','MIN','MUL','DIV','ASSIGN', 'EQ',
    'NE', 'GT', 'LT', 'REF', 'RARROW',
    'LPAREN','RPAREN', 'LBRACE', 'RBRACE',
    'ID', 'COMMA', 'COLON'
) + tuple(reserved.values())

# Tokens
t_ASSIGN  = r'='
t_ADD     = r'\+'
t_MIN     = r'-'
t_MUL     = r'\*'
t_DIV     = r'/'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

t_EQ      = r'=='
t_NE      = r'!='
t_GT      = r'>'
t_LT      = r'<'

t_RARROW   = r'->'

t_COMMA   = r'\,'
t_REF     = r'\&'
t_COLON   = r'\:'

# Ignored characters
t_ignore = " \t"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
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

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'[\'|\"][\s\S]*[\'|\"]'
    t.value = str(t.value)
    return t

# Build the lexer
lex.lex()