import re

from django.db.models import Q

# The precedence we're using is the same as Python uses
# Basically, OR < AND < NOT
OPERATORS = {
    '&': {  # AND
        'precedence': 1,
        'operands': 2,
    },
    '|': {  # OR
        'precedence': 0,
        'operands': 2,
    },
    '~': {  # NOT
        'precedence': 2,
        'operands': 1,
    },
}

# This regex is complicated, but when fed into re.findall, it will split an
# input string by spaces, while preserving spaces inside quotes.
# We could have used the builtin shlex.split, but that function will not
# preserve the quotation marks themselves, which we need later
TOKENIZER = re.compile(r'(?:[^\s"]|"(?:\\.|[^"])*")+')


def infix_to_postfix(query_string):
    '''
    Converts a query string from infix to postfix notation

    We receive an infix string from the front-end, because it's easier to build
    However, postfix is easier to process, so that's how we save it

    Infix vs. postfix notation is just a matter of where the operate sits;
    In infix notation, the operator is between the operands:
        A + B
    In postfix notation, the operator comes after the operands:
        A B +

    We prefer postfix for two reasons:
        1. The expression is always unambiguous
            Consider 3 - 4 + 5.
            Without brackets, this is an ambiguous formula; it could be either:
                (3 - 4) + 5 == 4
                3 - (4 + 5) == -6
            In postfix, those two formula have different constructions:
                3 4 - 5 +
                3 4 5 + -
            We can save some characters (and some parsing issues) by using
            postfix notation

        2. Parsing a postfix string is easy
            As the algorithms here indicate, it's somewhat more difficult
            to parse an infix expression, because an operator token is read
            before all of its operands are known

            There's negligible performance gain in modern computers,
            especially on input sizes this small, but it makes the algorithms
            easier to understand

    Positional arguments:
        query_string -- The infix string representing the query
    '''
    tokens = TOKENIZER.findall(str(query_string).encode('string-escape'))
    postfix_string = ''
    stack = []

    # This algorithm basically works by shunting operators and operands into
    # different places; hence why it's called the shunting-yard algorithm
    # We're using a simplified version of the algorithm because:
    #   1. We don't have functions, just binary and unary operators
    #   2. We don't care about operator associativity
    #   3. We don't have parentheses, though that would be a minor modification
    for t in tokens:
        if t in OPERATORS:
            op = OPERATORS[t]
            if len(stack) == 0:
                stack.append(t)
            # We want to save higher-precedence operators on top
            elif op['precedence'] > OPERATORS[stack[-1]]['precedence']:
                stack.append(t)
            else:
                # If we currently have a lower-precedence operator, then we can
                # push all the higher-precedence operators into the result
                while (
                        len(stack) > 0 and
                        op['precedence'] < OPERATORS[stack[-1]]['precedence']
                ):
                    postfix_string += stack.pop() + ' '
                stack.append(t)
        else:  # We are an operand, so it goes right onto the result
            postfix_string += t + ' '

    # We're out of tokens, so add the last of the operators
    while len(stack) > 0:
        postfix_string += stack.pop() + ' '

    return postfix_string.strip()


def postfix_to_query_filter(query_string):
    '''
    Essentially a postfix parser, but builds up Q objects for a query filter

    Positional arguments:
        query_string -- The postfix query string
    '''
    tokens = TOKENIZER.findall(str(query_string).encode('string-escape'))
    stack = []

    # The algorithm basically works by pushing tokens onto a stack, and popping
    # operands once we hit an operator
    for t in tokens:
        if t in OPERATORS:
            if t == '~':  # NOT is out only unary operator
                operand = stack.pop()
                stack.append(~operand)
            else:
                loperand = stack.pop()
                roperand = stack.pop()

                if t == '&':
                    push_obj = loperand & roperand
                elif t == '|':
                    push_obj = loperand | roperand
                stack.append(push_obj)
        else:  # We have an operand
            q_filter = t.split('=')[0]
            # We can finally remove the pesky quotes; otherwise the Q ctor
            # will interpret them as part of the query value
            try:
                filter_val = re.sub('["]', '', t.split('=')[1])
            except IndexError:
                pass
            else:
                if filter_val == 'true':
                    filter_val = True
                elif filter_val == 'false':
                    filter_val = False

                push_obj = {q_filter: filter_val}

                # Hooray for Q object creation using dicts
                stack.append(Q(**push_obj))

    try:
        return stack[-1]
    except IndexError:
        return ''
