# Based on asteval
from treelib import Node, Tree
from depexpressions import Expression
import ast
from asteval import Interpreter
import re

class FuncLister(ast.NodeVisitor):
    def __init__(self):
        self.visiting_call = False
        self.variables = []
        super().__init__()

    def visit_Call(self, node):
        self.visiting_call = True
        self.generic_visit(node)
        self.visiting_call = False

    def visit_Name(self, node):
        if self.visiting_call:
            self.visiting_call = False
        else:
            self.variables.append(node.id)
        self.generic_visit(node)

    def visit(self, tree):
        super().visit(tree)
        return self.variables

tree = ast.parse("x*y+abs(z,sin(e))+26")
out = FuncLister().visit(tree)
print(out)

def get_path(tree, node):
    if tree.get_node(node) is None:
        return None
    path = node
    while tree.get_node(node).bpointer is not None:
        node = tree.get_node(node).bpointer
        path = "{node_name}_{path}".format(path=path, node_name=node)
    return path

class MRS_Node(Node):
    def __init__(self, tree, name, identifier):
        self.tree = tree
        self.executables = {}
        super().__init__(name, identifier)

    def resolve(self, a):
        return "{id}_{varname}".format(id=self.identifier,varname=a)

    def resolve_list(self, b):
        return [self.resolve(elt) if elt not in self.tree else elt for elt in b]

    def add_executable(self, a, ast_str):
        resolved_a = self.resolve(a)
        tree = ast.parse(ast_str)  # need to handle syntax errors
        vars = FuncLister().visit(tree)
        #print(vars)
        resolved_b = self.resolve_list(vars)
        #print(resolved_b)

        if resolved_a not in self.tree:
            executable = Executable(">"+a, resolved_a, resolved_b, ast_str)
            self.tree.add_node(executable, self.identifier)
        else:
            #print("updating", resolved_a, ast_str)
            self.tree.get_node(resolved_a).execute_str = ast_str

        topo = self.tree.expressions.add(resolved_a, resolved_b)
        #print("e.add({a},{b})".format(a=resolved_a,b=resolved_b))
        #print("topo={topo}".format(topo=topo))
        return self.tree.eval_topo(topo)

class Executable(Node):
    def __init__(self, var_name, full_var_name, var_dep, execute_str):
        self.var_dep = var_dep
        self.execute_str = execute_str
        super().__init__(var_name, full_var_name)

class ModelReferenceSystem(Tree):
    def __init__(self):
        self.expressions = Expression()
        self.interpreter = Interpreter()
        super().__init__()

    def create_node(self, name, parent=None):
        if parent is not None:
            id = "{id}_{name}".format(id=parent, name=name)
        else:
            id = name
        print(name, id, parent)
        mrs_node = MRS_Node(self, name, id)
        return self.add_node(mrs_node, parent)

    def eval_topo(self, topo):
        for idx, elt in enumerate(topo):
            ast_executable_extended = "{id}={expr}".format(id=elt,
            expr=self.get_node(elt).execute_str)
            print(idx, ast_executable_extended)
            self.interpreter.eval(ast_executable_extended)
        #print(self.interpreter.symtable)
        return self.interpreter.symtable

mrs = ModelReferenceSystem()
mrs.create_node("saturnv")
mrs.create_node("rocket", "saturnv")
mrs.create_node("apollo", "saturnv_rocket")
mrs.create_node("cm", "saturnv_rocket_apollo")
mrs.create_node("les", "saturnv_rocket_apollo")
mrs.create_node("lm", "saturnv_rocket_apollo")
mrs.create_node("sm", "saturnv_rocket_apollo")
mrs.create_node("sic", "saturnv_rocket")
mrs.create_node("sii", "saturnv_rocket")
mrs.create_node("sivb", "saturnv_rocket")

mrs.get_node('saturnv_rocket_apollo_cm').add_executable("mass", "15");
mrs.get_node('saturnv_rocket_apollo_les').add_executable("mass", "35");
mrs.get_node('saturnv_rocket_apollo_lm').add_executable("mass", "35");

mrs.get_node('saturnv_rocket_apollo').add_executable("mass", "saturnv_rocket_apollo_cm_mass+saturnv_rocket_apollo_les_mass+saturnv_rocket_apollo_lm_mass");
symtable["saturnv_rocket_apollo_mass"]

print(mrs)



mrs.expressions.G.topo
# sum of children should automatically propagate this
tree.get_node('apollo').data.e.add("mass",["cm.mass"])
tree.get_node("saturnv").bpointer==None
