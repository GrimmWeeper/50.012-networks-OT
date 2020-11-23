import random

def gen_operation():
    value = str(random.randint(1,10))
    operation = random.choice(["plus","minus","multiply","divide"])

    return operation + ',' + value

def compute(current, operation):
    operation_list = operation.split(',')

    if operation_list[0] == 'plus':
        result = current + int(operation_list[1])
    
    elif operation_list[0] == 'minus':
        result = current - int(operation_list[1])

    elif operation_list[0] == 'multiply':
        result = current * int(operation_list[1])

    elif operation_list[0] == 'divide':
        result = current / int(operation_list[1])

    return result