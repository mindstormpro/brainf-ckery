import shutil
import subprocess
import os
import getopt
import sys

args: list[str] = sys.argv[1:]
options = "hi:o:rcv"
long_options: list[str] = ["Help", "Input=", "Output=", "RunOnComp", "Clean", "Verbose"]

inputFile: str = "in.bf"
outputFile: str = "out.exe"
runOnComplete: bool = False
verbose: bool = False
try:
    arguments, values = getopt.getopt(args, options, long_options)
    for currentArg, currentVal in arguments:
        if currentArg in ("-h", "--Help"):
            print("Here's where I would put a help message, but I'm too lazy, Ill do it later :b")
        elif currentArg in ("-i", "--Input"):
            inputFile = currentVal
        elif currentArg in ("-o", "--Output"):
            outputFile = currentVal
        elif currentArg in ("-r", "--Run"):
            runOnComplete = True
        elif currentArg in ("-v", "--Verbose"):
            verbose = True
except getopt.error as err:
    print(str(err))

if verbose : print("using verbose output:")

end: str = """
    push 0
    call _ExitProcess@4
"""
base: str = """
global _main

extern _getchar
extern _putchar
extern _ExitProcess@4

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
with open(inputFile) as inBf:
    bf = inBf.read()
if verbose : print(f"reading {len(bf)} chars from {inputFile}")
bfCounter: int = 0
for bfc in bf:
    if bfc == ">": # the > instruction
        bfCounter += 1
        asm += "    inc ebx\n" # ptrUp
    elif bfc == "<": # the < instruction
        bfCounter += 1
        asm += "    dec ebx\n" # ptrDown
    elif bfc == "+": # the + instruction
        bfCounter += 1
        asm += "    inc byte [ebx]\n" # cellUp
    elif bfc == "-": # the - instruction
        bfCounter += 1
        asm += "    dec byte [ebx]\n" # cellDown
    elif bfc == ",": # the , instruction
        bfCounter += 1
        asm += """
    call _getchar
    mov byte [ebx], AL 
""" # moves the output byte from getchar into the curr cell... why does AL hold the output if win32 pushes outputs to the stack instead?
    elif bfc == ".": # the . instructon
        bfCounter += 1
        asm += """
    movzx eax, byte [ebx]
    push eax
    call _putchar
"""
    elif bfc == "[": # for the [ instruction
        bfCounter += 1
        bracketCounter += 1
        bracketStack.append(bracketCounter)
        asm += f"""
loopStart{bracketCounter}:
    cmp byte [ebx], 0
    jz loopEnd{bracketCounter}
"""
    elif bfc == "]": # for the ] instruction
        bfCounter += 1
        endVal: int = bracketStack.pop()
        asm += f"""
loopEnd{endVal}:
    cmp byte [ebx], 0
    jnz loopStart{endVal}
"""

if verbose : print(f"read {bfCounter} out of {len(bf)} chars as valid BF code") #logging how many BF chars were counted

asm += end

# directory stuff
if verbose :  print("removing old build directory")
shutil.rmtree("build/", ignore_errors=True)
if verbose : print("creating new build directory")
os.makedirs("build", exist_ok=True)

with open("build/out.asm", "x") as out: # writing out the assembly
    out.write(asm)

if verbose : print("compiling to an object file...") # the compiling to an object file for GCC to use
subprocess.run("nasm -f win32 build/out.asm -o build/out.obj")

if verbose : print("assembling to binary") # the assembling to a raw binary executable + linking and other dark magic
subprocess.run(f"gcc build/out.obj -o {outputFile}")

if runOnComplete: # runs the exe if the -r or --Run flags are passed
    if verbose : print("running the compiled EXE...")
    subprocess.run(f"./{outputFile}")
