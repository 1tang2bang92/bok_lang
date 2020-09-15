import llvmlite.binding as llvm
import llvmlite.ir as ll

context = llvm.create_context()
module = ll.Module("Entry")
builder = ll.IRBuilder()

i1 = ll.IntType(32)
i8 = ll.IntType(32)
i16 = ll.IntType(32)
i32 = ll.IntType(32)
i64 = ll.IntType(64)

# lprint = ll.Function(module, ll.FunctionType(i64,[i64]), 'print')
# lprint = ll.Function(module, ll.FunctionType(i64,[]), 'input')

namedValues = {}

class Node:
    def __init__(self):
        pass

    def genCode(self):
        raise NotImplementedError
    
    def __repr__(self):
        return NotImplementedError

class NumNode(Node):
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f"{self.num}"

    def genCode(self):
        return ll.Constant(i64, self.num)

class AssignNode(Node):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __repr__(self):
        return f"(Var {self.id} {self.val})"

    def genCode(self):
        var = namedValues[self.id]
        val = self.val.genCode()
        builder.store(val, var)
        return val

class VarNode(Node):
    def __init__(self, id, val):
        self.id = id
        self.val = val

    def __repr__(self):
        return f"(Var {self.id} {self.val})"

    def genCode(self):
        block = builder.block
        builder.position_at_end(block)
        var = builder.alloca(i64, name=self.id)
        val = self.val.genCode()
        builder.store(val, var)
        namedValues[self.id] = var
        return val

class ValNode(Node):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"(Val {self.id})"

    def genCode(self):
        var = namedValues[self.id]
        return builder.load(var, name='loadtemp')

class UnaryNode(Node):
    def __init__(self, op, node1):
        self.op = op
        self.node1 = node1

    def __repr__(self):
        return f"({self.op} {self.node1})"

    def genCode(self):
        if self.op == '-':
            rhs = self.node1.genCode()
            return builder.neg(rhs)

class BinNode(Node):
    def __init__(self, op, node1, node2):
        self.op = op
        self.node1 = node1
        self.node2 = node2

    def __repr__(self):
        return f"({self.op} {self.node1} {self.node2})"

    def genCode(self):
        if self.op == '+':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.add(lhs, rhs, 'addtemp')
        elif self.op == '-':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.sub(lhs, rhs, 'subtemp')
        elif self.op == '*':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.mul(lhs, rhs, 'multemp')
        elif self.op == '/':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.sdiv(lhs, rhs, 'divtemp')
        elif self.op == '==':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.icmp_signed('==', lhs, rhs, 'cmptemp')
        elif self.op == '!=':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.icmp_signed('!=', lhs, rhs, 'cmptemp')
        elif self.op == '>':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.icmp_signed('>', lhs, rhs, 'cmptemp')
        elif self.op == '<':
            lhs = self.node1.genCode()
            rhs = self.node2.genCode()
            return builder.icmp_signed('<', lhs, rhs, 'cmptemp')

class StatementNode(Node):
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return f"(stmt {self.list})"

    def genCode(self):
        result = ll.Constant(i64, 0)
        for x in self.list:
            result = x.genCode()
        return result

class ExternFunctionNode(Node):
    def __init__(self, id, params):
        self.id = id
        self.params = params

    def __repr__(self):
        return f"(extern function {self.id} {self.params})"

    def genCode(self):
        functionType = ll.FunctionType(i64, [i64] * len(self.params))
        function = ll.Function(module, functionType, self.id)

class FunctionNode(Node):
    def __init__(self, id, params, body):
        self.id = id
        self.params = params
        self.body = body

    def __repr__(self):
        return f"(function {self.id} {self.params} {self.body})"

    def genCode(self):
        functionType = ll.FunctionType(i64, [i64] * len(self.params))
        function = ll.Function(module, functionType, self.id)
        namedValues.clear()
        args = function.args
        functionBlock = function.append_basic_block('Entry')
        builder.position_at_end(functionBlock)
        for (x, y) in zip(args, self.params):
            x._set_name(y.id)
            var = builder.alloca(i64, name=y.id)
            val = x
            builder.store(x, var)
            namedValues[y.id] = var
        builder.ret(self.body.genCode())

class CallNode(Node):
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def __repr__(self):
        return f"(call {self.id} {self.args})"

    def genCode(self):
        function = next(filter(lambda x: x._get_name() == self.id, module.functions))
        args = list(map(lambda x: x.genCode(), self.args))
        return builder.call(function, args, name='calltemp')

class CompareNode(Node):
    def __init__(self, co, th, el):
        self.co = co
        self.th = th
        self.el = el

    def __repr__(self):
        return f"(if {self.co} {self.th} {self.el})"

    def genCode(self):
        function = builder.function
        cond = self.co.genCode()
        cond = builder.icmp_signed('!=', cond, ll.Constant(i1, 0), 'cmptemp')

        tb = function.append_basic_block('then')
        eb = function.append_basic_block('else')
        mb = function.append_basic_block('murge')
        builder.cbranch(cond, tb, eb)

        builder.position_at_end(tb)
        tr = self.th.genCode()
        tb = builder.basic_block
        builder.branch(mb)

        builder.position_at_end(eb)

        er = ll.Constant(i64, 0)
        if self.el != None:
            er = self.el.genCode()
            eb = builder.basic_block
        builder.branch(mb)

        builder.position_at_end(mb)
        phi = builder.phi(i64, 'iftemp')
        phi.add_incoming(er, eb)
        phi.add_incoming(tr, tb)

        return phi

class LoopNode(Node):
    def __init__(self, co, bk):
        self.co = co
        self.bk = bk

    def __repr__(self):
        return f"(loop {self.co} {self.bk})"

    def genCode(self):
        function = builder.function
        
        sb = function.append_basic_block('startloop')
        lb = function.append_basic_block('loop')
        eb = function.append_basic_block('endloop')

        builder.branch(sb)

        builder.position_at_end(sb)
        cond = self.co.genCode()
        cond = builder.icmp_signed('!=', cond, ll.Constant(i1, 0), 'cmptemp')
        builder.cbranch(cond, lb, eb)

        builder.position_at_end(lb)
        self.bk.genCode()
        lb = builder.basic_block
        builder.position_at_end(lb)
        builder.branch(sb)

        builder.position_at_end(eb)

        return ll.Constant(i64, 0)

class ReturnNode(Node):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"(return {self.val})"

    def genCode(self):
        val = self.val.genCode()
        builder.ret(val)



class NoneNode(Node):
    def __init__(self):
        pass

    def __repr__(self):
        return f"(None)"