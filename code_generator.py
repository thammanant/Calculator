import re

def generate_assembly(input_content):
    assembly_output = ""
    variables = set()

    lines = input_content.split('\n')

    for line in lines:
        line = line.strip()

        if re.search(r'\d+[a-zA-Z_]+|[a-zA-Z_]+\d+', line):
            assembly_output += "ERROR\n\n"
        elif '+' in line:
            operands = line.split('+')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT + INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "ADD.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL + INT or INT + REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "ADD.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR + INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "ADD.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT + VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "ADD.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR + VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "ADD.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '*' in line:
            operands = line.split('*')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT * INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "MUL.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL * INT or INT * REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "MUL.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR * INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "MUL.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT * VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "MUL.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR * VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "MUL.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '/' in line:
            operands = line.split('/')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT / INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "DIV.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL / INT or INT / REAL

                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "DIV.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR / INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "DIV.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT / VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "DIV.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR / VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "DIV.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '-' in line:
            operands = line.split('-')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT - INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "SUB.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL - INT or INT - REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "SUB.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR - INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "SUB.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT - VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "SUB.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR - VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "SUB.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '^' in line:
            operands = line.split('^')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT ^ INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "POW.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL ^ INT or INT ^ REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "POW.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR ^ INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "POW.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT ^ VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "POW.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR ^ VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "POW.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '!=' in line:
            operands = line.split('!=')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT != INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "NEQ.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL != INT or INT != REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "NEQ.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR != INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "NEQ.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT != VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "NEQ.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR != VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "NEQ.i R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '<=' in line:
            operands = line.split('<=')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT <= INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "LTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL <= INT or INT <= REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "LTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR <= INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "LTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT <= VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "LTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR <= VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "LTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '>=' in line:
            operands = line.split('>=')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT >= INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL >= INT or INT >= REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR >= INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT >= VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "GTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR >= VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "GTE.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '<' in line:
            operands = line.split('<')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT < INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "LT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL < INT or INT < REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "LT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR < INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "LT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT < VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "LT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR < VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "LT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '>' in line:
            operands = line.split('>')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT > INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL > INT or INT > REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR > INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT > VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "GT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR > VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "GT.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif '==' in line:
            operands = line.split('==')
            if operands[0].isdigit() and operands[1].isdigit():
                # INT == INT
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "FL.i R0 R0\n"
                assembly_output += "FL.i R1 R1\n"
                assembly_output += "EQ.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif '.' in operands[0] or '.' in operands[1]:
                # REAL == INT or INT == REAL
                if '.' in operands[0]:
                    real_operand, int_operand = operands[0], operands[1]
                else:
                    real_operand, int_operand = operands[1], operands[0]
                assembly_output += f"LD R0 #{real_operand}\n"
                assembly_output += f"LD R1 #{int_operand}\n"
                assembly_output += "EQ.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1].isdigit():
                # VAR == INT
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 #{operands[1]}\n"
                assembly_output += "EQ.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[1] in variables and operands[0].isdigit():
                # INT == VAR
                assembly_output += f"LD R0 #{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "EQ.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            elif operands[0] in variables and operands[1] in variables:
                # VAR == VAR
                assembly_output += f"LD R0 @{operands[0]}\n"
                assembly_output += f"LD R1 @{operands[1]}\n"
                assembly_output += "EQ.f R2 R0 R1\n"
                assembly_output += "ST @print R2\n\n"
            else:
                assembly_output += "ERROR\n\n"

        elif '=' in line:
            assignment = line.split('=')
            if (assignment[1] in variables or assignment[1].isdigit() or '.' in assignment[1]) and assignment[0].isalpha():
                variable = assignment[0].strip()
                variables.add(variable)
                assembly_output += f"LD R0 #{assignment[1]}\n"
                assembly_output += f"ST @{variable} R0\n\n"
            else:
                assembly_output += "ERROR\n\n"
        elif line in variables:
            assembly_output += f"LD R0 @{line}\n"
            assembly_output += f"ST @print R0\n\n"
        else:
            assembly_output += "ERROR\n\n"

    return assembly_output

