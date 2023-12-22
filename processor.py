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

    token_patterns = read_lex_file(lex_file_name)

    with open(input_file_name, 'r') as input_file:
        input_string = input_file.read()

    tokenized_input = tokenize(input_string, token_patterns)

    with open(output_file_name, 'w') as output_file:
        for token in tokenized_input:
            if token[0] in {'ADD', 'SUB', 'MUL', 'DIV', 'INT_DIV', 'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ', 'ASSIGN'}:
                output_file.write(f"{token[1]}/{token[1]} ")
            elif token[0] == 'WS':
                output_file.write(f"{token[1]}")
            else:
                output_file.write(f"{token[1]}/{token[0]} ")

    print(f"Output written to {output_file_name}")


if __name__ == "__main__":
    main()
