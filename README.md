# Stack-Based Expression Evaluator

**Course:** DCOMP320 – Data Structures and Algorithms
**Assignment:** Stacks Implementation
**Institution:** Limkokwing University of Creative Technology, Sierra Leone

A Python program that reads mathematical expressions from `input.txt`, evaluates them using a **stack** data structure, and writes the results to `output.txt` in the same layout as the input.

---

## Features

- Custom `Stack` class with `push`, `pop`, `peek`, `is_empty` and `size`
- Two-stack variant of Dijkstra's **Shunting-Yard** algorithm (one stack for operands, one for operators)
- Operators: `+`, `-`, `*`, `/`
- Correct operator precedence and left-to-right associativity (`10 - 4 - 3` = `3`)
- Nested parentheses
- Decimal numbers (`7 / 2` = `3.5`)
- Unary minus (`-3 + 5` = `2`, `2 * -3` = `-6`)
- Works with or without spaces (`(8/4)+7*2`)
- Errors are reported per line and do not stop the program (division by zero, mismatched parentheses, invalid syntax, invalid characters)

---

## Project Files

| File | Purpose |
| --- | --- |
| `expression_evaluator.py` | Main program (Stack class, tokenizer, evaluator, file handling) |
| `test_evaluator.py` | Automated unit tests |
| `input.txt` | Sample input from the assignment |
| `edge_cases.txt` | Extra test expressions (nesting, decimals, errors) |
| `output.txt` | Generated output for `input.txt` |
| `edge_output.txt` | Generated output for `edge_cases.txt` |

---

## Requirements

- Python 3.7 or newer
- No external libraries (uses only `re` and `sys` from the standard library)

---

## How to Run

Run with the default files (`input.txt` → `output.txt`):

```bash
python expression_evaluator.py
```

Run with custom file names:

```bash
python expression_evaluator.py edge_cases.txt edge_output.txt
```

### Run the tests

```bash
python -m unittest -v
```

---

## Input / Output Format

The input file has one expression per line. Expressions are separated by a line of three or more dashes. The output file has the same structure, with each expression replaced by its result. Separator lines and blank lines are copied unchanged.

**input.txt**

```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

**output.txt**

```
13
-----
16
-----
-10
```

> **Note on the sample output:** The assignment sheet shows `17` for `(8 / 4) + 7 * 2`. Working it out by hand: `8 / 4 = 2`, `7 * 2 = 14`, and `2 + 14 = 16`. The mathematically correct answer is **16**, which is what this program produces.

---

## How It Works

The expression is read left to right, one token at a time:

1. **Number** – push onto the operand stack.
2. **`(`** – push onto the operator stack as a marker.
3. **`)`** – apply operators until `(` is on top, then discard the `(`.
4. **Operator** – while the operator on top of the stack has greater or equal precedence (and is not `(`), apply it first; then push the new operator.
5. **End of input** – apply all remaining operators. The single value left on the operand stack is the answer.

Unary minus is detected when `-` appears at the start of an expression, after `(`, or after another operator. It is stored as a special `neg` operator with the highest precedence.

### Program layers

| Layer | Contents |
| --- | --- |
| Data structure | `Stack` class |
| Parsing | `tokenize()` |
| Evaluation | `evaluate_expression()`, `_apply_operator()`, `ExpressionError` |
| Formatting | `format_result()` (prints `13.0` as `13`, keeps `3.5`) |
| File handling | `process_file()`, `main()` |

---

## Test Results

| Expression | Expected | Program Output |
| --- | --- | --- |
| `3 + 5 * 2` | 13 | 13 |
| `(8 / 4) + 7 * 2` | 16 | 16 |
| `10 - (2 + 3) * 4` | -10 | -10 |
| `((2 + 3) * (4 - 1)) / 5` | 3 | 3 |
| `10 - 4 - 3` | 3 | 3 |
| `7 / 2` | 3.5 | 3.5 |
| `-3 + 5` | 2 | 2 |
| `5 / 0` | Error | Error: division by zero |
| `(2 + 3` | Error | Error: mismatched parentheses |

All 10 unit tests in `test_evaluator.py` pass.

---

## Limitations

- Only the four basic operators are supported (no exponent, modulus or functions).
- Decimals use floating-point arithmetic, so results are rounded to 10 significant digits.

## Possible Improvements

- Add exponentiation and modulus
- Support functions such as `sqrt()`
- Use `Fraction` or `Decimal` for exact arithmetic

---

## Author

- **Name:** Abubakarr Bangura
- **Student ID:** 905006219
- **Lecturer:** Hawa Kallon
