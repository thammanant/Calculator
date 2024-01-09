
---

# Tokenizer Instruction Manual

## Overview

This tokenizer is designed to process input files using a set of defined lexical rules and generate tokenized output. It reads an input file, applies the lexical rules specified in the lex file, and produces a tokenized output based on those rules.

## Files

- `64011658_64011594.lex`: Lexical rules file.
- `64011658_64011594.tok`: Tokenized output file.
- `input.txt`: Input file containing expressions to be tokenized.
- `processor.py`: Python script for processing the input file and generating the tokenized output.

## Lexical Rules

The `64011658_64011594.lex` file contains the lexical rules used for tokenization. Each line in the file consists of a token type and its corresponding regular expression pattern. The available token types include POW, ADD, SUB, MUL, INT_DIV, DIV, GTE, GT, LTE, LT, EQ, NEQ, LPAREN, RPAREN, ASSIGN, VAR, REAL, INT, WS (whitespace), and ERR (error).

## Running the Tokenizer

1. **Install Python**: Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Run the Processor Script**:

    Open a terminal or command prompt and navigate to the directory containing `processor.py` and the input files.

    Run the following command:

    ```bash
    python processor.py
    ```

3. **Check Output**:

    The tokenized output will be written to `64011658_64011594.tok`. Open this file to view the tokenized expressions.

## Lexical Rule Modification

If you need to modify the lexical rules, edit the `64011658_64011594.lex` file following the specified format: `TOKEN_TYPE   REGULAR_EXPRESSION`.

## Example Usage

For example, if `input.txt` contains the expression `3+6`, the tokenized output will include tokens like `3/INT +/+ 6/INT`.

---

