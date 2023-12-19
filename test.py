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
t_LIST = r'list'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','


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
t_ignore = ' \t'

# Build the lexer
lexer = lex.lex()

# Test the lexer
data = '''
23+8
2.5 * 0
5NUM^ 3.0
x=5
10*x
x =y
x!=5
X#+8
x = list[10]
x[0] = 1
x[1]+1
'''

lexer.input(data)

output_file_content = []

# Tokenize the input
for tok in lexer:
    output_file_content.append(f"{tok.value}/{tok.type}")

# Write tokenized output to a file
with open("output_file.txt", "w") as output_file:
    for line in output_file_content:
        output_file.write(line + "\n")
