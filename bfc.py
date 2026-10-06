import shutil
import subprocess
import os
print("hello from the Brainf#ckery Compiler!")

end: str = """
    push 0
    call _ExitProcess
"""
base: str = """
global _main

extern _getchar
extern _putchar
extern _ExitProcess

section .bss
    tape resb 30000

section .text
_main:
    mov ebx, tape 
    
"""

bracketCounter: int = 0
bracketStack: list[int] = []

asm: str = base
bf: str
with open("in.bf") as inBf:
    bf = inBf.read()

for bfc in bf:
    if bfc == ">":
        asm += "    inc ebx\n" # ptrUp
    elif bfc == "<":
        asm += "    dec ebx\n" # ptrDown
    elif bfc == "+":
        asm += "    inc byte [ebx]\n" # cellUp
    elif bfc == "-":
        asm += "    dec byte [ebx]\n" # cellDown
    elif bfc == ",":
        asm += """
    call _getchar
    mov byte [ebx], AL 
""" # moves the output byte from getchar into the curr cell... why does AL hold the output if win32 pushes outputs to the stack instead?
    elif bfc == ".":
        asm += """
    movzx eax, byte [ebx]
    push eax
    call _putchar
"""
    elif bfc == "[":
        bracketCounter += 1
        bracketStack.append(bracketCounter)
        asm += f"""
loopStart{bracketCounter}:
    cmp byte [ebx], 0
    jz loopEnd{bracketCounter}
"""
    elif bfc == "]":
        endVal: int = bracketStack.pop()
        asm += f"""
loopEnd{endVal}:
    cmp byte [ebx], 0
    jnz loopStart{endVal}
"""

asm += end

shutil.rmtree("build/", ignore_errors=True)
os.makedirs("build", exist_ok=True)
with open("build/out.asm", "x") as out:
    out.write(asm)
subprocess.run("nasm -f win32 build/out.asm -o build/out.obj")
subprocess.run("gcc build/out.obj -o build/out.exe")
subprocess.run("./build/out.exe")