import parser
import generator

file = open('main.bk')
s = file.read()

ast = parser.parse(s)
ast.genCode()
generator.generate()