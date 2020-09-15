import ply.yacc as yacc
from lexer import *
from ast import *

# Precedence rules for the arithmetic operators
precedence = (
    ('right','ASSIGN'),
    ('left','EQ','NE','GT','LT'),
    ('left','ADD','MIN'),
    ('left','MUL','DIV'),
    ('right','MIN'),
    ('right','REF','DEREF')
)

### block
def p_program(p):
    'program : block'
    p[0] = p[1]

def p_block(p):
    'block : decls'
    p[0] = StatementNode(p[1])

def p_decls_1(p):
    'decls : decl'
    p[0] = [p[1]]

def p_decls_2(p):
    'decls : decls decl'
    p[1].append(p[2])
    p[0] = p[1]

def p_decl(p):
    'decl : statement'
    p[0] = p[1]

def p_statement(p):
    '''
    statement : expression_statement
              | compound_statement
    '''
    p[0] = p[1]

def p_expression_statement(p):
    'expression_statement : expression'
    p[0] = p[1]

def p_compound_statement_1(p):
    'compound_statement : LBRACE statement_list RBRACE'
    p[0] = StatementNode(p[2])

def p_compound_statement_2(p):
    'compound_statement : LBRACE RBRACE'
    p[0] = StatementNode([])

def p_statement_list_1(p):
    'statement_list : statement'
    p[0] = [p[1]]

def p_statement_list_2(p):
    'statement_list : statement_list statement'
    p[1].append(p[2])
    p[0] = p[1]

def p_statement_extern_function(p):
    'expression : EXTERN FN ID prototype'
    p[0] = ExternFunctionNode(p[3], p[4])

def p_statement_function(p):
    'expression : FN ID prototype statement'
    p[0] = FunctionNode(p[2], p[3], p[4])

def p_statement_prototype_1(p):
    'prototype : LPAREN RPAREN'
    p[0] = []

def p_statement_prototype_2(p):
    'prototype : LPAREN param_list RPAREN'
    p[0] = p[2]

def p_statement_param_list(p):
    'param_list : param'
    p[0] = [p[1]]

def p_statement_parame_list(p):
    'param_list : param_list COMMA param'
    p[1].append(p[3])
    p[0] = p[1]

def p_statement_param(p):
    'param : ID'
    p[0] = ValNode(p[1])

def p_expression_binop(p):
    '''
    expression : expression ADD expression
               | expression MIN expression
               | expression MUL expression
               | expression DIV expression
               | expression EQ expression
               | expression NE expression
               | expression GT expression
               | expression LT expression
    '''
    p[0] = BinNode(p[2], p[1], p[3])

def p_expression_let_assign_1(p):
    'expression : LET ID ASSIGN expression'
    p[0] = VarNode(p[2], None, p[4])

def p_expression_let_assign_2(p):
    'expression : LET ID COLON ID ASSIGN expression'
    p[0] = VarNode(p[2], p[4], p[6])

def p_expression_let_assign_3(p):
    'expression : LET ID COLON MUL ID ASSIGN expression'
    p[0] = VarNode(p[2], '*' + p[5], p[7])

def p_expression_ref(p):
    'expression : REF ID'
    p[0] = UnaryNode(p[1], ValNode(p[2]))

def p_expression_deref(p):
    'expression : DEREF ID'
    p[0] = UnaryNode(p[1], ValNode(p[2]))

def p_expression_loop_1(p):
    'expression : LOOP statement'
    p[0] = LoopNode(NumNode(1), p[2])

def p_expression_loop_2(p):
    'expression : LOOP expression statement'
    p[0] = LoopNode(p[2], p[3])

def p_expression_assign(p):
    'expression : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

def p_expression_uminus(p):
    'expression : MIN expression'
    # 'expression : MIN expression %prec UMINUS'
    p[0] = UnaryNode(p[1], p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumNode(p[1])

def p_expression_name(p):
    'expression : ID'
    p[0] = ValNode(p[1])

def p_expression_call_1(p):
    'expression : ID LPAREN RPAREN'
    p[0] = CallNode(p[1], [])

def p_expression_call_2(p):
    'expression : ID LPAREN args RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_expression_args_1(p):
    'args : arg'
    p[0] = [p[1]]

def p_expression_args_2(p):
    'args : args COMMA arg'
    p[1].append(p[3])
    p[0] = p[1]

def p_expression_arg_1(p):
    'arg : expression'
    p[0] = p[1]


def p_if_then_expression(p):
    'expression : IF expression statement'
    p[0] = CompareNode(p[2], p[3], None)

def p_if_else_expression(p):
    'expression : IF expression statement ELSE statement'
    p[0] = CompareNode(p[2], p[3], p[5])
    
def p_error(p):
    print(f"Syntax error at {p.value!r}")

yacc.yacc()

def parse(s):
    return yacc.parse(s)

