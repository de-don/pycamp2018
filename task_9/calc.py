import re
from operator import mul, truediv, add, sub, pow

number = r'-?\d+(?:\.\d+)?'

operations = {
    '*': mul,
    '/': truediv,
    '+': add,
    '-': sub,
    '^': pow,
}


def brackets(q):
    q = q.groups()
    return q[0] + str(calc(q[1])) + q[2]


def arithm_oper(q):
    q = q.groups()
    result = operations[q[1]](float(q[0]), float(q[2]))
    return str(result)


def calc(expr):
    # brackets
    while True:
        new_expr = re.sub(r'(.*?)\((.*)\)(.*?)', brackets, expr)
        if new_expr == expr:
            break
        expr = new_expr

    for oper in (r'\^', r'\*|\/', r'\+|-'):
        while True:
            new_expr = re.sub(
                r'({num})({op})({num})'.format(num=number, op=oper),
                arithm_oper,
                expr
            )
            if new_expr == expr:
                break
            expr = new_expr

    return float(expr)


def calculate(expr):
    # delete spaces
    expr = re.sub(r'\s', '', expr)
    # check other symbols:
    other = re.findall(r'[^\*\/\-\+0-9\(\)\.\^]', expr)
    if other:
        raise ValueError(f"Find not arithmetic symbols: {other}")

    return calc(expr)