#######################################
# Import
#######################################

from token import *
from ast import *

#######################################
# Parser
#######################################

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.cur_token = None
    self.size = len(self.tokens)
    self.idx = -1
    self.next()

  def next(self):
    self.cur_token = self.nextToken()
  
  def nextToken(self):
    if self.idx < self.size - 1:
      self.idx += 1
      return self.tokens[self.idx]
    else:
      return self.tokens[self.idx]

  def parse(self):
    return self.parseStatment()
  
  def parseStatment(self):
    list = []
    if self.cur_token == TT_LBRACE:
      self.next()
      while self.cur_token != TT_RBRACE:
        list.append(self.parseExpression())
        self.next()
    else:
      list.append(self.parseExpression())
    return list
        
  def parseExpression(self):
    return self.parseAssign()

  def parseAssign(self):
    node1 = self.parseSum()
    while True:
      if self.cur_token.type == TT_ASSIGN:
        token = self.cur_token
        self.next()
        node2 = self.parseAssign()
        node1 = BinOpNode(node1, token, node2)
        self.next()
      else:
        break
    return node1

  def parseSum(self):
    node1 = self.parseProduct()
    while True:
      if self.cur_token.type == TT_ADD:
        token = self.cur_token
        self.next()
        node2 = self.parseProduct()
        node1 = BinOpNode(node1, token, node2)
        self.next()
      elif self.cur_token.type == TT_SUB:
        token = self.cur_token
        self.next()
        node2 = self.parseProduct()
        print(node2)
        node1 = BinOpNode(node1, token, node2)
        self.next()
      else:
        break
    return node1
  
  def parseProduct(self):
    node1 = self.parseFactor()
    while True:
      if self.cur_token.type == TT_MUL:
        token = self.cur_token
        self.next()
        node2 = self.parseFactor()
        node1 = BinOpNode(node1, token, node2)
        self.next()
      elif self.cur_token.type == TT_DIV:
        token = self.cur_token
        self.next()
        node2 = self.parseFactor()
        node1 = BinOpNode(node1, token, node2)
        self.next()
      else:
        break
    return node1

  def parseFactor(self):
    while True:
      if self.cur_token.type == TT_IDENTIFIER:
        result = self.cur_token
        self.next()
        if self.cur_token.type == TT_LPAREN:
          return self.parseCall(result)
        else:
          return VariableNode(result)
      elif self.cur_token.type == TT_INT:
        result = self.cur_token
        self.next()
        return NumberNode(result)
      else:
        return Token(TT_EOF)

  def parseCall(self, ident):
    self.next()
    varlist = []
    while True:
      if self.cur_token.type == TT_RPAREN:
        self.next()
        break
      elif self.cur_token.type == TT_IDENTIFIER:
        varlist.append(VariableNode(self.cur_token))
        self.next()
      elif self.cur_token.type == TT_INT:
        varlist.append(NumberNode(self.cur_token))
        self.next()
      elif self.cur_token.type == TT_COMMA:
        self.next()
      else:
        return Token(TT_EOF)
    return CallNode(ident, varlist)


    
    
    
