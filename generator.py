import llvmlite.binding as llvm
import llvmlite.ir as ll
from ast import *
import print as p
import input as i

def generate():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    llvm.initialize_native_asmparser

    target = llvm.Target.from_default_triple()
    targetMachine = target.create_target_machine('generic', opt=3)
    module.triple = target.triple
    module.data_layout = targetMachine.target_data
    
    strmod = str(module)

    file = open('target/output.ll','w')
    file.write(strmod)
    file.close()

    llinput = llvm.parse_assembly(i.ir)
    llprint = llvm.parse_assembly(p.ir)
    llmod = llvm.parse_assembly(strmod)

    mpm = llvm.create_module_pass_manager()
    mpm.add_instruction_combining_pass()
    mpm.add_gvn_pass()
    mpm.add_cfg_simplification_pass()
    mpm.add_basic_alias_analysis_pass()
    mpm.add_instruction_combining_pass()
    mpm.run(llmod)


    file = open('target/print.o','wb')
    bytes = targetMachine.emit_object(llprint)
    file.write(bytes)
    file.close()

    file = open('target/input.o','wb')
    bytes = targetMachine.emit_object(llinput)
    file.write(bytes)
    file.close()

    file = open('target/output.o','wb')
    bytes = targetMachine.emit_object(llmod)
    file.write(bytes)
    file.close()

    # file = open('output.o','wb')
    # bytes = targetMachine.emit_object(llprint)
    # file.write(bytes)
    # bytes = targetMachine.emit_object(llmod)
    # file.write(bytes)
    # file.close()

    file = open('target/output.o.ll','w')
    file.write(str(llmod))
    file.close()