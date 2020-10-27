grammar Rules;

/* Lexical rules */

// Language symbols definition
IF   : 'IF';
THEN : 'THEN';
WITH : 'WITH';

AND : 'AND' ;
OR : 'OR';

TRUE: 'TRUE';
FALSE: 'FALSE';

// Assign operator
ASSIGN : ':=';

// Comparison Operators
GE : '>=';
GT : '>';
LE : '<=';
LT : '<';
EQ : '==';
NE : '!=';

// Parenthese for operator order definition
LPAREN: '(';
RPAREN : ')';

// Parenthese for uncertainty
LSPAREN : '[';
RSPAREN : ']';

// Data holder mark
DHM : '*';

// Float number
DECIMAL : '-'?[0-9]+('.'[0-9]+)? ;

// Identifier (Characters, undescrope and number)
IDENTIFIER : [a-zA-Z_][a-zA-Z_0-9]* ;

// Each rule ending with semicolon
SEMI : ';' ;

// Hashtag comments
COMMENT : '#' .+? ('\n'|EOF) -> skip ;

// Skip processing white spaces
WS : [ \r\t\u000C\n]+ -> skip ;


/* Grammar rules */

rules_set : single_rule* EOF;

// Single rule format
single_rule: IF condition THEN conclusion SEMI | IF condition THEN conclusion WITH DECIMAL SEMI;

condition: left_logical_expr;
conclusion: right_logical_expr;

// Condition format
left_logical_expr
 : left_logical_expr AND left_logical_expr  # LogicalExpressionAnd
 | left_logical_expr OR left_logical_expr   # LogicalExpressionOr
 | function_expr                            # ComparisonExpression
 | function_expr LSPAREN DECIMAL RSPAREN    # ComparisonExpression
 | LPAREN left_logical_expr RPAREN          # LogicalExpressionInParen
 ;

// One condition expression format
function_expr
            : IDENTIFIER DHM? args
            | IDENTIFIER DHM? args comp_operator DECIMAL
            | IDENTIFIER DHM?
            | IDENTIFIER DHM? comp_operator DECIMAL
            | IDENTIFIER DHM? comp_operator IDENTIFIER
            | IDENTIFIER DHM? args comp_operator IDENTIFIER
            | (TRUE | FALSE);

args : arg args | arg;
arg : DECIMAL | IDENTIFIER;
comp_operator : GT | GE | LT | LE | EQ | NE;

// Conclusion format
right_logical_expr
 : right_logical_expr AND right_logical_expr    # RLogicalExpressionAnd
 | LPAREN right_logical_expr RPAREN             # RLogicalExpressionInParen
 | r_function_expr                              # RLogicalExpression
 ;

// One conclusion expression format
r_function_expr
              : IDENTIFIER
              | IDENTIFIER args
              | IDENTIFIER args ASSIGN DECIMAL
              | IDENTIFIER args ASSIGN IDENTIFIER
              | IDENTIFIER ASSIGN DECIMAL
              | IDENTIFIER ASSIGN IDENTIFIER;

