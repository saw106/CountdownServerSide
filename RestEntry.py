from flask import Flask
from DBResources import *
import json
app = Flask(__name__)

'''  createuser
     createtask
     getactivetasksforuser
     getarchivedtasksforuser
     unarchivetask
     completetask
     deletetask
'''

@app.route("/users")
def usersEndPoint():
    ret = {}
    ret['number of users'] = getNumUsers()
    return json.dumps(ret)

@app.route("/tasks")
def tasksEndPoint():
    ret = {}
    ret['number of tasks'] = getNumTasks()
    return json.dumps(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0')