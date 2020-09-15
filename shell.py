import parser
import generator

file = open('main.bk')
s = file.read()

ast = parser.parse(s)
print(ast)
ast.genCode()
generator.generate()