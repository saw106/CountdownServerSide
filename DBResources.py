import sqlite3

TASK_COLUMNS = ['id', 'name', 'description', 'duedate', 'priority', 'tag', 'backgroundhex', 'foregroundhex', 'datecreated', 'lastmodified', 'completed', 'completiontime', 'subtaskof']

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

    def getNumUsers(self):
        rows = self.cursor.execute('''select count(*) from users''')
        for row in rows:
            return row[0]

    def getNumTasks(self):
        rows = self.cursor.execute('''select count(*) from tasks''')
        for row in rows:
            return row[0]

    def createUser(self):
        self.cursor.execute('''INSERT INTO users VALUES ({}, '{}', '{}', DATETIME('now'))'''.format(self.getNumUsers(), self.user_info['username'], self.user_info['password'])).fetchall()
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

    @checkUserCredentials
    def createTask(self, task, parentTaskId=None):
        task['id'] = self.getNumTasks()
        if parentTaskId is not None:
            task['parent'] = parentTaskId
        else:
            task['parent'] = 'NULL'
        userid = self.getCurrentUserId()
        self.cursor.execute('''INSERT INTO tasks VALUES ({id}, '{name}', '{description}', DATETIME('{duedate}', 'unixepoch'), '{priority}', '{tag}', '{backgroundhex}', '{foregroundhex}', DATETIME('now'), DATETIME('now'), 'f', NULL, {parent})'''.format(**task))
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
        completedSQL = {True: 't', False:'f'}
        userid = self.getCurrentUserId()
        for row in self.cursor.execute('''select * from tasks where subtaskof is null and completed='{}' and id in (select taskid from hastask where userid={})'''.format(completedSQL[completed], userid)):
            task = {}
            i = 0
            for column_name in TASK_COLUMNS:
                task[column_name] = row[i]
                i += 1
            tasks.append(task)
        return tasks

    @checkUserCredentials
    def getSubTasksForTask(self, parentid):
        userid = self.getCurrentUserId()
        query = {'parentid': parentid, "userid": userid}
        tasks = []
        print query
        for row in self.cursor.execute('''select * from tasks where subtaskof = {parentid} and id in (select taskid from hastask where userid={userid}) '''.format(**query)):
            task = {}
            i = 0
            for column_name in TASK_COLUMNS:
                task[column_name] = row[i]
                i += 1
            tasks.append(task)
        return tasks

    @checkUserCredentials
    def getNextCountdown(self):
        userid = self.getCurrentUserId()
        rows = self.cursor.execute('''select * from tasks T where T.subtaskof is null and T.completed='f' and T.id in (select taskid from hastask where userid={}) and T.duedate = (select min(duedate) from tasks)'''.format(userid))
        task = {}
        for row in rows:
            i = 0
            for column_name in TASK_COLUMNS:
                task[column_name] = row[i]
                i += 1
            return task

#used for testing
if __name__ == "__main__":
    db = DBResource(user_info={'username':'walter', 'password':'wat'})
    print db.getNextCountdown()