from lark import Lark, Transformer, v_args

# Load grammar
with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start", parser="lalr")

@v_args(inline=True)
class ASTTransformer(Transformer):
    def convert_command(self, number):
        return {"type": "convert", "value": int(number)}

    def start(self, stmt):
        return stmt  # unwrap Tree('start', [...]) and return just the dict

def parse_code(code):
    tree = parser.parse(code)
    ast = ASTTransformer().transform(tree)
    return ast

