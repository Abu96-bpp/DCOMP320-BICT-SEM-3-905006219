"""
DCOMP320 - Data Structures and Algorithms
Assignment: Stacks Implementation

Evaluates mathematical expressions read from input.txt using a two-stack
variant of Dijkstra's Shunting-Yard algorithm and writes the results to
output.txt, keeping the same layout (separator lines are copied unchanged).

Supported: + - * /  nested parentheses, decimal numbers, unary minus.

Usage:
    python expression_evaluator.py                 # input.txt -> output.txt
    python expression_evaluator.py in.txt out.txt  # custom file names
"""

import re
import sys


# --------------------------------------------------------------------------
# Layer 1: Data structure
# --------------------------------------------------------------------------
class Stack:
    """LIFO stack built on a Python list (end of list = top of stack)."""

    def __init__(self):
        self._items = []          # private: only changed via stack operations

    def push(self, item):
        """Place an item on top of the stack. O(1)."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True when the stack holds no items."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items currently stored."""
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


# --------------------------------------------------------------------------
# Layer 2: Parsing
# --------------------------------------------------------------------------
class ExpressionError(Exception):
    """Raised for invalid expressions (bad characters, syntax, div by zero...)."""


_TOKEN_RE = re.compile(r"\s*(?:(\d+\.?\d*|\.\d+)|(.))")


def tokenize(expression):
    """Split a string into numbers, operators and parentheses.

    "(8 / 4) + 7 * 2" -> ["(", "8", "/", "4", ")", "+", "7", "*", "2"]
    """
    tokens = []
    pos = 0
    expression = expression.rstrip()
    while pos < len(expression):
        match = _TOKEN_RE.match(expression, pos)
        if not match:
            break
        number, other = match.group(1), match.group(2)
        if number is not None:
            tokens.append(number)
        elif other in "+-*/()":
            tokens.append(other)
        else:
            raise ExpressionError(f"invalid character '{other}'")
        pos = match.end()
    return tokens


# --------------------------------------------------------------------------
# Layer 3: Evaluation
# --------------------------------------------------------------------------
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "neg": 3}


def _apply_operator(operators, operands):
    """Pop one operator and its operand(s), compute, push the result."""
    op = operators.pop()
    try:
        if op == "neg":                      # unary minus needs one operand
            operands.push(-operands.pop())
            return
        b = operands.pop()
        a = operands.pop()
    except IndexError:
        raise ExpressionError("invalid expression")

    if op == "+":
        operands.push(a + b)
    elif op == "-":
        operands.push(a - b)
    elif op == "*":
        operands.push(a * b)
    elif op == "/":
        if b == 0:
            raise ExpressionError("division by zero")
        operands.push(a / b)


def evaluate_expression(expression):
    """Evaluate an infix expression using an operand stack and operator stack."""
    tokens = tokenize(expression)
    if not tokens:
        raise ExpressionError("empty expression")

    operands = Stack()
    operators = Stack()
    expect_operand = True    # is a number, "(" or unary minus legal next?

    for token in tokens:
        if token[0].isdigit() or token[0] == ".":         # number
            if not expect_operand:
                raise ExpressionError("invalid expression")
            operands.push(float(token))
            expect_operand = False

        elif token == "(":
            if not expect_operand:
                raise ExpressionError("invalid expression")
            operators.push("(")

        elif token == ")":
            if expect_operand:
                raise ExpressionError("invalid expression")
            while not operators.is_empty() and operators.peek() != "(":
                _apply_operator(operators, operands)
            if operators.is_empty():
                raise ExpressionError("mismatched parentheses")
            operators.pop()                               # discard "("

        else:                                             # + - * /
            if expect_operand:
                if token == "-":                          # unary minus
                    operators.push("neg")
                    continue
                raise ExpressionError("invalid expression")
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]):
                _apply_operator(operators, operands)
            operators.push(token)
            expect_operand = True

    if expect_operand:                                    # e.g. "2 +"
        raise ExpressionError("invalid expression")

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ExpressionError("mismatched parentheses")
        _apply_operator(operators, operands)

    result = operands.pop()
    if not operands.is_empty():
        raise ExpressionError("invalid expression")
    return result


# --------------------------------------------------------------------------
# Layer 4: Formatting
# --------------------------------------------------------------------------
def format_result(value):
    """Print 13.0 as 13 and keep decimals such as 3.5 (10 significant digits)."""
    value = float(f"{value:.10g}")
    if value == int(value):
        return str(int(value))
    return str(value)


# --------------------------------------------------------------------------
# Layer 5: File handling
# --------------------------------------------------------------------------
_SEPARATOR_RE = re.compile(r"^\s*-{3,}\s*$")


def process_file(input_path="input.txt", output_path="output.txt"):
    """Evaluate every expression line; copy separators and blank lines as-is."""
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        for raw_line in infile:
            line = raw_line.rstrip("\n")
            if line.strip() == "" or _SEPARATOR_RE.match(line):
                outfile.write(line + "\n")
                continue
            try:
                outfile.write(format_result(evaluate_expression(line)) + "\n")
            except ExpressionError as err:
                outfile.write(f"Error: {err}\n")


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    try:
        process_file(input_path, output_path)
    except FileNotFoundError:
        print(f"Could not find input file: {input_path}")
        sys.exit(1)
    print(f"Done. Results written to {output_path}")


if __name__ == "__main__":
    main()
