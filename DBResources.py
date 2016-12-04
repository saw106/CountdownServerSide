import sqlite3
import re
from datetime import datetime as datetime

TASK_COLUMNS = ['id', 'name', 'description', 'duedate', 'priority', 'tag', 'backgroundhex', 'foregroundhex', 'datecreated', 'lastmodified', 'completed', 'completiontime', 'subtaskof']
truthMap = {True:'true', False:'false', 'true': True, 'false': False}

class DBResource:

    def __init__(self, user_info=None, conn=None) :
        self.user_info = user_info
        if conn is None:
            self.conn = sqlite3.connect('countdown.db')
        else:
            self.conn = conn
        self.cursor = self.conn.cursor()

    def checkUserCredentials(func):
        def func_wrapper(*args, **kwargs):
            if (args[0].verifyPassword()):
                return func(*args, **kwargs)
            return {'Error': 'User {} given with invalid password.'.format(args[0].user_info['username'])}
        return func_wrapper

    def verifyPassword(self):
        rows = self.cursor.execute('''select * from users where username='{}' and password='{}' '''.format(self.user_info['username'], self.user_info['password']))
        for row in rows:
            return True
        return False

    def createUser(self):
        now = self.turnTimeIntoISO8601Time(datetime.now())
        self.cursor.execute('''INSERT INTO users VALUES ({}, '{}', '{}', '{}') '''.format(self.getMaxUserId() + 1, self.user_info['username'], self.user_info['password'], now)).fetchall()
        print "Created new User {}".format(self.user_info['username'])
        self.conn.commit()

    def doesUserExist(self):
        rows = self.cursor.execute('''select * from users where username='{}' '''.format(self.user_info['username']))
        for row in rows:
            return True
        return False

    def getUserId(self, username):
        for row in self.cursor.execute('''select * from users where username='{}' '''.format(username)):
            return row[0]
        return -1

    def getCurrentUserId(self):
        return self.getUserId(self.user_info['username'])

    def getMaxTaskId(self):
        rows = self.cursor.execute('''select MAX(id) from tasks''')
        for row in rows:
            if row[0] is None:
                return -1
            return int(row[0])

    def getMaxUserId(self):
        rows = self.cursor.execute('''select MAX(id) from users''')
        for row in rows:
            if row[0] is None:
                return -1
            return int(row[0])

    @checkUserCredentials
    def createTask(self, task, parentTaskId=None):
        task['id'] = self.getMaxTaskId() + 1
        task['now'] = self.turnTimeIntoISO8601Time(datetime.now())
        if parentTaskId is not None:
            task['parent'] = parentTaskId
        else:
            task['parent'] = 'NULL'
        userid = self.getCurrentUserId()
        self.cursor.execute('''INSERT INTO tasks VALUES ({id}, '{name}', '{description}', '{duedate}', '{priority}', '{tag}', '{backgroundhex}', '{foregroundhex}', '{now}', '{now}', 'false', NULL, {parent})'''.format(**task))
        self.cursor.execute('''INSERT INTO hastask VALUES ({},{})'''.format(userid, task['id']))
        print "Created New task for {}".format(self.user_info['username'])
        self.conn.commit()
        return task['id']

    @checkUserCredentials
    def getActiveTasksForUser(self):
        return self.getActiveOrNotTasksForUser(False)

    @checkUserCredentials
    def getArchivedTasksForUser(self):
        return self.getActiveOrNotTasksForUser(True)

    def getActiveOrNotTasksForUser(self, completed):
        tasks = []
        completedSQL = {True: 'true', False:'false'}
        userid = self.getCurrentUserId()
        for row in self.cursor.execute('''select * from tasks where subtaskof is null and completed='{}' and id in (select taskid from hastask where userid={})'''.format(completedSQL[completed], userid)):
            task = {}
            i = 0
            for column_name in TASK_COLUMNS:
                if column_name is 'completed':
                    task[column_name] = truthMap[row[i]]
                else:
                    task[column_name] = row[i]
                i += 1
            tasks.append(task)
        return tasks

    @checkUserCredentials
    def getSubTasksForTask(self, parentid):
        userid = self.getCurrentUserId()
        query = {'parentid': parentid, "userid": userid}
        tasks = []
        for row in self.cursor.execute('''select * from tasks where subtaskof = {parentid} and id in (select taskid from hastask where userid={userid}) '''.format(**query)):
            task = {}
            i = 0
            for column_name in TASK_COLUMNS:
                if column_name is 'completed':
                    task[column_name] = truthMap[row[i]]
                else:
                    task[column_name] = row[i]
                i += 1
            tasks.append(task)
        return tasks

    @checkUserCredentials
    def getNextCountdown(self):
        userid = self.getCurrentUserId()
        rows = self.cursor.execute('''select * from tasks T where T.subtaskof is null and T.completed='false'
                                      and T.id in (select taskid from hastask where userid={})
                                      and T.duedate = (select min(TS.duedate) from tasks TS, hastask HS where TS.id = HS.taskid and HS.userid = {} and TS.completed='false')'''.format(userid, userid))
        task = {}
        for row in rows:
            i = 0
            for column_name in TASK_COLUMNS:
                if column_name is 'completed':
                    task[column_name] = truthMap[row[i]]
                else:
                    task[column_name] = row[i]
                i += 1
            return task

    @checkUserCredentials
    def unarchiveTask(self, taskid):
        return self.setTaskCompletion(taskid, False)

    @checkUserCredentials
    def completeTask(self, taskid):
        return self.setTaskCompletion(taskid, True)

    def setTaskCompletion(self, taskid, completed):
        if self.hasAccessToTask(taskid):
            status = truthMap[completed]
            now = self.turnTimeIntoISO8601Time(datetime.now())
            completedtime = "NULL"
            if completed:
                completedtime = now
            self.cursor.execute('''update tasks set completed='{}', completiontime='{}', lastmodified='{}' where id={} '''.format(status, completedtime, now, taskid))
            self.conn.commit()
            return True
        return False

    def hasAccessToTask(self, taskid):
        userid = self.getCurrentUserId()
        for row in self.cursor.execute('''select * from hastask where userid={} and taskid={}'''.format(userid, taskid)):
            return True
        return False

    @checkUserCredentials
    def deleteTask(self, taskid):
        if self.hasAccessToTask(taskid):
            userid = self.getCurrentUserId()
            if self.isSingleUserTask(taskid):
                self.cursor.execute('''delete from tasks where id={} '''.format(taskid))
                self.conn.commit()
            self.cursor.execute('''delete from hastask where taskid={} and userid={} '''.format(taskid, userid))
            self.conn.commit()
            return True
        return False

    def isSingleUserTask(self, taskid):
        numUsers = 0
        for row in self.cursor.execute('''select * from hastask where taskid={}'''.format(taskid)):
            numUsers += 1
        if numUsers == 1:
            return True
        return False

    @checkUserCredentials
    def getTask(self, taskid):
        if self.hasAccessToTask(taskid):
            for row in self.cursor.execute("select * from tasks where id={}".format(taskid)):
                i = 0
                task = {}
                for column_name in TASK_COLUMNS:
                    if column_name is 'completed':
                        task[column_name] = truthMap[row[i]]
                    else:
                        task[column_name] = row[i]
                    i += 1
                return task
        return None


    @checkUserCredentials
    def editTask(self, task):
        if self.hasAccessToTask(task['id']):
            task['now'] = self.turnTimeIntoISO8601Time(datetime.now())
            self.cursor.execute('''update tasks set name='{name}', description='{description}', duedate='{duedate}', 
            priority='{priority}', tag='{tag}', backgroundhex='{backgroundhex}', foregroundhex='{foregroundhex}', lastmodified='{now}' where id={id}'''.format(**task))
            self.conn.commit()
            return True
        return False

    def turnTimeIntoISO8601Time(self, time):
        stringTime = str(time)
        return re.sub(r'(.*) ([0-9][0-9]:[0-9][0-9]).*',r'\1T\2Z',stringTime)

#used for testing
if __name__ == "__main__":
    db = DBResource(user_info={'username':"user_1", 'password':'password_1'})
