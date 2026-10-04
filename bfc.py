print("hello from the Brainf#ckery Compiler!")
base: str = None
end: str = """
    pop rbx
    mov rax, 0
    ret
"""
with open("base.asm") as b:
    base = b.read()

bracketCounter: int = 0
bracketStack: list[int] = []

asm: str = base


bf: str = input()

for bfc in bf:
    if bfc == ">":
        asm += "    inc rbx\n" # ptrUp
    elif bfc == "<":
        asm += "    dec rbx\n" # ptrDown
    elif bfc == "+":
        asm += "    inc byte [rbx]\n" # cellUp
    elif bfc == "-":
        asm += "    dec byte [rbx]\n" # cellDown
    elif bfc == ",":
        asm += "    ; PLACEHOLDER"
    elif bfc == ".":
        asm += "    ; PLACEHOLDER"
    elif bfc == "[":
        lasm += "    ; PLACEHOLDER"
    elif bfc == "]":
        asm += "    ; PLACEHOLDER"

with open("out.asm", "x") as out:
    out.write(asm)