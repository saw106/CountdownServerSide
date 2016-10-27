import requests
import json

if __name__ == "__main__":
    r = requests.post('http://localhost:5000/create_user', data=json.dumps({'username':'walter', 'password':'wat'}))
    print r.content
    r = requests.post('http://localhost:5000/create_task', data=json.dumps({'username':'walter', 'task': {'name': 'taskthing', 'completed': 'f'}}))
    print r.content