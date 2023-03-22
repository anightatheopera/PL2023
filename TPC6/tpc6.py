import ply.lex as lex
import re

# Lista de tokens
tokens = (
  'INT',
  'FLOAT',
  'STRING',
  'PLUS',  
  'MINUS',  
  'TIMES',  
  'DIVIDE',  
  'LPAREN',  
  'RPAREN',  
  'LBRACE',  
  'RBRACE',  
  'LBRACKET',
  'RBRACKET',
  'COMMA',   
  'SEMICOLON', 
  'DOT',     
  'EQUAL',   
  'EQEQUAL', 
  'LT',      
  'GT',      
  'FUNCTION',
  'PROGRAM',
  'WHILE',
  'FOR',     
  'IN',      
  'IF',      
  'DOTS',
  'INIT_COMMENT',
  'END_COMMENT',
  'LINE_COMMENT',
  'IDENTIFIER',
  'FULL_COMMENT'
)
    
# Expressões regulares para tokens simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACKET= r'\['
t_RBRACKET= r'\]'
t_COMMA   = r','
t_SEMICOLON = r';'
t_DOT     = r'\.'
t_EQUAL   = r'='
t_EQEQUAL = r'=='
t_LT      = r'<'
t_GT      = r'>'
t_FUNCTION= r'function'
t_PROGRAM = r'program'
t_WHILE   = r'while'
t_FOR     = r'for'
t_IN      = r'in'
t_IF      = r'if'
t_DOTS    = r'\.\.'
t_INIT_COMMENT = r'\/\*'  
t_END_COMMENT = r'\*\/'
t_LINE_COMMENT = r'\/\/.*\n'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
    
# Expressão regular para números inteiros
def t_INT(t):
    r'\d+'
    t.value = int(t.value)    
    return t
      
# Expressão regular para números reais
def t_FLOAT(t):
  r'\d+\.\d+'
  t.value = float(t.value)    
  return t
      
# Expressão regular para strings
def t_STRING(t):
  r'\".*?\"'
  t.value = str(t.value)    
  return t
      
# Expressão regular para ignorar espaços em branco
t_ignore  = ' \t'
     
# Expressão regular para ignorar quebras de linha
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
        
# Expressão regular para identificar erros
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)
    
# Constrói o analisador léxico
lexer = lex.lex(reflags=re.MULTILINE)

def test():
  code = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
'''
  lexer.input(code)
  for tok in lexer:
    print(tok.type, tok.value)
  
test()