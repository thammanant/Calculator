LD R0 #23
LD R1 #8
ADD.i R2 R0 R1
ST @print R2

LD R0 #2.5 
LD R1 # 0
FL.i R1 R1
MUL.f R2 R0 R1
ST @print R2

ERROR

LD R0 #5
ST @x R0

LD R0 #10
LD R1 @x
MUL.i R2 R0 R1
ST @print R2

ERROR

LD R0 @x
LD R1 #5
NEQ.i R2 R0 R1
ST @print R2

ERROR

LD R0 #3
LD R1 #6
SUB.i R2 R0 R1
ST @print R2

LD R0 #3
LD R1 #8
DIV.i R2 R0 R1
ST @print R2

LD R0 #4
LD R1 #9
FL.i R0 R0
FL.i R1 R1
LT.f R2 R0 R1
ST @print R2

LD R0 #0
LD R1 #7
FL.i R0 R0
FL.i R1 R1
GT.f R2 R0 R1
ST @print R2

LD R0 #0
LD R1 #5
FL.i R0 R0
FL.i R1 R1
EQ.f R2 R0 R1
ST @print R2

LD R0 #3
LD R1 #2
FL.i R0 R0
FL.i R1 R1
LTE.f R2 R0 R1
ST @print R2

LD R0 #4
LD R1 #3
FL.i R0 R0
FL.i R1 R1
GTE.f R2 R0 R1
ST @print R2

LD R0 #5
LD R1 #2
POW.i R2 R0 R1
ST @print R2

