#######################################
# CONSTANT
#######################################

DIGITS = '0123456789'


#######################################
# TOKENS
#######################################

INT = 'Int'
STR = 'Str'
ADD = 'Add'
MIN = 'Min'
MUL = 'Mul'
DIV = 'Div'
LParen = 'LP'
RParen = 'RP'

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# Lexer
#######################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[pos] if self.pos <= len(self.text) else None

    def make_token(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self. current_char in DIGITS:
                tokens.append(self.make_number())
                self.advance()
            elif self. current_char == '+':
                tokens.append(Token(ADD))
                self.advance()
            elif self. current_char == '-':
                tokens.append(Token(MIN))
                self.advance()
            elif self. current_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self. current_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self. current_char == '(':
                tokens.append(Token(LParen))
                self.advance()
            elif self. current_char == ')':
                tokens.append(Token(RParen))
                self.advance()

        return tokens

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
        
        if dot_count == 0:
            return Token(INT, int(num_str))

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error