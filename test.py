import re

# Define the token regular expressions
patterns = {
    'INT': r'[0-9]+',
    'REAL': r'[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?',
    'POW': r'\^',
    'VAR': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'ADD': r'\+',
    'SUB': r'-',
    'MUL': r'\*',
    'DIV': r'/',
    'INT_DIV': r'//',
    'GT': r'>',
    'GTE': r'>=',
    'LT': r'<',
    'LTE': r'<=',
    'EQ': r'==',
    'NEQ': r'!=',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'ASSIGN': r'=',
    'LIST': r'list\[[0-9]+\]'
}


# Tokenizing function
def tokenize(input_string):
    tokens = []
    # remove all whitespace
    input_string = input_string.replace(" ", "")
    while input_string:
        match = None
        for token_type, pattern in patterns.items():
            regex = re.compile(r'\A(' + pattern + r')')
            match = regex.match(input_string)
            if match:
                value = match.group(1)
                tokens.append((value, token_type))
                input_string = input_string[match.end():]
                break
        if not match:
            print("Error: Invalid token at '{}'".format(input_string[0]))
            return tokens
    return tokens


# Example input
input_expr = input("Enter an expression: ")

# Tokenize the input expression
tokens = tokenize(input_expr)
for token in tokens:
    print(f"{token[0]}/{token[1]}", end=" ")
