from flask import Flask
from flask import request
from DBResources import DBResource
import json
app = Flask(__name__)

'''  createuser x
     createtask x
     getactivetasksforuser x
     getarchivedtasksforuser
     unarchivetask
     completetask
     deletetask
     getNextCountDownForUser x
     login x
'''

@app.route("/create_user", methods=["POST"])
def createNewUser():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(user_info=req['user_info'])
    if (not db.doesUserExist()):
        db.createUser()
        ret['status'] = True
    else:
        ret['status'] = False
    return json.dumps(ret)

@app.route("/create_task", methods=["POST"])
def createNewTask():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    if (db.doesUserExist()):
        db.createTask(req['task'])
        ret['status'] = True
    else:
        ret['status'] = False
        ret['problem'] = "User {} does not exist.".format(req['user_info']['username'])
    return json.dumps(ret)

@app.route('/get_active_tasks', methods=["GET"])
def getActiveUserTasks():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    ret['tasks'] = db.getActiveTasksForUser()
    return json.dumps(ret)

@app.route('/get_next_countdown', methods=['GET'])
def getNextCountdownForUser():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    if (db.doesUserExist()):
        task = db.getNextCountdown()
        ret['task'] = task
        ret['status'] = True
    else:
        ret['status'] = False
        ret['problem'] = "User {} does not exist".format(req['user_info']['username'])
    return json.dumps(ret)

@app.route('/login', methods=['GET'])
def login():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    ret['status'] = db.verifyPassword()
    return json.dumps(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0')