import ply.lex as lex

# Define token types
tokens = (
    'INT',
    'REAL',
    'VAR',
    'POW',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'INT_DIVIDE',
    'GREATER',
    'GREATER_EQUAL',
    'LESS',
    'LESS_EQUAL',
    'EQUAL',
    'NOT_EQUAL',
    'LPAREN',
    'RPAREN',
    'LIST',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'PRINT',
    'TRUE',
    'FALSE',
    'ERROR',
)

# Define regex for each token type
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_INT_DIVIDE = r'//'
t_POW = r'\^'
t_GREATER = r'>'
t_GREATER_EQUAL = r'>='
t_LESS = r'<'
t_LESS_EQUAL = r'<='
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_PRINT = r'print'
t_TRUE = r'1'
t_FALSE = r'0'


def t_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.type = 'ERROR'
    t.value = t.value[0]
    t.lexer.skip(1)
    return t


# Ignore whitespace characters
t_ignore = ' \t\n'


# Symbol table to store variables and their values
symbol_table = {}


def create_list(size, initial_value=0):
    return [initial_value] * size


def access_element(var_name, index):
    if var_name in symbol_table and index < len(symbol_table[var_name]):
        return symbol_table[var_name][index]
    else:
        print("Index out of range or variable not found.")
        return None


def update_element(var_name, index, value):
    if var_name in symbol_table and index < len(symbol_table[var_name]):
        symbol_table[var_name][index] = value
    else:
        print("Index out of range or variable not found.")


# Build the lexer
lexer = lex.lex()

# Test the lexer
data = '''
x = list[10]
y = list[2]
x[0] = 1
y[1] = x[0] + 1
print(y[1])
'''

lexer.input(data)

output_file_content = ["PHASE I: LEXICAL ANALYZER"]

# Tokenize the input
line = ""
for tok in lexer:
    if tok.type not in ['ERROR', 'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'PRINT']:
        line += f"{tok.value}/{tok.type} "
    elif tok.type in ['EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL']:
        if tok.type == 'EQUAL':
            line += "1/TRUE "
        else:
            line += "0/FALSE "
    else:
        if line:
            output_file_content.append(line.strip())
            line = ""

# Interpretation of tokens
lexer = lex.lex()
lexer.input(data)

for tok in lexer:
    if tok.type == 'VAR' and lexer.token() and lexer.token().type == 'LBRACKET':
        var_name = tok.value
        lexer.token()  # Move to the LBRACKET token
        lexer.token()  # Move to the index value
        index = lexer.token().value
        lexer.token()  # Move to the RBRACKET token
        lexer.token()  # Move to the ASSIGN token or PLUS, MINUS, etc.
        if lexer.token().type == 'ASSIGN':
            lexer.token()  # Skip the ASSIGN token
            lexer.token()  # Move to the value token
            value = lexer.token().value
            update_element(var_name, index, value)

    # Add other token interpretation logic here for your specific use case

# Write tokenized output to a file
with open("output_file.txt", "w") as output_file:
    for line in output_file_content:
        output_file.write(line + "\n")
