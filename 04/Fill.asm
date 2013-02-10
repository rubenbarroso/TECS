// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

(START)
        @KBD
        D=M
        @WHITE
        D;JEQ
        
(BLACK) 
        @zero
        M=0
        D=M
        @minus_one
        M=D-1
        @SCREEN
        D=A
        @i
        M=D

(PRINT_BLACK_ROW)
        @minus_one
        D=M
        @i
        A=M
        M=D
        @i
        M=M+1
        D=M
        @24575
        D=D-A
        @START
        D;JGT
        @PRINT_BLACK_ROW
        0;JMP

(WHITE)
        @SCREEN
        D=A
        @i
        M=D

(PRINT_WHITE_ROW)
        @i
        A=M
        M=0
        @i
        M=M+1
        D=M
        @24575
        D=D-A
        @START
        D;JGT
        @PRINT_WHITE_ROW
        0;JMP