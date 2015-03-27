OPERATOR_PRECEDENCE = {
    'AND': 1,
    'OR': 0,
    'NOT': 2,
}


def infix_to_postfix(query_string):
    tokens = query_string.split()
    postfix_string = ''
    stack = []

    for t in tokens:
        if t in OPERATOR_PRECEDENCE.keys():
            if len(stack) == 0:
                stack.append(t)
            elif OPERATOR_PRECEDENCE[t] > OPERATOR_PRECEDENCE[stack[-1]]:
                stack.append(t)
            else:
                while (
                        len(stack) > 0 and
                        OPERATOR_PRECEDENCE[t] < OPERATOR_PRECEDENCE[stack[-1]]
                ):
                    postfix_string += stack.pop() + ' '
                stack.append(t)
        else:
            postfix_string += t + ' '

    while len(stack) > 0:
        postfix_string += stack.pop() + ' '

    return postfix_string.strip()
