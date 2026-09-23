# Calculator Console Rendering Explained

## Overview

The calculator renders results to the console through a collaboration of two files: `main.py` and `pkg/render.py`.

## Step-by-Step Flow

### 1. Entry Point (`main.py`)
- The `main()` function is the starting point.
- It reads the command-line argument, e.g., `python main.py "3 + 5"`.
- Joins all arguments into a single expression string.
- Creates a `Calculator` instance and calls `calculator.evaluate(expression)`.
- If a valid numeric result is returned (not `None`), it passes the expression and result to `format_json_output()`.
- The returned string is printed to the console via `print()`.

### 2. Formatting (`pkg/render.py`)
- `format_json_output(expression, result)` builds a dictionary:
  ```python
  {"expression": expression, "result": result_to_dump}
  ```
- **Smart type handling**: If `result` is a float but represents a whole number (e.g., `5.0`), it converts it to an `int` (e.g., `5`) for cleaner output.
- Uses `json.dumps(data, indent=2)` to produce a **pretty-printed JSON string** with 2-space indentation.

### 3. Console Output Example
Running `python main.py "3 + 5"` produces:
```json
{
  "expression": "3 + 5",
  "result": 8
}
```

Running `python main.py "10 / 2"` produces:
```json
{
  "expression": "10 / 2",
  "result": 5
}
```
Note: `10 / 2` evaluates to `5.0` as a float, but `render.py` converts it to integer `5`.

### 4. Error Cases
- **Empty expression**: Prints `Error: Expression is empty or contains only whitespace.`
- **Invalid input**: Catches the exception and prints `Error: <message>`.

## Complete Data Flow
```
sys.argv → main() → Calculator.evaluate() → format_json_output() → print() → Console (stdout)
```

## Summary
The rendering mechanism is a **two-step pipeline**:
1. **Compute**: `Calculator.evaluate()` parses and evaluates the infix expression using a shunting-yard-like algorithm.
2. **Format & Display**: `format_json_output()` serializes the result as pretty-printed JSON, and `print()` writes it to the console.
