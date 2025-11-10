import sys
import re
import os

def getVal(tokens, vars, varsValue):
    tokens = [str(varsValue[vars.index(t)]) if t in vars else t for t in tokens]

    if tokens[len(tokens) - 1] == ")":
        del tokens[len(tokens) - 1]
    
    if any(op in tokens for op in ["+", "-", "*", "/"]):
        try:
            return eval(" ".join(tokens))
        except Exception as e:
            return "Error evaluating expression"

    if len(tokens) == 1 and tokens[0] in vars:
        return varsValue[vars.index(tokens[0])]

    return "".join(tokens).replace('"', '')
    

def getNLine(lineNumber, file):
    with open(file, "r") as file:
        allLines = file.readlines()
        if 0 <= lineNumber - 1 < len(allLines):
            specificLine = allLines[lineNumber - 1]
            return specificLine

def cmds(tokens, vars, varsValue, line, lineNumber):
    try:
        if tokens[0] == "yap":
            print(getVal(tokens[2:], vars, varsValue))
    
        elif tokens[0] == "lowkey":
            if tokens[2] in vars:    
                varsValue[vars.index(tokens[1])] = getVal(tokens[3:], vars, varsValue)
            else:
                varsValue.append(getVal(tokens[3:], vars, varsValue))
                vars.append(tokens[1])

    except IndexError as e:
        pass

args = sys.argv
lineNumber = 1
vars = []
varsValue = []
if len(args) == 1:
    lineCount = 9999999999999999

if len(args) > 1:
    fileExtension = args[1][(len(args[1]) - 6):]
    file = args[1]

    if fileExtension != "bussin":
        root, extension = os.path.splitext(file)
        print(f"Bro, the {extension} file is not as peak as a .bussin, use the goated file type.")
        sys.exit()

    with open(file, "r") as f:
        lineCount = sum(1 for line in f)

while lineNumber <= lineCount:
    if len(args) > 1:
        line = getNLine(lineNumber, file)
        lineNumber += 1
    else:
        line = input("> ")

    # Regex the line
    tokens = re.findall(r'"|[A-Za-z0-9_]+|[()=]|[^A-Za-z0-9_\s]', line)

    if "W" in tokens:
        del tokens[tokens.index("W"):]
    
    if "L" in tokens:
        del tokens[tokens.index("L"):]

    if not tokens:
        continue

    cmds(tokens, vars, varsValue, line, lineNumber)
