
From parser.ipynb:

Loads grammar.lark 

Parses source code → AST using Lark

Saves as ast.json

```
from lark import Lark, Transformer, v_args
import json

with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, parser='lalr', start='start')

@v_args(inline=True)
class ASTBuilder(Transformer):
    def start(self, *stmts): return {"type": "Program", "body": list(stmts)}

    def qubit_decl(self, *ids): return {"type": "QubitDecl", "qubits": list(ids)}
    def qop_stmt(self, gate, args): return {"type": "QuantumOp", "gate": gate, "qubits": args}

    def measure_stmt(self, *args): 
        mid = len(args) // 2
        return {"type": "Measure", "qubits": list(args[:mid]), "classical": list(args[mid:])}
    def print_stmt(self, *args): return {"type": "Print", "args": list(args)}

    def if_stmt(self, cond, *blocks):
        if_block = blocks[0]
        else_block = blocks[1] if len(blocks) > 1 else None
        return {
            "type": "If",
            "condition": cond,
            "then": if_block,
            "else": else_block
        }

    def condition(self, var, val):
        return {"type": "Condition", "var": var, "value": int(val)}

    def id_list(self, *args): return list(args)
    def GATE_NAME(self, token): return str(token)
    def CNAME(self, token): return str(token)
    def INT(self, token): return int(token)
    def stmt(self, stmt): return stmt

def parse_qucpl(source_code):
    tree = parser.parse(source_code)
    return ASTBuilder().transform(tree)

if name == "main":
    print("Enter your QuCPL code (end with a blank line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    code = "\n".join(lines)

    try:
        ast = parse_qucpl(code)
        with open("teleportation_ast.json", "w") as f:
            json.dump(ast, f, indent=2)
        print("AST saved to teleportation_ast.json")
    except Exception as e:
        print("Error during parsing:", e)
```
The output is an abstract syntax tree (AST) used by the compiler.