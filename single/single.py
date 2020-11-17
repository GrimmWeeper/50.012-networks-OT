import sys
sys.path.append('../')
from delta import Delta

# Operation test: Sequential insert/delete
def seq_OT():
    a = Delta().insert('ABCDE')
    b = Delta().retain(3).insert('Z')
    c = Delta().delete(4)

    result_1 = a.compose(b)
    result_2 = result_1.compose(c)
    print(result_1)
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
    seq_OT()
    concurrency_OT()
    