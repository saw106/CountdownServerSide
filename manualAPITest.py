import requests
import json
import base64

if __name__ == "__main__":
    walter_headers = {"Authorization": "Basic " + base64.b64encode("walter:wat")}
    bad_walter_headers = {"Authorization": "Basic " + base64.b64encode("walter:nowat")}
    print "\nCreate Walter"
    r = requests.post('http://localhost:5000/create_user', data=json.dumps({'user_info': {'username':'walter', 'password':'wat'}}))
    print r.content

    print "\nLogging in with good credentials"
    r = requests.get('http://localhost:5000/login', headers=walter_headers)
    print r.content

    print "\nLogging in with bad credentials"
    r = requests.get('http://localhost:5000/login', headers=bad_walter_headers)
    print r.content

    print "\nCreate 2 tasks"
    r = requests.post('http://localhost:5000/create_task', headers=walter_headers, data=json.dumps({'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '10-1-2016T00:00Z',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content                                                    
    r = requests.post('http://localhost:5000/create_task', headers=walter_headers, data=json.dumps({'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '10-2-2016T00:00Z',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content

    print "\nCreateSubtask for task 0"
    r = requests.post('http://localhost:5000/create_subtask', headers=walter_headers, data=json.dumps({'parentid': '0', 'task': 
                                                    {'name': 'I AM A SUBTASK',
                                                    'description': 'I DO NOT BELONG WITH NORMAL TASKS',
                                                    'duedate': '10-2-2016T00:00Z',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content                                                    

    print "\nSee active tasks"
    r = requests.get('http://localhost:5000/get_active_tasks', headers=walter_headers)
    print r.content

    print "\nSee next ending task"
    r = requests.get('http://localhost:5000/get_next_countdown', headers=walter_headers)
    print r.content

    print "\nSee subtasks of task 0"
    r = requests.get('http://localhost:5000/get_subtasks/0', headers=walter_headers)
    print r.content

    print "\nComplete subtask"
    r = requests.post('http://localhost:5000/complete_task', headers=walter_headers, data=json.dumps({'taskid': '2'}))
    print r.content

    print "\nCheck status of subtask"
    r = requests.get('http://localhost:5000/get_subtasks/0', headers=walter_headers)
    print r.content

    print "\nComplete task 1"
    r = requests.post('http://localhost:5000/complete_task', headers=walter_headers, data=json.dumps({'taskid': '1'}))
    print r.content

    print "\nVerify in Inactive Tasks, not in Active"
    r = requests.get('http://localhost:5000/get_active_tasks', headers=walter_headers)
    print r.content
    r = requests.get('http://localhost:5000/get_inactive_tasks', headers=walter_headers)
    print r.content    

    print "\nUnarchive Task 1"
    r = requests.post('http://localhost:5000/unarchive_task', headers=walter_headers, data=json.dumps({'taskid': '1'}))
    print r.content

    print "\nVerify in Active tasks"
    r = requests.get('http://localhost:5000/get_active_tasks', headers=walter_headers)
    print r.content

    print "\nDelete Task 0"
    r = requests.post('http://localhost:5000/delete_task', headers=walter_headers, data=json.dumps({'taskid': '0'}))
    print r.content

    print "\nVerify not in Active tasks"
    r = requests.get('http://localhost:5000/get_active_tasks', headers=walter_headers)
    print r.content

    print "\nEdit Task 1"
    r = requests.post('http://localhost:5000/edit_task', headers=walter_headers, data=json.dumps({'task': 
                                                    {'id': '1',
                                                    'name': 'better task',
                                                    'description': 'this is a task and it has been modified',
                                                    'duedate': '10-2-2016T00:00Z',
                                                    'priority': 'swag',
                                                    'tag': 'wow',
                                                    'backgroundhex': '#1111',
                                                    'foregroundhex': '#1111'}}))
    print r.content
    print "\nVerify updates"
    r = requests.get('http://localhost:5000/get_active_tasks', headers=walter_headers)
    print r.content