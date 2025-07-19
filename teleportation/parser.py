from lark import Lark, Transformer, v_args
import json

# Load grammar from grammar.lark file
with open("grammar.lark") as f:
    grammar = f.read()

# Create parser
parser = Lark(grammar, parser='lalr', start='start')

# Transformer to convert parse tree to AST
@v_args(inline=True)
class ASTBuilder(Transformer):

    def start(self, *stmts):
        return {"type": "Program", "body": list(stmts)}

    def qubit_decl(self, *ids):
        return {"type": "QubitDecl", "qubits": list(ids)}

    def qop_stmt(self, gate, *args):
        return {"type": "QuantumOp", "gate": gate, "qubits": list(args)}

    def measure_stmt(self, *args):
        mid = len(args) // 2
        return {
            "type": "Measure",
            "qubits": list(args[:mid]),
            "classical": list(args[mid:])
        }

    def barrier_stmt(self, *args):
        return {
            "type": "Barrier",
            "qubits": list(args) if args else []  # Optional qubit list
        }

    def print_stmt(self, *args):
        return {"type": "Print", "args": list(args)}

    def convert_command(self, value):
        return {"type": "Convert", "value": int(value)}

    def if_stmt(self, cond, then_block, else_block=None):
        return {
            "type": "If",
            "condition": cond,
            "then": then_block,
            "else": else_block if else_block else None
        }

    def condition(self, var, val):
        return {"type": "Condition", "var": var, "value": int(val)}

    def id_list(self, *args):
        return list(args)

    def stmt(self, *args):
        return args[0]

    def GATE_NAME(self, token):
        return str(token)

    def CNAME(self, token):
        return str(token)

    def INT(self, token):
        return int(token)

    def DECIMAL(self, token):
        return int(token)

def parse_qucpl(source_code: str):
    tree = parser.parse(source_code)
    return ASTBuilder().transform(tree)

# Command-line entry point
if __name__ == "__main__":
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
        with open("ast.json", "w") as f:
            json.dump(ast, f, indent=2)
        print("✅ AST saved to ast.json")
    except Exception as e:
        print("❌ Error during parsing:", e)
