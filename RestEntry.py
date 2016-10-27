from flask import Flask
from flask import request
from DBResources import *
import json
app = Flask(__name__)

'''  createuser x
     createtask x
     getactivetasksforuser x
     getarchivedtasksforuser
     unarchivetask
     completetask
     deletetask
     getNextCountDownForUser
'''

@app.route("/create_user", methods=["POST"])
def createNewUser():
    ret = {}
    req = json.loads(request.get_data())
    if (not doesUserExist(req['username'])):
        createUser(req['username'], req['password'])
        ret['status'] = True
    else:
        ret['status'] = False
    return json.dumps(ret)

@app.route("/create_task", methods=["POST"])
def createNewTask():
    ret = {}
    req = json.loads(request.get_data())
    if (doesUserExist(req['username'])):
        createTask(getUserId(req['username']), req['task']['name'])
        ret['status'] = True
    else:
        ret['status'] = False
    return json.dumps(ret)

@app.route('/get_active_tasks', methods=["GET"])
def getActiveUserTasks():
    ret = {}
    req = json.loads(request.get_data())
    ret['tasks'] = getActiveTasksForUser(getUserId(req['username']))
    return json.dumps(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0')