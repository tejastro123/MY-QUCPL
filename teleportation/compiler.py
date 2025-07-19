# compiler.py — Compiles QuCPL source to AST and IR

import pathlib
import json
from parser import parse_qucpl

def flatten(x):
    if not isinstance(x, list):
        return [x]
    out = []
    for item in x:
        out.extend(flatten(item))
    return out

def build_maps(qnames, cnames):
    qmap = {str(n): i for i, n in enumerate(qnames)}
    cmap = {str(n): i for i, n in enumerate(cnames)}
    return qmap, cmap

def to_list(n):
    return [] if n is None else (n if isinstance(n, list) else [n])

def compile_stmt(n, qmap, cmap):
    t = n["type"]

    if t == "QubitDecl":
        return []

    if t == "QuantumOp":
        for q in flatten(n["qubits"]):
            if str(q) not in qmap:
                raise ValueError(f"Undefined qubit '{q}' in gate '{n['gate']}'")
        return [{
            "gate": n["gate"],
            "qubits": [qmap[str(q)] for q in flatten(n["qubits"])]
        }]

    if t == "Measure":
        for q in flatten(n["qubits"]):
            if str(q) not in qmap:
                raise ValueError(f"Undefined qubit '{q}' in measurement")
        for c in flatten(n["classical"]):
            if str(c) not in cmap:
                raise ValueError(f"Undefined classical register '{c}' in measurement")
        return [{
            "gate": "measure",
            "qubits": [qmap[str(q)] for q in flatten(n["qubits"])],
            "cregs": [cmap[str(c)] for c in flatten(n["classical"])]
        }]

    if t == "Barrier":
        if not n["qubits"]:
            return [{
                "gate": "barrier",
                "qubits": list(qmap.values())
            }]
        for q in flatten(n["qubits"]):
            if str(q) not in qmap:
                raise ValueError(f"Undefined qubit '{q}' in barrier")
        return [{
            "gate": "barrier",
            "qubits": [qmap[str(q)] for q in flatten(n["qubits"])]
        }]

    if t == "Print":
        return [{
            "gate": "print",
            "args": flatten(n["args"])
        }]

    if t == "Convert":
        return [{
            "op": "convert",
            "value": n["value"]
        }]

    if t == "If":
        cond = n["condition"]
        if str(cond["var"]) not in cmap:
            raise ValueError(f"Undefined classical register '{cond['var']}' in if condition")
        then_block = compile_block(to_list(n["then"]), qmap, cmap)
        else_block = compile_block(to_list(n["else"]), qmap, cmap) if n.get("else") else None
        node = {
            "gate": "if",
            "creg": cmap[str(cond["var"])],
            "val": cond["value"],
            "body": then_block
        }
        if else_block:
            node["else"] = else_block
        return [node]

    raise ValueError(f"Unsupported AST node: {t}")

def compile_block(block, qmap, cmap):
    ir = []
    for stmt in block:
        ir.extend(compile_stmt(stmt, qmap, cmap))
    return ir

def compile_ast(ast):
    if ast.get("type") != "Program":
        ast = {"type": "Program", "body": [ast]}

    qnames = []
    cnames = []

    def collect_names(node):
        if node["type"] == "QubitDecl":
            qnames.extend(flatten(node["qubits"]))
        elif node["type"] == "Measure":
            qnames.extend(flatten(node["qubits"]))
            cnames.extend(flatten(node["classical"]))
        elif node["type"] == "QuantumOp":
            qnames.extend(flatten(node["qubits"]))
        elif node["type"] == "Barrier":
            qnames.extend(flatten(node["qubits"]))
        elif node["type"] == "If":
            cnames.append(node["condition"]["var"])
            for s in to_list(node["then"]):
                collect_names(s)
            if node.get("else"):
                for s in to_list(node["else"]):
                    collect_names(s)

    for stmt in ast["body"]:
        collect_names(stmt)

    qnames = list(dict.fromkeys(qnames))
    cnames = list(dict.fromkeys(cnames))

    qmap, cmap = build_maps(qnames, cnames)
    ir = compile_block(ast["body"], qmap, cmap)

    return {
        "qubits": len(qnames),
        "cregs": len(cnames),
        "oper": ir
    }

if __name__ == "__main__":
    SOURCE = "teleportation.qucpl"
    AST_FILE = "ast.json"
    IR_FILE = "ir.json"

    try:
        code = pathlib.Path(SOURCE).read_text()
        ast = parse_qucpl(code)
        pathlib.Path(AST_FILE).write_text(json.dumps(ast, indent=2))
        print("✅ AST saved to", AST_FILE)

        ir = compile_ast(ast)
        pathlib.Path(IR_FILE).write_text(json.dumps(ir, indent=2))
        print("✅ IR saved to", IR_FILE)

    except FileNotFoundError:
        print(f"❌ Source file '{SOURCE}' not found.")
    except ValueError as e:
        print(f"❌ Compilation error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
