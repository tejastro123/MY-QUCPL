def compile_ast_to_ir(ast):
    if ast["type"] == "convert":
        number = ast["value"]
        bin_str = bin(number)[2:]
        return {
            "type": "program",
            "decimal": number,
            "binary": bin_str,
            "instructions": [
                {"gate": "x", "target": i}
                for i, b in enumerate(reversed(bin_str)) if b == '1'
            ]
        }
    else:
        raise ValueError("Unknown AST type")
