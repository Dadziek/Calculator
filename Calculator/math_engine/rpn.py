import math
from .tokenizer import tokenize


def infix_to_rpn(expression: str) -> str:
    precedence = {
        '+': 1, '-': 1,
        '*': 2, '/': 2, '%': 2,
        '^': 3,
        'sqrt': 4, 'sin': 4, 'cos': 4, 'tan': 4,
        'asin': 4, 'acos': 4, 'atan': 4,
        'sinh': 4, 'cosh': 4, 'tanh': 4,
        'asinh': 4, 'acosh': 4, 'atanh': 4,
        'log': 4, 'log2': 4, 'ln': 4,
        'abs': 4, 'exp': 4,
        'floor': 4, 'ceil': 4, 'trunc': 4,
        'deg': 4, 'rad': 4,
        '!': 5
    }
    left_assoc = {'+', '-', '*', '/', '%'}
    output, stack = [], []
    tokens = tokenize(expression)

    for token in tokens:
        if token.replace('.', '', 1).isdigit() or token in ('pi', 'e', 'tau', 'phi', 'x'):
            output.append(token)
        elif token in precedence:
            while (stack and stack[-1] in precedence and
                   ((precedence[stack[-1]] > precedence[token]) or
                    (precedence[stack[-1]] == precedence[token] and token in left_assoc))):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif token == ',':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
        else:
            raise ValueError(f'Nieznany token: {token}')

    while stack:
        output.append(stack.pop())

    return ' '.join(output)


def rpn(expression: str, x_val=None) -> float:
    stack = []
    for token in expression.split():
        if token.replace('.', '', 1).isdigit():
            stack.append(float(token))
        elif token == 'pi':
            stack.append(math.pi)
        elif token == 'e':
            stack.append(math.e)
        elif token == 'tau':
            stack.append(math.tau)
        elif token == 'phi':
            stack.append((1 + math.sqrt(5)) / 2)
        elif token == 'x':
            stack.append(x_val if x_val is not None else 0)

        elif token in ('+', '-', '*', '/', '%', '^'):
            b, a = stack.pop(), stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
            elif token == '%':
                stack.append(a % b)
            elif token == '^':
                stack.append(a ** b)

        elif token == '!':
            a = stack.pop()
            stack.append(math.factorial(int(a)))

        elif token in ('sqrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
                       'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
                       'log2', 'ln', 'abs', 'exp', 'floor', 'ceil', 'trunc', 'deg', 'rad'):
            a = stack.pop()
            if token == 'sqrt':
                stack.append(math.sqrt(a))
            elif token == 'sin':
                stack.append(math.sin(a))
            elif token == 'cos':
                stack.append(math.cos(a))
            elif token == 'tan':
                stack.append(math.tan(a))
            elif token == 'asin':
                stack.append(math.asin(a))
            elif token == 'acos':
                stack.append(math.acos(a))
            elif token == 'atan':
                stack.append(math.atan(a))
            elif token == 'sinh':
                stack.append(math.sinh(a))
            elif token == 'cosh':
                stack.append(math.cosh(a))
            elif token == 'tanh':
                stack.append(math.tanh(a))
            elif token == 'asinh':
                stack.append(math.asinh(a))
            elif token == 'acosh':
                stack.append(math.acosh(a))
            elif token == 'atanh':
                stack.append(math.atanh(a))
            elif token == 'log2':
                stack.append(math.log2(a))
            elif token == 'ln':
                stack.append(math.log(a))
            elif token == 'abs':
                stack.append(abs(a))
            elif token == 'exp':
                stack.append(math.exp(a))
            elif token == 'floor':
                stack.append(math.floor(a))
            elif token == 'ceil':
                stack.append(math.ceil(a))
            elif token == 'trunc':
                stack.append(math.trunc(a))
            elif token == 'deg':
                stack.append(math.degrees(a))
            elif token == 'rad':
                stack.append(math.radians(a))

        elif token == 'log':
            base = stack.pop()
            value = stack.pop()
            stack.append(math.log(value, base))
        else:
            raise ValueError(f'Nieznany token: {token}')
    return stack.pop()
