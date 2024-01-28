import re


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


def tokenize_input_file(input_file):
    with open(input_file) as file:
        input_lines = file.readlines()

    token_types_list = []

    for line_number, line in enumerate(input_lines, start=1):
        types = [token.split('/')[1] for token in re.findall(r'\S+', line)]
        token_types_list.append(types)

    return token_types_list



def parse(grammar_dict, token_types, line_number=1, position=0):
    for start_symbol in grammar_dict.keys():
        print(f"\nTrying to parse line {line_number} with start symbol: {start_symbol}")
        print(f"Token Types: {token_types}")
        result, parse_tree, symbol_table = parse_helper(grammar_dict, start_symbol, token_types,
                                                        line_number, position)

        if result is not False:
            print(f"Matches Grammar with start symbol {start_symbol}: True")
            print("Parse Tree:", parse_tree)
            print("Symbol Table:", symbol_table)
            return True, parse_tree, symbol_table

    print("Matches Grammar: False")
    return False, None, None


def parse_helper(grammar_dict, current_symbol, token_types, line_number, position):
    if current_symbol not in grammar_dict:
        print(f"Error: Symbol {current_symbol} not found in grammar.")
        return False, None, None

    parse_node = ParseNode(current_symbol)
    symbol_table = {}

    for production in grammar_dict[current_symbol]:
        match, remaining_tokens, child_nodes, child_symbol_table = match_production(
            grammar_dict, production, token_types, line_number, position
        )

        if match:
            parse_node.children = child_nodes
            symbol_table.update(child_symbol_table)
            return True, parse_node, symbol_table

    return False, None, None


def match_production(grammar_dict, production, token_types, line_number, position):
    remaining_tokens = position
    child_nodes = []
    child_symbol_table = {}

    for symbol in production:
        if symbol == 'EPSILON':
            continue

        if isinstance(symbol, list):  # Non-terminal
            result, node, symbol_table = parse_helper(
                grammar_dict, symbol, token_types, line_number, remaining_tokens
            )

            if not result:
                return False, remaining_tokens, [], {}

            child_nodes.append(node)
            child_symbol_table.update(symbol_table)
        elif symbol in ('INT', 'REAL', 'VAR'):
            result, remaining_tokens, specific_nodes, specific_symbol_table = match_specific_context(
                token_types, line_number, remaining_tokens, symbol
            )

            if not result:
                return False, remaining_tokens, [], {}

            child_nodes.extend(specific_nodes)
            child_symbol_table.update(specific_symbol_table)
        else:  # Terminal
            if remaining_tokens < len(token_types) and token_types[remaining_tokens] == symbol:
                # Matched a terminal symbol
                child_nodes.append(ParseNode(symbol, token_types[remaining_tokens]))
                remaining_tokens += 1
            else:
                # Unexpected token, handle gracefully
                return False, remaining_tokens, [], {}

    return True, remaining_tokens, child_nodes, child_symbol_table


def match_specific_context(token_types, line_number, position, symbol):
    if symbol == 'INT':
        # Handle context for 'INT'
        result, remaining_tokens, int_nodes, int_symbol_table = match_int_context(
            token_types, line_number, position
        )
        return result, remaining_tokens, int_nodes, int_symbol_table
    elif symbol == 'REAL':
        # Handle context for 'REAL'
        result, remaining_tokens, real_nodes, real_symbol_table = match_real_context(
            token_types, line_number, position
        )
        return result, remaining_tokens, real_nodes, real_symbol_table
    elif symbol == 'VAR':
        # Handle context for 'VAR'
        result, remaining_tokens, var_nodes, var_symbol_table = match_var_context(
            token_types, line_number, position
        )
        return result, remaining_tokens, var_nodes, var_symbol_table
    else:
        return False, position, [], {}

def match_var_context(token_types, line_number, position):
    if position < len(token_types) and token_types[position] == 'VAR':
        # Matched 'VAR'
        node = ParseNode('VAR', token_types[position])
        return True, position + 1, [node], {'VAR': token_types[position]}
    else:
        return False, position, [], {}


def match_real_context(token_types, line_number, position):
    if position < len(token_types) and token_types[position] == 'REAL':
        # Matched 'REAL'
        node = ParseNode('REAL', token_types[position])
        return True, position + 1, [node], {'REAL': token_types[position]}
    else:
        return False, position, [], {}


def match_int_context(token_types, line_number, position):
    if position < len(token_types) and token_types[position] == 'INT':
        # Matched 'REAL'
        node = ParseNode('INT', token_types[position])
        return True, position + 1, [node], {'INT': token_types[position]}
    else:
        return False, position, [], {}


def compare_with_grammar(grammar_dict, token_types_list):
    for line_number, token_types in enumerate(token_types_list, start=1):
        result, parse_tree, symbol_table = parse(grammar_dict, token_types)
        if not result:
            print(f"Token Types: {token_types}, Matches Grammar: False")
        else:
            print(f"Token Types: {token_types}, Matches Grammar: True")
            print("Parse Tree:", parse_tree)
            print("Symbol Table:", symbol_table)


# Example usage:
grammar_file = '64011658_64011594.grammar'
input_file = '64011658_64011594.tok'

# Load grammar
grammar_dict = convert_grammar_file(grammar_file)
print("Grammar:", grammar_dict)

# Tokenize input file
token_types_list = tokenize_input_file(input_file)

# Compare with grammar
compare_with_grammar(grammar_dict, token_types_list)