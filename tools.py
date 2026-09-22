import ast
import operator as op
from config import COURSE_FEES


def get_course_fee(course_code):
    course_code = course_code.upper()

    if course_code not in COURSE_FEES:
        return f"Unknown course code: {course_code}"

    return COURSE_FEES[course_code]


def calculate(expression):
    allowed_operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            operator = allowed_operators[type(node.op)]
            return operator(left, right)

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee for a course.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202, or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A mathematical expression such as 12000 + 18000"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# Test the tools
print("get_course_fee('ai202') ->", get_course_fee("ai202"))
print("calculate('(12000 + 18000) * 0.9') ->", calculate("(12000 + 18000) * 0.9"))
print("calculate('15000 - 12000') ->", calculate("15000 - 12000"))