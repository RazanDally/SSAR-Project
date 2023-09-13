from while_lang.syntax import WhileParser
import operator
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat

OP = {'+': operator.add, '-': operator.sub,
      '*': operator.mul, '/': operator.floordiv,
      '!=': operator.ne, '>': operator.gt, '<': operator.lt,
      '<=': operator.le, '>=': operator.ge, '=': operator.eq}


def mk_env(pvars):
    return {v: Int(v) for v in pvars}


def upd(d, k, v):
    d = d.copy()
    d[k] = v
    return d


def aux_verify(ast, Q, linv, env1):
    if ast.root == 'skip':
        return Q

    elif ast.root == ':=':  # wp[x := e]Q = Q[e/x]
        x = ast.subtrees[0].subtrees[0].root
        e = aux_verify(ast.subtrees[1], Q, linv, env1)
        return lambda env: Q(upd(env, x, e(env)))

    elif ast.root == ';':  # wp[c1;c2]Q = wp[c1][wp[c2]Q]
        wp_c2 = aux_verify(ast.subtrees[1], Q, linv, env1)
        return aux_verify(ast.subtrees[0], wp_c2, linv, env1)

    elif ast.root == 'if':  # wp[if b then c1 else c2]Q = (b && wp[c1]Q) || (!b && wp[c2]Q)
        b_cond = aux_verify(ast.subtrees[0], Q, linv, env1)
        c1_then = aux_verify(ast.subtrees[1], Q, linv, env1)
        c2_else = aux_verify(ast.subtrees[2], Q, linv, env1)
        return lambda env: Or(And(b_cond(env), c1_then(env)), And(Not(b_cond(env)), c2_else(env)))

    elif ast.root == 'while':  # wp[while b do c]Q = linv && Forall v in env(linv && b -> wp[c](linv)) && (linv && !b -> Q))
        b_cond = aux_verify(ast.subtrees[0], Q, linv, env1)
        wp_c = aux_verify(ast.subtrees[1], linv, linv, env1)
        return lambda env: And(linv(env),
                               ForAll(list(env1.values()),
                                      And(Implies(And(linv(env1), b_cond(env1)), wp_c(env1)),
                                          Implies(And(linv(env1), Not(b_cond(env1))), Q(env1)))))

    # Evaluate expressions
    elif ast.root == 'id':
        return lambda env: env[ast.subtrees[0].root]

    elif ast.root == 'num':
        return lambda env: ast.subtrees[0].root

    elif ast.root in OP.keys():
        op = OP[ast.root]
        lhs_expr = aux_verify(ast.subtrees[0], Q, linv, env1)
        rhs_expr = aux_verify(ast.subtrees[1], Q, linv, env1)
        return lambda env: op(lhs_expr(env), rhs_expr(env))


def verify(P, ast, Q, linv=None):
    """
    Verifies a Hoare triple {P} c {Q}
    Where P, Q are assertions (see below for examples)
    and ast is the AST of the command c.
    Returns `True` iff the triple is valid.
    Also prints the counterexample (model) returned from Z3 in case
    it is not.
    """

    print(ast)
    # from lib.adt.tree.viz import dot_print
    # dot_print(ast)
    # ...
    solver = Solver()
    pvars = set(n for n in ast.terminals if isinstance(n, str) and n != 'skip')
    env = mk_env(pvars)
    formula = Implies(P(env), aux_verify(ast, Q, linv, env)(env))
    solver.add(Not(formula))

    if solver.check() == unsat:
        return True
    else:
        print(solver.model())
        return False


if __name__ == '__main__':
    # # example program
    pvars = ['a', 'b', 'i', 'n']
    program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
    P = lambda _: True
    Q = lambda d: d['a'] == d['b']
    linv = lambda d: d['a'] == d['b']

    #
    # Following are other programs that you might want to try
    #

    # Program 1
    # pvars = ['x', 'i', 'y']
    # program = "y := 0 ; while y < i do ( x := x + y ; if (x * y) < 10 then y := y + 1 else skip )"
    # P = lambda d: d['x'] > 0
    # Q = lambda d: d['x'] > 0
    # linv = lambda d: **figure it out!**

    ## Program 2
    # pvars = ['a', 'b']
    # program = "while a != b do if a > b then a := a - b else b := b - a"
    # P = lambda d: And(d['a'] > 0, d['b'] > 0)
    # Q = lambda d: And(d['a'] > 0, d['a'] == d['b'])
    # linv = lambda d: ???

    ast = WhileParser()(program)

    if ast:
        print(">> Valid program.")
        # Your task is to implement "verify"
        verify(P, ast, Q, linv=linv)
    else:
        print(">> Invalid program.")
