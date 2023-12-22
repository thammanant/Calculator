import re

# Read token definitions from the .lex file
def read_lex_file(file_name):
    with open(file_name, 'r') as file:
        patterns = {}
        for line in file:
            if line.strip():
                token_type, pattern = line.strip().split(None, 1)
                patterns[token_type] = pattern
        return patterns

# Tokenize function
def tokenize(input_string, patterns):
    # Regular expression pattern to match any token
    pattern = '|'.join(f'(?P<{token}>{regex})' for token, regex in patterns.items())

    tokens = []
    for match in re.finditer(pattern, input_string):
        for name, value in match.groupdict().items():
            if value:
                tokens.append((name, value))
                break
    return tokens

# Read token definitions from the .lex file
token_patterns = read_lex_file('64011658_64011594.lex')

# Read input from file
with open('input.txt', 'r') as input_file:
    input_string = input_file.read()

# Tokenize the input string
tokenized_input = tokenize(input_string, token_patterns)

# Print tokenized output
for token in tokenized_input:
    print(f"{token[1]}/{token[0]}", end=' ')
print()
