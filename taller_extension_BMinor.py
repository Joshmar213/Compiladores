import os
from railroad import Diagram, Choice, Optional, Terminal, NonTerminal, Sequence

# 1. Configuración de carpetas
BASE_PATH = 'out/svg/'
os.makedirs(BASE_PATH, exist_ok=True)

def T(x): return Terminal(x)
def N(x): return NonTerminal(x)

# --- [ SECCIÓN: DECLARACIONES ] ---

def d_decl():
    # Fiel a: decl ::= ID : type ; | ... | decl_init | class_decl
    return Diagram(Choice(0, 
        Sequence(T("ID"), T(":"), N("type_simple"), T(";")),
        Sequence(T("ID"), T(":"), N("type_array_sized"), T(";")),
        Sequence(T("ID"), T(":"), N("type_func"), T(";")),
        N("decl_init"),
        N("class_decl") # Extensión B-Minor+
    ))

def d_class_decl():
    # Extensión: class_decl ::= CLASS ID { class_body }
    return Diagram(Sequence(T("CLASS"), T("ID"), T("{"), N("class_body"), T("}")))

# --- [ SECCIÓN: STATEMENTS ] ---

def d_while_stmt_closed():
    # while_stmt_closed ::= WHILE ( opt_expr ) closed_stmt
    return Diagram(Sequence(T("WHILE"), T("("), N("opt_expr"), T(")"), N("closed_stmt")))

def d_while_stmt_open():
    # while_stmt_open ::= WHILE ( opt_expr ) stmt
    return Diagram(Sequence(T("WHILE"), T("("), N("opt_expr"), T(")"), N("stmt")))

# --- [ SECCIÓN: EXPRESIONES (RECURSIVAS) ] ---

# expr1 ::= lval assign_op expr1 | expr_ternary
def d_expr1():
    return Diagram(Choice(1, 
        N("expr_ternary"),
        Sequence(N("lval"), Choice(0, T("="), T("+="), T("-="), T("*="), T("/=")), N("expr1"))
    ))

# expr_ternary ::= expr2 ? expr : expr_ternary | expr2
def d_expr_ternary():
    return Diagram(Choice(0,
        N("expr2"),
        Sequence(N("expr2"), T("?"), N("expr"), T(":"), N("expr_ternary"))
    ))

# expr2 ::= expr2 LOR expr3 | expr3 (Recursión Izquierda)
def d_expr2():
    return Diagram(Choice(1,
        N("expr3"),
        Sequence(N("expr2"), T("LOR"), N("expr3"))
    ))

# expr5 ::= expr5 + expr6 | expr5 - expr6 | expr6
def d_expr5():
    return Diagram(Choice(2,
        N("expr6"),
        Sequence(N("expr5"), T("+"), N("expr6")),
        Sequence(N("expr5"), T("-"), N("expr6"))
    ))

# expr8 ::= - expr8 | NOT expr8 | ++ expr8 | -- expr8 | expr9
def d_expr8():
    return Diagram(Choice(4,
        N("expr9"),
        Sequence(T("-"), N("expr8")),
        Sequence(T("NOT"), N("expr8")),
        Sequence(T("++"), N("expr8")), # B-Minor+
        Sequence(T("--"), N("expr8"))  # B-Minor+
    ))

# expr9 ::= expr9 INC | expr9 DEC | expr9 . ID | group
def d_expr9():
    return Diagram(Choice(3,
        N("group"),
        Sequence(N("expr9"), T("INC")),
        Sequence(N("expr9"), T("DEC")),
        Sequence(N("expr9"), T("."), T("ID")) # B-Minor+
    ))

# --- [ GUARDAR ARCHIVOS ] ---

diagramas = {
    "decl_base": d_decl,
    "class_decl": d_class_decl,
    "while_closed": d_while_stmt_closed,
    "expr1_assign": d_expr1,
    "expr_ternary": d_expr_ternary,
    "expr2_logical": d_expr2,
    "expr5_arith": d_expr5,
    "expr8_unary": d_expr8,
    "expr9_postfix": d_expr9
}

for name, func in diagramas.items():
    with open(f"{BASE_PATH}{name}.svg", 'w', encoding='utf-8') as f:
        func().writeSvg(f.write)

print("¡Hecho! Se generaron los diagramas respetando la recursión literal.")