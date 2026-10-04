from typing import Any
print("hello from the Brainf#ckery Compiler!")
base: str = None

with open("base.asm") as b:
    base = b.read()

bracketCounter: int = 0
bracketStack: list[int] = []

asm: str = base
def ptrUp():
    asm += "    inc rbx\n"

def ptrDown():
    asm += "    dec rbx\n"

def cellUp():
    asm += "    inc byte [rbx]\n"

def cellDown():
    asm += "    dec byte [rbx]\n"

def dataIn():
    asm += "    ; PLACEHOLDER"

def dataOut():
    asm += "    ; PLACEHOLDER"

def loopStart():
    asm += "    ; PLACEHOLDER"

def loopEnd():
    asm += "    ; PLACEHOLDER"