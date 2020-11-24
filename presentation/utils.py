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