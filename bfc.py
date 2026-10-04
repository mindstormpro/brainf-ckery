from typing import Any
print("hello from the Brainf#ckery Compiler!")
base: str = None

with open("base.asm") as b:
    base = b.read()

bracketCounter: int = 0
bracketStack: list[int] = []