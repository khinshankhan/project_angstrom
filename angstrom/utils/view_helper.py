def valid(u_id, pw):
    if u_id.isnumeric():
        return valid_login(u_id, pw)
    return False

def extract_task_id(tasks):
    '''
        tasks is a dict
    '''
    

def gen_task_dict(form):
    task_list = {}
        
    for key in form.keys():
        temp = key.split("_")
        if len(temp) > 1:
            if form[key].isdigit():
                task_list[int(temp[0])] = int(form[key])
            else:
                if str(form[key]) == "on":
	            task_list[int(temp[0])] = 1
                elif str(form[key]) == "off":
	            task_list[int(temp[0])] = 0
    #add missing indices
    for x in range(0, 13):
        if not x in task_list.keys():
            task_list[x] = 0
    return task_list

