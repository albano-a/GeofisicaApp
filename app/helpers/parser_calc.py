from lark import Lark, Transformer, v_args
import math

# Grammar for mathematical expressions
grammar = """
    ?start: expr

    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub

    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div

    ?factor: power
           | "+" factor   -> pos
           | "-" factor   -> neg

    ?power: atom
          | atom "^" factor -> pow

    ?atom: NUMBER           -> number
         | NAME             -> variable
         | NAME "(" expr ")" -> function
         | "(" expr ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)
class MathTransformer(Transformer):
    def number(self, n):
        return float(n)

    def variable(self, name):
        # Define common variables
        variables = {"x": 0, "pi": math.pi, "e": math.e}
        return variables.get(str(name), 0)

    def function(self, name, arg):
        functions = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "ln": math.log,
            "sqrt": math.sqrt,
            "abs": abs,
        }
        return functions.get(str(name), lambda x: x)(arg)

    def add(self, left, right):
        return left + right

    def sub(self, left, right):
        return left - right

    def mul(self, left, right):
        return left * right

    def div(self, left, right):
        return left / right if right != 0 else float("inf")

    def pow(self, base, exp):
        return base**exp

    def pos(self, value):
        return +value

    def neg(self, value):
        return -value


# Create parser and transformer separately
math_parser = Lark(grammar, parser="lalr")  # Changed from 'earley' to 'lalr'