from flask import Flask
from flask import request
from DBResources import DBResource
import json
app = Flask(__name__)

@app.route("/create_subtask", methods=["POST"])
def createNewSubTask():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    if (db.doesUserExist()):
        db.createTask(req['task'], parentTaskId = req['parentid'])
        ret['status'] = True
    else:
        ret['status'] = False
        ret['problem'] = "User {} does not exist.".format(req['user_info']['username'])
    return json.dumps(ret)

@app.route("/get_subtasks", methods=["POST"])
def getSubTasks():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    ret['tasks'] = db.getSubTasksForTask(req['parentid'])
    return json.dumps(ret)

@app.route("/unarchive_task", methods=["POST"])
def unarchiveTask():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(user_info=req['user_info'])
    ret['status'] = db.unarchiveTask(req['taskid'])
    return json.dumps(ret)

@app.route("/complete_task", methods=["POST"])
def completeTask():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(user_info=req['user_info'])
    ret['status'] = db.completeTask(req['taskid'])
    return json.dumps(ret)

@app.route("/delete_task", methods=["POST"])
def deleteTask():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(user_info=req['user_info'])
    ret['status'] = db.deleteTask(req['taskid'])
    return json.dumps(ret)

@app.route("/edit_task", methods=["POST"])
def editTask():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(user_info=req['user_info'])
    ret['status'] = db.editTask(req['task'])
    return json.dumps(ret)

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
        if req.has_key('parentid'):
            db.createTask(req['task'], parentTaskId=req['parentid'])
        else:    
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

@app.route('/get_inactive_tasks', methods=["GET"])
def getInactiveUserTasks():
    ret = {}
    req = json.loads(request.get_data())
    db = DBResource(req['user_info'])
    ret['tasks'] = db.getArchivedTasksForUser()
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