POW     \^
ADD     \+
SUB     -
MUL     \*
INT_DIV //
DIV     /
GTE     >=
GT      >
LTE     <=
LT      <
EQ      ==
NEQ     !=
LPAREN  \(
RPAREN  \)
ASSIGN  =
VAR     [a-zA-Z_][a-zA-Z0-9_]*
REAL    [0-9]+\.[0-9]+([eE][+-]?[0-9]+)?
INT     [0-9]+
OP      [\+\-\*\/]
WS      [" "\t\r\n\f\v]+
VAR_ASSIGN \[VAR\] = (\[REAL\]|\[VAR\]|\[INT\]) (\[OP\] (\[REAL\]|\[VAR\]|\[INT\]))?
ERR     .