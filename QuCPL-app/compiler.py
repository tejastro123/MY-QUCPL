import json

def flatten(lst):
    if isinstance(lst, list):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(flatten(item))
            else:
                result.append(item)
        return result
    return [lst]

def compile_stmt(stmt):
    stype = stmt["type"]

    if stype == "QubitDecl":
        return ("qubits", flatten(stmt["qubits"]))

    elif stype == "QuantumOp":
        return {
            "op": stmt["gate"],
            "args": flatten(stmt["qubits"])
        }

    elif stype == "Measure":
        return {
            "op": "measure",
            "qubits": flatten(stmt["qubits"]),
            "classical": flatten(stmt["classical"])
        }

    elif stype == "Print":
        return {
            "op": "print",
            "args": flatten(stmt["args"])
        }

    elif stype == "If":
        return {
            "type": "if",
            "condition": stmt["condition"],
            "then": [compile_stmt(stmt["then"])],
            "else": [compile_stmt(stmt["else"])] if stmt["else"] else []
        }

    else:
        raise ValueError(f"Unknown statement type: {stype}")

def ast_to_ir(ast):
    ir = {
        "type": "Program",
        "qubits": [],
        "instructions": [],
        "control_flow": []
    }

    for stmt in ast["body"]:
        compiled = compile_stmt(stmt)
        if isinstance(compiled, tuple) and compiled[0] == "qubits":
            ir["qubits"].extend(compiled[1])
        elif isinstance(compiled, dict) and "op" in compiled:
            ir["instructions"].append(compiled)
        elif isinstance(compiled, dict) and "type" in compiled:
            ir["control_flow"].append(compiled)

    return ir

if __name__ == "__main__":
    with open("teleportation_ast.json") as f:
        ast = json.load(f)

    ir = ast_to_ir(ast)

    with open("teleportation_ir.json", "w") as f:
        json.dump(ir, f, indent=2)

    print("IR saved to teleportation_ir.json")