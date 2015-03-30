import re

from django.db.models import Q

OPERATORS = {
    '&': {
        'precedence': 1,
        'operands': 2,
    },
    '|': {
        'precedence': 0,
        'operands': 2,
    },
    '~': {
        'precedence': 2,
        'operands': 1,
    },
}


def infix_to_postfix(query_string):
    tokens = re.findall(
        r'(?:[^\s"]|"(?:\\.|[^"])*")+',
        str(query_string).encode('string-escape')
    )
    postfix_string = ''
    stack = []

    for t in tokens:
        if t in OPERATORS:
            op = OPERATORS[t]
            if len(stack) == 0:
                stack.append(t)
            elif op['precedence'] > OPERATORS[stack[-1]]['precedence']:
                stack.append(t)
            else:
                while (
                        len(stack) > 0 and
                        op['precedence'] < OPERATORS[stack[-1]]['precedence']
                ):
                    postfix_string += stack.pop() + ' '
                stack.append(t)
        else:
            postfix_string += t + ' '

    while len(stack) > 0:
        postfix_string += stack.pop() + ' '

    return postfix_string.strip()


def postfix_to_query_filter(query_string):
    tokens = re.findall(
        r'(?:[^\s"]|"(?:\\.|[^"])*")+',
        str(query_string).encode('string-escape')
    )
    stack = []

    for t in tokens:
        if t in OPERATORS:
            if len(stack) < OPERATORS[t]['operands']:
                raise TypeError(
                    '''Not enough arguments to operator {0}.
                    Expected {1}, found {2}'''.format(
                        t,
                        OPERATORS[t]['operand'],
                        len(stack)
                    )
                )
            elif t == '~':
                operand = stack.pop()
                stack.push(~operand)
            else:
                loperand = stack.pop()
                roperand = stack.pop()

                if t == '&':
                    push_obj = loperand & roperand
                elif t == '|':
                    push_obj = loperand | roperand
                stack.append(push_obj)
        else:
            q_filter = t.split('=')[0]
            filter_val = re.sub('["]', '', t.split('=')[1])

            if filter_val == 'true':
                filter_val = True
            elif filter_val == 'false':
                filter_val = False

            push_obj = {q_filter: filter_val}

            stack.append(Q(**push_obj))

    if len(stack) == 1:
        return stack[-1]
    else:
        raise TypeError(
            'Too many tokens ({0}) left on stack'.format(len(stack))
        )
