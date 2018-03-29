import re
from operator import mul, truediv, add, sub, pow

number_pattern = r'-?(?:\d+(?:\.\d+)?|\d*(?:\.\d+)+)'
operation_format = r'(%s)({op})(%s)' % (number_pattern, number_pattern)

operations = {
    '*': mul,
    '/': truediv,
    '+': add,
    '-': sub,
    '^': pow,
}


def calc_brackets(match_obj):
    """ Function to replace result of re.sub for find expression in brackets

    Args:
        match_obj: match object with 3 groups:
            1 - before brackets,
            2 - in brackets,
            3 - after brackets

    Returns:
        str: string with replace expr in brackets on result of expr:
            {before brackets}{result}{after brackets}
    """

    matches = match_obj.groups()
    result = calculate(matches[1])
    return matches[0] + str(result) + matches[2]


def arithm_oper(match_obj):
    """ Function to replace result of re.sub for find arithmetic operation

    Args:
        match_obj: match object with 3 groups:
            1 - before operand,
            2 - operand,
            3 - after operand

    Returns:
        str: string with replace all expr on result of expr.
    """
    matches = match_obj.groups()
    operand = operations[matches[1]]
    result = operand(float(matches[0]), float(matches[2]))
    return str(result)


def validate(expr):
    """ Function to validate arithmetic expression

    Args:
        expr(str): arithmetic expression.

    Returns:
        float: clearly arithmetic expression.
    """

    # delete spaces
    expr = re.sub(r'\s', '', expr)
    # check other symbols:
    other = re.findall(r'[^\*\/\-\+0-9\(\)\.\^]', expr)
    if other:
        raise ValueError(f"Find not arithmetic symbols: {other}")

    return expr


def calculate(expr):
    """ Function to evaluate arithmetic expression

    Args:
        expr(str): arithmetic expression.

    Returns:
        float: result of arithmetic expression.
    """

    expr = validate(expr)

    # calc all in brackets
    while True:
        new_expr = re.sub(r'(.*?)\(([^\(\)]*)\)(.*?)', calc_brackets, expr)
        if new_expr == expr:
            break
        expr = new_expr

    # eval all arithmetic operations by priority
    for oper_pattern in (r'\^', r'\*|\/', r'\+|-'):
        # create pattern
        pattern = operation_format.format(op=oper_pattern)
        while True:
            # try to evaluate. If expr not change, go to next operation
            new_expr = re.sub(pattern, arithm_oper, expr)
            if new_expr == expr:
                break
            expr = new_expr

    return float(expr)
