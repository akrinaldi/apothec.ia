def multijoin(opcode,arg1,arg2):
    arg1type = type(arg1)
    arg2type = type(arg2)
    #plus rules
    if opcode == '+':
        if arg1type or arg2type is str and arg1type or arg2type is int:
            #print('str and int')
            string_add = arg1 if arg1type is int else arg2
            string_base = arg1 if arg1type is str else arg2
            evald = f'{string_base}{string_add}'
        elif arg1type or arg2type is str and arg1type or arg2type is bool:
            #print('str and bool')
            string_add = arg1 if arg1type is bool else arg2
            string_base = arg1 if arg1type is str else arg2
            evald = f'{string_base}{string_add}'
        elif arg1type or arg2type is str and arg1type or arg2type is list:
            #print('str and list')
            string_add = arg1 if arg1type is list else arg2
            string_base = arg1 if arg1type is str else arg2
            evald = f'{string_base}{string_add}'
        elif arg1type or arg2type is int and arg1type or arg2type is bool:
            #print('int and bool')
            myint = arg1 if arg1type is int else arg2
            mybool = arg1 if arg1type is bool else arg2
            if mybool == True:
                mybool = 1
            else:
                mybool = 0
            evald = myint + mybool
        elif arg1type or arg2type is int and arg1type or arg2type is list:
            #print('int and list')
            my_list_add = arg1 if arg1type is int else arg2
            my_list_val = arg1 if arg1type is list else arg2
            evald = my_list_val.append(my_list_add)
        elif arg1type or arg2type is bool and arg1type or arg2type is list:
            #print('bool and list')
            my_list_val = arg1 if arg1type is list else arg2
            my_list_add = arg1 if arg1type is bool else arg2
            evald = my_list_val.append(my_list_add)
    elif opcode == '-':
        if arg1type or arg2type is str and arg1type or arg2type is int:
            #print('str and int')
            string_sub = arg1 if arg1type is int else arg2
            string_base = arg1 if arg1type is str else arg2
            string_list = string_base.split()
            try:
                new_string_list = string_list.pop(string_sub)
            except Exception:
                new_string_list.clear()
            evald = ''.join(new_string_list)
        elif arg1type or arg2type is str and arg1type or arg2type is bool:
            #print('str and bool')
            string_bool = arg1 if arg1type is bool else arg2
            string_base = arg1 if arg1type is str else arg2
            if string_bool == True:
                string_bool = 1
            else:
                string_bool = 0
            string_list = string_base.split()
            try:
                new_string_list = string_list.pop(string_bool)
            except Exception:
                new_string_list.clear()
            evald = ''.join(new_string_list)
        elif arg1type or arg2type is str and arg1type or arg2type is list:
            #print('str and list')
            string_sub = arg1 if arg1type is list else arg2
            string_base = arg1 if arg1type is str else arg2
            string_list = string_base.split()
            try:
                new_string_list = string_list.pop(len(string_sub))
            except Exception:
                new_string_list.clear()
            evald = ''.join(new_string_list)
        elif arg1type or arg2type is int and arg1type or arg2type is bool:
            #print('int and bool')
            myint = arg1 if arg1type is int else arg2
            mybool = arg1 if arg1type is bool else arg2
            if mybool == True:
                mybool = 1
            else:
                mybool = 0
            evald = myint - mybool
        elif arg1type or arg2type is int and arg1type or arg2type is list:
            #print('int and list')
            my_list_sub = arg1 if arg1type is int else arg2
            my_list_val = arg1 if arg1type is list else arg2
            evald = my_list_val.pop(my_list_sub)
        elif arg1type or arg2type is bool and arg1type or arg2type is list:
            #print('bool and list')
            my_list_val = arg1 if arg1type is list else arg2
            my_list_sub = arg1 if arg1type is bool else arg2
            try:
                evald = my_list_val.pop(my_list_sub)
            except Exception:
                new_string_list.clear()
    elif opcode == '*':
        if arg1type or arg2type is str and arg1type or arg2type is int:
            #print('str and int')
            string_multiplier = arg1 if arg1type is int else arg2
            string_base = arg1 if arg1type is str else arg2
            evald = string_base * string_multiplier
        elif arg1type or arg2type is str and arg1type or arg2type is bool:
            #print('str and bool')
            string_bool = arg1 if arg1type is bool else arg2
            if string_bool == True:
                string_bool = 1
            else:
                string_bool = 0
            string_base = arg1 if arg1type is str else arg2
            evald = string_base * string_bool
        elif arg1type or arg2type is str and arg1type or arg2type is list:
            #print('str and list')
            string_list = arg1 if arg1type is list else arg2
            string_multiplier = len(string_list)
            string_base = arg1 if arg1type is str else arg2
            evald = string_base * string_multiplier
        elif arg1type or arg2type is int and arg1type or arg2type is bool:
            #print('int and bool')
            myint = arg1 if arg1type is int else arg2
            mybool = arg1 if arg1type is bool else arg2
            if mybool == True:
                mybool = 1
            else:
                mybool = 0
            evald = myint * mybool
        elif arg1type or arg2type is int and arg1type or arg2type is list:
            #print('int and list')
            my_list_len = arg1 if arg1type is int else arg2
            my_list_val = arg1 if arg1type is list else arg2
            evald = [my_list_val]*my_list_len
        elif arg1type or arg2type is bool and arg1type or arg2type is list:
            #print('bool and list')
            my_list_val = arg1 if arg1type is list else arg2
            my_list_len = len(my_list_val)
            my_list_multiplier = arg1 if arg1type is bool else arg2
            count = 0
            while count <= my_list_len:
                my_list_val.append(my_list_multiplier)
                count+=1
            evald = my_list_val
    elif opcode == '/':
        if arg1type or arg2type is str and arg1type or arg2type is int:
            #print('str and int')
            string_multiplier = arg1 if arg1type is int else arg2
            string_base = arg1 if arg1type is str else arg2
            string_list = string_base.split()
            while count <= string_multiplier:
                try:
                    string_list.pop()
                    count+=1
                except Exception:
                    string_list.clear()
            evald = ''.join(string_list)
        elif arg1type or arg2type is str and arg1type or arg2type is bool:
            #print('str and bool')
            string_bool = arg1 if arg1type is bool else arg2
            if string_bool == True:
                string_bool = 1
            else:
                string_bool = 0
            string_base = arg1 if arg1type is str else arg2
            string_list = string_base.split()
            while count <= string_bool:
                try:
                    string_list.pop()
                    count+=1
                except Exception:
                    string_list.clear()
            evald = ''.join(string_list)
        elif arg1type or arg2type is str and arg1type or arg2type is list:
            #print('str and list')
            string_list = arg1 if arg1type is list else arg2
            pop_mod = len(string_list)
            string_base = arg1 if arg1type is str else arg2
            string_list = string_base.split()
            while count <= pop_mod:
                try:
                    string_list.pop()
                    count+=1
                except Exception:
                    string_list.clear()
            evald = ''.join(string_list)
        elif arg1type or arg2type is int and arg1type or arg2type is bool:
            #print('int and bool')
            myint = arg1 if arg1type is int else arg2
            mybool = arg1 if arg1type is bool else arg2
            if mybool == True:
                mybool = 1
            else:
                mybool = 0
            evald = myint / mybool
        elif arg1type or arg2type is int and arg1type or arg2type is list:
            #print('int and list')
            my_list_pop = arg1 if arg1type is int else arg2
            my_list_val = arg1 if arg1type is list else arg2
            while count <= my_list_pop:
                try:
                    my_list_val.pop()
                    count+=1
                except Exception:
                    my_list_val.clear()
            evald = my_list_val
        elif arg1type or arg2type is bool and arg1type or arg2type is list:
            #print('bool and list')
            my_list_val = arg1 if arg1type is list else arg2
            my_list_len = len(my_list_val)
            mybool = arg1 if arg1type is bool else arg2
            if mybool == True:
                mybool = 1
            else:
                mybool = 0
            count = 0
            while count <= mybool:
                try:
                    my_list_val.pop()
                    count+=1
                except Exception:
                    my_list_val.clear()
            evald = my_list_val
    return evald

def stringjoin(opcode,arg1,arg2):
    if opcode == '+':
        evald = f'{arg1} + {arg2}'
    elif opcode == '-':
        evald = f'{arg1} - {arg2}'
    elif opcode == '*':
        evald = f'{arg1} * {arg2}'
    elif opcode == '/':
        evald = f'{arg1} / {arg2}'
    return evald

def booljoin(opcode,arg1,arg2):
    if arg1 == True:
        val1 = 1
    else:
        val1 = 0
    if arg2 == True:
        val2 = 1
    else:
        val2 = 0
    if opcode == '+':
        evald = val1 + val2
    elif opcode == '-':
        evald = val1 - val2
    elif opcode == '*':
        evald = val1 * val2
    elif opcode == '/':
        evald = val1 / val2
    return evald

def intjoin(opcode,arg1,arg2):
    if opcode == '+':
        evald = arg1 + arg2
    elif opcode == '-':
        evald = arg1 - arg2
    elif opcode == '*':
        evald = arg1 * arg2
    elif opcode == '/':
        evald = arg1 / arg2
    return evald

def charjoin(opcode,arg1,arg2):
    evald_list = arg1
    evald_list.append(opcode)
    for i in arg2:
        evald_list.append(i)
    evald = evald_list
    return evald