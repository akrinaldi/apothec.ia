#basic stuff we need

import sys
import random
import ast


from multijoin import multijoin,charjoin,intjoin,booljoin,stringjoin


system_weight = random.randint(0,4)

# read arguments
program_filepath = sys.argv[1]

# read file lines
program_lines = []
with open(program_filepath, "r") as program_file:
    program_lines = [
        line.strip() 
            for line in program_file.readlines()]


tokens_list = []

for line in program_lines:
    tokens = line.split()
    tokens_list.append(tokens)

#print(tokens_list)

#declare env

env = {}

declared_state = tokens_list[0][0]
#print(declared_state)

def state_selector(some_state):
        states_list = ['ennui','strict','floaty','fugue']
        val = len(some_state) + system_weight
        if val == 10:
            program_state = declared_state
        else:
            states_list.remove(some_state)
            program_state = states_list[random.randint(0,2)]
        return program_state


program_state = state_selector(declared_state)
#print(program_state)

env.update({'program_state':program_state})

built_ins = {
        'observe':'observe',
        'assign':'has',
        'if': 'propose',
        'else':'unless',
        'length': 'scope',
        'while': 'until',
        'in': 'isin',
        'not in': 'notin',
        'add':'+',
        'subtract':'-',
        'multiply':'*',
        'divide':'/'   
    }

#what if it only observed? It only proposed new possibliities for the variables and then observed them?
#what would we even want for that?
#things can either be in x or not in x, and while loops only operate on those properties



class statement:
    pass

class state(statement):
    def __init__(self, value):
        self.value = program_state

    if program_state == None:
        program_state == 'ennui'
    else:
        state_selector(program_state)

class has(statement):
    def __init__(self,key,val):
        self.key = key
        self.val = val

class observe(statement):
    def __init__(self, expression):
        self.expression = expression

class operator(statement):
    def __init__(self, symbol, arg1, arg2):
        self.symbol = symbol
        self.arg1 = arg1
        self.arg2 = arg2

class containsearch(statement):
    def __init__(self, searchobject, listobject):
        self.searchobject = searchobject
        self.listobject = listobject

class scope:
    def __init__(self, list):
        self.list = list

class propose:
    def __init__(self, testval, cond, target, truecond, falsecond):
        self.testval = testval
        self.cond = cond
        self.target = target
        self.truecond = truecond
        self.falsecond = falsecond      


### strict functions ###

def scope_eval_strict(my_line,env):
    current_env = env
    target_list = my_line[1]
    #print(target_list)
    list_obj = scope(current_env[target_list])
    env[target_list].append('scoped')
    print(len(list_obj.list))

def observe_eval_strict(my_line,env):
    current_env = env
    expression = ' '.join(my_line[1:])
    observe_statement = observe(expression)
    current_env_keys = [v for v in env.keys()]
    #print(observe_statement.expression)
    if observe_statement.expression in current_env_keys:
        #print("beans")
        env[observe_statement.expression].append('observed')
        trace_vals = current_env[(observe_statement.expression)]
        print(str(trace_vals[0]) + ' has been ' + str([i for i in trace_vals[1:]]))
    else:
        print(observe_statement.expression)

def operator_eval_strict(my_line,env):
    op_token = my_line[0]
    arg1 = my_line[1]
    arg2 = my_line[2]
    current_env_keys = [v for v in env.keys()]
    if arg1 in current_env_keys:
        store_key = arg1
        val_items = env[arg1]
        val_items.append('called')
        var_assign = has(store_key, val_items)
        env.update({store_key: var_assign.val})
        arg1 = int(env[arg1][0])
    if arg2 in current_env_keys:
        store_key = arg2
        val_items = env[arg2]
        val_items.append('called')
        var_assign = has(store_key, val_items)
        env.update({store_key: var_assign.val})
        arg2 = int(env[arg2][0])
    if op_token == '+':
        evald = int(arg1) + int(arg2)
        print(evald)
    elif op_token == '-':
        evald = int(arg1) - int(arg2)
        print(evald)
    elif op_token == '*':
        evald = int(arg1) * int(arg2)
        print(evald)
    elif op_token == '/':
        evald = int(arg1) / int(arg2)
        print(evald)

def variable_eval_strict(my_line,env):
    current_env = env
    var = my_line[0]
    val = []
    val.append(' '.join(my_line[2:]))
    #print(val)
    if '~' not in val[0]:
        val.append('assigned')
        var_assign = has(var, val)
        env.update({var_assign.key: var_assign.val})
        #print(env)
    else:
        val_items = current_env[var]
        #print(val_items)
        subvals = val[0].split(' ')
        #print(subvals)
        if '+' or '-' or '*' or '/' in subvals:
            current_env = env
            op_token = subvals[1]
            arg1 = subvals[2]
            arg2 = subvals[3]
            current_env_keys = [v for v in current_env.keys()]
            if arg1 in current_env_keys:
                key = arg1
                arg1 = int(env[arg1][0])
            if arg2 in current_env_keys:
                key = arg2
                arg2 = int(env[arg2][0])
            if op_token == '+':
                evald = int(arg1) + int(arg2)
                #print(val_items)
                new_items = [val_items[0],'added','reassigned']
                val_items.extend(new_items)
                val_items[0] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
                #print(var_assign.val)
            elif op_token == '-':
                evald = int(arg1) - int(arg2)
                new_items = [val_items[0],'subtracted','reassigned']
                val_items.extend(new_items)
                val_items[0] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            elif op_token == '*':
                evald = int(arg1) * int(arg2)
                new_items = [val_items[0],'multiplied','reassigned']
                val_items.extend(new_items)
                val_items[0] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            elif op_token == '/':
                evald = int(arg1) / int(arg2)
                new_items = [val_items[0],'divided','reassigned']
                val_items.extend(new_items)
                val_items[0] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            

def propose_eval_strict(my_line,env):
    current_env = env
    #print("found join")
    cond_val = my_line[1]
    cond = my_line[2]
    target_var = my_line[3]
    filtered_truecond = []
    env[target_var].append('proposed')
    for i in my_line[5:]:
        if i != 'unless':
            filtered_truecond.append(i)
        elif i == 'unless':
            break
    if 'unless' not in my_line[4:]:
        no_false_cond = True
        falsecond = None
    else:
        no_false_cond = False
        faldex = my_line.index('unless')
        false_cond_start_dex = faldex + 2
        falsecond = my_line[false_cond_start_dex:]
        #print(falsecond)
    truecond = filtered_truecond
    #print(truecond)
    #print(no_false_cond)
    propose_cond = propose(cond_val, cond, target_var, truecond, falsecond)
    current_env_keys = [v for v in current_env.keys()]
    target_list = env[propose_cond.target]
    if propose_cond.testval in current_env_keys:
        propose_cond.testval = env[propose_cond.testval][0]
    else:
        propose_cond.testval = propose_cond.testval
    if propose_cond.cond == 'isin':
        #grab target, grab the cond_val, compare
        if propose_cond.testval in target_list and no_false_cond == False:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval not in target_list and no_false_cond == False:
            eval_cond = propose_cond.falsecond
        elif propose_cond.testval in target_list and no_false_cond == True:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval not in target_list and no_false_cond == True:
            print('huh?')

    elif propose_cond.cond == 'notin':
        #grab target, grab the cond_val, compare
        if propose_cond.testval not in target_list and no_false_cond == False:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval in target_list and no_false_cond == False:
            eval_cond = propose_cond.falsecond
        elif propose_cond.testval not in target_list and no_false_cond == True:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval in target_list and no_false_cond == True:
            print('huh?')
            
    #print(eval_cond)
    #look at eval_cond and deliver - eval conds can only be actions, like observe, scope, arithmatic, or reassignments
    #get a load of this recursion in its rawest form
    if 'has' in eval_cond:
        variable_eval_strict(eval_cond,env)
    elif 'observe' in eval_cond:
        observe_eval_strict(eval_cond,env)
    elif 'scope' in eval_cond:
        scope_eval_strict(eval_cond,env)
    elif '+' or '-' or '*' or '/' in eval_cond:
        operator_eval_strict(eval_cond,env)        


### floaty functions ###

def observe_eval_floaty(my_line,env):
    current_env = env
    expression = ' '.join(my_line[1:])
    observe_statement = observe(expression)
    current_env_keys = [v for v in env.keys()]
    #print(observe_statement.expression)
    if observe_statement.expression in current_env_keys:
        #print("beans")
        env[observe_statement.expression].append('observed')
        trace_vals = current_env[(observe_statement.expression)]
        try:
            type_options = [trace_vals[0], str(trace_vals[0]), int(trace_vals[0]), bool(trace_vals[0]), trace_vals[0].split()]
            val_select = type_options[random.randint(0,4)]
            print(str(val_select) + ' has been ' + str([i for i in trace_vals[1:]]))
        except ValueError:
            type_options = [trace_vals[0], str(trace_vals[0]), int(len(trace_vals[0])), bool(trace_vals[0]), trace_vals[0].split()]
            val_select = type_options[random.randint(0,4)]
            print(str(val_select) + ' has been ' + str([i for i in trace_vals[1:]]))
    else:
        try:
            type_options = [observe_statement.expression, str(observe_statement.expression), int(observe_statement.expression), bool(observe_statement.expression), observe_statement.expression.split()]
            print(str(type_options[random.randint(0,4)]))
        except ValueError:
            type_options = [observe_statement.expression, str(observe_statement.expression), int(len(observe_statement.expression)), bool(observe_statement.expression), observe_statement.expression.split()]
            print(str(type_options[random.randint(0,4)]))


def scope_eval_floaty(my_line,env):
    current_env = env
    target = my_line[1]
    try:
        target_options = [target, str(target), int(target), bool(target), target.split()]
        #print(target_list)
        our_select_option = random.randint(0,4)
        env[target].append('scoped')
        print(len(target_options[our_select_option]))
    except ValueError:
        target_options = [target, str(target), int(len(target)), bool(target), target.split()]
        #print(target_list)
        our_select_option = random.randint(0,4)
        env[target].append('scoped')
        print(len(str(target_options[our_select_option])))



def operator_eval_floaty(my_line,env):
    op_token = my_line[0]
    arg1 = my_line[1]
    arg2 = my_line[2]
    current_env_keys = [v for v in env.keys()]
    if arg1 in current_env_keys:
        store_key = arg1
        val_items = env[arg1]
        val_items.append('called')
        var_assign = has(store_key, val_items)
        env.update({store_key: var_assign.val})
        #print(var_assign.val)
        arg1 = env[arg1][0]
        try:
            type_options1 = [arg1, str(arg1), int(arg1), bool(arg1), arg1.split()]
            arg1 = type_options1[random.randint(0,4)]

        except ValueError:
            type_options1 = [arg1, str(arg1), int(len(arg1)), bool(arg1), arg1.split()]
            arg1 = type_options1[random.randint(0,4)]
 

    if arg2 in current_env_keys:
        store_key = arg2
        val_items = env[arg2]
        val_items.append('called')
        var_assign = has(store_key, val_items)
        env.update({store_key: var_assign.val})
        arg2 = env[arg2][0]
        try:
            type_options2 = [arg2, str(arg2), int(arg2), bool(arg2), arg2.split()]
            arg2 = type_options2[random.randint(0,4)]

        except ValueError:
            type_options2 = [arg2, str(arg2), int(len(arg2)), bool(arg2), arg2.split()]
            arg2 = type_options2[random.randint(0,4)]


    if op_token == '+':
        if type(arg1) == type(arg2) and type(arg1) is str:
            evald = stringjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is int:
            evald = intjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is bool:
            evald = booljoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is list:
            evald = charjoin(op_token,arg1,arg2)
        else:
            evald = multijoin(op_token,arg1,arg2)
        #print(evald)
    elif op_token == '-':
        if type(arg1) == type(arg2) and type(arg1) is str:
            evald = stringjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is int:
            evald = intjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is bool:
            evald = booljoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is list:
            evald = charjoin(op_token,arg1,arg2)
        else:
            evald = multijoin(op_token,arg1,arg2)
        #print(evald)
    elif op_token == '*':
        if type(arg1) == type(arg2) and type(arg1) is str:
            evald = stringjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is int:
            evald = intjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is bool:
            evald = booljoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is list:
            evald = charjoin(op_token,arg1,arg2)
        else:
            evald = multijoin(op_token,arg1,arg2)
        #print(evald)
    elif op_token == '/':
        if type(arg1) == type(arg2) and type(arg1) is str:
            evald = stringjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is int:
            evald = intjoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is bool:
            evald = booljoin(op_token,arg1,arg2)
        elif type(arg1) == type(arg2) and type(arg1) is list:
            evald = charjoin(op_token,arg1,arg2)
        else:
            evald = multijoin(op_token,arg1,arg2)
        #print(evald)


def variable_eval_floaty(my_line,env):
    current_env = env
    var = my_line[0]
    val = []
    val.append(' '.join(my_line[2:]))
    #print(val)
    if '~' not in val[0]:
        val.append('assigned')
        var_assign = has(var, val)
        env.update({var_assign.key: var_assign.val})
        #print(env)
    else:
        val_items = current_env[var]
        #print(val_items)
        subvals = val[0].split(' ')
        #print(subvals)
        if '+' or '-' or '*' or '/' in subvals:
            current_env = env
            op_token = subvals[1]
            arg1 = subvals[2]
            arg2 = subvals[3]
            current_env_keys = [v for v in current_env.keys()]
            if arg1 in current_env_keys:
                key = arg1
                arg1 = env[arg1][0]
                try:
                    type_options1 = [arg1, str(arg1), int(arg1), bool(arg1), arg1.split()]
                    arg1_typed = type_options1[random.randint(0,4)]
                    arg1type = type(arg1_typed)
                except ValueError:
                    type_options1 = [arg1, str(arg1), int(len(arg1)), bool(arg1), arg1.split()]
                    arg1 = type_options1[random.randint(0,4)]
                    arg1type = type(arg1_typed)

            if arg2 in current_env_keys:
                key = arg2
                arg2 = env[arg2][0]
                try:
                    type_options2 = [arg2, str(arg2), int(arg2), bool(arg2), arg2.split()]
                    arg2_typed = type_options2[random.randint(0,4)]
                    arg2type = type(arg2_typed)
                except ValueError:
                    type_options2 = [arg2, str(arg2), int(len(arg2)), bool(arg2), arg2.split()]
                    arg2 = type_options2[random.randint(0,4)]
                    arg2type = type(arg2_typed)
                

            if op_token == '+':
                if type(arg1) == type(arg2) and type(arg1) is str:
                    evald = stringjoin(op_token,arg1,arg2)
                    #print(evald)
                elif type(arg1) == type(arg2) and type(arg1) is int:
                    evald = intjoin(op_token,arg1,arg2)
                    #print(evald)
                elif type(arg1) == type(arg2) and type(arg1) is bool:
                    evald = booljoin(op_token,arg1,arg2)
                    #print(evald)
                elif type(arg1) == type(arg2) and type(arg1) is list:
                    evald = charjoin(op_token,arg1,arg2)
                    #print(evald)
                else:
                    evald = multijoin(op_token,arg1,arg2)
                    #print(evald)
                #print(val_items)
                new_items = [val_items[0],'added','reassigned']
                val_items.extend(new_items)
                val_items[0] = evald
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
                #print(var_assign.val)
            elif op_token == '-':
                if type(arg1) == type(arg2) and type(arg1) is str:
                    eval = stringjoin(op_token,arg1,arg2)
                elif type(arg1) == type(arg2) and type(arg1) is int:
                    eval = intjoin(op_token,arg1,arg2)
                elif type(arg1) == type(arg2) and type(arg1) is bool:
                    eval = booljoin(op_token,arg1,arg2)
                elif type(arg1) == type(arg2) and type(arg1) is list:
                    eval = charjoin(op_token,arg1,arg2)
                else:
                    eval = multijoin(op_token,arg1_typed,arg2_typed)
                new_items = [val_items[0],'subtracted','reassigned']
                val_items.extend(new_items)
                val_items[0] = evald
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            elif op_token == '*':
                if type(arg1) == type(arg2) and type(arg1) is str:
                    eval = stringjoin(op_token,arg1,arg2)
                    print(evald)
                elif type(arg1) == type(arg2) and type(arg1) is int:
                    eval = intjoin(op_token,arg1,arg2)
                    print(evald)
                elif type(arg1) == type(arg2) and type(arg1) is bool:
                    eval = booljoin(op_token,arg1,arg2)
                    print(evald)
                elif type(arg1) == type(arg2) and type(arg1) is list:
                    eval = charjoin(op_token,arg1,arg2)
                    print(evald)
                else:
                    eval = multijoin(op_token,arg1,arg2)
                    print(evald)
                new_items = [val_items[0],'multiplied','reassigned']
                val_items.extend(new_items)
                val_items[0] = evald
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            elif op_token == '/':
                if type(arg1) == type(arg2) and type(arg1) is str:
                    eval = stringjoin(op_token,arg1,arg2)
                elif type(arg1) == type(arg2) and type(arg1) is int:
                    eval = intjoin(op_token,arg1,arg2)
                elif type(arg1) == type(arg2) and type(arg1) is bool:
                    eval = booljoin(op_token,arg1,arg2)
                elif type(arg1) == type(arg2) and type(arg1) is list:
                    eval = charjoin(op_token,arg1,arg2)
                else:
                    eval = multijoin(op_token,arg1_typed,arg2_typed)
                new_items = [val_items[0],'divided','reassigned']
                val_items.extend(new_items)
                val_items[0] = evald
                var_assign = has(key, val_items)
                print
                env.update({var_assign.key: var_assign.val})


def propose_eval_floaty(my_line,env):
    current_env = env
    #print("found join")
    cond_val = my_line[1]
    cond = my_line[2]
    target_var = my_line[3]
    filtered_truecond = []
    env[target_var].append('proposed')
    for i in my_line[5:]:
        if i != 'unless':
            filtered_truecond.append(i)
        elif i == 'unless':
            break
    if 'unless' not in my_line[4:]:
        no_false_cond = True
        falsecond = None
    else:
        no_false_cond = False
        faldex = my_line.index('unless')
        false_cond_start_dex = faldex + 2
        falsecond = my_line[false_cond_start_dex:]
        #print(falsecond)
    truecond = filtered_truecond
    #print(truecond)
    #print(no_false_cond)
    propose_cond = propose(cond_val, cond, target_var, truecond, falsecond)
    current_env_keys = [v for v in current_env.keys()]
    target_list = env[propose_cond.target]
    if propose_cond.testval in current_env_keys:
        propose_cond.testval = env[propose_cond.testval][0]
    else:
        propose_cond.testval = propose_cond.testval
    if propose_cond.cond == 'isin':
        #grab target, grab the cond_val, compare
        if propose_cond.testval in target_list and no_false_cond == False:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval not in target_list and no_false_cond == False:
            eval_cond = propose_cond.falsecond
        elif propose_cond.testval in target_list and no_false_cond == True:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval not in target_list and no_false_cond == True:
            print('huh')

    elif propose_cond.cond == 'notin':
        #grab target, grab the cond_val, compare
        if propose_cond.testval not in target_list and no_false_cond == False:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval in target_list and no_false_cond == False:
            eval_cond = propose_cond.falsecond
        elif propose_cond.testval not in target_list and no_false_cond == True:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval in target_list and no_false_cond == True:
            print('huh?')
            
    #print(eval_cond)
    #look at eval_cond and deliver - eval conds can only be actions, like observe, scope, arithmatic, or reassignments
    #get a load of this recursion in its rawest form
    if 'has' in eval_cond:
        variable_eval_floaty(eval_cond,env)
    elif 'observe' in eval_cond:
        observe_eval_floaty(eval_cond,env)
    elif 'scope' in eval_cond:
        scope_eval_floaty(eval_cond,env)
    elif '+' or '-' or '*' or '/' in eval_cond:
        operator_eval_floaty(eval_cond,env)       


### fugue functions ###

fugue_codes = ['seen', 'scoped', 'observed', 'called', 'assigned', 'proposed', 'added', 'subtracted', 'multiplied', 'divided', 'reassigned']

def scope_eval_fugue(my_line,env):
    current_env = env
    target_list = my_line[1]
    #print(target_list)
    list_obj = scope(current_env[target_list])
    choices = ['no leak', 'partial leak', 'full leak']
    memory_check = random.choice(choices)
    if memory_check == 'no leak':
        env[target_list].append(fugue_codes[random.randint(0,len(fugue_codes))])
    elif memory_check == 'partial leak':
        env[target_list].append('seen')
    else:
        pass
    print(len(list_obj.list))

def observe_eval_fugue(my_line,env):
    current_env = env
    expression = ' '.join(my_line[1:])
    observe_statement = observe(expression)
    current_env_keys = [v for v in env.keys()]
    #print(observe_statement.expression)
    if observe_statement.expression in current_env_keys:
        #print("beans")
        choices = ['no leak', 'partial leak', 'full leak']
        memory_check = random.choice(choices)
        if memory_check == 'no leak':
            env[observe_statement.expression].append('observed')
        elif memory_check == 'partial leak':
            env[observe_statement.expression].append(fugue_codes[random.randint(0,len(fugue_codes))])
        else:
            pass
        trace_vals = current_env[(observe_statement.expression)]
        print(str(trace_vals[random.randint(0,(len(trace_vals)-1))]) + ' has (I think) been ' + str([i for i in trace_vals]))
    else:
        print(observe_statement.expression)

def variable_eval_fugue(my_line, env):
    current_env = env
    var = my_line[0]
    val = []
    val.append(' '.join(my_line[2:]))
    choices = ['no leak', 'partial leak', 'full leak']
    memory_check = random.choice(choices)
    #print(val)
    if '~' not in val[0]:
        if memory_check == 'no leak':
            val.append('assigned')
        elif memory_check == 'partial leak':
            val.append(fugue_codes[random.randint(0,len(fugue_codes))])
        else:
            pass
        var_assign = has(var, val)
        env.update({var_assign.key: var_assign.val})
        #print(env)
    else:
        val_items = current_env[var]
        #print(val_items)
        subvals = val[0].split(' ')
        #print(subvals)
        if '+' or '-' or '*' or '/' in subvals:
            current_env = env
            op_token = subvals[1]
            arg1 = subvals[2]
            arg2 = subvals[3]
            current_env_keys = [v for v in current_env.keys()]
            if arg1 in current_env_keys:
                key = arg1
                #we can grab from anywhere in env[arg1]
                arg_vals = env[arg1]
                arg_vals_len = (len(arg_vals)-1)
                choice_range = random.randint(0,arg_vals_len)
                try:
                    arg1 = int(env[arg1][choice_range])
                except ValueError:
                    arg1 = int(len(env[arg1][choice_range]))
            if arg2 in current_env_keys:
                key = arg2
                arg_vals = env[arg2]
                arg_vals_len = (len(arg_vals)-1)
                choice_range = random.randint(0,arg_vals_len)
                try:
                    arg2 = int(env[arg2][choice_range])
                except ValueError:
                    arg2 = int(len(env[arg2][choice_range]))
            if op_token == '+':
                try:
                    evald = int(arg1) + int(arg2)
                except ValueError:
                    evald = int(len(arg1)) + int(len(arg2))
                #print(val_items)
                if memory_check == 'no leak':
                    new_items = [val_items[0],'added','reassigned']
                elif memory_check == 'partial leak':
                    new_items = [val_items[0],fugue_codes[random.randint(0,len(fugue_codes))],fugue_codes[random.randint(0,len(fugue_codes))]]
                else:
                    new_items = None
                    pass
                if new_items is not None:
                    val_items.extend(new_items)
                val_items[random.randint(0,(len(val_items)-1))] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
                #print(var_assign.val)
            elif op_token == '-':
                try:
                    evald = int(arg1) - int(arg2)
                except ValueError:
                    evald = int(len(arg1)) - int(len(arg2))
                if memory_check == 'no leak':
                    new_items = [val_items[0],'subtracted','reassigned']
                elif memory_check == 'partial leak':
                    new_items = [val_items[0],fugue_codes[random.randint(0,(len(fugue_codes)-1))],fugue_codes[random.randint(0,(len(fugue_codes)-1))]]
                else:
                    new_items = None
                    pass
                if new_items is not None:
                    val_items.extend(new_items)
                val_items[random.randint(0,(len(val_items)-1))] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            elif op_token == '*':
                try:
                    evald = int(arg1) * int(arg2)
                except ValueError:
                    evald = int(len(arg1)) * int(len(arg2))
                if memory_check == 'no leak':
                    new_items = [val_items[0],'multiplied','reassigned']
                elif memory_check == 'partial leak':
                    new_items = [val_items[0],fugue_codes[random.randint(0,(len(fugue_codes)-1))],fugue_codes[random.randint(0,(len(fugue_codes)-1))]]
                else:
                    new_items = None
                    pass
                if new_items is not None:
                    val_items.extend(new_items)
                val_items[random.randint(0,(len(val_items)-1))] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})
            elif op_token == '/':
                try:
                    evald = int(arg1) / int(arg2)
                except ValueError:
                    evald = int(len(arg1)) / int(len(arg2))
                if memory_check == 'no leak':
                    new_items = [val_items[0],'divided','reassigned']
                elif memory_check == 'partial leak':
                    new_items = [val_items[0],fugue_codes[random.randint(0,(len(fugue_codes)-1))],fugue_codes[random.randint(0,(len(fugue_codes)-1))]]
                else:
                    new_items = None
                    pass
                if new_items is not None:
                    val_items.extend(new_items)
                val_items[random.randint(0,(len(val_items)-1))] = int(evald)
                var_assign = has(key, val_items)
                env.update({var_assign.key: var_assign.val})

def operator_eval_fugue(my_line, env):
    op_token = my_line[0]
    arg1 = my_line[1]
    arg2 = my_line[2]
    current_env_keys = [v for v in env.keys()]
    choices = ['no leak', 'partial leak', 'full leak']
    memory_check = random.choice(choices)
    if arg1 in current_env_keys:
        store_key = arg1
        val_items = env[arg1]
        if memory_check == 'no leak':
            val_items.append('called')
        elif memory_check == 'partial leak':
            val_items.append(fugue_codes[random.randint(0,(len(fugue_codes)-1))])
        else:
            pass
        var_assign = has(store_key, val_items)
        env.update({store_key: var_assign.val})
        arg_vals = env[arg1]
        arg_vals_len = (len(arg_vals)-1)
        choice_range = random.randint(0,arg_vals_len)
        try:
            arg1 = int(env[arg1][choice_range])
        except ValueError:
            arg1 = int(len(env[arg1][choice_range]))
    if arg2 in current_env_keys:
        store_key = arg2
        val_items = env[arg2]
        if memory_check == 'no leak':
            val_items.append('called')
        elif memory_check == 'partial leak':
            val_items.append(fugue_codes[random.randint(0,(len(fugue_codes)-1))])
        else:
            pass
        var_assign = has(store_key, val_items)
        env.update({store_key: var_assign.val})
        arg_vals = env[arg2]
        arg_vals_len = (len(arg_vals)-1)
        choice_range = random.randint(0,arg_vals_len)
        try:
            arg2 = int(env[arg2][choice_range])
        except ValueError:
            arg2 = int(len(env[arg2][choice_range]))
    if op_token == '+':
        try:
            evald = int(arg1) + int(arg2)
        except ValueError:
            evald = int(len(arg1)) + int(len(arg2))
        print(evald)
    elif op_token == '-':
        try:
            evald = int(arg1) - int(arg2)
        except ValueError:
            evald = int(len(arg1)) - int(len(arg2))
        print(evald)
    elif op_token == '*':
        try:
            evald = int(arg1) * int(arg2)
        except ValueError:
            evald = int(len(arg1)) * int(len(arg2))
        print(evald)
    elif op_token == '/':
        try:
            evald = int(arg1) / int(arg2)
        except ValueError:
            evald = int(len(arg1)) / int(len(arg2))
        print(evald)

def propose_eval_fugue(my_line, env):
    current_env = env
    #print("found join")
    cond_val = my_line[1]
    cond = my_line[2]
    target_var = my_line[3]
    filtered_truecond = []
    env[target_var].append('proposed')
    for i in my_line[5:]:
        if i != 'unless':
            filtered_truecond.append(i)
        elif i == 'unless':
            break
    if 'unless' not in my_line[4:]:
        no_false_cond = True
        falsecond = None
    else:
        no_false_cond = False
        faldex = my_line.index('unless')
        false_cond_start_dex = faldex + 2
        falsecond = my_line[false_cond_start_dex:]
        #print(falsecond)
    truecond = filtered_truecond
    #print(truecond)
    #print(no_false_cond)
    propose_cond = propose(cond_val, cond, target_var, truecond, falsecond)
    current_env_keys = [v for v in current_env.keys()]
    target_list = env[propose_cond.target]
    if propose_cond.testval in current_env_keys:
        propose_cond.testval = env[propose_cond.testval][0]
    else:
        propose_cond.testval = propose_cond.testval
    if propose_cond.cond == 'isin':
        #grab target, grab the cond_val, compare
        if propose_cond.testval in target_list and no_false_cond == False:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval not in target_list and no_false_cond == False:
            eval_cond = propose_cond.falsecond
        elif propose_cond.testval in target_list and no_false_cond == True:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval not in target_list and no_false_cond == True:
            print('huh?')

    elif propose_cond.cond == 'notin':
        #grab target, grab the cond_val, compare
        if propose_cond.testval not in target_list and no_false_cond == False:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval in target_list and no_false_cond == False:
            eval_cond = propose_cond.falsecond
        elif propose_cond.testval not in target_list and no_false_cond == True:
            eval_cond = propose_cond.truecond
        elif propose_cond.testval in target_list and no_false_cond == True:
            print('huh?')
            
    #print(eval_cond)
    #look at eval_cond and deliver - eval conds can only be actions, like observe, scope, arithmatic, or reassignments
    #get a load of this recursion in its rawest form
    if 'has' in eval_cond:
        variable_eval_fugue(eval_cond,env)
    elif 'observe' in eval_cond:
        observe_eval_fugue(eval_cond,env)
    elif 'scope' in eval_cond:
        scope_eval_fugue(eval_cond,env)
    elif '+' or '-' or '*' or '/' in eval_cond:
        operator_eval_fugue(eval_cond,env)        

### state-based parsers ###

def strict_parse_and_eval(list,env):
    sep = ' '
    program_len = len(list)
    for i in range(1,program_len):
        my_line = list[i]
        #print(my_line)
        joined_line = sep.join(my_line)
        #print(joined_line)
        if 'propose' in joined_line:
            propose_eval_strict(my_line,env)    
        elif 'has' in joined_line:
            variable_eval_strict(my_line,env)
        elif 'observe' in joined_line:
            observe_eval_strict(my_line,env)
        elif 'scope' in joined_line:
            scope_eval_strict(my_line, env)
        elif '+' or '-' or '*' or '/' in joined_line:
            operator_eval_strict(my_line,env)
        else:
            program_state = state_selector(program_state)
        
            
def floaty_parse_and_eval(list,env):
    sep = ' '
    program_len = len(list)
    for i in range(1,program_len):
        my_line = list[i]
        #print(my_line)
        joined_line = sep.join(my_line)
        if 'propose' in joined_line:
            propose_eval_floaty(my_line,env) 
        elif 'has' in joined_line:
            variable_eval_floaty(my_line,env)
        elif 'scope' in joined_line:
            scope_eval_floaty(my_line,env)
        elif 'observe' in joined_line:
            observe_eval_floaty(my_line,env)
        elif '+' or '-' or '*' or '/' in joined_line:
            operator_eval_floaty(my_line,env)
        else:
            program_state = state_selector(program_state)


def fugue_parse_and_eval(list,env):
    sep = ' '
    program_len = len(list)
    for i in range(1,program_len):
        my_line = list[i]
        #print(my_line)
        joined_line = sep.join(my_line)
        if 'propose' in joined_line:
            propose_eval_fugue(my_line,env) 
        elif 'has' in joined_line:
            variable_eval_fugue(my_line,env)
        elif 'scope' in joined_line:
            scope_eval_fugue(my_line,env)
        elif 'observe' in joined_line:
            observe_eval_fugue(my_line,env)
        elif '+' or '-' or '*' or '/' in joined_line:
            operator_eval_fugue(my_line,env)
        else:
            program_state = state_selector(program_state)

def ennui_parse(list,env):
    sys.exit()

#strict_parse_and_eval(tokens_list,env)
#floaty_parse_and_eval(tokens_list,env)
#fugue_parse_and_eval(tokens_list,env)

#except Exception as e - this is how we will handle state change
#if you encounter an exception, run state_selector again
        
while program_state is not None:
    try:
        if program_state == 'strict':
             strict_parse_and_eval(tokens_list,env)
        elif program_state == 'ennui':
             ennui_parse(tokens_list,env)
        elif program_state == 'floaty':
             floaty_parse_and_eval(tokens_list,env)
        elif program_state == 'fugue':
             fugue_parse_and_eval(tokens_list,env)
        else:
             print('uncertainty encountered')
     except Exception as e:
         program_state = state_selector(program_state)
         print("error detected, state has changed to " + program_state)
         continue

     break
