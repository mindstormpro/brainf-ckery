global main

extern putchar

section .bss
    tape resb 30000

section .text
main:
    ; rbx is a register that's gonna hold the cell pointer
    mov rbx, 0 ; mov is move, rbx is a register, and 0 is 0 (I hope)
    ; mov byte [rbx], x where x is a number between 0-255, writes that value into the cell being pointed to by rbx

    ret ; this returns the current function, so this is the end of the program.