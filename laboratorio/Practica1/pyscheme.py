# scheme.py
#
# Challenge: Can you implement a scheme interpreter in Python that's
# capable of executing the following procedure?

# A procedure definition for:
#
#   (define fact
#      (lambda (n) (if (= n 1)
#                   1
#                   (* n (fact (- n 1))))
#       )
#    )
#
# It's represented in Python using the following tuple:

fact = ('define', 'fact', 
        ('lambda', ('n'), ('if', ('=', 'n', 1),
                            1,
                            ('*', 'n', ('fact', ('-', 'n', 1))))))

def pon_en_env(x, y):
    global env
    env[x] = seval(y)


env = {'+': lambda x, y: x+y,
       '-': lambda x, y: x-y,
       '*': lambda x, y: x*y,
       '=':lambda x,y: x==y,
    }

def hacer_funcion(argumentos, cuerpo):
    def funcion(*valores):
        old_env = env.copy()  
        for nombre, valor in zip(argumentos, valores):
            env[nombre] = valor
        resultado = seval(cuerpo)
        env.update(old_env)
        return resultado
    return funcion

def sustitucion(exp, nombre, valor):
    if exp == nombre:
        return valor
    elif isinstance(exp, tuple):
        return tuple(sustitucion(e, nombre, valor) for e in exp)
    else:
        return exp

# You will define the following procedure for evaluating an expression
def seval(sexp):
    if isinstance(sexp, int):
        return sexp
    elif isinstance(sexp, str):
        return env.get(sexp, sexp) 
    elif isinstance(sexp, tuple):
        if sexp[0] == 'if':
            condicion = sexp[1]
            se_cumple = sexp[2]
            no_cumple = sexp[3]
            if seval(condicion):
                return seval(se_cumple)
            return seval(no_cumple)
        elif sexp[0] == 'lambda':
            args = sexp[1]
            cuerpo = sexp[2]
            func = hacer_funcion(args, cuerpo)
            return func
        elif sexp[0] == 'define':
            nombre = sexp[1]
            func = sexp[2]
            pon_en_env(nombre, func)
            return
        func = seval(sexp[0])
        args = [seval(e) for e in sexp[1:]]
        return func(*args)

# In writing seval, you are ONLY allowed to use the rules of Scheme
# evaluation that you currently know about.  So far, this includes the
# substitution model and the notion of special forms.
    
# Some basic tests
assert seval(42) == 42
assert seval(('+', ('+', 2,1), 3)) == 6
assert seval(('-', 5,1)) == 4
seval(('define', 'n', 5))

assert seval('n') == 5

# Now the ultimate test--can you run your procedure?
seval(fact)
#print(env)
assert seval(('fact', 'n')) == 120