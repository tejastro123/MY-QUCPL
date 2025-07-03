
# --- Embedded QuCPL grammar ---
grammar = r"""
?start: stmt+

?stmt: qubit_decl ";"
     | qop_stmt ";"
     | measure_stmt ";"
     | print_stmt ";"

qubit_decl: "qubit" id_list
qop_stmt: "qop" GATE_NAME id_list
measure_stmt: "measure" id_list "->" id_list
print_stmt: "print" id_list

id_list: CNAME ("," CNAME)*

GATE_NAME: "h" | "x" | "y" | "z" | "cx" | "cz"

%import common.CNAME
%import common.WS
%ignore WS
%ignore /\/\/.*/

"""

from lark import Lark, Transformer, v_args
import json

# --- Create parser ---
parser = Lark(grammar, parser='lalr', start='start')

# --- AST Builder Transformer ---
@v_args(inline=True)
class ASTBuilder(Transformer):
    def start(self, *stmts): return {"type": "Program", "body": list(stmts)}

    def qubit_decl(self, *ids): return {"type": "QubitDecl", "qubits": list(ids)}
    def qop_stmt(self, gate, *args): return {"type": "QuantumOp", "gate": gate, "qubits": list(args)}
    def measure_stmt(self, *args):
        mid = len(args) // 2
        return {
            "type": "Measure",
            "qubits": list(args[:mid]),
            "classical": list(args[mid:])
        }
    def print_stmt(self, *args): return {"type": "Print", "args": list(args)}

    def id_list(self, *args): return list(args)
    def GATE_NAME(self, token): return str(token)
    def CNAME(self, token): return str(token)

# --- Parsing function ---
def parse_qucpl(source_code):
    tree = parser.parse(source_code)
    return ASTBuilder().transform(tree)

# --- Main script ---
if __name__ == "__main__":
    print("🔹 Enter your QuCPL code (end with a blank line):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        except EOFError:
            break

    code = "\n".join(lines)

    try:
        ast = parse_qucpl(code)
        with open("ast.json", "w") as f:
            json.dump(ast, f, indent=2)
        print("✅ AST saved to ast.json")
    except Exception as e:
        print("❌ Error during parsing:", e)
