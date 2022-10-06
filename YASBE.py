# YASBE Interpreter 1.1

import sys

def end_program(reason):
    return f"\n\n== PROGRAM ENDED == \nProgram execution finished: {reason}"

try:
    with open(" ".join(sys.argv[2:])) as codefile:
        code = codefile.read()
except Exception:
    code = input("Code: ")

tokens = {"push":0, "pop":1, "copy":2, "flip":3, "add":4, "subt":5, "mult":6, "div":7, "char":8, "value":9, "cget":10, "iget":11, "jump":12, "condjump":13, "break":14, "condbreak":15, "swap":16, "pushback":17, "debug":999}
tape = [0] * 1000

def tokenize(code):
    cd = code.lower().split()

    for i in range(len(cd)):
        if cd[i] in tokens:
            cd[i] = tokens[cd[i]]
        else:
            try:
                cd[i] = int(cd[i])
            except ValueError:
                print(f"Error: invalid token: {cd[i]}")
                return []

    return cd

def interpret(code):
    stack = []

    pointer = 0

    while pointer < len(code):
        opcode = code[pointer]

        if opcode == 0: # push
            pointer += 1
            stack.append(code[pointer])
        
        if opcode == 1: # pop
            try:
                stack.pop()
            except IndexError:
                print(end_program("Pop from empty stack"))
                return 0
        
        if opcode == 2: # copy
            stack.append(stack[-1])
        
        if opcode == 3: # flip
            stack.reverse()
        
        if opcode == 4: # add
            num1 = stack[-1]
            num2 = stack[-2]

            stack.append(num1 + num2)
        
        if opcode == 5: # subt
            num1 = stack[-1]
            num2 = stack[-2]

            stack.append(num1 - num2)
        
        if opcode == 6: # mult
            num1 = stack[-1]
            num2 = stack[-2]

            stack.append(num1 * num2)
        
        if opcode == 7: # div
            num1 = stack[-1]
            num2 = stack[-2]

            stack.append(num1 // num2)
        
        if opcode == 8: # char
            print(chr(stack[-1]), end="")
        
        if opcode == 9: # value
            print(stack[-1])
        
        if opcode == 10: # cget
            stack.append(ord(input("char? ")[0]))
        
        if opcode == 11: # iget
            stack.append(int(input("int? ")))
        
        if opcode == 12: # jump
            pointer += 1
            addr = code[pointer] - 1
            pointer = addr
        
        if opcode == 13: # condjump
            pointer += 1
            addr = code[pointer] - 1
            pointer += 1
            if stack[-1] != stack[code[pointer]]:
                pointer = addr
        
        if opcode == 14: # break
            print(end_program("Break instruction reached"))
            return 0
        
        if opcode == 15: # condbreak
            pointer += 1
            
            if stack[-1] != stack[code[pointer]]:
                print(end_program("Break instruction reached"))
                return 0
        
        if opcode == 16: # swap
            buf = stack[0]
            stack[0] = stack[-1]
            stack[-1] = buf
        
        if opcode == 17: # pushback
            pointer += 1
            stack.insert(0, code[pointer])
        
        if opcode == 999: # debug
            print(stack)

        pointer += 1

interpret(tokenize(code))
