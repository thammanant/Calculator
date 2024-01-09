import re


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
    assigned_vars = set()  # Track assigned variables

    for match in re.finditer(pattern, input_string):
        for name, value in match.groupdict().items():
            if value:
                if name == 'VAR_ASSIGN':
                    assigned_vars.add(value.split('=')[0].strip())  # Add assigned variable to set
                tokens.append((name, value))
                break

    return tokens, assigned_vars


def main():
    lex_file_name = '64011658_64011594.lex'
    input_file_name = 'input.txt'
    output_file_name = '64011658_64011594.tok'
    outputbracket_file_name = '64011658_64011594.bracket'

    token_patterns = read_lex_file(lex_file_name)

    with open(input_file_name, 'r') as input_file:
        input_string = input_file.read()

    tokenized_input, assigned_vars = tokenize(input_string, token_patterns)

    line_number = 1
    char_position = 1
    error_messages = []

    with open(output_file_name, 'w') as output_file:
        for token in tokenized_input:
            if token[0] in {'ADD', 'SUB', 'MUL', 'DIV', 'INT_DIV', 'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ', 'ASSIGN'}:
                output_file.write(f"{token[1]}/{token[1]} ")
            elif token[0] == 'WS':
                output_file.write(f"{token[1]}")
            else:
                output_file.write(f"{token[1]}/{token[0]} ")

    print(f"Output written to {output_file_name}")

    with open(outputbracket_file_name, 'w') as output_file:
        parsed_output = []
        for token in tokenized_input:
            if token[0] in {'NUM', 'VAR'}:
                parsed_output.append(token[1])
            elif token[0] in {'ADD', 'SUB', 'MUL', 'DIV', 'POW', 'INT_DIV', 'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ',
                              'ASSIGN'}:
                parsed_output.append(token[1])
            else:
                expression = ''.join(parsed_output)
                if token[1] == '\n':
                    if len(parsed_output) > 1:
                        output_file.write(f"({expression[0]}{expression[1:-1]}{expression[-1]})\n")
                    else:
                        output_file.write(f"{expression}\n")
                    parsed_output = []
                else:
                    parsed_output.append(token[1])

                if token[0] == 'ERR':
                    error_messages.append(f"SyntaxError at line {line_number}, pos {char_position}")
                elif token[0] == 'VAR':
                    var_name = token[1]
                    if var_name not in assigned_vars:
                        error_messages.append(
                            f"Undefined variable {var_name} at line {line_number}, pos {char_position}")
                elif token[0] == 'NUM':
                    error_messages.append(f"Use of unassigned NUM at line {line_number}, pos {char_position}")

            if token[1] == '\n':
                line_number += 1
                char_position = 1
            else:
                char_position += len(token[1])

        if error_messages:
            output_file.write('\n'.join(error_messages))

    print(f"Parsed output written to {outputbracket_file_name}")


if __name__ == "__main__":
    main()
