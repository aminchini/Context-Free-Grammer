grammar calculator;

equation
   : expression eq expression
   ;

expression
   : multiplyingExpression ((PLUS | MINUS) multiplyingExpression)*
   ;

multiplyingExpression
   : powExpression ((MULT | DIV) powExpression)*
   ;

powExpression
   : atom (POW atom)*
   ;

atom
   : PLUS atom
   | MINUS atom
   | func
   | scientific
   | variable
   | constant
   | LPAREN expression RPAREN
   ;

eq : EQUAL;

scientific
   : VALID_NUMBER
   ;

constant
   : PI
   | NEPER
   ;

variable
   : VARIABLE
   ;

func
   : funcname LPAREN expression (COMMA expression)* RPAREN
   ;

funcname
   : COS
   | SIN
   | TAN
   | COT
   | LOG
   | SQRT
   | FLOOR
   | FRACTION
   | SIGN_FUNC
   | STEP_FUNC
   ;

COS : 'cos';
SIN : 'sin';
TAN : 'tan';
COT :'cot';
LOG : 'log';
SQRT : 'sqrt';
FLOOR : 'floor';
FRACTION : 'fraction';
SIGN_FUNC : 'sign_func';
STEP_FUNC : 'step_func';
LPAREN : '(';
RPAREN : ')';
PLUS : '+';
MINUS : '-';
MULT : '*';
DIV : '/';
POW : '^';
COMMA : ',';
EQUAL : '=';
PI : 'pi' ;
NEPER : E2 ;

VARIABLE : VALID_START VALID_CHAR* ;

fragment VALID_START : ('a' .. 'z') | ('A' .. 'Z') | '_' ;

fragment VALID_CHAR : VALID_START | ('0' .. '9') ;


VALID_NUMBER : NUMBER ((E1 | E2) SIGN? NUMBER)? ;

NUMBER : ('0' .. '9') + ('.' ('0' .. '9') +)? ;

E1 : 'E' ;
E2 : 'e' ;
SIGN : ('+' | '-') ;

WS  :   [ \t\r\n] -> channel(HIDDEN);