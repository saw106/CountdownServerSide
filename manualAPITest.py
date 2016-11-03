import requests
import json

if __name__ == "__main__":
    r = requests.post('http://localhost:5000/create_user', data=json.dumps({'user_info': {'username':'walter', 'password':'wat'}}))
    print r.content
    r = requests.post('http://localhost:5000/create_task', data=json.dumps({'user_info': {'username':'walter', 'password': 'wat'}, 'task': 
                                                    {'name': 'good task',
                                                    'description': 'this is a task and it will be done',
                                                    'duedate': '1092941466',
                                                    'priority': 'omega',
                                                    'tag': 'things I hate to do',
                                                    'backgroundhex': '#000000',
                                                    'foregroundhex': '#000000'}}))
    print r.content
    r = requests.get('http://localhost:5000/get_active_tasks', data=json.dumps({'user_info' :{'username':'walter', 'password': 'wat'}}))
    print r.content