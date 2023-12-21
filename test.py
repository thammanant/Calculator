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
assembly_file_content = []

for line in input_data:
    lexer.input(line.strip())
    tokens = []

    # Tokenize each line
    tokenized_line = ""
    assembly_code = ""
    result_var = ""
    for tok in lexer:
        if tok.type in tokens:
            if tok.type not in ['ERROR', 'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS', 'GREATER_EQUAL',
                                'LESS_EQUAL', 'PRINT']:
                tokens.append(f"{tok.value}/{tok.type}")
            else:
                tokens.append(f"{tok.value}/{tok.type}")

        # Tokenized line for output file
        tokenized_line += f"{tok.value}/{tok.type} "

        # Generate assembly code for various token types
        if tok.type == 'INT' or tok.type == 'REAL' or tok.type == 'VAR':
            assembly_code += f"MOV EAX, {tok.value}\n"
            result_var = str(tok.value)

        elif tok.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POW']:
            if tok.type == 'PLUS':
                assembly_code += f"ADD EAX, {tok.value}\n"
            elif tok.type == 'MINUS':
                assembly_code += f"SUB EAX, {tok.value}\n"
            elif tok.type == 'TIMES':
                assembly_code += f"IMUL EAX, {tok.value}\n"
            elif tok.type == 'DIVIDE':
                assembly_code += f"DIV EAX, {tok.value}\n"
            elif tok.type == 'POW':
                pass  # Placeholder for exponentiation

        elif tok.type == 'ASSIGN':
            assembly_code += f"MOV {result_var}, EAX\n"
            result_var = None

        elif tok.type in ['LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL', 'NOT_EQUAL']:
            assembly_code += f"MOV EBX, {tok.value}\n"
            assembly_code += f"CMP EAX, EBX\n"

            if tok.type == 'LESS':
                assembly_code += "SETl AL\n"
            elif tok.type == 'GREATER':
                assembly_code += "SETg AL\n"
            elif tok.type == 'LESS_EQUAL':
                assembly_code += "SETle AL\n"
            elif tok.type == 'GREATER_EQUAL':
                assembly_code += "SETge AL\n"
            elif tok.type == 'EQUAL':
                assembly_code += "SETE AL\n"
            elif tok.type == 'NOT_EQUAL':
                assembly_code += "SETNE AL\n"

            assembly_code += "MOVZX EAX, AL\n"
            assembly_code += "MOV print, EAX\n"
            result_var = "print"

        elif tok.type in ['AND', 'OR', 'NOT']:
            assembly_code += f"MOV EBX, {tok.value}\n"
            if tok.type == 'AND':
                assembly_code += f"AND EAX, EBX\n"
            elif tok.type == 'OR':
                assembly_code += f"OR EAX, EBX\n"
            elif tok.type == 'NOT':
                assembly_code += f"NOT EAX\n"

        # Add the tokenized line to the output content
    output_file_content.append(tokenized_line.strip())

    # Add the assembly code for the line to the assembly content
    assembly_file_content.append(assembly_code)

# Write output to a file
with open("output_file.txt", "w") as output_file:
    output_file.write("\n".join(output_file_content))

# Write assembly-like output to a file
with open("assembly_output.txt", "w") as assembly_file:
    assembly_file.write("\n".join(assembly_file_content))
