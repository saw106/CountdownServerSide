import requests
import json

if __name__ == "__main__":
    print "\nCreate Walter"
    r = requests.post('http://localhost:5000/create_user', data=json.dumps({'user_info': {'username':'walter', 'password':'wat'}}))
    print r.content

    print "\nLogging in with good credentials"
    r = requests.get('http://localhost:5000/login', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nLogging in with bad credentials"
    r = requests.get('http://localhost:5000/login', data=json.dumps({'user_info' :{'username':'walter', 'password': 'nowat'}}))
    print r.content

    print "\nCreate 2 tasks"
    r = requests.post('http://localhost:5000/create_task', data=json.dumps({'user_info': {'username':'walter', 'password': 'wat'}, 'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '1092941466',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content                                                    
    r = requests.post('http://localhost:5000/create_task', data=json.dumps({'user_info': {'username':'walter', 'password': 'wat'}, 'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '1092901466',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content

    print "\nCreateSubtask for task 0"
    r = requests.post('http://localhost:5000/create_subtask', data=json.dumps({'parentid': '0', 'user_info': {'username':'walter', 'password': 'wat'}, 'task': 
                                                    {'name': 'I AM A SUBTASK',
                                                    'description': 'I DO NOT BELONG WITH NORMAL TASKS',
                                                    'duedate': '1092938466',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content                                                    

    print "\nSee active tasks"
    r = requests.get('http://localhost:5000/get_active_tasks', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nSee next ending task"
    r = requests.get('http://localhost:5000/get_next_countdown', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nSee subtasks of task 0"
    r = requests.post('http://localhost:5000/get_subtasks', data=json.dumps({'parentid': '0', 'user_info': {'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nComplete subtask"
    r = requests.post('http://localhost:5000/complete_task', data=json.dumps({'taskid': '2', 'user_info': {'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nCheck status of subtask"
    r = requests.post('http://localhost:5000/get_subtasks', data=json.dumps({'parentid': '0', 'user_info': {'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nComplete task 1"
    r = requests.post('http://localhost:5000/complete_task', data=json.dumps({'taskid': '1', 'user_info': {'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nVerify in Inactive Tasks, not in Active"
    r = requests.get('http://localhost:5000/get_active_tasks', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content
    r = requests.get('http://localhost:5000/get_inactive_tasks', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content    

    print "\nUnarchive Task 1"
    r = requests.post('http://localhost:5000/unarchive_task', data=json.dumps({'taskid': '1', 'user_info': {'username':'walter', 'password': 'wat'}}))
    print r.content

    print "\nVerify in Active tasks"
    r = requests.get('http://localhost:5000/get_active_tasks', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content