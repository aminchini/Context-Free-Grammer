grammar num_var;

start : variable | number;

variable : VAR NAME ;

number
    : NUMBER
    | signed_number
    | LPAREN NUMBER RPAREN
    | LPAREN signed_number RPAREN
    | signs LPAREN NUMBER RPAREN
    | signs LPAREN signed_number RPAREN;

signed_number: signs NUMBER;
signs: (PLUS | MINUS )?;

NAME: ALPHA ( ALPHA | NUMBER )*;
ALPHA: [a-zA-Z_];
NUMBER : ('0' .. '9') + ('.' ('0' .. '9') +)? ;

VAR: '$';
SPACE: ' ';
LPAREN : '(';
RPAREN : ')';
PLUS : '+';
MINUS : '-';