import re

number = r'-?\d+(?:\.\d+)?'


def brackets(q):
    q = q.groups()
    return q[0] + str(calc(q[1])) + q[2]


def calc(expr):
    q = re.search(r'(.*?)\((.*)\)(.*?)', expr)
    if q:
        result = brackets(q)
        expr = re.sub(r'(.*?)\((.*)\)(.*?)', str(result), expr)

        return calc(expr)

    # тут выражение уже без скобочек

    def mul_div(q):
        q = q.groups()
        i1 = q[0]
        i2 = q[2]
        op = q[1]
        if op == "*":
            result = float(i1) * float(i2)
        if op == "/":
            result = float(i1) / float(i2)
        return str(result)

    while True:
        new_expr = re.sub(r'(' + number + r')(\*|\/)(' + number + r')', mul_div, expr)
        if new_expr == expr:
            break
        expr = new_expr


    def plus_minus(q):
        q = q.groups()
        i1 = q[0]
        i2 = q[2]
        op = q[1]
        if op == "+":
            result = float(i1) + float(i2)
        if op == "-":
            result = float(i1) - float(i2)
        return str(result)

    while True:
        new_expr = re.sub(r'(' + number + r')(\+|-)(' + number + r')', plus_minus, expr)
        if new_expr == expr:
            break
        expr = new_expr

    return float(expr)
