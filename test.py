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

# Read input file
with open("input_file.txt", "r") as input_file:
    input_data = input_file.readlines()

output_file_content = []

for line in input_data:
    lexer.input(line.strip())
    tokens = []

    # Tokenize each line and generate assembly-like code
    assembly_code = ""
    result_var = ""
    for tok in lexer:
        if tok.type not in ['ERROR', 'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'PRINT']:
            tokens.append(f"{tok.value}/{tok.type}")
        elif tok.type in ['EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL']:
            if tok.type == 'EQUAL':
                tokens.append("=/= ")
            else:
                tokens.append("!=/= ")
        else:
            tokens.append(f"{tok.value}/{tok.type}")

        # Generate assembly code
        if tok.type in ['INT', 'REAL', 'VAR']:
            assembly_code += f"LOAD {tok.value}\n"
            result_var = tok.value
        elif tok.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'INT_DIVIDE', 'POW']:
            assembly_code += f"{tok.type}\n"
        elif tok.type in ['EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL']:
            assembly_code += f"{tok.type}\n"
            result_var = "print"  # Logical expression sets result to 'print'
        elif tok.type == 'PRINT':
            if result_var != "print":
                assembly_code += f"STORE print\n"
            output_file_content.append(assembly_code)
            tokens = []
            assembly_code = ""
            result_var = ""

    # Add the last statement to output if any
    if assembly_code:
        if result_var != "print":
            assembly_code += f"STORE print\n"
        output_file_content.append(assembly_code)

# Write assembly-like output to a file
with open("assembly_output.txt", "w") as output_file:
    output_file.write("\n".join(output_file_content))