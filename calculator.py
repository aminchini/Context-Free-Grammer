from CFG import Grammer

calculator = Grammer([
    9,
    "<START> -> <VALUE>|<VALUE><OPERATOR><START>",
    "<VALUE> -> <NUMBER>|<SIGN><NUMBER>",
    "<NUMBER> -> <UNSIGNED>|<UNSIGNED><DOT><UNSIGNED>",
    "<UNSIGNED> -> <DIGIT>|<DIGIT><UNSIGNED>",
    "<DIGIT> -> 0|1|2|3|4|5|6|7|8|9",
    "<OPERATOR> -> +|-|*|/|^",
    "<SIGN> -> (+)|(-)",
    "<DOT> -> ."
])

operators = {
    '+' : 0,
    '-' : 0,
    '*' : 1,
    '/' : 1,
    '^' : None
}


# Making a proper postfix notation of the input
# To be used in calculatin Stack
def proper_input(elements):
    out = list()
    stack = list()
    for element in elements:
        if element in operators.keys():
            while len(stack) and stack[-1] in operators.keys():

                if operators[element] - operators[stack[-1]] <= 0:
                    out.append(stack.pop())
                    continue
                break

            stack.append(element)
        else:
            out.append(element)
    while len(stack):
        out.append(stack.pop())
    return out


def calculate(string):
    s = 0
    validate = list()
    exp = list()
    temp = ''
    while s < len(string):
        if(string[s] == '('):
            item = string[s:s+3:]
            validate.append(item)
            temp += item[1]
            s += 3
        else:
            item = string[s]
            validate.append(item)
            if item in operators.keys():
                exp.append(temp)
                exp.append(item)
                temp = ''
            else:
                temp += item
            s += 1
    exp.append(temp)

    if calculator.IsGenerateByGrammer(' '.join(validate)):
        statement = list()
        counter = 0
        for item in exp:
            if item == '^':
                statement += ['*', exp[counter-1]]*(int(exp[counter+1])-1)
                exp.pop(counter+1)
                counter += 1
            else:
                statement.append(item)
                counter += 1
        queue = proper_input(statement)
        stack = list()
        while len(queue):
            op = queue.pop(0)
            if op in operators.keys():
                item1 = stack.pop()
                item2 = stack.pop()
                value = eval(item2 + op + item1)
                stack.append(str(value))
            else:
                stack.append(op)
        return stack.pop()

    else:
        return 'Invalid Input!!'
