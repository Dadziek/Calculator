from sympy import symbols, Eq, solve


def solve_equation(expr: str):
    x = symbols('x')
    if '=' not in expr:
        raise ValueError("Równanie musi zawierać '='")
    left, right = expr.split('=')
    eq = Eq(eval(left, {'x': x}), eval(right, {'x': x}))
    roots = solve(eq, x)
    if not roots:
        return []
    return [float(r) for r in roots]


def solve_system(equations, variables):
    vars_symbols = symbols(",".join(variables))
    eqs = []
    for eq_text in equations:
        if '=' not in eq_text:
            raise ValueError("Równanie musi zawiera '='")
        left, right = eq_text.split('=')
        eqs.append(Eq(eval(left, dict(zip(variables, vars_symbols))),
                      eval(right, dict(zip(variables, vars_symbols)))))
    sol = solve(eqs, vars_symbols, dict=True)
    if sol:
        return {str(k): float(v) for k, v in sol[0].items()}
    return {}
