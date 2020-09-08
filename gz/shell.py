from lexer import *
from parser import *

while True:
    text = input('basic > ')
    lexer = Lexer(None, text)
    tokens, err = lexer.make_tokens()
    print(tokens)
    parser = Parser(tokens)
    print(parser.parse())