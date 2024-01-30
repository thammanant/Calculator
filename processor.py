import re
from ply import yacc, lex
import code_generator


def read_lex_file(file_name):
    patterns = {}
    with open(file_name, 'r') as file:
        for line in file:
            if line.strip():
                token_type, pattern = line.strip().split(None, 1)
                patterns[token_type] = pattern
    return patterns


def tokenize(input_string, patterns):
    sorted_patterns = sorted(patterns.items(), key=lambda x: len(x[1]), reverse=True)
    pattern = '|'.join(f'(?P<{token}>{regex})' for token, regex in sorted_patterns)

    tokens = []
    for match in re.finditer(pattern, input_string):
        for name, value in match.groupdict().items():
            if value:
                tokens.append((name, value))
                break
    return tokens


class ParseNode:
    def __init__(self, symbol, value=None, children=None):
        self.symbol = symbol
        self.value = value
        self.children = children or []

    def __repr__(self):
        if self.value is not None:
            return f"{self.symbol}({self.value})"
        children_repr = ', '.join(repr(child) for child in self.children)
        return f"{self.symbol}([{children_repr}])" if self.children else f"{self.symbol}([])"


def convert_grammar_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    grammar = {}
    for line in content.split('\n'):
        if not line:
            continue
        non_terminal, productions = line.split(' ::= ')
        non_terminal = non_terminal.strip('<>') if non_terminal.isalpha() else non_terminal.strip()
        grammar[non_terminal] = [prod.strip() for prod in productions.split('|')]

    converted_grammar = {}
    for non_terminal, productions in grammar.items():
        converted_productions = []
        for production in productions:
            symbols = [sym.strip('<>') if sym.isalpha() else sym for sym in production.split()]
            if len(symbols) == 1 and symbols[0] == 'EPSILON':
                converted_productions.append('EPSILON')
            else:
                converted_productions.append([sym if sym.isalpha() else sym.strip('<>') for sym in symbols])

        converted_grammar[non_terminal.strip('<>')] = converted_productions

    return converted_grammar


def tokenize_input_file(input_file_path):
    with open(input_file_path, 'r') as file:
        input_lines = file.readlines()

    # Remove leading and trailing whitespaces from each line
    input_lines = [line.replace(" ", "") for line in input_lines]

    token_types_list = []

    for line_number, line in enumerate(input_lines, start=1):
        # Split the line into tokens using spaces
        tokens = line.split()
        token_types_list.append(tokens)

    return token_types_list


def parse_line(list_of_tokens, line_number):
    if 0 <= line_number < len(list_of_tokens):
        temp = list_of_tokens[line_number]
        # join the tokens into a string
        temp = ' '.join(temp)
        return temp
    else:
        print(f"Error: Line number {line_number} is out of range.")
        return ""


# Modify the parse function to set global_input_lines


def parse_helper(non_terminal, current_index, input_tokens, grammar, symbol_table):
    global index

    if non_terminal not in grammar:
        raise ValueError(f"Non-terminal {non_terminal} not found in grammar")

    for production in grammar[non_terminal]:
        match = True  # flag to check if the production matches
        index = current_index  # save the current index for backtracking
        temp_table = {}  # temporary symbol table for this production

        if production == ['EPSILON']:
            print(f"Trying production ['EPSILON'] for {non_terminal} at index {index}")
            return True, temp_table, index

        print(f"Trying production {production} for {non_terminal} at index {index}")

        for symbol in production:
            if symbol == 'EPSILON':
                continue
            if isinstance(symbol, str):  # terminal symbol
                if index < len(input_tokens):
                    if input_tokens[index][1] == symbol:  # Compare with token type
                        print(f"Matched terminal {symbol} at index {index}")
                        index += 1
                    else:
                        match = False
                        print(f"Failed to match terminal {symbol} at index {index}")
                        break
                else:
                    match = False
                    print(f"Failed to match terminal {symbol} at index {index}")
                    break
            else:  # non-terminal symbol
                result, value, index = parse_helper(symbol, index, input_tokens, grammar, temp_table)
                if result:
                    temp_table[symbol] = value
                    print(f"Matched non-terminal {symbol} at index {index}")
                else:
                    match = False
                    print(f"Failed to match non-terminal {symbol} at index {index}")
                    break

        if match:
            print(f"Production {production} matched for {non_terminal}")
            symbol_table.update(temp_table)  # update the main symbol table
            return True, temp_table, index

    # Backtrack to the previous index if none of the productions match
    print(f"Backtracking to index {index}")
    return False, None, current_index


# Token definition
tokens = (
    'INT', 'REAL', 'VAR', 'ADD', 'SUB', 'MUL', 'DIV', 'POW', 'GTE', 'GT', 'LTE', 'LT', 'EQ', 'NEQ', 'LPAREN',
    'RPAREN', 'ASSIGN', 'INT_DIV'
)

# Regular expression rules for tokens
t_INT = r'\d+'
t_REAL = r'\d+\.\d+'
t_VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_INT_DIV = r'//'
t_POW = r'\*\*'
t_GTE = r'>='
t_GT = r'>'
t_LTE = r'<='
t_LT = r'<'
t_EQ = r'=='
t_NEQ = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='

# Ignored characters
t_ignore = ' \t\n'


# Error handling rule
# Error handling rule for invalid tokens
def t_invalid(t):
    r'[0-9]+[a-zA-Z_]+'
    output_file.write(f"SyntaxError: Invalid token '{t.value}' at line {line_number}, position {t.lexpos+1}\n")
    raise SyntaxError


# Error handling rule
def t_error(t):
    output_file.write(f"SyntaxError '{t.value[0]}' at line {line_number-1}, position {t.lexpos+1}\n")
    raise SyntaxError


# Build the lexer
lexer = lex.lex()


# Grammar rules
def p_program(p):
    '''program : statement statements
               | '''
    if len(p) == 1:
        p[0] = ParseNode('program', [])
    else:
        p[0] = ParseNode('program', [p[1]] + p[2].children)


def p_statements(p):
    '''statements : statement statements
                  | '''
    if len(p) == 1:
        p[0] = ParseNode('statements', [])
    else:
        p[0] = ParseNode('statements', [p[1]] + p[2].children)


def p_statement(p):
    '''statement : assignment
                 | expression
                 | error'''
    p[0] = ParseNode('statement', [p[1]])


def p_assignment(p):
    '''assignment : variable ASSIGN expression'''
    p[0] = ParseNode('assignment', [p[1], p[2], p[3]])


def p_expression(p):
    '''expression : term
                  | term binary-operator expression'''
    if len(p) == 2:
        p[0] = ParseNode('expression', [p[1]])
    else:
        p[0] = ParseNode('expression', [p[1], p[2], p[3]])


def p_term(p):
    '''term : factor
            | factor POW term'''
    if len(p) == 2:
        p[0] = ParseNode('term', [p[1]])
    else:
        p[0] = ParseNode('term', [p[1], p[2], p[3]])


def p_factor(p):
    '''factor : number
              | variable
              | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = ParseNode('factor', [p[1]])
    elif len(p) == 3 and p[1] == '-':
        p[0] = ParseNode('factor', [ParseNode('unary-operator', [p[1]]), p[2]])
    else:
        p[0] = ParseNode('factor', [p[2]])


def p_number(p):
    '''number : INT
              | REAL'''
    p[0] = ParseNode('number', [p[1]])


def p_variable(p):
    '''variable : VAR
                | VAR ASSIGN number'''
    if len(p) == 2:
        p[0] = ParseNode('variable', [p[1]])
    else:
        p[0] = ParseNode('variable', [p[1], p[2], p[3]])
        value_type = p[3].symbol
        if value_type == 'number':
            # Assuming p[3].value is a list containing a single number
            value = eval(p[3].value[0])
            value_type = 'INT' if type(value) == int else 'REAL'
        else:
            value = p[3].value
        csv_value.append(f"{p[1]}, {line_number - 1}, 1, {len(p[1])}, {value_type}, {value}")


def p_binary_operator(p):
    '''binary-operator : ADD
                      | SUB
                      | MUL
                      | DIV
                      | INT_DIV
                      | GTE
                      | GT
                      | LTE
                      | LT
                      | EQ
                      | NEQ'''
    p[0] = ParseNode('binary-operator', [p[1]])


# Error handling rule
def p_error(p):
    output_file.write(f"Undefined variable '{p.value[0]}' at line {line_number-1}, position {p.lexpos+1}\n")
    raise SyntaxError


# Build the parser
parser = yacc.yacc()

global line_number, csv_value

lex_file_name = '64011658_64011594.lex'
input_file_name = 'input.txt'
output_file_name = '64011658_64011594.tok'
grammar_file = '64011658_64011594.grammar'
outputbracket_file_name = '64011658_64011594.bracket'
outputcsv_file_name = '64011658_64011594.csv'
outputasm_file_name = '64011658_64011594.asm'

token_patterns = read_lex_file(lex_file_name)

with open(input_file_name, 'r') as input_file:
    input_string = input_file.read()

tokenized_input = tokenize(input_string, token_patterns)


with open(output_file_name, 'w') as output_file:
    for token in tokenized_input:
        if token[0] == 'WS':
            output_file.write(f"{token[1]}")
        else:
            output_file.write(f"{token[1]}/{token[0]} ")

print(f"Output written to {output_file_name}")

with open(outputbracket_file_name, 'w') as output_file:
    csv_value = []
    grammar_dict = convert_grammar_file(grammar_file)

    # Tokenize input file
    token_types_line = tokenize_input_file(input_file_name)

    for line_number, token_types in enumerate(token_types_line, start=1):
        line_number += 1
        # Parse input
        input_tokens = parse_line(token_types_line, line_number - 2)

        try:
            result = parser.parse(input_tokens, tracking=True)
            output_file.write(f"({input_tokens})\n")
        except:
            continue


print(f"Output written to {outputbracket_file_name}")

with open(outputcsv_file_name, 'w') as output_file:
    output_file.write("Variable, Line, Length, Type, Value\n")
    for i in csv_value:
        output_file.write(f"{i}\n")

print(f"Output written to {outputcsv_file_name}")


with open(input_file_name, 'r') as input_file:
    lines = input_file.read()

with open(outputasm_file_name, 'w') as output_file:
    output_file.write(code_generator.generate_assembly(lines))

print(f"Output written to {outputasm_file_name}")
