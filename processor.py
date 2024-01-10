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


def check_op_compare(current_expression, line_number, output_file):
    if list(current_expression[1].values())[0] in {'ADD', 'SUB', 'MUL', 'DIV', 'INT_DIV'}:
        if list(current_expression[2].values())[0] in {'INT', 'REAL', 'VAR'}:
            pass
        elif list(current_expression[2].values())[0] in {'ADD', 'SUB'}:
            if list(current_expression[3].values())[0] in {'INT', 'REAL', 'VAR'}:
                pass
            else:
                output_file.write(f"Syntax error at line {line_number}, pos 4")
        else:
            output_file.write(f"Syntax error at line {line_number}, pos 3")
    elif list(current_expression[1].values())[0] in {'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ'}:
        if list(current_expression[2].values())[0] in {'INT', 'REAL', 'VAR'}:
            pass
        elif list(current_expression[2].values())[0] in {'ADD', 'SUB'}:
            if list(current_expression[3].values())[0] in {'INT', 'REAL', 'VAR'}:
                pass
            else:
                output_file.write(f"Syntax error at line {line_number}, pos 4")
        else:
            output_file.write(f"Syntax error at line {line_number}, pos 3")
    else:
        output_file.write(f"Syntax error at line {line_number}, pos 2")


def varnum(current_expression, line_number, output_file, var, csv_value):
    if list(current_expression[0].values())[0] in {'VAR'}:
        if list(current_expression[1].values())[0] in {'ASSIGN'}:
            if list(current_expression[2].values())[0] in {'INT', 'REAL', 'VAR'}:
                if list(current_expression[2].values())[0] in 'VAR' and list(current_expression[2].keys())[
                    0] not in var:  # Eg:x=y
                    output_file.write(f"Undefined variable {list(current_expression[2].keys())[0]} at line {line_number}, pos 3")
                elif list(current_expression[0].keys())[0] not in var:  # var assigned
                    var.append(list(current_expression[0].keys())[0])
                    csv_value.append(
                        f"{list(current_expression[0].keys())[0]}, {line_number}, {len(list(current_expression[0].keys())[0])}, {list(current_expression[0].values())[0]}, {list(current_expression[2].keys())[0]}")
                else:  # var updated
                    csv_value.append(
                        f"{list(current_expression[0].keys())[0]}, {line_number}, {len(list(current_expression[0].keys())[0])}, {list(current_expression[0].values())[0]}, {list(current_expression[2].keys())[0]}")
            elif list(current_expression[2].values())[0] in {'ADD', 'SUB'}:
                if list(current_expression[3].values())[0] in {'INT', 'REAL', 'VAR'}:
                    if list(current_expression[3].values())[0] in 'VAR' and list(current_expression[3].keys())[0] not in var:  # Eg:x=-z
                        output_file.write(f"Undefined variable {list(current_expression[3].keys())[0]} at line {line_number}, pos 4")
                    elif list(current_expression[0].keys())[0] not in var:  # var assigned
                        var.append(list(current_expression[0].keys())[0])
                        csv_value.append(f"{list(current_expression[0].keys())[0]}, {line_number}, {len(list(current_expression[0].keys())[0])}, {list(current_expression[0].values())[0]}, {list(current_expression[2].keys())[0] + list(current_expression[3].keys())[0]}")
                    else:  # var updated
                        csv_value.append(f"{list(current_expression[0].keys())[0]}, {line_number}, {len(list(current_expression[0].keys())[0])}, {list(current_expression[0].values())[0]}, {list(current_expression[2].keys())[0] + list(current_expression[3].keys())[0]}")
                else:  # Eg:x=+*
                    output_file.write(f"Syntax error at line {line_number}, pos 4")
            else:
                output_file.write(f"Syntax error at line {line_number}, pos 3")
        else:  # var assigned
            if list(current_expression[0].keys())[0] in var:
                check_op_compare(current_expression, line_number, output_file)
            else:  # var not assigned
                output_file.write(f"Undefined variable {list(current_expression[0].keys())[0]} at line {line_number},pos 1")

    elif list(current_expression[0].values())[0] in {'INT', 'REAL'}:
        check_op_compare(current_expression, line_number, output_file)


def validation(current_expression, line_number, output_file, var, csv_value):
    if list(current_expression[0].values())[0] in {'ADD', 'SUB', 'INT', 'REAL', 'VAR'}:
        if list(current_expression[0].values())[0] in {'ADD', 'SUB'}:
            output_file.write(list(current_expression[0].keys())[0])
            del current_expression[0]
            varnum(current_expression, line_number, output_file, var, csv_value)
        else:
            varnum(current_expression, line_number, output_file, var, csv_value)

    else:
        output_file.write(f"Syntax error at line {line_number}, pos 1")


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
        current_expression = []
        csv_value = []
        var = []

        for token in tokenized_input:
            if token[1] == '\n':
                if len(current_expression) >= 3:
                    validation(current_expression, line_number, output_file, var, csv_value)
                else:
                    output_file.write(f"Syntax error at line {line_number}, pos {len(current_expression)}")
                output_file.write("\n")
                current_expression = []
                line_number += 1
            elif token[0] == 'WS':
                continue
            else:
                dict = {token[1]: token[0]}
                current_expression.append(dict)
        print(csv_value)

    print(f"Output written to {outputbracket_file_name}")


if __name__ == "__main__":
    main()
