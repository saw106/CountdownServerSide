from flask import Flask
from flask import request
from DBResources import DBResource
import json
app = Flask(__name__)

@app.route("/create_subtask", methods=["POST"])
def createNewSubTask():
    ret = {}
    req = json.loads(request.get_data())
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info)
    if (db.doesUserExist()):
        ret['taskid'] = db.createTask(req['task'], parentTaskId = req['parentid'])
        ret['status'] = True
    else:
        ret['status'] = False
        ret['problem'] = "User {} does not exist.".format(user_info['username'])
    return json.dumps(ret)

@app.route("/get_subtasks/<parentid>", methods=["GET"])
def getSubTasks(parentid):
    ret = {}
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info)
    ret['tasks'] = db.getSubTasksForTask(parentid)
    ret['status'] = True
    return json.dumps(ret)

@app.route("/get_task/<taskid>", methods=["GET"])
def getSingleTask(taskid):
    ret = {}
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info)
    ret['task'] = db.getTask(taskid)
    if ret['task'] is not None:
        ret['status'] = True
    else:
        ret['status'] = False
    return json.dumps(ret)

@app.route("/unarchive_task", methods=["POST"])
def unarchiveTask():
    ret = {}
    req = json.loads(request.get_data())
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['status'] = db.unarchiveTask(req['taskid'])
    return json.dumps(ret)

@app.route("/complete_task", methods=["POST"])
def completeTask():
    ret = {}
    req = json.loads(request.get_data())
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['status'] = db.completeTask(req['taskid'])
    return json.dumps(ret)

@app.route("/delete_task", methods=["POST"])
def deleteTask():
    ret = {}
    req = json.loads(request.get_data())
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['status'] = db.deleteTask(req['taskid'])
    return json.dumps(ret)

@app.route("/edit_task", methods=["POST"])
def editTask():
    ret = {}
    req = json.loads(request.get_data())
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['status'] = db.editTask(req['task'])
    ret['status'] = True
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
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    if (db.doesUserExist()):
        if req.has_key('parentid'):
            ret['taskid'] = db.createTask(req['task'], parentTaskId=req['parentid'])
        else:    
            ret['taskid'] = db.createTask(req['task'])
        ret['status'] = True
    else:
        ret['status'] = False
        ret['problem'] = "User {} does not exist.".format(req['user_info']['username'])
    return json.dumps(ret)

@app.route('/get_active_tasks', methods=["GET"])
def getActiveUserTasks():
    ret = {}
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['tasks'] = db.getActiveTasksForUser()
    ret['status'] = True
    return json.dumps(ret)

@app.route('/get_inactive_tasks', methods=["GET"])
def getInactiveUserTasks():
    ret = {}
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['tasks'] = db.getArchivedTasksForUser()
    ret['status'] = True
    return json.dumps(ret)

@app.route('/get_next_countdown', methods=['GET'])
def getNextCountdownForUser():
    ret = {}
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
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
    user_info = {'username': request.authorization.username, 'password': request.authorization.password}
    db = DBResource(user_info=user_info)
    ret['status'] = db.verifyPassword()
    return json.dumps(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0')