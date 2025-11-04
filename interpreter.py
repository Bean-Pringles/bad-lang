import sys
import re
from itertools import product

from itertools import product

def makeTable(inputVars, outputVars):
    allVars = inputVars + outputVars

    chartMode = True

    # Compute column widths for alignment
    colWidths = [max(len(v), 1) for v in allVars]

    # Build header row
    header = ""
    for i, v in enumerate(allVars):
        header += v.ljust(colWidths[i]) + " "
        if i == len(inputVars) - 1:
            header += "| "
    print(header.rstrip())

    # Build separator row between inputs and outputs
    sep = ""
    for i, w in enumerate(colWidths):
        sep += "-"*w + " "
        if i == len(inputVars) - 1:
            sep += "| "
    print(sep.rstrip())

    # Generate all binary combinations for input variables
    numInputs = len(inputVars)
    binaryRows = list(product([0, 1], repeat=numInputs))

    for inputs in binaryRows:
        row = ""
        # Add input values
        for i, val in enumerate(inputs):
            row += str(val).ljust(colWidths[i]) + " "
            if i == numInputs - 1:
                row += "| "
        # Add output placeholders (all zeros for now)
        for i in range(len(outputVars)):
            row += "0".ljust(colWidths[numInputs + i]) + " "
        print(row.rstrip())

def getNLine(lineNumber, file):
    with open(file, "r") as file:
        allLines = file.readlines()
        if 0 <= lineNumber - 1 < len(allLines):
            specificLine = allLines[lineNumber - 1]
            return specificLine

def cmds(tokens, vars, varsValue, inputVars, lineNumber, file, line):
    if tokens[0] == "INPUT":
        if not chartMode:
            for i in tokens[1:]:
                tempInput = ""
            
                while not tempInput in ["0", "1"]:
                    tempInput = input("Value of " + i + "? ")
                    if not tempInput in ["0", "1"]:
                        print("The value of " + i + " must be 0 or 1.")
        
                vars.append(tokens[tokens.index(i)])
                varsValue.append(tempInput)
                inputVars.append(i)
    
    # elif tokens[0] == "CHART":
        # makeTable(inputVars, vars)

    elif tokens[0] == "PRINT":
        print(varsValue[vars.index(tokens[1])])

    elif tokens[0] == "IF":
        left = tokens[1]
        op = tokens[2]
        right = tokens[3]

        if not left == "NOT":
            if left in vars:
                left = varsValue[vars.index(left)]
            if right in vars:
                right = varsValue[vars.index(right)]
            
            if op == "AND":
                if left == "1" and right == "1":
                    result = True
                else:
                    result = False
            
            elif op == "OR":
                if left == "1" or right == "1":
                    result = True
                else:
                    result = False
            
            elif op == "XOR":
                if not left == "1" and right == "1" and left == "1" or right == "1":
                    result = True
                else:
                    result = False

            elif op == "NOR":
                if not left == "1" or right == "1":
                    result = True
                else:
                    result = False
            
            elif op == "XNOR":
                if left == right:
                    result = True
                else:
                    result = False
            elif op == "NAND":
                if not left == "1" == right == "2":
                    result = True
                else:
                    result = False

            if result:
                pass
            else:
                while not line == "END":
                    getNLine(lineNumber, file)
                    lineNumber =+ 1
                    print(line)
    
    elif tokens[0] == "END":
        pass

    elif tokens[1] == "=":
        if not any(op in tokens for op in ["NOT", "AND", "OR", "XOR", "NOR", "XNOR", "NAND"]):
            if not tokens[0] in vars:
                vars.append(tokens[0])
        
                if tokens[2] in ["0", "1"]:
                    varsValue.append(tokens[2])
            else:
                varsValue[vars.index(tokens[0])] = tokens[2]

        else:
            if "NOT" in tokens:
                left = tokens[0]
                right = tokens[3]

                if right in vars:
                    right = varsValue[vars.index(right)]

                if not left in vars:
                    vars.append(left)

                    if right == "0":
                        varsValue.append("1")
                    else:  
                        varsValue.append("0")

                if left in vars:
                    if right == "0":
                        varsValue[vars.index(left)] = "1"
                    else:  
                        varsValue[vars.index(left)] = "0"
            else:
                left = tokens[0]
                middle = tokens[2]
                right = tokens[4]

                if middle in vars:
                    middle = varsValue[vars.index(middle)]
                if right in vars:
                    right = varsValue[vars.index(right)]

                if "AND" in tokens:
                    if not left in vars:
                        vars.append(left)
                        if middle == "1" and right == "1":
                            varsValue.append("1")
                        else:  
                            varsValue.append("0")
                
                    elif left in vars:
                        if middle == "1" and right == "1":
                            varsValue[vars.index(left)] = "1"
                        else:  
                            varsValue[vars.index(left)] = "0"
            
                elif "OR" in tokens:
                    if not left in vars:
                        vars.append(left)

                        if middle == "1" or right == "1":
                            varsValue.append("1")
                        else:  
                            varsValue.append("0")
                
                    elif left in vars:
                        if middle == "1" or right == "1":
                            varsValue[vars.index(left)] = "1"
                        else:  
                            varsValue[vars.index(left)] = "0"
            
                elif "XNOR" in tokens:
                    if not left in vars:
                        vars.append(left)

                        if middle == "0" and right == "0" or middle == "1" and right == "1":
                            varsValue.append("1")
                        else:  
                            varsValue.append("0")
                
                    elif left in vars:
                        if middle == "0" and right == "0" or middle == "1" and right == "1":
                            varsValue[vars.index(left)] = "1"
                        else:  
                            varsValue[vars.index(left)] = "0"
            
                elif "NOR" in tokens:
                    if not left in vars:
                        vars.append(left)

                        if middle == "0" and right == "0":
                            varsValue.append("1")
                        else:  
                            varsValue.append("0")
                
                    elif left in vars:
                        if middle == "0" and right == "0":
                            varsValue[vars.index(left)] = "1"
                        else:  
                            varsValue[vars.index(left)] = "0"
            
                elif "XOR" in tokens:
                    if not left in vars:
                        vars.append(left)

                        if middle == "0" and right == "0" or middle == "1" and right == "1":
                            varsValue.append("0")
                        else:  
                            varsValue.append("1")
                
                    elif left in vars:
                        if middle == "0" and right == "0" or middle == "1" and right == "1":
                            varsValue[vars.index(left)] = "0"
                        else:  
                            varsValue[vars.index(left)] = "1"

                elif "NAND" in tokens:
                    if not left in vars:
                        vars.append(left)

                        if middle == "1" and right == "1":
                            varsValue.append("0")
                        else:  
                            varsValue.append("1")
                
                    elif left in vars:
                        if middle == "1" and right == "1":
                            varsValue[vars.index(left)] = "0"
                        else:  
                            varsValue[vars.index(left)] = "1"
    
    elif tokens[0] == "TABLE":
        if tokens[1] == "AND":
            print("""
            AND
            A B | O
            0 0 | 0
            1 0 | 0
            0 1 | 0
            1 1 | 1
            """)
        
        elif tokens[1] == "OR":
            print("""
            OR
            A B | O
            0 0 | 0
            1 0 | 1
            0 1 | 1
            1 1 | 1
            """)

        elif tokens[1] == "XOR":
            print("""
            XOR
            A B | O
            0 0 | 0
            1 0 | 1
            0 1 | 1
            1 1 | 0
            """)

        elif tokens[1] == "NOR":
            print("""
            NOR
            A B | O
            0 0 | 1
            1 0 | 0
            0 1 | 0
            1 1 | 0
            """)

        elif tokens[1] == "XNOR":
            print("""
            XNOR
            A B | O
            0 0 | 1
            1 0 | 0
            0 1 | 0
            1 1 | 1
            """)

        elif tokens[1] == "NOT":
            print("""
            NOT
            A | O
            0 | 1
            1 | 0
            """)

        elif tokens[1] == "NAND":
            print("""
            NAND
            A B | O
            0 0 | 1
            1 0 | 1
            0 1 | 1
            1 1 | 0
            """)
    
    elif tokens[0] == "OUTPUT":
        for var in tokens[1:]:
            if var in vars:
                indexOfVar = vars.index(var)
                
                print(varsValue[indexOfVar])
                
                del vars[indexOfVar]
                del varsValue[indexOfVar]

    elif tokens[0] == "DEL":
        if tokens[1] in vars:
            indexOfVar = vars.index(tokens[1])
        
            del vars[indexOfVar]
            del varsValue[indexOfVar]

args = sys.argv
lineNumber = 1
vars = []
varsValue = []
inputVars =[]
chartMode = False
if len(args) == 1:
    lineCount = 9999999999999999

if len(args) > 1:
    fileExtension = args[1][(len(args[1]) - 4):]
    file = args[1]

    if fileExtension != "logi":
        print("You must give a .logi file.")
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
    tokens = re.findall(r"[A-Za-z0-9#!@$%^&*(){}|:<>?,./;'[\]\\\-+=]+", line)

    if "#" in tokens:
        hashIndex = tokens.index("#")
        del tokens[hashIndex:]

    if not tokens:
        continue

    cmds(tokens, vars, varsValue, inputVars, lineNumber, file, line)