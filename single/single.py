import sys
sys.path.append('../')
from delta import Delta

def string_to_delta(text):
    temp_text = text[7:]
    delta_text = temp_text[:-2]
    delta_list = delta_text.split(',')

    if len(delta_list) == 1:
        ops = delta_list[0][2:8]
        
        if ops == 'insert':
            value = delta_list[0][12:-2]
            print(value)
            return Delta().insert(value)
        
        elif ops == 'delete':
            value = int(delta_list[0][11:-1])
            return Delta().delete(value)

    elif len(delta_list) == 2:
        for i in range(2):
            if i == 0:
                ops_1 = delta_list[0][2:8]
                value_1 = int(delta_list[0][11:12])

            elif i == 1:
                ops_2 = delta_list[1][3:9]

                if ops_2 == 'insert':
                    value_2 = delta_list[1][13:-2]
                    return Delta().retain(value_1).insert(value_2)
                
                elif ops_2 == 'delete':
                    value_2 = int(delta_list[1][12:-1])
                    return Delta().retain(value_1).delete(value_2)

    return Delta()


# Test on string_to_delta
def string_to_delta_test():
    a = Delta().insert('ABCDE')
    b = Delta().retain(3).delete(4)
    c = Delta().delete(4)

    print(a)
    print(string_to_delta(str(a)))
    print(b)
    print(string_to_delta(str(b)))
    print(c)
    print(string_to_delta(str(c)))

# Operation test: Sequential insert/delete
def seq_OT():
    a = Delta().insert('ABCDE')
    print('a')
    print(a)
    b = Delta().retain(3).insert('Z')
    c = Delta().delete(4)

    result_1 = a.compose(b)
    result_2 = result_1.compose(c)
    print("result 1:")
    print(result_1)
    print("result 2:")
    print(result_2)


# Transformation test: Concurrency
def concurrency_OT():

    initial = Delta().insert('ABCD')
    client_operation = Delta().retain(3).insert("X")
    server_operation = Delta().retain(1).delete(1)

    # Client
    client_local = initial.compose(client_operation)
    client_transform = client_operation.transform(server_operation)
    client_result = client_local.compose(client_transform)

    # Server
    server_local = initial.compose(server_operation)
    server_transform = server_operation.transform(client_operation) # Change from retaining 3rd pos to 2nd pos
    server_result = server_local.compose(server_transform)

    print(client_result) #ACXD
    print(server_result) #ACXD

if __name__ == "__main__":
    string_to_delta_test()
    # seq_OT()
    # concurrency_OT()
    