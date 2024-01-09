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
    for match in re.finditer(pattern, input_string):
        for name, value in match.groupdict().items():
            if value:
                tokens.append((name, value))
                break
    return tokens


def main():
    lex_file_name = '64011658_64011594.lex'
    input_file_name = 'input.txt'
    output_file_name = '64011658_64011594.tok'
    outputbracket_file_name = '64011658_64011594.bracket'

    token_patterns = read_lex_file(lex_file_name)

    with open(input_file_name, 'r') as input_file:
        input_string = input_file.read()

    tokenized_input = tokenize(input_string, token_patterns)

    line_number = 1
    char_position = 1

    with open(output_file_name, 'w') as output_file:
        for token in tokenized_input:
            if token[0] in {'ADD', 'SUB', 'MUL', 'DIV', 'INT_DIV', 'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ', 'ASSIGN'}:
                output_file.write(f"{token[1]}/{token[1]} ")
            elif token[0] == 'WS':
                output_file.write(f"{token[1]}")
            else:
                output_file.write(f"{token[1]}/{token[0]} ")

    print(f"Output written to {output_file_name}")

    new_line = False
    var = []

    with open(outputbracket_file_name, 'w') as output_file:
        current_expression = ''
        prev_token_type = None

        for i, token in enumerate(tokenized_input):
            # Use i directly to get the next token
            next_token = tokenized_input[i + 1] if i + 1 < len(tokenized_input) else None
            if new_line and token[1] != '\n':
                continue
            else:
                new_line = False

            if token[0] in {'ADD', 'SUB', 'MUL', 'DIV', 'POW', 'INT_DIV', 'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ'}:
                current_expression += token[1]
            elif token[0] in {'ASSIGN'}:
                current_expression += token[1]
            elif token[0] == 'WS':
                pass
            elif token[0] in {'VAR', 'REAL', 'INT'}:  # operand
                if token[0] == 'VAR' and token[1] not in var:
                    if next_token[0] != 'ASSIGN':
                        output_file.write(f"Undefined variable {token[1]} at line {line_number}, pos {char_position}")
                        current_expression = ''
                        new_line = True
                    else:
                        var.append(token[1])

                if prev_token_type in {'VAR', 'REAL', 'INT'}:
                    output_file.write(f"Syntax error at line {line_number}, pos {char_position}")
                    current_expression = ''
                    new_line = True
                else:
                    current_expression += token[1]
            else:             # error
                if token[0] == 'ERR':           # not sure
                    output_file.write(f"Syntax error at line {line_number}, pos {char_position}")
                    current_expression = ''
                    new_line = True

            prev_token_type = token[0]

            if token[1] == '\n':
                if current_expression:
                    output_file.write(f"({current_expression})\n")
                    current_expression = ''
                else:
                    output_file.write(f"\n")
                line_number += 1
                char_position = 1
            else:
                char_position += len(token[1])

    print(f"Output written to {outputbracket_file_name}")


if __name__ == "__main__":
    main()
