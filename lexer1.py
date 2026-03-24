# lexer.py
from rich import print
import sly
import sys

class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas
        ARRAY, BOOLEAN, CHAR, ELSE, FALSE, FLOAT, FOR, FUNCTION, IF,
        INTEGER, PRINT, RETURN, STRING, TRUE, VOID, WHILE,
        CLASS, THIS, SUPER, EXTENDS, NEW,

        # Operadores de Relación y Lógicos
        LT, LE, GT, GE, EQ, NE, LAND, LOR, NOT,

        # Operadores de Asignación 
        ADDEQ, SUBEQ, MULEQ, DIVEQ, MODEQ, INC, DEC,

        # Identificador y Literales
        ID,
        LITERAL_INTEGER, LITERAL_FLOAT, LITERAL_CHAR, LITERAL_STRING,
    }
    literals = '+-*/%^=;,.:()[]{}?'

    # Símbolos a ignorar 
    ignore = ' \t\r\n'

    # Ignorar comentarios 
    ignore_comment    = r'/\*(.|\n)*?\*/'
    ignore_cppcomment = r'//.*\n'

 
    # Expresiones regulares para los tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*' 

    # Palabra Reservadas
    ID['array']    = ARRAY
    ID['boolean']  = BOOLEAN
    ID['char']     = CHAR
    ID['else']     = ELSE
    ID['false']    = FALSE
    ID['float']    = FLOAT
    ID['for']      = FOR
    ID['function'] = FUNCTION
    ID['if']       = IF
    ID['integer']  = INTEGER
    ID['print']    = PRINT
    ID['return']   = RETURN
    ID['string']   = STRING
    ID['true']     = TRUE
    ID['void']     = VOID
    ID['while']    = WHILE
    ID['class']    = CLASS
    ID['this']     = THIS
    ID['super']    = SUPER
    ID['extends']  = EXTENDS
    ID['new']      = NEW

    # Operadores 
    LT    = r'<'
    LE    = r'<='   
    GT    = r'>'
    GE    = r'>='
    EQ    = r'=='
    NE    = r'!='
    LAND  = r'&&'
    LOR   = r'\|\|'
    NOT   = r'!'

    # Operadores de 2 caracteres
    INC   = r'\+\+'
    DEC   = r'--'
    ADDEQ = r'\+='
    SUBEQ = r'-='
    MULEQ = r'\*='
    DIVEQ = r'/='
    MODEQ = r'%='

    # Literales Numéricos y de Texto
    LITERAL_FLOAT   = r'\d+\.\d+'
    LITERAL_INTEGER = r'\d+'
    LITERAL_STRING  = r'\"([^\\\n]|(\\.))*?\"'
    LITERAL_CHAR    = r'\'([^\\]|\\.)\''
    
    def error(self, t):
        print(f"Línea {self.lineno}: Carácter ilegal '{t.value[0]}'")
        self.index += 1

def tokenize(txt):
    lex = Lexer()
    tokens = []
    for tok in lex.tokenize(txt):
        tokens.append((tok.type, tok.value, tok.lineno))
    print(tokens)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'usage: python lexer.py <filename>')
        sys.exit(1)

    txt = open(sys.argv[1], encoding='utf-8').read()
    tokenize(txt)
